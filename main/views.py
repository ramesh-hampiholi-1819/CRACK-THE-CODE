from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import UserProfile
from main.models import Challenge, Language, Progress, Submission, Tutorial

from .services import ExecutionService


def get_default_language(request):
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return profile.default_language
    return 'python'


def home(request):
    languages = Language.objects.all()[:5]
    featured_challenges = Challenge.objects.filter(is_featured=True)[:3]
    return render(request, 'main/home.html', {
        'languages': languages,
        'featured_challenges': featured_challenges,
    })


def languages(request):
    languages = Language.objects.order_by('order')
    return render(request, 'main/languages.html', {'languages': languages})


def language_detail(request, slug):
    language = get_object_or_404(Language, slug=slug)
    tutorials = Tutorial.objects.filter(language=language).order_by('order')
    challenges = Challenge.objects.filter(language=language)
    return render(request, 'main/language_detail.html', {
        'language': language,
        'tutorials': tutorials,
        'challenges': challenges,
    })


def practice(request):
    default_language = get_default_language(request)
    return render(request, 'main/practice.html', {'default_language': default_language})


@require_POST
def execute_code(request):
    language = request.POST.get('language', 'python')
    code = request.POST.get('code', '')
    stdin = request.POST.get('input', '')
    result = ExecutionService.execute(language, code, stdin)
    return JsonResponse(result)


def challenge_list(request):
    query = request.GET.get('q', '').strip()
    language_slug = request.GET.get('language', '').strip()
    difficulty = request.GET.get('difficulty', '').strip()
    challenges = Challenge.objects.select_related('language')
    if query:
        challenges = challenges.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if language_slug:
        challenges = challenges.filter(language__slug=language_slug)
    if difficulty:
        challenges = challenges.filter(difficulty=difficulty)
    return render(request, 'main/challenges.html', {
        'challenges': challenges,
        'languages': Language.objects.all(),
        'query': query,
        'language_slug': language_slug,
        'difficulty': difficulty,
    })


def challenge_detail(request, slug):
    challenge = get_object_or_404(Challenge, slug=slug)
    user_progress = None
    if request.user.is_authenticated:
        user_progress, _ = Progress.objects.get_or_create(user=request.user, challenge=challenge)
    if request.method == 'POST':
        code = request.POST.get('code', '')
        submission = Submission.objects.create(
            user=request.user if request.user.is_authenticated else None,
            challenge=challenge,
            code=code,
            output='',
            passed=False,
        )
        result = ExecutionService.execute(challenge.language.slug, code, challenge.example_input)
        passed = result.get('status') == 'success' and str(result.get('output', '')).strip() == str(challenge.expected_output).strip()
        submission.output = result.get('output', '')
        submission.passed = passed
        submission.save()
        if request.user.is_authenticated:
            progress, _ = Progress.objects.get_or_create(user=request.user, challenge=challenge)
            progress.attempts += 1
            progress.is_solved = passed
            progress.save()
            if passed:
                messages.success(request, 'Challenge solved! Great work.')
            else:
                messages.info(request, 'Submission captured. Configure the execution service to verify automated outputs.')
        if passed:
            return redirect('challenge_detail', slug=challenge.slug)
        return render(request, 'main/challenge_detail.html', {
            'challenge': challenge,
            'submission': submission,
            'user_progress': user_progress,
            'execution_result': result,
            'recent_submissions': Challenge.objects.none(),
        })
    recent_submissions = Submission.objects.filter(challenge=challenge).order_by('-created_at')[:5]
    return render(request, 'main/challenge_detail.html', {
        'challenge': challenge,
        'user_progress': user_progress,
        'recent_submissions': recent_submissions,
    })


@login_required
def dashboard(request):
    progress = Progress.objects.filter(user=request.user)
    completed = progress.filter(is_solved=True).count()
    attempted = progress.count()
    submitted = Submission.objects.filter(user=request.user).order_by('-created_at')[:8]
    language_progress = {}
    for language in Language.objects.all():
        total = challenge_count = Challenge.objects.filter(language=language).count()
        solved = progress.filter(challenge__language=language, is_solved=True).count()
        language_progress[language.name] = {'total': total, 'solved': solved, 'percent': (solved / total) * 100 if total else 0}
    return render(request, 'main/dashboard.html', {
        'completed': completed,
        'attempted': attempted,
        'submitted': submitted,
        'language_progress': language_progress,
    })


def about(request):
    return render(request, 'main/about.html', {'project_github_url': 'https://github.com/your-org/crack-the-code'})
