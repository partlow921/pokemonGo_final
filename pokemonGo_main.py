from pokemon import *
from player import *
from item import *
import random
import sqlite3
import database

def main_menu(player):
    main_menu="\nWhat do you want to do? Enter a number.\n" +\
               "1: Battle Pokemon\n2: Capture Pokemon\n" +\
               "3: Use an Item\n4: View Pokemon\n" +\
               "5: View Player Stats\n"+\
               "0: Exit and Save Progress\n"
    print(main_menu)
    option=int(input())
    while(option!=0):
        if (option==1):
            player.battle()
        elif(option==2):
            player.enter_capture_menu()
        elif(option==3):
            player.show_item_menu()
        elif(option==4):
            player.show_pokemon_in_hand()
        elif(option==5):
            print(player)
        else:
            print("Please select a valid option\n")
        option=int(input(main_menu))
    database.save_progress(player)
    print("Exiting game")

def login_module():
    player_name=input("Username: ")
    user_exist=database.check_user_name(player_name)
    if(user_exist):
        user_name, user_password, level, experience = database.get_user_info(player_name)
        while(input("Please enter your password:")!=user_password):
            print("Incorrect password. Please try again.")
        player=Player(user_name,user_password,experience,level)
        database.sync_from_db(player)
        print("\nWelcome back!\n")
    else:
        password=input("Welcome new player! Please create your password:")
        player=Player(player_name,password,0,1)
        database.create_new_player(player)
        print(player,"\n")
        pokemon1=generate_pokemon_by_name(random.choice(["Charmander","Squirtle","Bulbasaur"]))
        database.update_pokedex(pokemon1)
        database.insert_player_pokemon(player,pokemon1)
        player.pokemon_in_hand.append(pokemon1)
        print("You recieved a level " + str(pokemon1.pokemon_level) + " " + pokemon1.name + " (HP: " + str(pokemon1.hp) + ", CP: " + str(pokemon1.cp) + ")")

        for i in range(10):
            player.bag.add_item(PokeBall("Poke Ball"))
            player.bag.add_item(Potion("Potion"))
            player.bag.add_item(Revive("Revive"))
        print("10 Potions, Poke Balls and Revives have been added to your bag\n")

    return player


player1=login_module()
main_menu(player1)
