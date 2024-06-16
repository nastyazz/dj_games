"""This module include serializer."""
from django.utils import timezone
from rest_framework import serializers

from .models import Client, Comment, Games, Genre


def check_date(dt) -> bool:
    """
    Check if the given date is in the future.

    Args:
        dt: The date to check.

    Returns:
        bool: True if the date is in the future, False otherwise.
    """
    return dt > timezone.now().date()


class GamesSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Games model.

    This serializer converts the Games model instance into a JSON representation
    and validates the data for creating or updating a Games instance.
    """

    class Meta:
        """Class Meta about GamesSerializer."""

        model = Games
        fields = [
            'id', 'title', 'price',
        ]


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Client model.

    This serializer converts the Client model instance into a JSON representation
    and validates the data for creating or updating a Client instance.
    """

    date_registrate = serializers.DateField(format='%Y-%m-%d')

    class Meta:
        """Class Meta about ClientSerializer."""

        model = Client
        fields = [
            'id', 'nickname', 'money', 'date_registrate',
        ]

    def validate(self, date_registrate):
        """Validate the date_registrate field.

        Args:
            date_registrate: data

        Raises:
            ValidationError: if the date_registrate is in the future.

        Returns:
            validation date_registrate
        """
        if check_date(date_registrate['date_registrate']):
            raise serializers.ValidationError('Registration date cannot be in the future.')
        return super().validate(date_registrate)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Comment model.

    This serializer converts the Comment model instance into a JSON representation
    and validates the data for creating or updating a Comment instance.
    """

    date_public = serializers.DateField(format='%Y-%m-%d')

    class Meta:
        """Class Meta about CommentSerializer."""

        model = Comment
        fields = [
            'id', 'description', 'date_public', 'estimation',
        ]

    def validate(self, date_registrate):
        """Validate the date_registrate field.

        Args:
            date_registrate: data

        Raises:
            ValidationError: if the date_registrate is in the future.

        Returns:
            validation date_registrate
        """
        if check_date(date_registrate['date_public']):
            raise serializers.ValidationError('Publication date cannot be in the future.')
        return super().validate(date_registrate)


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Genre model.

    This serializer converts the Genre model instance into a JSON representation
    and validates the data for creating or updating a Genre instance.
    """

    class Meta:
        """Class Meta about GenreSerializer."""

        model = Genre
        fields = [
            'id', 'title',
        ]
