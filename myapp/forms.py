"""This module include forms."""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, ModelForm

from .models import Games


class RegistrationForm(UserCreationForm):
    """Forms for RegistrtionForm."""

    first_name = CharField(max_length=100, required=True)
    last_name = CharField(max_length=100, required=True)
    email = CharField(max_length=100, required=True)

    class Meta:
        """Class Meta about Registration Form."""

        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class GameForm(ModelForm):
    """Forms for GameForm."""

    class Meta:
        """Class Meta about Game Form."""

        model = Games
        fields = ['title', 'price', 'genres']
