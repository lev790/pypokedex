"""PokéAPI client. Uses only Python's standard library."""

from __future__ import annotations

import json
import random
import re
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

_BASE_URL = "https://pokeapi.co/api/v2"
_TIMEOUT = 12
_CACHE_TTL = 60 * 30
_cache: dict[str, tuple[float, dict]] = {}
_lock = threading.Lock()


class PokemonAPIError(Exception):
    """Raised when the PokéAPI cannot be reached or returns invalid data."""


class PokemonNotFoundError(PokemonAPIError):
    """Raised when a Pokémon or resource does not exist."""


def _request(endpoint: str) -> dict:
    url = f"{_BASE_URL}/{endpoint.strip('/')}/"
    now = time.time()
    with _lock:
        cached = _cache.get(url)
        if cached and now - cached[0] < _CACHE_TTL:
            return cached[1]

    req = Request(url, headers={"User-Agent": "pypokedex/1.0.0"})
    try:
        with urlopen(req, timeout=_TIMEOUT) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code == 404:
            raise PokemonNotFoundError(f"No Pokémon/resource found for: {endpoint}") from exc
        raise PokemonAPIError(f"PokéAPI returned HTTP {exc.code}") from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise PokemonAPIError(f"Could not retrieve data from PokéAPI: {exc}") from exc

    if not isinstance(data, dict):
        raise PokemonAPIError("PokéAPI returned an unexpected response.")
    with _lock:
        _cache[url] = (now, data)
    return data


def _slug(value: str | int) -> str:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise TypeError("Pokémon identifier must be a name (str) or Pokédex number (int).")
    normalized = re.sub(r"[\s.]+", "-", str(value).strip().lower())
    return quote(normalized, safe="-")


def get_pokemon(identifier: str | int) -> dict:
    """Get a Pokémon's full PokéAPI record by name or National Pokédex number."""
    if isinstance(identifier, str) and not identifier.strip():
        raise ValueError("Pokémon name cannot be empty.")
    return _request(f"pokemon/{_slug(identifier)}")


def get_pokedex_number(name: str) -> int:
    """Return the National Pokédex number for a Pokémon name."""
    return int(get_pokemon(name)["id"])


def get_pokemon_name(number: int) -> str:
    """Return the canonical Pokémon name for a National Pokédex number."""
    return str(get_pokemon(number)["name"])


def random_pokemon(min_number: int = 1, max_number: int = 1025) -> dict:
    """Return a random Pokémon record from an inclusive Pokédex number range.

    The default range covers the 1,025 species known in the current main
    Pokédex dataset. The API remains the source of truth for availability.
    """
    if not isinstance(min_number, int) or not isinstance(max_number, int):
        raise TypeError("Pokédex bounds must be integers.")
    if min_number < 1 or max_number < min_number:
        raise ValueError("Use bounds where 1 <= min_number <= max_number.")
    return get_pokemon(random.randint(min_number, max_number))


def search_pokemon(query: str, limit: int = 20) -> list[dict]:
    """Find Pokémon whose names contain query (case-insensitive).

    Searches the API's Pokémon index. Returns small records with ``name``
    and ``url``; use get_pokemon(name) for full details.
    """
    query = query.strip().lower()
    if not query:
        raise ValueError("Search query cannot be empty.")
    if not isinstance(limit, int) or limit < 1:
        raise ValueError("limit must be a positive integer.")
    index = _request("pokemon?limit=2000")
    matches = [item for item in index.get("results", []) if query in item["name"]]
    return matches[:limit]


def get_pokemon_types(identifier: str | int) -> list[str]:
    """Return a Pokémon's types, e.g. ['grass', 'poison']."""
    data = get_pokemon(identifier)
    return [entry["type"]["name"] for entry in data["types"]]


def get_pokemon_abilities(identifier: str | int) -> list[str]:
    """Return a Pokémon's abilities (including hidden abilities)."""
    data = get_pokemon(identifier)
    return [entry["ability"]["name"] for entry in data["abilities"]]


def get_type(type_name: str) -> dict:
    """Get type details, including damage relations and Pokémon of that type."""
    if not type_name.strip():
        raise ValueError("Type name cannot be empty.")
    return _request(f"type/{_slug(type_name)}")


def list_generation(generation: str | int) -> list[str]:
    """List Pokémon species names in a generation (e.g. 1 or 'generation-i')."""
    if isinstance(generation, int):
        if generation < 1:
            raise ValueError("Generation number must be positive.")
        generation = f"generation-{_roman(generation)}"
    data = _request(f"generation/{_slug(generation)}")
    return sorted(item["name"] for item in data.get("pokemon_species", []))


def _roman(number: int) -> str:
    pairs = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    result = ""
    for value, numeral in pairs:
        while number >= value:
            result += numeral
            number -= value
    return result


def clear_cache() -> None:
    """Clear the in-memory response cache."""
    with _lock:
        _cache.clear()
