from django.db import models  # noqa F401
from django.utils.timezone import localtime


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='pokemons', blank=True, null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True, default=0)
    longitude = models.FloatField(blank=True, default=0)
    appeared_at = models.DateTimeField(blank=True, null=True)
    disappeared_at = models.DateTimeField(blank=True, null=True)
    level = models.IntegerField(blank=True, default=0)
    health = models.IntegerField(blank=True, default=0)
    strength = models.IntegerField(blank=True, default=0)
    defence = models.IntegerField(blank=True, default=0)
    stamina = models.IntegerField(blank=True, default=0)

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
