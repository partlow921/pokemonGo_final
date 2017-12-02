import string
import random
import database
from item import *
from pokemon import *

def validated(password_str):

    num_of_uppercase=0
    num_of_digits=0
    num_of_symbols=0
    unpermitted_symbols=0
    num_of_lowercase=0
    unpermitted_symbols=""
    result=True

    for char in password_str:
        if(char in string.ascii_uppercase):
            num_of_uppercase+=1
        elif(char in string.punctuation):
            num_of_symbols+=1
        elif(char in string.digits):
            num_of_digits+=1
        elif(char in string.ascii_lowercase):
            num_of_lowercase+=1
        else:
            unpermitted_symbols+=char

    if(len(password_str)<8):
        print("Password must contain at least 8 letters!")
        result=False

    if(num_of_uppercase==0):
        print("Password must contain at least one uppercase letter!")
        result=False

    if(num_of_digits==0):
        print("Password must contain at least one digit!")
        result=False

    if(num_of_symbols==0):
        print("Password must contain at least one symbol!")
        result=False

    if(len(unpermitted_symbols)>0):
        print("The following cannot be used in a password: ",unpermitted_symbols.replace(" ","(whitespace)"))
        result=False

    return result



class Player(object):

    #Add doc string for Player

    EXPERIENCE_CAP_AT_LEVEL=range(0,100*1000,1000)

    def __init__(self, username_str="-",password_str="",experience_points=0,current_level=1):
        
        while (validated(password_str)==False):
            password_str=input("Password does not meet requirements, try again: ")
        self.username=username_str
        self.__password=password_str
        self.experience=experience_points
        self.level=current_level
        self.bag=Bag()
        self.pokemon_in_hand=[]
        self.encountering_pokemon=[]

    def __str__(self):
        return "\nPlayer Status: " + str(self.username) + "     Level:" + str(self.level) + "     Experience:" + str(self.experience)

    def get_password(self):
        return self.__password
    
    def change_password(self,old_password_str):
        max_attempts=3
        failed_attempts=0
        while(old_password_str != self.__password):
            failed_attempts+=1
            if(failed_attempts<max_attempts):
                old_password_str=input("Password is incorrect. Please try again.\nYou have "+str(max_attempts-failed_attempts) + " attempts remaining\n")
            else:
                print("You have exceeded the maximum numer of attempts. Your account is locked temporarily.")
                break
            
        if(failed_attempts<max_attempts):
            new_password=input("Please enter new password: Your password must:\n\
             1. Contain at least 8 letters.\n\
             2. Contain at least one uppercase letter, at least one symbol, and at least one digit.\n\
             3. The symbol only allows: !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n")
            while(validated(new_password)==False):
                new_password=input("Password does not meet requirements, try again: ")

            self.__password=new_password
            print("Your password has been updated")

    def level_up(self):
        """
        More advanced items are assigned as player increases in level.
        A random number is also generated to give player potential to earn candy each time leveled up. Intended to make harder to get candy to level up Pokemon.
        """
        
        self.level+=1
        special_check = random.uniform(0,1)
        if (self.level<10):
            new_items=[PokeBall("Poke Ball"), Potion("Potion"), RazzBerry("RazzBerry"),Revive("Revive")]
        elif (self.level<20):
            new_items=[PokeBall("Great Ball"), Potion("Super Potion"), RazzBerry("RazzBerry"),Revive("Revive")]
        else:
            new_items=[PokeBall("Ultra Ball"), Potion("Super Potion"), RazzBerry("Great RazzBerry"),Revive("Full Revive")]
        for i in range(0,5):
            self.bag.add_item(random.choice(new_items))

        if special_check >= 0.85:
            self.bag.add_item(Candy("Candy"))
    
    def increase_experience(self,amount):
        self.experience+=int(amount)
        print(self.username + " has gained " + str(amount) + " experience points\n")
        if(self.experience >= self.EXPERIENCE_CAP_AT_LEVEL[self.level]):
           while(self.experience >= self.EXPERIENCE_CAP_AT_LEVEL[self.level]):
               self.level_up()
               print(self.username + " has increased to level "+ str(self.level) + "!\n")

    def use_item(self,item):
        item.invoke(self)

    def show_item_menu(self):
        item_option_table={}
        i=1
        menu_str="Select a number to pick the item you want to use:\n"
        for item_name, quantity in self.bag.item_dict.items():
            menu_str+=str(i)+":"+ item_name +" ("+str(quantity)+") "
            
            item_option_table[i]=item_name
            i+=1

        print(menu_str)
        user_selection=int(input())

        if(user_selection in item_option_table.keys()):
            for item in self.bag.inventory:
                if (item_option_table[user_selection]==item.name):
                    self.use_item(item)
                    break
            else:
                print("You've selected an invalid option. Please try again.")

    def show_pokemon_in_hand(self):
        player_pokemon=""
        for pokemon in self.pokemon_in_hand:
            player_pokemon+="Level " + str(pokemon.pokemon_level) + " ("+str(pokemon.pokemon_xp) +") " + pokemon.name +\
                             " (HP: " + str(pokemon.current_hp) + "/" + str(pokemon.hp) +\
                             ", CP: " + str(pokemon.cp) + ")\n"\
                             "Primary Move: "+ str(pokemon.move) + "\nSecondary Move: " + str(pokemon.move2) + "\n"
        print("Current Pokemon:\n" + player_pokemon + "\n")
        #Don't just print all, allow user to select one to see more details (print Pokemon)

    def encounter_pokemon(self,pokemon):
        self.encountering_pokemon.append(pokemon)
        print("A wild level "+ str(pokemon.pokemon_level) + " " + pokemon.name +\
              " has appeared! ("+ str(pokemon.hp) + " HP, " + str(pokemon.cp) + " CP)\n")

    def enter_capture_menu(self):
        pokemon=generate_pokemon(self.level)
        self.encounter_pokemon(pokemon)
        while(len(self.encountering_pokemon)>0):
              self.invoke_capture_menu()

    def invoke_capture_menu(self):
        pokemon = self.encountering_pokemon[0]
        item_option_table = {0:"Escape"}
        i=1

        item_menu_str="Choose an option below (input number):\n"
        for item_name, quantity in self.bag.item_dict.items():
            item_menu_str+=str(i) + ":" + item_name + " (" + str(quantity) + ")\n"
            item_option_table[i] = item_name
            i+=1
            #Restrict to Pokeballs
        item_menu_str += "0: Escape from Pokemon"

        if("Poke Ball" not in self.bag.item_dict.keys() and\
           "Great Ball" not in self.bag.item_dict.keys() and\
           "Ultra Ball" not in self.bag.item_dict.keys()):
            print("You have no Pokeballs left! Please get some before catching a Pokemon!\n")

        print(item_menu_str)
        user_selection=int(input())
        if(user_selection in item_option_table.keys()):
            item_found=False
            for item in self.bag.inventory:
                if(item_option_table[user_selection]==item.name):
                    self.use_item(item)
                    item_found=True
                    break
            if(not item_found):
                if(user_selection==0):
                    print("Escaping from", pokemon.name,".....Success!")
                    #Add probability check
                    self.encountering_pokemon.remove(pokemon)
                else:
                    print("There's no ", item_option_table[user_command], " left! Choose another item")

        else:
            print("Invalid selection. Please try again.")
            
    def battle(self):

        battle_pokemon=generate_pokemon(self.level)
        self.encounter_pokemon(battle_pokemon)
        pokemon_selection = self.select_pokemon(battle_pokemon)
        
        if(pokemon_selection!=0):
            pokemon1=self.pokemon_in_hand[pokemon_selection-1]
            print("You sent out " + pokemon1.name + "!\n")
            
            battle_menu = "What will you do?\n 1. Attack\n 2. Use Item\n 3. Change Pokemon\n 4. Run\n"
            print(battle_menu)
            selection = int(input())
    
            while(selection!=0):
    
                if(selection==1):

                    battle_move=self.select_move(pokemon1)
                    pokemon1.attack(battle_move, battle_pokemon)
                    
                    if battle_pokemon.current_hp > 0:
                        battle_pokemon.attack(battle_pokemon.move, pokemon1)
                    else:
                        print(pokemon1.name + " has won the battle!\n")
                        pokemon1.pokemon_increase_experience(int(((1.5*battle_pokemon.pokemon_level)*10)*(battle_pokemon.pokemon_level/pokemon1.pokemon_level)))
                        self.increase_experience(int((1.5*battle_pokemon.pokemon_level)*10))
                        self.encountering_pokemon.remove(battle_pokemon)
                        break
    
                    if pokemon1.current_hp == 0:

                        hand_hp = 0
                        for pokemon in self.pokemon_in_hand:
                            hand_hp+=pokemon.current_hp
                        if hand_hp == 0:
                            print(battle_pokemon.name + " has won the battle!\n")
                            self.encountering_pokemon.remove(battle_pokemon)
                            break
                        else:
                            new_selection=self.select_pokemon(battle_pokemon)
                            pokemon1=self.pokemon_in_hand[new_selection-1]
                            print("You sent out " + pokemon1.name + "!\n")
    
                elif(selection==2):
    
                    self.show_item_menu()
    
                elif(selection==3):

                    new_selection = self.select_pokemon(battle_pokemon)
                    pokemon1=self.pokemon_in_hand[new_selection-1]
                    print("You sent out " + pokemon1.name + "!\n")

                elif(selection==4):
                    escape_chance = battle_pokemon.pokemon_level/100
                    attempt = random.uniform(0,1)
                    #top range needs scaling or will pretty much always escape lower levels.
                    if attempt >= escape_chance:
                        print("You escaped!")
                        self.encountering_pokemon.remove(battle_pokemon)
                        break
                    else:
                        print("Escape failed!")
    
                else:
                    print("Please select a valid option")
                selection=int(input(battle_menu))
                
    def select_pokemon(self,battle_pokemon):

        pokemon_list=""
        i=1
    
        for pokemon in self.pokemon_in_hand:
            pokemon_list+=str(i)+":"+pokemon.name+" (Level: "+str(pokemon.pokemon_level)+\
                           ", HP: "+str(pokemon.current_hp)+"/"+str(pokemon.hp)+", CP: "+str(pokemon.cp)+")\n"
            i+=1
    
        pokemon_selection = int(input("Who will battle "+battle_pokemon.name+"?\n"+pokemon_list+"\n"))

        hp_val = self.pokemon_in_hand[pokemon_selection-1]
        while hp_val.current_hp == 0:
              print("Pokemon can't be selected\n")
              pokemon_selection = int(input("Who will battle "+battle_pokemon.name+"?\n"+pokemon_list+"\n"))
              hp_val = self.pokemon_in_hand[pokemon_selection-1]
              
        return pokemon_selection

    def select_move(self,pokemon):
        move_list=""
        move_selection=int(input("Select the move you want to use:\n1: "+str(pokemon.move) + "\n2: " + str(pokemon.move2) + "\n"))

        while (move_selection !=0):
            if (move_selection == 1):
                battle_move = pokemon.move
                break
            elif (move_selection == 2):
                battle_move = pokemon.move2
                break
            else:
                print("Please select a move from the list")
        return battle_move
        
    #Define pokestop method, call Google Map API

