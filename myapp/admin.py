from django.contrib import admin
from .models import Games, Client, Comment, Genre, GameClient, GameGenre

class GameClientInline(admin.TabularInline):
    model = GameClient
    extra = 1

class GameGenreInline(admin.TabularInline):
    model = GameGenre
    extra = 1

@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    model = Games
    inlines = [GameClientInline, GameGenreInline]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = [GameClientInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    model = Genre
    inlines = [GameGenreInline]

@admin.register(GameClient)
class GameBuyerAdmin(admin.ModelAdmin):
    model = GameClient

@admin.register(GameGenre)
class GameGenreAdmin(admin.ModelAdmin):
    model = GameGenre
