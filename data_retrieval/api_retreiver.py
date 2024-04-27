"""Using the pokeapi.co to pull information and sprites"""
import json
import time
import requests
import sqlite3


def retrieve_json():
    pokemon = {}
    i = 1
    while i < 152:
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


def write_to_database(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    con = sqlite3.connect('pokedex/db.sqlite3', isolation_level=None)
    cur = con.cursor()
    for pokemon_number in data:
        poke_type = []
        abilities = []
        name = data[pokemon_number]['name']
        for num in range(len(data[pokemon_number]['type'])):
            poke_type.append(data[pokemon_number]['type']
                             [num]['type']['name'].title())
        pokemon_type = ' / '.join(poke_type)
        weight_grams = data[pokemon_number]['weight']/10.0
        weight_imperial = data[pokemon_number]['weight']/10 * 2.2046
        height_meters = data[pokemon_number]['height']/10.0
        convert = height_meters * 39.37
        feet = round(convert//12)
        inches = round(convert - (feet * 12))
        height_imperial = f'{feet}ft {inches}in'
        for num in range(len(data[pokemon_number]['abilities'])):
            abilities.append(data[pokemon_number]['abilities']
                             [num]['ability']['name'].title())
        abilities = ' / '.join(abilities)
        species = data[pokemon_number]['species']
        print(pokemon_number)
        print(name)
        print(pokemon_type)
        print(species)
        print(height_meters)
        print(height_imperial)
        print(weight_grams)
        print(weight_imperial)
        print(abilities)
        sql = f"""Insert or REPLACE INTO national_dex_pokemon (national_number,
                name,type,species,height_meters,height_imperial,
                weight_grams,weight_imperial,abilities)
                        VALUES (
                            {pokemon_number},'{name}','{pokemon_type}',
                            '{species}',{height_meters} ,'{height_imperial}' ,
                            {weight_grams}, {weight_imperial},'{abilities}');
                        """
        res = cur.execute(sql)
        print(res.fetchone())


with open(r'/Users/home/Documents/Programming/django/pokemon/pokemon.json', 'r') as f:
    data = json.load(f)
for pokemon_number in data:
    img_data = requests.get(
        f'https://img.pokemondb.net/sprites/scarlet-violet/icon/avif/{data[pokemon_number]['name']}.avif', timeout=10).content
    with open(f'pokedex/national_dex/static/national_dex/sprite/{data[pokemon_number]['name']}.avif', 'wb') as handler:
        handler.write(img_data)
    print(data[pokemon_number]['name'])
    time.sleep(10)

# pokemon = retrieve_json()
# write_to_json(pokemon, 'pokemon')

# write_to_database(r'pokemon.json')