class Bag(object):

    #Add doc stream

    def __init__(self):
        self.inventory=[]
        self.item_dict={}
        #Add owner attribute

    def __str__(self):
        current_inv_str=""
        for name,quantity in self.item_dict.items():
            current_inv_str+=name+" ("+str(quantity)+") "
        return current_inv_str

    def add_item(self,item):
        self.inventory.append(item)

        if(item.name in self.item_dict.keys()):
            self.item_dict[item.name]+=1
        else:
            self.item_dict[item.name]=1

       #database.update_player_item(self.owner,item,1)
       #needs table to run

    def remove_item(self,item):
        if(item.name in self.item_dict.keys()):
            self.item_dict[item.name]-=1
            self.inventory.remove(item)
        #dabatase.update_player_item(self.owner,item,-1)
        #needs table to run

    def sync_items_by_name(self,item_name,quantity=1):
        item=Item()
        for i in range(quantity):
            if(item_name.find("Ball")!=-1):
                item=PokeBall(item_name)
            elif(item_name.find("Potion")!=-1):
                item=Potion(item_name)
            elif(item_name.find("Razz")!=-1):
                item=RazzBerry(item_name)
            elif(item_name.find("Revive")!=-1):
                item=Revive(item_name)
            elif(item_name.find("Candy")!=-1):
                item=Candy(item_name)
            
            self.inventory.append(item)
            
            if (item.name in self.item_dict.keys()):
                self.item_dict[item.name]+=1
            else:
                self.item_dict[item.name]=1
                      
