import sqlite3
from pokemon import *


conn = sqlite3.connect('pokemonGo.db')
c = conn.cursor()


    

c.execute("CREATE TABLE players (\
            player_name varchar (20) NOT NULL,\
            password varchar (20) NOT NULL,\
            level INT NOT NULL,\
            experience INT NOT NULL,\
            PRIMARY KEY (player_name))")

#contains variables fixed by pokemon in csv
c.execute("CREATE TABLE pokemon_meta(\
            pokedex_ID INT NOT NULL,\
            name varchar (20) NOT NULL,\
            type1 varchar (10) NOT NULL,\
            type2 varchar (10) NOT NULL,\
            move varchar(10) NOT NULL,\
            move_power INT NOT NULL,\
            move2 varchar(10) NOT NULL,\
            move2_power INT NOT NULL,\
            evolve_to varchar (20) NOT NULL,\
            evolve_lvl INT NOT NULL,\
            catch_chance real NOT NULL,\
            PRIMARY KEY (pokedex_ID))")



c.execute("CREATE TABLE player_pokemon(\
            pokedex_ID INT NOT NULL,\
            player_name varchar (20) NOT NULL,\
            cp INT NOT NULL,\
            hp INT NOT NULL,\
            current_hp INT NOT NULL,\
            weight real NOT NULL,\
            height real NOT NULL,\
            sex varchar(10) NOT NULL,\
            pokemon_xp INT NOT NULL,\
            pokemon_level INT NOT NULL,\
            FOREIGN KEY (pokedex_ID) REFERENCES pokemon_meta (pokedex_ID),\
            FOREIGN KEY (player_name) REFERENCES players (player_name))")


c.execute("CREATE TABLE player_items(\
            player_name varchar (20) NOT NULL,\
            item_name varchar (20) NOT NULL,\
            quantity INT NOT NULL,\
            FOREIGN KEY (player_name) REFERENCES players (player_name))")



result=c.execute("SELECT * FROM players")
for row in result:
    print(row)

result=c.execute("SELECT * FROM pokemon_meta")
for row in result:
    print(row)

result=c.execute("SELECT * FROM player_pokemon")
for row in result:
    print(row)                                                                                                                                     
            
conn.commit()
conn.close()
