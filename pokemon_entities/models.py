from django.core.validators import MinValueValidator
from django.db import models  # noqa F401


class PokemonElementType(models.Model):
    title = models.CharField(max_length=50, verbose_name='Тип стихии')

    def __str__(self) -> str:
        return f'<{self.pk}> {self.title}'


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя (RU)')
    title_en = models.CharField(max_length=200, verbose_name='Имя (EN)', blank=True, null=True)
    title_jp = models.CharField(max_length=200, verbose_name='Имя (JP)', blank=True, null=True)
    description = models.TextField(blank=True, verbose_name='Описание', null=True)
    photo = models.ImageField(
        upload_to='pokemons',
        verbose_name='Фотокарточка',
        blank=True,
        null=True
    )
    element_type = models.ManyToManyField(
        PokemonElementType,
        verbose_name='Тип стихии',
        related_name='element_types',
    )
    previous_evolution = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Предыдущая эволюция',
        related_name='next_evolutions',
    )

    def __str__(self) -> str:
        return f'<{self.pk}> {self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон',
        related_name='entities'
    )
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появится в')
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет в')
    level = models.IntegerField(
        verbose_name='Уровень',
        validators=[
            MinValueValidator(0),
        ],
    )
    health = models.IntegerField(
        verbose_name='Здоровье',
        validators=[
            MinValueValidator(0),
        ],
    )
    strength = models.IntegerField(
        verbose_name='Сила',
        validators=[
            MinValueValidator(0),
        ],
    )
    defence = models.IntegerField(
        verbose_name='Защита',
        validators=[
            MinValueValidator(0)
        ],
    )
    stamina = models.IntegerField(
        verbose_name='Выносливость',
        validators=[
            MinValueValidator(0),
        ],
    )

    def get_specs(self) -> dict:
        return {
            'Уровень': self.level,
            'Здоровье': self.health,
            'Сила': self.strength,
            'Защита': self.defence,
            'Выносливость': self.stamina
        }

    def __str__(self) -> str:
        return f'{self.pk} {self.pokemon}: ({self.latitude} , {self.longitude})'
