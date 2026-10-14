from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    THEME_CHOICES = [
        ('dark', 'Dark'),
        ('light', 'Light'),
        ('system', 'System'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='system')
    accent_color = models.CharField(max_length=7, default='#4f46e5')
    editor_font_size = models.PositiveIntegerField(default=14)
    editor_tab_size = models.PositiveIntegerField(default=4)
    auto_indent = models.BooleanField(default=True)
    default_language = models.CharField(max_length=20, default='python')

    def __str__(self):
        return f'{self.user.username} profile'
