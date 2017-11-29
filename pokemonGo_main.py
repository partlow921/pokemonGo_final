from pokemon import *
from player import *
from item import *
import random
import sqlite3
import database


"""
Current is for lab assignment and project testing
Currently only creates new player versus allowing user to log back in

"""
def login_module():
    player=Player(input("Please enter your username: "),input("Please enter new password: Your password must:\n\
                 1. Contain at least 8 letters.\n\
                 2. Contain at least one uppercase letter, at least one symbol, and at least one digit.\n\
                 3. The symbol only allows: !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n"))
    print(player,"\n")
    pokemon1=generate_pokemon_by_name(random.choice(["Charmander","Squirtle","Bulbasaur"]))
    #does not cap level but selections have level cap between 1-15, so should suffice at player creation.
    #initial pokemon should actually call capture menu to demonstrate capture function for new player.
    #Same Pokemon should be generated but would require current capture menu to be modified.
    player.pokemon_in_hand.append(pokemon1)
    print("You recieved a level " + str(pokemon1.pokemon_level) + " " + pokemon1.name + " (HP: " + str(pokemon1.hp) + ", CP: " + str(pokemon1.cp) + ")")

    for i in range(10):
        player.bag.add_item(PokeBall("Poke Ball"))
        player.bag.add_item(Potion("Potion"))
        player.bag.add_item(Revive("Revive"))
    print("10 Potions, Poke Balls and Revives have been added to your bag\n")

    return player

"""
An additional option for evolutios is added solely for demostration.
If a pokemon who can't evolve is selected, error will be returned.
There is no way to handle this error as it is solely for demonstration for the lab and will be removed.
This can also be demonstrated through battles by would require several encounters to evolve.

"""
def main_menu(player):
    main_menu="\nWhat do you want to do? Enter a number.\n" +\
               "1: Battle Pokemon\n2: Capture Pokemon\n" +\
               "3: Use an Item\n4: View Pokemon\n5: Force Evolution\n" +\
               "6: View Player Stats\n"
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
            print("The following is only for testing evolutions and not actual game mechanics. As a result, selecting a Pokemon who can't evolve and has no evolve_to attribute will return an error.\n")
            poke_list=""
            i=1
            for pokemon in player.pokemon_in_hand:
                poke_list+=str(i)+":"+pokemon.name+" "
                i+=1
            force_evo=int(input("Who will evolve? "+poke_list+"\n"))
            if(force_evo!=0):
                poke_evo=player.pokemon_in_hand[force_evo-1]
                poke_evo.evolve()
        elif(option==6):
            print(player)
        else:
            print("Please select a valid option\n")
        option=int(input(main_menu))
    print("Exiting game")

player1=login_module()
main_menu(player1)
