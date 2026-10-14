from django.conf import settings
from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=120)
    description = models.TextField()
    color = models.CharField(max_length=20, default='#4f46e5')
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Tutorial(models.Model):
    language = models.ForeignKey(Language, related_name='tutorials', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    excerpt = models.TextField()
    content = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate')], default='Beginner')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        unique_together = ('language', 'slug')

    def __str__(self):
        return self.title


class Challenge(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    language = models.ForeignKey(Language, related_name='challenges', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Easy')
    description = models.TextField()
    instructions = models.TextField(default='')
    starter_code = models.TextField(default='')
    example_input = models.TextField(default='')
    example_output = models.TextField(default='')
    constraints = models.TextField(default='')
    hints = models.TextField(default='')
    is_featured = models.BooleanField(default=False)
    expected_output = models.TextField(default='')

    class Meta:
        ordering = ['difficulty', 'title']

    def __str__(self):
        return self.title


class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='progress_entries')
    is_solved = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f'{self.user.username} - {self.challenge.title}'


class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='submissions')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='submissions')
    code = models.TextField()
    output = models.TextField(blank=True, default='')
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f'{self.user.username} submitted {self.challenge.title}'
        return f'Anonymous submission for {self.challenge.title}'
