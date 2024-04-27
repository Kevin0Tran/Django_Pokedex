"""Using the pokeapi.co to pull information and sprites"""
import json
import time
import requests
import sqlite3


def retrieve_json():
    pokemon = {}
    i = 1
    while i < 101:
        response_general = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{i}/", timeout=10)
        response_species = requests.get(
            f"https://pokeapi.co/api/v2/pokemon-species/{i}/", timeout=10)
        file_general = response_general.json()
        file_species = response_species.json()
        individual = {"national_dex": i, "name": file_general['name'],
                      "type": file_general['types'],
                      "weight": file_general['weight'], "height": file_general['height'],
                      "abilities": file_general['abilities'],
                      "species": file_species['genera'][7]['genus']}
        print(individual)
        pokemon[i] = individual
        i += 1
        time.sleep(1)
    return pokemon


def write_to_json(json_load, name):
    with open(f'{name}.json', 'w') as f:
        json.dump(json_load, f)


def write_to_database(json):
    with open(json, 'r') as f:
        data = json.load(f)

    con = sqlite3.connect('pokedex/db.sqlite3', isolation_level=None)
    cur = con.cursor()
    for pokemon_number in data:
        poke_type = []
        abilities = []
        name = data[pokemon_number]['name']
        print(name)
        for num in range(len(data[pokemon_number]['type'])):
            poke_type.append(data[pokemon_number]['type']
                             [num]['type']['name'].title())
        pokemon_type = ' / '.join(poke_type)
        # print(pokemon_type)
        weight = data[pokemon_number]['weight']/10.0
        print(weight)
        height = data[pokemon_number]['height']/10.0
        print(height)
        for num in range(len(data[pokemon_number]['abilities'])):
            abilities.append(data[pokemon_number]['abilities']
                             [num]['ability']['name'].title())
        abilities = ' / '.join(abilities)
        species = data[pokemon_number]['species']

        sql = f"""Insert or REPLACE INTO national_dex_pokemon
                        VALUES (
                        {pokemon_number},{
            pokemon_number},'{name}','{pokemon_type}', '{abilities}',
        {height} ,'{species}'
                        , {height} ,{weight}, {weight}
                        )
                        """
        res = cur.execute(sql)
        print(res.fetchone())
