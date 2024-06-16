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
from django.contrib.auth import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('games', views.GamesViewSet)
router.register('clients', views.ClientViewSet)
router.register('comment', views.CommentViewSet)
router.register('genre', views.GenreViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.users_games_catalog, name='games'),
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/', include(router.urls), name='api'),
    path('games_comments/<uuid:game_id>/', views.games_comments, name='games_comments'),
    path('search/', views.search_games, name='search_games'),
    path('add_game/', views.add_game, name='add_game'),
    path('games/<uuid:game_id>/delete/', views.delete_game, name='confirm_delete'),
    path('cart', views.view_cart, name='cart'),
    path('add_to_cart/<uuid:game_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy_game/<uuid:game_id>/', views.buy_game, name='buy_game'),
    path('remove_from_cart/<uuid:game_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('games_detail/<uuid:game_id>/', views.game_details, name='games_detail'),
    path('comments/<uuid:comment_id>/delete', views.delete_comment, name='comment_delete'),
    path('comments/<uuid:comment_id>/update', views.update_comment, name='update_comment'),
]
