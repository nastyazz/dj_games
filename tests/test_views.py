"""This module include test for views."""
from django.contrib.auth.models import User
from django.test import Client as TestClient
from django.test import TestCase
from django.urls import reverse

from myapp.models import Client, GameClient, Games, Genre

FIFTY = 50.0
TWOHUNDRED = 200
THREEHUNDREDANDTWO = 302


class ViewTests(TestCase):
    """Class about views test."""

    def setUp(self):
        """Set up initial data for each test case.

        Creates instances of TestClient, User, Games, Client, and GameClient for testing purposes.
        """
        self.client = TestClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.game = Games.objects.create(title='Test Game', price=FIFTY)
        self.client_model = Client.objects.create(user=self.user, nickname='testclient', money=100.0)
        self.game_client = GameClient.objects.create(client=self.client_model, game=self.game)

    def test_home_view(self):
        """Test case for the home view.

        Checks if the home page loads successfully and uses the correct template.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, TWOHUNDRED)
        self.assertTemplateUsed(response, 'home.html')

    def test_register_view(self):
        """Test case for the register view.

        Checks if the registration page loads successfully and uses the correct template.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, TWOHUNDRED)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_login_view(self):
        """Test case for the login view.

        Checks if the login page loads successfully and uses the correct template.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, TWOHUNDRED)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_add_to_cart(self):
        """Test case for adding a game to the cart.

        Checks if a game can be successfully added to the cart and the corresponding database entry is updated.
        """
        response = self.client.post(reverse('add_to_cart', args=[self.game.id]))
        self.assertEqual(response.status_code, THREEHUNDREDANDTWO)
        self.game_client.refresh_from_db()
        self.assertTrue(self.game_client.in_cart)

    def test_remove_from_cart(self):
        """Test case for removing a game from the cart.

        Checks if a game can be successfully removed from the cart and the corresponding database entry is updated.
        """
        self.game_client.in_cart = True
        self.game_client.save()
        response = self.client.post(reverse('remove_from_cart', args=[self.game.id]))
        self.assertEqual(response.status_code, THREEHUNDREDANDTWO)
        self.game_client.refresh_from_db()
        self.assertFalse(self.game_client.in_cart)

    def test_buy_game(self):
        """Test case for buying a game.

        Checks if a game can be successfully purchased and the corresponding database entries are updated.
        """
        response = self.client.post(reverse('buy_game', args=[self.game.id]))
        self.assertEqual(response.status_code, THREEHUNDREDANDTWO)
        self.game_client.refresh_from_db()
        self.assertTrue(self.game_client.purchased)

    def test_view_cart(self):
        """Test case for viewing the cart.

        Checks if the cart page loads successfully and uses the correct template.
        """
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, TWOHUNDRED)
        self.assertTemplateUsed(response, 'cart.html')

    def test_game_details(self):
        """Test case for viewing game details.

        Checks if the game details page loads successfully and uses the correct template.
        """
        response = self.client.get(reverse('games_detail', args=[self.game.id]))
        self.assertEqual(response.status_code, TWOHUNDRED)
        self.assertTemplateUsed(response, 'games_detail.html')

    def test_users_games_catalog(self):
        """Test case for viewing the games catalog.

        Checks if the games catalog page loads successfully and uses the correct template.
        """
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, TWOHUNDRED)
        self.assertTemplateUsed(response, 'games.html')

    def test_search_games(self):
        """Test case for searching games.

        Checks if the search functionality returns results successfully and uses the correct template.
        """
        response = self.client.get(reverse('search_games'), {'query': 'Test'})
        self.assertEqual(response.status_code, TWOHUNDRED)
        self.assertTemplateUsed(response, 'home.html')

    def test_add_game(self):
        """Test case for adding a new game.

        Checks if a new game can be successfully added and the corresponding database entry is created.
        """
        Genre.objects.create(title='testgenre')
        genre = Genre.objects.get(title='testgenre')
        response = self.client.post(reverse('add_game'), {'title': 'New Game', 'price': 60.0, 'genres': genre.id})
        self.assertEqual(response.status_code, THREEHUNDREDANDTWO)
        self.assertTrue(Games.objects.filter(title='New Game').exists())

    def test_delete_game(self):
        """Test case for deleting a game.

        Checks if a game can be successfully deleted and the corresponding database entry is removed.
        """
        response = self.client.post(reverse('confirm_delete', args=[self.game.id]))
        self.assertEqual(response.status_code, THREEHUNDREDANDTWO)
        self.assertFalse(GameClient.objects.filter(game=self.game).exists())
