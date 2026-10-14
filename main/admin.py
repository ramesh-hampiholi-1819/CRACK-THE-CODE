from django.contrib import admin

from .models import Challenge, Language, Progress, Submission, Tutorial


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_featured')


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'difficulty', 'order')


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'difficulty', 'slug')
    search_fields = ('title', 'description')


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'is_solved', 'attempts')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'passed', 'created_at')
