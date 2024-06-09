from rest_framework import viewsets, permissions, authentication
from .models import Games, Client, Comment, Genre, GameClient
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from typing import Any
from .serializers import GamesSerializer, ClientSerializer, GenreSerializer, CommentSerializer
from .forms import RegistrationForm
from django.http.request import HttpRequest
from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, GameForm
from django.utils import timezone
from django.core.exceptions import ValidationError

@login_required
def home(request):
    query = request.GET.get('query')
    games_q = Games.objects.filter(title__icontains=query) if query else None
    games_all = Games.objects.all()
    paginator = Paginator(games_all, 10)  # Показывать 10 игр на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cart_count = GameClient.objects.filter(client__user=request.user, in_cart=True).count()
    
    return render(request, 'home.html', {
        'games_q': games_q,
        'page_obj': page_obj,
        'cart_count': cart_count
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Перенаправление аутентифицированного пользователя на домашнюю страницу
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Перенаправление после успешной регистрации
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    errors = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
            return redirect('home')
        else:
            errors = form.errors
    else:
        form = RegistrationForm()
    return render(
        request,
        'registration/register.html',
        {'form': form, 'errors': errors}
    )


safe_methods = 'GET', 'HEAD', 'OPTIONS'
unsafe_methods = 'POST', 'DELETE', 'PUT'

class MyPermission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in safe_methods:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in unsafe_methods:
            return bool(request.user and request.user.is_superuser)
        return False

def create_viewset(model_class, serializer):
    class ViewSet(viewsets.ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = serializer
        permission_classes = [MyPermission]
        authentication_classes = [authentication.TokenAuthentication, authentication.BasicAuthentication]

    return ViewSet

GamesViewSet = create_viewset(Games, GamesSerializer)
ClientViewSet = create_viewset(Client, ClientSerializer)
GenreViewSet = create_viewset(Genre, GenreSerializer)
CommentViewSet = create_viewset(Comment, CommentSerializer)

def users_games_catalog(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('home')
    print(request.user.id)
    client_id = Client.objects.filter(user=request.user.id)[0].id
    instances = Games.objects.filter(clients=client_id)
    return render(request, 'games.html', context={'games_list': instances})

def games_comments(request: HttpRequest, game_id):
    if not request.user.is_authenticated:
        return redirect('home')
    
    client = Client.objects.filter(user=request.user).first()
    if not client:
        return render(request, 'error.html', {'error_message': 'User is not associated with a client.'})
    
    game = get_object_or_404(Games, pk=game_id)
    comments = Comment.objects.filter(game=game)
    return render(request, 'games_comments.html', {'game': game, 'comments': comments})


@login_required
def add_to_cart(request, game_id):
    client = Client.objects.get(user=request.user)
    game = get_object_or_404(Games, pk=game_id)
    game_client, created = GameClient.objects.get_or_create(client=client, game=game)
    game_client.in_cart = True
    game_client.save()
    return redirect('home')

@login_required
def buy_game(request: HttpRequest, game_id):
    client = Client.objects.get(user=request.user)
    game = get_object_or_404(Games, pk=game_id)
    
    if client.money < game.price:
        raise ValidationError('You have not money.')

    game_client, created = GameClient.objects.get_or_create(client=client, game=game)
    
    if game_client.in_cart:
        # Убираем игру из корзины
        game_client.in_cart = False

    # Отмечаем игру как купленную
    game_client.purchased = True
    game_client.save()
    
    return redirect('cart')



@login_required
def remove_from_cart(request, game_id):
    client = Client.objects.get(user=request.user)
    game = get_object_or_404(Games, pk=game_id)
    game_client = GameClient.objects.get(client=client, game=game)
    game_client.in_cart = False
    game_client.save()
    return redirect('home')

def search_games(request):
    query = request.GET.get('query')
    if query:
        games = Games.objects.filter(title__icontains=query)
    else:
        games = Games.objects.none()
    return render(request, 'home.html', {'games': games})

@login_required
def view_cart(request):
    client = Client.objects.get(user=request.user)
    cart_items = GameClient.objects.filter(client=client, in_cart=True)
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def game_details(request, game_id):
    game = get_object_or_404(Games, id=game_id)
    if request.method == 'POST':
        description = request.POST.get('description')
        estimation = request.POST.get('estimation')
        if description and estimation:
            Comment.objects.create(
                description=description,
                game=game,
                date_public=timezone.now(),
                estimation=estimation
            )
            return redirect('games_detail', game_id=game.id)
    comments = Comment.objects.filter(game=game)
    return render(request, 'games_detail.html', {'game': game, 'comments': comments})


@login_required
def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GameForm()
    return render(request, 'add_game.html', {'form': form})


@login_required
def delete_game(request, game_id):
    game_client = get_object_or_404(GameClient, game_id=game_id)

    if request.method == "POST":
        game_client.delete()
        return redirect('games')  # Редирект на страницу списка игр пользователя

    return render(request, 'myapp/confirm_delete.html', {'game': game_client})