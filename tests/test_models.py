"""This module include test for models."""
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from myapp.models import (Client, Comment, GameClient, Games, Genre,
                          check_date_created, check_estimation, check_money,
                          check_price)

TEN = 10.0
FIFTY = 50.0
FOUR = 4.5


class ModelTests(TestCase):
    """Class about ModelTests."""

    def test_check_date_created(self):
        """Test case for check_date_created function.

        Raises a ValidationError if a future date is passed to check_date_created().
        """
        future_date = date.today() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            check_date_created(future_date)

    def test_check_price(self):
        """Test case for check_price function.

        Raises a ValidationError if a negative price is passed to check_price().
        """
        with self.assertRaises(ValidationError):
            check_price(-1)

    def test_check_money(self):
        """Test case for check_money function.

        Raises a ValidationError if a negative money value is passed to check_money().
        """
        with self.assertRaises(ValidationError):
            check_money(-1)

    def test_check_estimation(self):
        """Test case for check_estimation function.

        Raises a ValidationError if a negative estimation value is passed to check_estimation().
        """
        with self.assertRaises(ValidationError):
            check_estimation(-1)

    def test_client_creation(self):
        """Test case for creating a Client object.

        Creates a User and Client object, and verifies the attributes of the Client.
        """
        user = User.objects.create(username='testuser', password='12345')
        client = Client.objects.create(user=user, nickname='testclient', money=TEN)
        self.assertEqual(client.user.username, 'testuser')
        self.assertEqual(client.nickname, 'testclient')
        self.assertEqual(client.money, TEN)

    def test_game_creation(self):
        """Test case for creating a Games object.

        Creates a Games object and verifies its attributes.
        """
        game = Games.objects.create(title='Test Game', price=FIFTY)
        self.assertEqual(game.title, 'Test Game')
        self.assertEqual(game.price, FIFTY)

    def test_comment_creation(self):
        """Test case for creating a Comment object.

        Creates a Games object, then a Comment object associated with the game,
        and verifies the attributes of the Comment.
        """
        game = Games.objects.create(title='Test Game', price=FIFTY)
        comment = Comment.objects.create(description='Great game!', game=game, estimation=FOUR)
        self.assertEqual(comment.description, 'Great game!')
        self.assertEqual(comment.estimation, FOUR)
        self.assertEqual(comment.game, game)

    def test_genre_creation(self):
        """Test case for creating a Genre object.

        Creates a Genre object and verifies its attributes.
        """
        genre = Genre.objects.create(title='Fiction')
        self.assertEqual(genre.title, 'Fiction')

    def test_game_client_creation(self):
        """Test case for creating a GameClient object.

        Creates a User, Client, Games, and GameClient objects, and verifies the
        attributes of the GameClient.
        """
        user = User.objects.create(username='testuser', password='12345')
        client = Client.objects.create(user=user, nickname='testclient', money=TEN)
        game = Games.objects.create(title='Test Game', price=FIFTY)
        game_client = GameClient.objects.create(client=client, game=game)
        self.assertEqual(game_client.client, client)
        self.assertEqual(game_client.game, game)
