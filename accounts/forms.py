from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileSettingsForm(forms.Form):
    theme = forms.ChoiceField(choices=[('dark', 'Dark'), ('light', 'Light'), ('system', 'System')], required=False)
    accent_color = forms.CharField(max_length=7, required=False)
    editor_font_size = forms.IntegerField(min_value=10, max_value=22, required=False)
    editor_tab_size = forms.IntegerField(min_value=2, max_value=8, required=False)
    auto_indent = forms.BooleanField(required=False)
    default_language = forms.ChoiceField(choices=[('html', 'HTML'), ('css', 'CSS'), ('python', 'Python'), ('java', 'Java'), ('c', 'C')], required=False)
