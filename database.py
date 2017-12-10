import sqlite3
import random
from pokemon import *
from move import *
from item import *

db_name = "pokemonGo.db"

def check_user_name(player_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM players WHERE player_name='"+player_name+"'")
    result = len(c.fetchall())>0
    conn.close()

    return result

def get_user_info(username):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM players WHERE player_name='"+username+"'")
    player_name, password, level, experience= c.fetchone()
    conn.close()

    return player_name, password, level, experience

def sync_from_db(player):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    c.execute("SELECT * from player_items WHERE player_name='"+player.username+"'")
    for row in c.fetchall():
        player_name, item_name, quantity = row
        for i in range(quantity):
            player.bag.sync_items_by_name(item_name)
            
    c.execute("SELECT * from player_pokemon WHERE player_name='"+player.username+"'")
    for row in c.fetchall():
        pokedex_id, player_name, cp, hp, current_hp, weight, height, sex, pokemon_xp, gen_level = row
        c.execute("SELECT name,type1, type2, move, move_power, move2, move2_power, evolve_to, evolve_lvl, catch_chance FROM pokemon_meta WHERE pokedex_ID="+str(pokedex_id))        
        name, type1, type2, move, move_power, move2, move2_power, evolve_to, evolve_lvl, catch_chance=c.fetchone()
        move=Move(move,move_power,type1)
        move2=Move(move2,move2_power,type2)
        
        if(evolve_to=="None"):
            pokemon=Pokemon(pokedex_id,name,hp,cp, type1, type2, move, move2, weight, height, sex, catch_chance, gen_level, pokemon_xp)
        else:
            pokemon=EvolvablePokemon(pokedex_id,name,hp,cp, type1, type2, move, move2, weight, height, sex, catch_chance, gen_level, pokemon_xp, evolve_to, evolve_lvl)
        pokemon.current_hp=current_hp    
        player.pokemon_in_hand.append(pokemon)
    conn.close()

        
def create_new_player(player):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO players VALUES ('"+player.username+"','"+player.get_password()+"',"+str(player.level)+","+str(player.experience)+")")
    print("Your player info has been successfully created and stored into database.\n")
    conn.commit()
    conn.close()
    
def save_progress(player):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("UPDATE players SET password='"+player.get_password()+"',level="+str(player.level)+",experience="+str(player.experience)+\
              " WHERE player_name='"+player.username+"'")
    for pokemon in player.pokemon_in_hand:
        c.execute("UPDATE player_pokemon SET cp="+str(pokemon.cp)+",hp="+str(pokemon.hp)+\
                  ",current_hp="+str(pokemon.current_hp)+",weight="+str(pokemon.weight)+",height="+str(pokemon.height)+\
                  ",pokemon_xp="+str(pokemon.pokemon_xp)+",pokemon_level="+str(pokemon.pokemon_level)+\
                  " WHERE player_name='"+player.username+"' AND pokedex_ID="+str(pokemon.pokedex_id))
    print("Your player info has been successfully saved into database.\n")
    conn.commit()
    conn.close()

def update_player_item(player,item,quantity):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT count(*) from player_items WHERE player_name='"+player.username+"' AND item_name='"+item.name+"'")
    item_record_count=c.fetchone()[0]
    
    if(item_record_count==0):
        c.execute("INSERT INTO player_items VALUES ('"+player.username+"','"+item.name+"',"+str(quantity)+")")
    else:
        c.execute("SELECT quantity from player_items WHERE player_name='"+player.username+"' AND item_name='"+item.name+"'")
        num_of_items=c.fetchone()[0]
        c.execute("UPDATE player_items SET quantity="+str(max(0, (num_of_items+quantity)))+" WHERE player_name='"+player.username+"' AND item_name='"+item.name+"'")
    conn.commit()
    conn.close()

def update_pokedex(pokemon):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM pokemon_meta WHERE pokedex_ID="+str(pokemon.pokedex_id))
    result = len(c.fetchall())==0
    evolution = pokemon.is_evolvable()
    if(result):
        if(evolution):
            c.execute("INSERT INTO pokemon_meta VALUES ('"+\
                      str(pokemon.pokedex_id)+"','"+\
                      pokemon.name+"','"+\
                      pokemon.type1+"','"+\
                      pokemon.type2+"','"+\
                      pokemon.move.name+"',"+\
                      str(pokemon.move.power)+",'"+\
                      pokemon.move2.name+"',"+\
                      str(pokemon.move2.power)+",'"+\
                      pokemon.evolve_to+"',"+\
                      str(pokemon.evolution_lvl)+","+\
                      str(pokemon.catch_chance)+")")
        else:
            c.execute("INSERT INTO pokemon_meta VALUES ('"+\
                      str(pokemon.pokedex_id)+"','"+\
                      pokemon.name+"','"+\
                      pokemon.type1+"','"+\
                      pokemon.type2+"','"+\
                      pokemon.move.name+"',"+\
                      str(pokemon.move.power)+",'"+\
                      pokemon.move2.name+"',"+\
                      str(pokemon.move2.power)+",'None',0,"+\
                      str(pokemon.catch_chance)+")")                  
    conn.commit()
    conn.close()

def insert_player_pokemon(player,pokemon):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO player_pokemon VALUES ('"+\
              str(pokemon.pokedex_id)+"','"+\
              player.username+"',"+\
              str(pokemon.cp)+","+\
              str(pokemon.hp)+","+\
              str(pokemon.current_hp)+","+\
              str(pokemon.weight)+","+\
              str(pokemon.height)+",'"+\
              pokemon.sex+"',"+\
              str(pokemon.pokemon_xp)+","+\
              str(pokemon.pokemon_level)+")")
    conn.commit()
    conn.close()

