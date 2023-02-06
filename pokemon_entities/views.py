import folium

from django.shortcuts import get_object_or_404, render

from .models import PokemonEntity, Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
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


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.select_related('pokemon')

    pokemons = [pokemon_entity for pokemon_entity in pokemon_entities if pokemon_entity.pokemon.photo and pokemon_entity.is_active]

    for pokemon in pokemons:
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon.latitude,
            lon=pokemon.longitude,
            image_url=request.build_absolute_uri(pokemon.pokemon.photo.url)
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.pk,
            'img_url': pokemon.photo.url if pokemon.photo else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    current_pokemon = {
        'pokemon_id': pokemon.id,
        'img_url': request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else DEFAULT_IMAGE_URL,
        'title_ru': pokemon.title,
    }

    pokemon_entities = PokemonEntity.objects.filter(pokemon__title=pokemon.title)
    pokemons = [pokemon_entity for pokemon_entity in pokemon_entities if pokemon_entity.pokemon.photo]

    for pokemon in pokemons:
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon.latitude,
            lon=pokemon.longitude,
            image_url=request.build_absolute_uri(pokemon.pokemon.photo.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': current_pokemon
    })
