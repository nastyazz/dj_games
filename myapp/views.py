from django.shortcuts import render
from rest_framework import viewsets, permissions, authentication
from .models import Games, Client, Comment, Genre
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render, redirect
from typing import Any
from .serializers import GamesSerializer, ClientSerializer, GenreSerializer, CommentSerializer
from .forms import RegistrationForm


def home_page(request):
    return render(
        request,
        "index.html",
        context={
            'games': Games.objects.count(),
            'clients': Client.objects.count(),
            'comments': Comment.objects.count(),
            'genres': Genre.objects.count(),
        },
    )


def create_listview(model_class, template, plural_name):
    class View(LoginRequiredMixin, ListView):
        model = model_class
        template_name = template
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            instances = model_class.objects.all()
            paginator = Paginator(instances, 10)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{plural_name}_list'] = page_obj
            return context
    return View

GamesListView = create_listview(Games, "catalog/games.html", "games")
ClientsListView = create_listview(Client, "catalog/clients.html", "clients")
CommentListView = create_listview(Comment, "catalog/comments.html", "comments")
GenreListView = create_listview(Genre, "catalog/genres.html", "genres")

def create_view(model_class, template, model_name):
    def view(request):
        target_id = request.GET.get("id", "")
        if request.user.is_authenticated:
            return render(
                request,
                template,
                context={
                    model_name: (
                        model_class.objects.get(id=target_id) if target_id else None
                    )
                },
            )
        return redirect("homepage")

    return view


game_view = create_view(Games, 'entities/game.html', 'game')
genre_view = create_view(Genre, 'entities/genre.html', 'genre')
client_view = create_view(Client, 'entities/client.html', 'client')
comment_view = create_view(Comment, 'entities/comment.html', 'comment')

def register(request):
    errors = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
            return redirect('homepage')
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
