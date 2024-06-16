"""This module include apps."""
from django.apps import AppConfig


class MyappConfig(AppConfig):
    """Class with my app config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
