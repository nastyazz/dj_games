"""This module about models."""
from datetime import date
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def check_date_created(dt: date) -> None:
    """Check date create.

    Args:
        dt: date create profule

    Raises:
        ValidationError: if date created in future
    """
    if dt > timezone.now().date():
        raise ValidationError(
            _('Date is bigger than current!'),
            params={'created': dt},
        )


def check_price(digit: float | int) -> None:
    """Check price about positive.

    Args:
        digit: price

    Raises:
        ValidationError: if price is not positive
    """
    if digit < 0:
        raise ValidationError(
            _('The price should be positive'),
        )


def check_money(digit: float | int) -> None:
    """Check money about positive.

    Args:
        digit: money

    Raises:
        ValidationError: if money is not positive
    """
    if digit < 0:
        raise ValidationError(
            _('The money should be positive'),
        )


def check_estimation(digit: float | int) -> None:
    """Check estimation about positive.

    Args:
        digit: estimation

    Raises:
        ValidationError: if estimation is not positive
    """
    if digit < 0:
        raise ValidationError(
            _('The estimation should be positive'),
        )


class UUIDMixin(models.Model):
    """Class for uuid."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        """Class Meta for UUIDMixin."""

        abstract = True


GAMES_GENRE = (
    ('Fiction', 'Fiction'),
    ('PVP', 'PVP'),
    ('Horror', 'Horror'),
    ('Card', 'Card'),
    ('Simulator', 'Sumilator'),
    ('Strategy', 'Strategy'),
    ('Casual', 'Casual'),
    ('Adventures', 'Adventures'),
    ('Verbal', 'Verbal'),
    ('Puzzles', 'Puzzles'),
)

TWOHUNDRED = 200
THREEHUNDRED = 300


class Genre(UUIDMixin):
    """Class Genre game."""

    title = models.TextField(
        _('title'),
        null=False,
        blank=False,
        max_length=TWOHUNDRED,
        choices=GAMES_GENRE,
    )
    game = models.ManyToManyField('Games', through='GameGenre')

    def __str__(self) -> str:
        """Write title of genre.

        Returns:
            str: title genre
        """
        return self.title

    class Meta:
        """Class Meta about Genre."""

        db_table = '"games_data"."genre"'
        ordering = ['title']
        verbose_name = _('genre')
        verbose_name_plural = _('genre')


class Games(UUIDMixin):
    """Class of Games."""

    title = models.TextField(_('title'), null=False, blank=False, max_length=100)
    price = models.DecimalField(
        verbose_name=('price'),
        decimal_places=2,
        max_digits=10,
        default=0,
        validators=[check_price],
    )

    clients = models.ManyToManyField('Client', through='GameClient')
    genres = models.ManyToManyField(Genre, through='GameGenre')

    def __str__(self) -> str:
        """Write info of game.

        Returns:
            str: info of game
        """
        return f'"{self.title}", {self.genres}, {self.price}'

    class Meta:
        """Class Meta about Games."""

        db_table = '"games_data"."games"'
        ordering = ['title', 'genre', 'price']
        verbose_name = _('games')
        verbose_name_plural = _('games')


class Client(UUIDMixin):
    """Class of Client."""

    user = models.OneToOneField(
        User,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    nickname = models.TextField(_('nickname'), null=False, blank=False, max_length=THREEHUNDRED)
    money = models.DecimalField(
        _('money'),
        decimal_places=2,
        max_digits=10,
        default=0,
        validators=[check_money],
    )
    date_registrate = models.DateField(
        _('date_registrate'),
        validators=[check_date_created],
        auto_now_add=True,
    )

    game = models.ManyToManyField(Games, through='GameClient')

    def __str__(self) -> str:
        """Write info of client.

        Returns:
            str: info of client
        """
        return f'"{self.nickname}", {self.date_registrate.isoformat()}'

    class Meta:
        """Class Meta about Client."""

        db_table = '"games_data"."client"'
        ordering = ['nickname', 'date_registrate']
        verbose_name = _('client')
        verbose_name_plural = _('client')


class Comment(UUIDMixin):
    """Class of Comment."""

    description = models.TextField(_('description'), null=False, blank=False, max_length=1000)
    date_public = models.DateField(_('date_public'), default=timezone.now)
    estimation = models.DecimalField(
        verbose_name=_('estimation'),
        decimal_places=1,
        max_digits=5,
        default=0,
        validators=[check_estimation],
    )
    game = models.ForeignKey(Games, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self) -> str:
        """Wrire info of comment.

        Returns:
            str: info of comment
        """
        return f'{self.description}, {self.date_public.isoformat()}, {self.estimation}'

    class Meta:
        """Class Meta about Comment."""

        db_table = '"games_data"."comment"'
        ordering = ['description', 'date_public', 'estimation']
        verbose_name = _('comment')
        verbose_name_plural = _('comment')


class GameClient(UUIDMixin):
    """Class of game and client connection."""

    game = models.ForeignKey(Games, verbose_name=_('games'), on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, verbose_name=_('client'), on_delete=models.DO_NOTHING)
    in_cart = models.BooleanField(default=False)
    purchased = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Write info of gameclient table.

        Returns:
            str: info of gameclient table
        """
        return f'{self.game.title} - {self.client.nickname}'

    class Meta:
        """Class Meta about GameClient."""

        db_table = '"games_data"."games_to_client"'
        unique_together = (('game', 'client'),)
        verbose_name = _('relationship games client')
        verbose_name_plural = _('relationships games client')


class GameGenre(UUIDMixin):
    """Class of game and genre connection."""

    game = models.ForeignKey(Games, verbose_name=_('game'), on_delete=models.DO_NOTHING)
    genre = models.ForeignKey(Genre, verbose_name=_('genre'), on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        """Write info of gamegenre table.

        Returns:
            str: info of gameclient table
        """
        return f'{self.game.title} - {self.genre.title}'

    class Meta:
        """Class Meta about GameGenre table."""

        db_table = '"games_data"."games_to_genre"'
        unique_together = (
            ('game', 'genre'),
        )
        verbose_name = _('relationship games genre')
        verbose_name_plural = _('relationships games genre')
