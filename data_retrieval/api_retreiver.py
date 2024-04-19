import requests
import time
import json

pokemon = {}
i = 1
while i < 101:
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}/")

    file = response.json()
    individual = {"national_dex": i, "name": file['name'], "type": file['types'],
                  "weight": file['weight'], "height": file['height'],
                  "abilities": file['abilities']}
    print(individual)
    pokemon[i] = individual
    i += 1
    time.sleep(1)

with open('pokemon.json', 'w') as f:
    json.dump(pokemon, f)
