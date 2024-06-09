from rest_framework import serializers
from .models import Games, Client, Comment, Genre, check_date_created
from django.utils import timezone


def check_date(dt) -> bool:
    return dt > timezone.now().date()

class GamesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Games
        fields = [
            'id', 'title', 'price',
        ]

class ClientSerializer(serializers.HyperlinkedModelSerializer):
    date_registrate = serializers.DateField(format='%Y-%m-%d')
    class Meta:
        model = Client
        fields = [
            'id', 'nickname', 'money', 'date_registrate',
        ]

    def validate(self, data):
        if check_date(data['date_registrate']):
            raise serializers.ValidationError()
        return super().validate(data)

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    date_public = serializers.DateField(format='%Y-%m-%d')
    class Meta:
        model = Comment
        fields = [
            'id', 'description', 'date_public', 'estimation',
        ]
    def validate(self, data):
        if check_date(data['date_public']):
            raise serializers.ValidationError()
        return super().validate(data)


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = [
            'id', 'title',
        ]