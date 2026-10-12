"""
Web forms for user registration and publisher management.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Publisher


class UserRegisterForm(UserCreationForm):
    """Form for registering new users with role selection."""
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']


class PublisherForm(forms.ModelForm):
    """Form for creating and managing publishers."""
    class Meta:
        model = Publisher
        fields = ['name']
