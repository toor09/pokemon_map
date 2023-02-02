from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
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

    def __str__(self):
        return f'{self.pokemon}: ({self.latitude} , {self.longitude})'
