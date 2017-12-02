import sqlite3
import random
from pokemon import *
from move import *
from item import *

db_name = "pokemonGo.db"

def check_user_name(player.name):
    conn = sqllite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM players WHERE player_name='"+player+name+"'")
    result = len(c.fetchall())>0
    conn.close()

    return result

def get_user_info(username):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM players WHERE player_name='"+username+"'")
    player_name, password, level, experience= c.fetchnone()
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
        pokedex_id, player_name, move, move2, cp, hp, current_hp, weight, height, sex, pokemon_xp, gen_level = row
        c.execute("SELECT name,type1, type2, evolve_to, catch_chance from pokemon_meta WHERE pokedex_ID="+str(pokedex_id))        
        pokemon_name, type1, type2, evolve_to, evolution_lvl, catch_chance=c.fetchone()
        
        c.execute("SELECT type,power from moves WHERE name='"+move_name+"'")
        type, power =c.fetchone()
        move=Move(move_name,power,type)
        
        c.execute("SELECT type,power from moves WHERE name='"+move2_name+"'")
        type, power=c.fetchone()
        move2=Move(move2_name, power, type)
        
        if(evolve_to=="None"):
            pokemon=Pokemon(pokedex_id,pokemon_name,hp,cp, type1, type2, move, move2, weight, height, sex, catch_chance, gen_level, pokemon_xp)
        else:
            pokemon=EvolvablePokemon(pokedex_id,pokemon_name,hp,cp, type1, type2, move, move2, weight, height, sex, catch_chance, gen_level, pokemon_xp, evolve_to, evolution_lvl)
        pokemon.current_hp=current_hp    
        player.pokemons_in_hand.append(pokemon)
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
    c.execute("UPDATE players SET password='"+player.get_password()+"',level="+str(player.level)+",experience="+str(player.experience)+" WHERE player_name='"+player.username+"'")
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


def insert_player_pokemon(player,pokemon):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO player_pokemon VALUES ('"+\
              str(pokemon.pokedex_id)+"','"+\
              player.username+"','"+\
              pokemon.move.name+"','"+\
              pokemon.move2.name+"',"+\
              str(pokemon.cp)+","+\
              str(pokemon.hp)+","+\
              str(pokemon.current_hp)+","+\
              str(pokemon.weight)+","+\
              str(pokemon.height)+",'"+\
              pokemon.sex+",'"+\
              str(pokemon.pokemon_xp))+",'"+\
              str(pokemon.pokemon_level)+"')")
    conn.commit()
    conn.close()

"""
#get_pokemon (random) handled with generate_pokemon in pokemon module versus using database. Could be rewritten here

def get_pokemon(pokemon_name="Random"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    POKEMON_FOUND=True
    if(pokemon_name=="Random"):
        c.execute("SELECT * FROM pokemon_meta")
        i=1
        result=c.fetchall()
        num_of_rows=int(len(result))
        seed=random.randint(1,num_of_rows)
        for row in result:
            if(i==seed):
                pokedex_id, player_name, move, move2, cp, hp, current_hp, weight, height, sex, pokemon_xp, gen_level = row
            i+=1
    else:
        c.execute("SELECT * FROM pokemon_meta WHERE name='"+pokemon_name.title()+"'")
        result=c.fetchall()
        if(len(result)>0):
            pokedex_id,name,type1,type2,base_weight,base_height,evolve_to,catch_chance=result
        else:
            POKEMON_FOUND=False
    
    if(POKEMON_FOUND):
        # Randomizing fast move:
        c.execute("SELECT name,power,type, required_gauge FROM moves, pokemon_moves WHERE pokedex_ID="+str(pokedex_id)+" AND required_gauge=0 AND moves.move_id=pokemon_moves.move_id")
        i=1
        result=c.fetchall()
        num_of_rows=int(len(result))
        seed=random.randint(1,num_of_rows)
        for row in result:
            if(i==seed):
                move_name,power,type,gauge=row
                fast_move=Move(move_name,power,type,gauge)
            i+=1
            
        # Randomizing special move:
        c.execute("SELECT name,power,type, required_gauge FROM moves, pokemon_moves WHERE pokedex_ID="+str(pokedex_id)+" AND required_gauge>0 AND moves.move_id=pokemon_moves.move_id")
        i=1
        result=c.fetchall()
        num_of_rows=int(len(result))
        seed=random.randint(1,num_of_rows)
        for row in result:
            if(i==seed):
                move_name,power,type,gauge=row
                special_move=Move(move_name,power,type,gauge)
            i+=1
        
        #Randomize weight and height
        weight=round(base_weight*(1+0.5*random.uniform(-1,1)),2)
        height=round(base_height*(1+0.5*random.uniform(-1,1)),2)
        
        if(evolve_to=="None"):
            pokemon=Pokemon(pokedex_id,name,0,1,type1,type2,fast_move,special_move,weight,height,"Unknown",float(catch_chance))
        else:
            pokemon=EvolvablePokemon(pokedex_id,name,0,1,type1,type2,fast_move,special_move,weight,height,"Unknown", float(catch_chance), evolve_to)
        pokemon.randomize_status()
    else:
        pokemon=Pokemon()
    conn.commit()
    conn.close()  
    
    return pokemon
"""
