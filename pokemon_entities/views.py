from typing import Union

import folium
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import localtime

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def _get_photo_uri(request: HttpRequest, photo_url: Union[Pokemon, PokemonEntity]) -> str:
    return request.build_absolute_uri(photo_url.url) if photo_url else DEFAULT_IMAGE_URL


def add_pokemon(
        folium_map: folium,
        lat: float,
        lon: float,
        image_url: str = DEFAULT_IMAGE_URL
) -> None:
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request: HttpRequest) -> HttpResponse:
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now = localtime()
    pokemon_entities = PokemonEntity.objects.select_related('pokemon').filter(
        disappeared_at__gte=now,
        appeared_at__lte=now,
    )

    pokemons = [
        pokemon_entity for pokemon_entity in pokemon_entities
        if pokemon_entity.pokemon.photo
    ]

    for pokemon in pokemons:
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon.latitude,
            lon=pokemon.longitude,
            image_url=_get_photo_uri(request=request, photo_url=pokemon.pokemon.photo)
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.pk,
            'img_url': _get_photo_uri(request=request, photo_url=pokemon.photo),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request: HttpRequest, pokemon_id: int) -> HttpRequest:
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    current_pokemon = {
        'pokemon_id': pokemon.id,
        'img_url': _get_photo_uri(request=request, photo_url=pokemon.photo),
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
    }
    if pokemon.previous_evolution:
        current_pokemon['previous_evolution'] = {
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': _get_photo_uri(request=request, photo_url=pokemon.previous_evolution.photo),
            'title_ru': pokemon.previous_evolution.title,
        }
    evolution = pokemon.next_evolutions.first()
    if evolution:
        current_pokemon['next_evolution'] = {
            'pokemon_id': evolution.id,
            'title_ru': evolution.title,
            'img_url': _get_photo_uri(request=request, photo_url=evolution.photo),
        }
    now = localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        disappeared_at__gte=now,
        appeared_at__lte=now,
    )
    pokemons = [
        pokemon_entity for pokemon_entity in pokemon_entities
        if pokemon_entity.pokemon.photo
    ]

    for pokemon in pokemons:
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon.latitude,
            lon=pokemon.longitude,
            image_url=_get_photo_uri(request=request, photo_url=pokemon.pokemon.photo),
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': current_pokemon
    })
