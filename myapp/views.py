"""This module include views."""
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from rest_framework import authentication, permissions, viewsets

from .forms import GameForm, RegistrationForm
from .models import Client, Comment, GameClient, Games, Genre
from .serializers import (ClientSerializer, CommentSerializer, GamesSerializer,
                          GenreSerializer)


@login_required
def home(request):
    """
    Show display the home page with a list of games and user-specific information.

    Args:
        request: the HTTP request object containing user data and query parameters

    Returns:
        HttpResponse: The HTTP response rendering the 'home.html' template with the context data
    """
    query = request.GET.get('query')
    games_q = Games.objects.filter(title__icontains=query) if query else None
    games_all = Games.objects.all()
    paginator = Paginator(games_all, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cart_count = GameClient.objects.filter(client__user=request.user, in_cart=True).count()
    money_client = Client.objects.get(user=request.user).money
    return render(request, 'home.html', {
        'games_q': games_q,
        'page_obj': page_obj,
        'cart_count': cart_count,
        'money_client': money_client,
    })


def register_view(request):
    """
    Handle user registration.

    Args:
        request: the HTTP request object containing user data and POST data if applicable

    Returns:
        HttpResponse: the HTTP response rendering the 'registration/register.html' template with the form context
        HttpResponseRedirect: redirect to the home page if the user is already authenticated or after successful registration
    """
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """
    Handle user login.

    Args:
        request: the HTTP request object containing user data and POST data if applicable

    Returns:
        HttpResponse: the HTTP response rendering the 'registration/login.html' template with the form context
        HttpResponseRedirect: redirect to the home page after successful login
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """Handle user logout.

    Args:
        request: the HTTP request object containing user data

    Returns:
        HttpResponseRedirect: redirect to the home page after logout
    """
    logout(request)
    return redirect('home')


def register(request):
    """Handle user registration.

    Args:
        request: The HTTP request object containing user data and POST data if applicable

    Returns:
        HttpResponse: the HTTP response rendering the 'registration/register.html' template with the form context and errors
        HttpResponseRedirect: redirect to the home page after successful registration
    """
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
        {'form': form, 'errors': errors},
    )


safe_methods = 'GET', 'HEAD', 'OPTIONS'
unsafe_methods = 'POST', 'DELETE', 'PUT'


class MyPermission(permissions.BasePermission):
    """Custom permission class to handle permission checks based on request methods."""

    def has_permission(self, request, _):
        """
        Check if the user has permission to access the view based on the request method.

        Args:
            request: the HTTP request object containing the user and method
            _ (Any): placeholder for the view argument (not used in this method)

        Returns:
            bool: true if the user has the appropriate permissions, False otherwise
        """
        if request.method in safe_methods:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in unsafe_methods:
            return bool(request.user and request.user.is_superuser)
        return False


def create_viewset(model_class, serializer):
    """
    Create a viewset for a given model class and serializer.

    Args:
        model_class: the Django model class for which the viewset is being created
        serializer: the serializer class to use for the viewset

    Returns:
        Type: a dynamically created viewset class for the specified model and serializer
    """
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
    """
    Display the catalog of games associated with the authenticated user.

    Args:
        request: the HTTP request object

    Returns:
        HttpResponse: the rendered 'games.html' template with the user's games
    """
    if not request.user.is_authenticated:
        return redirect('home')
    client_id = Client.objects.filter(user=request.user.id)[0].id
    instances = Games.objects.filter(clients=client_id)
    return render(request, 'games.html', context={'games_list': instances})


def games_comments(request: HttpRequest, game_id):
    """
    Display comments for a specific game.

    Args:
        request: the HTTP request object
        game_id: The ID of the game

    Returns:
        HttpResponse: the rendered 'games_comments.html' template with the game's comments
    """
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
    """
    Add a game to the user's cart.

    Args:
        request: the HTTP request object
        game_id: the ID of the game to be added

    Returns:
        HttpResponseRedirect: redirects to 'home'
    """
    client = Client.objects.get(user=request.user)
    game = get_object_or_404(Games, pk=game_id)
    game_client, created = GameClient.objects.get_or_create(client=client, game=game)
    game_client.in_cart = True
    game_client.save()
    return redirect('home')


@login_required
def buy_game(request: HttpRequest, game_id):
    """
    Purchase a game for the user.

    Args:
        request: the HTTP request object
        game_id: the ID of the game to be purchased

    Raises:
        ValidationError: if the user does not have enough money to buy the game

    Returns:
        HttpResponseRedirect: redirects to 'cart'
    """
    client = Client.objects.get(user=request.user)
    game = get_object_or_404(Games, pk=game_id)

    if client.money < game.price:
        raise ValidationError('You have not money.')

    client.money = client.money - game.price
    client.save()

    game_client, created = GameClient.objects.get_or_create(client=client, game=game)

    if game_client.in_cart:
        game_client.in_cart = False
    game_client.purchased = True
    game_client.save()

    return redirect('cart')


@login_required
def remove_from_cart(request, game_id):
    """
    Remove a game from the user's cart.

    Args:
        request: the HTTP request object.
        game_id: the ID of the game to be removed

    Returns:
        HttpResponseRedirect: redirects to 'home'
    """
    client = Client.objects.get(user=request.user)
    game = get_object_or_404(Games, pk=game_id)
    game_client = GameClient.objects.get(client=client, game=game)
    game_client.in_cart = False
    game_client.save()
    return redirect('home')


def search_games(request):
    """
    Search for games by title.

    Args:
        request: the HTTP request object

    Returns:
        HttpResponse: the rendered 'home.html' template with the search results
    """
    query = request.GET.get('query')
    if query:
        games = Games.objects.filter(title__icontains=query)
    else:
        games = Games.objects.none()
    return render(request, 'home.html', {'games': games})


@login_required
def view_cart(request):
    """
    Display the user's cart with the games added to it.

    Args:
        request: the HTTP request object

    Returns:
        HttpResponse: the rendered 'cart.html' template with the cart items
    """
    client = Client.objects.get(user=request.user)
    cart_items = GameClient.objects.filter(client=client, in_cart=True)
    return render(request, 'cart.html', {'cart_items': cart_items})


@login_required
def game_details(request: HttpRequest, game_id):
    """
    Display details for a specific game, including comments.

    Args:
        request: the HTTP request object
        game_id: the ID of the game

    Returns:
        HttpResponse: the rendered 'games_detail.html' template with the game's details and comments
    """
    game = get_object_or_404(Games, id=game_id)
    client = Client.objects.get(user=request.user)
    if request.method == 'POST':
        description = request.POST.get('description')
        estimation = request.POST.get('estimation')
        if description and estimation:
            Comment.objects.create(
                description=description,
                game=game,
                date_public=timezone.now(),
                estimation=estimation,
                client=client,
            )
            return redirect('games_detail', game_id=game.id)
    comments = Comment.objects.filter(game=game)
    count_comment_user = Comment.objects.all().filter(client=client).count()
    return render(request, 'games_detail.html', {'game': game, 'comments': comments, 'count_comment_user': count_comment_user})


@login_required
def add_game(request):
    """
    Add a new game to the catalog.

    Args:
        request: the HTTP request object

    Returns:
        HttpResponse: the rendered 'add_game.html' template with the form to add a new game
        HttpResponseRedirect: redirects to 'home' upon successful form submission
    """
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
    """
    Delete a game from the catalog.

    Args:
        request: the HTTP request object
        game_id: the ID of the game to be deleted

    Returns:
        HttpResponse: the rendered 'confirm_delete.html' template with the game to be deleted
        HttpResponseRedirect: redirects to 'games' upon successful deletion
    """
    game_client = get_object_or_404(GameClient, game_id=game_id)

    if request.method == 'POST':
        game_client.delete()
        return redirect('games')

    return render(request, 'myapp/confirm_delete.html', {'game': game_client})


def delete_comment(request: HttpRequest, comment_id):
    """
    Delete a comment.

    Args:
        request: the HTTP request object
        comment_id: the ID of the comment to be deleted

    Returns:
        HttpResponseRedirect: redirects to the game's detail page
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('games_detail', comment.game.id)


def update_comment(request: HttpRequest, comment_id):
    """
    Update a comment.

    Args:
        request: the HTTP request object
        comment_id: the ID of the comment to be updated

    Returns:
        HttpResponse: the rendered 'comment_update.html' template with the comment to be updated
        HttpResponseRedirect: redirects to the game's detail page upon successful form submission
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    game_id = comment.game.id
    if request.method == 'POST':
        description = request.POST.get('description')
        estimation = request.POST.get('estimation')
        comment.estimation = estimation
        comment.description = description
        comment.save()
        return redirect('games_detail', game_id)
    return render(request, 'comment_update.html', {'game_id': game_id, 'comment_id': comment_id})
