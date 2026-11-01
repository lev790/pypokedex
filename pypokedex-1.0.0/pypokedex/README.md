# PyPokedex

A lightweight Python library for Pokémon lookups, random Pokémon, type data,
and generation lists. It uses the public [PokéAPI](https://pokeapi.co/) and
has no third-party runtime dependencies.

## Install

From this folder:

```bash
python -m pip install .
```

Or install the built wheel from a package build. Python 3.9+ is supported.

## Quick start

```python
import pypokedex

# Look up a Pokémon by name or National Pokédex number
pikachu = pypokedex.get_pokemon("pikachu")
print(pikachu["name"], pikachu["id"])  # pikachu 25

# Find a Pokédex number
print(pypokedex.get_pokedex_number("charizard"))  # 6

# Get the name for a Pokédex number
print(pypokedex.get_pokemon_name(150))  # mewtwo

# Generate a random Pokémon
print(pypokedex.random_pokemon()["name"])

# Restrict random selection to a range
print(pypokedex.random_pokemon(1, 151)["name"])

# Search by part of a name
print([p["name"] for p in pypokedex.search_pokemon("saur")])

# Get types and abilities
print(pypokedex.get_pokemon_types("bulbasaur"))
print(pypokedex.get_pokemon_abilities("pikachu"))

# Get type information and a generation's species
fire = pypokedex.get_type("fire")
print(fire["damage_relations"]["double_damage_to"])
print(pypokedex.list_generation(1)[:10])

# Clear cached API responses
pypokedex.clear_cache()
```

## Main functions

| Function | Description |
|---|---|
| `get_pokemon(name_or_number)` | Full Pokémon data from PokéAPI |
| `get_pokedex_number(name)` | National Pokédex number |
| `get_pokemon_name(number)` | Canonical name for a number |
| `random_pokemon(min_number=1, max_number=1025)` | Random Pokémon record |
| `search_pokemon(query, limit=20)` | Search names by substring |
| `get_pokemon_types(name_or_number)` | List of type names |
| `get_pokemon_abilities(name_or_number)` | List of ability names |
| `get_type(type_name)` | Type details and damage relations |
| `list_generation(generation)` | Species names in a generation |
| `clear_cache()` | Clear the in-memory API cache |

## Notes

- An internet connection is required for the first lookup of a resource.
- Successful responses are cached in memory for 30 minutes.
- API errors raise `PokemonAPIError`; missing resources raise
  `PokemonNotFoundError`.
- PokéAPI data and availability are controlled by the PokéAPI project.
- Pokémon and related names are trademarks of their respective owners.
  This is an unofficial fan-made library and is not affiliated with Nintendo,
  Game Freak, or The Pokémon Company.

## License

MIT
