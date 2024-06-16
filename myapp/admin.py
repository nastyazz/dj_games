"""This module inclide admin."""
from django.contrib import admin

from .models import Client, Comment, GameClient, GameGenre, Games, Genre


class GameClientInline(admin.TabularInline):
    """Class for table GameClient."""

    model = GameClient
    extra = 1


class GameGenreInline(admin.TabularInline):
    """Class for table GameGenre."""

    model = GameGenre
    extra = 1


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    """Class for tabe Game."""

    model = Games
    inlines = [GameClientInline, GameGenreInline]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Class for table Client."""

    model = Client
    inlines = [GameClientInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Class fot table Comment."""

    model = Comment


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Class for table Genre."""

    model = Genre
    inlines = [GameGenreInline]


@admin.register(GameClient)
class GameBuyerAdmin(admin.ModelAdmin):
    """Class for table GameClient."""

    model = GameClient


@admin.register(GameGenre)
class GameGenreAdmin(admin.ModelAdmin):
    """Class for table GameGenre."""

    model = GameGenre
