from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import ProfileSettingsForm, RegistrationForm
from .models import UserProfile


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now sign in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def settings_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST)
        if form.is_valid():
            profile.theme = form.cleaned_data.get('theme') or profile.theme
            profile.accent_color = form.cleaned_data.get('accent_color') or profile.accent_color
            profile.editor_font_size = form.cleaned_data.get('editor_font_size') or profile.editor_font_size
            profile.editor_tab_size = form.cleaned_data.get('editor_tab_size') or profile.editor_tab_size
            profile.auto_indent = bool(form.cleaned_data.get('auto_indent'))
            profile.default_language = form.cleaned_data.get('default_language') or profile.default_language
            profile.save()
            messages.success(request, 'Your preferences have been saved.')
            return redirect('settings')
    else:
        form = ProfileSettingsForm(initial={
            'theme': profile.theme,
            'accent_color': profile.accent_color,
            'editor_font_size': profile.editor_font_size,
            'editor_tab_size': profile.editor_tab_size,
            'auto_indent': profile.auto_indent,
            'default_language': profile.default_language,
        })
    return render(request, 'accounts/settings.html', {'form': form, 'profile': profile})
