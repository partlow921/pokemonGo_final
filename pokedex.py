from pokemon import *
from move import Move


pokemon_entries={}

pokedex_db=open("pokedex.csv","r", encoding="windows-1252")
#Encoding added to run on Mac
pokedex_db.readline()
for line in pokedex_db:
    pokedex_id, name, type1, type2, weight, height, move_name, move_power, move_name2, move_power2, initial_lvl, gen_lvl_cap, evolve_to, evolve_lvl, catch_chance = line.strip().split(",")
    move=Move(move_name,float(move_power),type1)
    move2=Move(move_name2,float(move_power2),type2)
    pokemon_info={}
    pokemon_info["pokedex_id"]=int(pokedex_id)
    pokemon_info["name"]=name
    pokemon_info["type1"]=type1
    pokemon_info["type2"]=type2
    pokemon_info["weight"]=float(weight)
    pokemon_info["height"]=float(height)
    pokemon_info["move"]=move
    pokemon_info["move2"]=move2
    pokemon_info["initial_lvl"]=int(initial_lvl)
    pokemon_info["gen_lvl_cap"]=int(gen_lvl_cap)
    pokemon_info["evolve_to"]=evolve_to
    pokemon_info["evolve_lvl"]=int(evolve_lvl)
    pokemon_info["catch_chance"]=float(catch_chance)
    #vary catch chance in csv

    pokemon_entries[int(pokedex_id)]=pokemon_info

pokedex_db.close()
