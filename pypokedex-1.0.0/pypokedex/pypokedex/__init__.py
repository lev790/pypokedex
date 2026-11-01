"""A small Python library for looking up Pokémon using the PokéAPI."""

from .client import (
    PokemonAPIError,
    PokemonNotFoundError,
    get_pokemon,
    get_pokedex_number,
    get_pokemon_name,
    random_pokemon,
    search_pokemon,
    get_pokemon_types,
    get_pokemon_abilities,
    get_type,
    list_generation,
    clear_cache,
)

__version__ = "1.0.0"

__all__ = [
    "PokemonAPIError", "PokemonNotFoundError", "get_pokemon",
    "get_pokedex_number", "get_pokemon_name", "random_pokemon",
    "search_pokemon", "get_pokemon_types", "get_pokemon_abilities",
    "get_type", "list_generation", "clear_cache",
]
