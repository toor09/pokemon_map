from django.contrib import admin

from .models import Pokemon, PokemonElementType, PokemonEntity

admin.site.register(Pokemon)
admin.site.register(PokemonEntity)
admin.site.register(PokemonElementType)
