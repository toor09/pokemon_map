from django.db import models  # noqa F401
from django.utils.timezone import localtime
from django.core.validators import MaxValueValidator, MinValueValidator


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя (RU)')
    title_en = models.CharField(max_length=200, verbose_name='Имя (EN)', blank=True, null=True)
    title_jp = models.CharField(max_length=200, verbose_name='Имя (JP)', blank=True, null=True)
    description = models.TextField(blank=True, verbose_name='Описание', null=True)
    photo = models.ImageField(upload_to='pokemons', verbose_name='Фотокарточка', blank=True, null=True)
    previous_evolution = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Предыдущая эволюция',
        related_name='next_evolutions',
    )

    def __str__(self):
        return f'<{self.pk}> {self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон',
        related_name='entities'
    )
    latitude = models.FloatField(verbose_name='Широта', blank=True, default=0)
    longitude = models.FloatField(verbose_name='Долгота', blank=True, default=0)
    appeared_at = models.DateTimeField(verbose_name='Появится в', blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет в', blank=True, null=True)
    level = models.IntegerField(verbose_name='Уровень', validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, default=0)
    health = models.IntegerField(verbose_name='Здоровье', validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, default=0)
    strength = models.IntegerField(verbose_name='Сила', validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, default=0)
    defence = models.IntegerField(verbose_name='Защита', validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, default=0)
    stamina = models.IntegerField(verbose_name='Выносливость', validators=[MinValueValidator(0), MaxValueValidator(100)],blank=True, default=0)

    @property
    def is_active(self):
        now = localtime()
        appeared_at = localtime(self.appeared_at)
        disappeared_at = localtime(self.disappeared_at)

        if self.appeared_at and self.disappeared_at:
            if disappeared_at >= now >= appeared_at:
                return True
            return False

        elif not self.appeared_at and not self.disappeared_at:
            return True

        elif self.appeared_at and appeared_at <= now:
            return True

        elif self.disappeared_at and disappeared_at >= now:
            return True
        return False

    def __str__(self):
        return f'{self.pk} {self.pokemon}: ({self.latitude} , {self.longitude})'
