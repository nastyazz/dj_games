"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

from . import views



router = DefaultRouter()
router.register(r'games', views.GamesViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'genre', views.GenreViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.users_games_catalog, name='games'),
    # path('game/', views.game_view, name='game'),
    # path('clients/', views.ClientListView.as_view(), name='clients'),
    # path('client/', views.client_view, name='client'),
    # path('comments/', views.CommentListView.as_view(), name='comments'),
    # path('comment/', views.comment_view, name='comment'),
    # path('genres/', views.GenreListView.as_view(), name='genres'),
    # path('genre/', views.gerne_view, name='genre'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls), name='api'),
    path('games_comments/<uuid:game_id>/', views.games_comments, name='games_comments'),
    path('search/', views.search_games, name='search_games'),
    path('add_game/', views.add_game, name='add_game'),
    path('games/<uuid:game_id>/delete/', views.delete_game, name='confirm_delete'),
    # path('profile/', views.profile, name='profile'),
    # path('buy/', views.buy, name='buy'),
    path('cart', views.view_cart, name='cart'),
    path('add_to_cart/<uuid:game_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy_game/<uuid:game_id>/', views.buy_game, name='buy_game'),
    path('remove_from_cart/<uuid:game_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('games_detail/<uuid:game_id>/', views.game_details, name='games_detail'),
]