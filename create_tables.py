import sqlite3
from pokemon import *


conn = sqlite3.connect('pokemonGo.db')
c = conn.cursor()


    
# Create table
"""
c.execute("CREATE TABLE players (\
            player_name varchar (20) NOT NULL,\
            password varchar (20) NOT NULL,\
            level INT NOT NULL,\
            experience INT NOT NULL,\
            PRIMARY KEY (player_name))")
"""

# Insert into players
#c.execute("INSERT INTO players VALUES ('Testplayer','@S@S@c2eesw',1,0)")

"""
c.execute("CREATE TABLE pokemon_meta(\
            pokedex_ID INT NOT NULL,\
            name varchar (20) NOT NULL,\
            type_1 varchar (10) NOT NULL,\
            type_2 varchar (10) NOT NULL,\
            base_weight real NOT NULL,\
            base_height real NOT NULL,\
            evolve_to varchar (20) NOT NULL,\
            catch_chance real NOT NULL,\
            PRIMARY KEY (pokedex_ID))")
"""
#Insert into pokemon_meta
"""
c.execute("INSERT INTO pokemon_meta VALUES (1,'Bulbsaur','grass','poison',6.9,0.7,'Ivysaur',1.0)")
c.execute("INSERT INTO pokemon_meta VALUES (2,'Ivysaur','grass','poison',13.0,1.0,'Venusaur',1.0)")
c.execute("INSERT INTO pokemon_meta VALUES (3,'Venusaur','grass','poison',100.0,2.0,'None',1.0)")
c.execute("INSERT INTO pokemon_meta VALUES (4,'Charmander','fire','None',8.5,0.6,'None',1.0)")
"""

"""
c.execute("CREATE TABLE moves(\
            move_id INT NOT NULL,\
            name varchar (20) NOT NULL,\
            type varchar (10) NOT NULL,\
            power real NOT NULL,\
            required_gauge INT NOT NULL,\
            PRIMARY KEY (move_id))")
"""

"""
#Insert into moves
c.execute("INSERT INTO moves VALUES (1,'Vine Whip','grass',11.67,0)")
c.execute("INSERT INTO moves VALUES (2,'Ember','fire',10.00,0)")
c.execute("INSERT INTO moves VALUES (501,'Power Whip','grass',34.62,2)")
c.execute("INSERT INTO moves VALUES (502,'Flame Burst','fire',26.92,2)")
"""

'''
c.execute("CREATE TABLE player_pokemon(\
            pokedex_ID INT NOT NULL,\
            player_name varchar (20) NOT NULL,\
            fast_move varchar (20) NOT NULL,\
            special_move varchar (20) NOT NULL,\
            cp INT NOT NULL,\
            hp INT NOT NULL,\
            current_hp INT NOT NULL,\
            weight real NOT NULL,\
            height real NOT NULL,\
            sex varchar(10) NOT NULL,\
            FOREIGN KEY (pokedex_ID) REFERENCES pokemon_meta (pokedex_ID),\
            FOREIGN KEY (fast_move) REFERENCES pokemon_moves (name),\
            FOREIGN KEY (special_move) REFERENCES pokemon_moves (name),\
            FOREIGN KEY (player_name) REFERENCES players (player_name))")
'''



"""
c.execute("CREATE TABLE pokemon_moves(\
            move_id INT NOT NULL,\
            pokedex_ID INT NOT NULL,\
            FOREIGN KEY (pokedex_ID) REFERENCES pokemon_meta (pokedex_ID),\
            FOREIGN KEY (move_ID) REFERENCES moves (move_id))")
"""

"""
c.execute("INSERT INTO pokemon_moves VALUES (1,1)")
c.execute("INSERT INTO pokemon_moves VALUES (2,4)")
c.execute("INSERT INTO pokemon_moves VALUES (501,1)")
c.execute("INSERT INTO pokemon_moves VALUES (502,1)")

c.execute("INSERT INTO pokemon_moves VALUES (502,4)")
c.execute("INSERT INTO pokemon_moves VALUES (501,2)")
c.execute("INSERT INTO pokemon_moves VALUES (1,2)")
c.execute("INSERT INTO pokemon_moves VALUES (501,3)")
c.execute("INSERT INTO pokemon_moves VALUES (1,3)")
"""

"""
c.execute("CREATE TABLE player_items(\
            player_name varchar (20) NOT NULL,\
            item_name varchar (20) NOT NULL,\
            quantity INT NOT NULL,\
            FOREIGN KEY (player_name) REFERENCES players (player_name))")
"""
#c.execute("INSERT INTO player_items VALUES ('Anna','Poke Ball',1)")



#Select
result=c.execute("SELECT * FROM players")
for row in result:
    print(row)

result=c.execute("SELECT * FROM pokemon_meta")
for row in result:
    print(row)

result=c.execute("SELECT * FROM moves")
for row in result:
    print(row)
    
result=c.execute("SELECT * FROM pokemon_moves")
for row in result:
    print(row)

result=c.execute("SELECT * FROM player_pokemon")
for row in result:
    print(row)
            
conn.commit()
conn.close()