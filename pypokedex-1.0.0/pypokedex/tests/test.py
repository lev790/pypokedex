import pypokedex as pypokedex

pokemon = pypokedex.random_pokemon()

print("Random Pokémon:", pokemon["name"])
print("Pokédex Number:", pokemon["id"])

print("Pikachu's number:",
      pypokedex.get_pokedex_number("pikachu"))