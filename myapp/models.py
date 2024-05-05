from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _
from datetime import timezone, datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def get_date() -> datetime:
    return datetime.now(timezone.utc).date()

def check_date_created(dt: datetime) -> None:
    if dt > get_date():
        raise ValidationError(
            _('Date is bigger than current!'),
            params={'created': dt}
        )

def check_price(digit: float | int) -> None:
    if digit < 0:
        raise ValidationError(
            _('The price should be positive')
        )
    
def check_money(digit: float | int) -> None:
    if digit < 0:
        raise ValidationError(
            _('The money should be positive')
        )
    
def check_estimation(digit: float | int) -> None:
    if digit < 0:
        raise ValidationError(
            _('The estimation should be positive')
        )

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True

GAMES_GENRE = (('Fiction', 'Fiction'),
               ('PVP', 'PVP'),
               ('Horror', 'Horror')
               )
class Genre(UUIDMixin):
    title = models.TextField(_('title'), null=False, blank=False, max_length=200, choices = GAMES_GENRE)
    game = models.ManyToManyField('Games', through='GameGenre')
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        db_table = '"games_data"."genre"'
        ordering = ['title']
        verbose_name = _('genre')
        verbose_name_plural = _('genre')

class Games(UUIDMixin):
    title = models.TextField(_('title'), null=False, blank=False, max_length=100)
    price = models.DecimalField(verbose_name=('price'), decimal_places=2, max_digits=10, default=0, validators=[check_price])
    
    clients = models.ManyToManyField('Client', through='GameClient')
    genres = models.ManyToManyField(Genre, through='GameGenre')

    def __str__(self) -> str:
        return f'"{self.title}", {self.genres}, {self.price}'

    class Meta:
        db_table = '"games_data"."games"'
        ordering = ['title', 'genre', 'price']
        verbose_name = _('games')
        verbose_name_plural = _('games')

class Client(UUIDMixin):
    user = models.OneToOneField(User, verbose_name=_('user'), on_delete=models.CASCADE, null=True, blank=True)
    nickname = models.TextField(_('nickname'),null=False, blank=False, max_length=300)
    money = models.DecimalField(_('money'), decimal_places=2, max_digits=10, default=0, validators=[check_money])
    date_registrate = models.DateField(_('date_registrate'), validators=[check_date_created])

    game = models.ManyToManyField(Games, through='GameClient')

    def __str__(self) -> str:
        return f'{self.nickname}: {self.date_registrate.isoformat()}'

    class Meta:
        db_table = '"games_data"."client"'
        ordering = ['nickname', 'date_registrate']
        verbose_name = _('client')
        verbose_name_plural = _('client')

class Comment(UUIDMixin):
    description = models.TextField(_('description'), null=False, blank=False, max_length=1000)
    date_public = models.DateField(_('date_public'), default=get_date)
    estimation = models.DecimalField(verbose_name=_('estimation'), decimal_places=1, max_digits=5, default=0, validators=[check_estimation])
    game = models.ForeignKey(Games, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.description}, {self.date_public.isoformat()}, {self.estimation}'

    class Meta:
        db_table = '"games_data"."comment"'
        ordering = ['description', 'date_public', 'estimation']
        verbose_name = _('comment')
        verbose_name_plural = _('comment')

class GameClient(UUIDMixin):
    game = models.ForeignKey(Games, verbose_name=_('games'), on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name=_('client'), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.game.title} - {self.client.nickname}'

    class Meta:
        db_table = '"games_data"."games_to_client"'
        unique_together = (
            ('game', 'client'),
        )
        verbose_name = _('relationship games client')
        verbose_name_plural = _('relationships games client')

class GameGenre(UUIDMixin):
    game = models.ForeignKey(Games, verbose_name=_('game'), on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, verbose_name=_('genre'), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.game.title} - {self.genre.title}'
    
    class Meta:
        db_table = '"games_data"."games_to_genre"'
        unique_together = (
            ('game', 'genre'),
        )
        verbose_name = _('relationship games genre')
        verbose_name_plural = _('relationships games genre')
