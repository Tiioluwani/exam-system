from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.role = 'student'  # Explicitly set role as 'student' for this form
        if commit:
            user.save()
        return user
