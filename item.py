import random
import database

class Item(object):

    #Add doc string

    def __init__(self, name_str="-"):
        self.name=name_str


    def __repr__(self):
        return self.name

    def invoke(self,player):
        pass

    def remove_item_from(self,player):
        player.bag.remove_item(self)

class Potion(Item):

    def __init__(self,name):
        self.restore_amount = 0
        super(self.__class__, self).__init__(name)
        if(self.name == "Potion"):
            self.restore_amount=20
        elif(self.name == "Super Potion"):
            self.restore_amount=50
        elif(self.name == "Hyper Potion"):
            self.restore_amount=200
        elif(self.name == "Max Potion"):
            self.restore_amount=500
            #needs to set current to pokemon hp total, full restore
        else:
            self.restore_amount=0

    def invoke(self,player):

        prompt_message=""
        i=1
        for pokemon in player.pokemon_in_hand:
            prompt_message+=str(i)+":"+pokemon.name+" (HP: "+str(pokemon.current_hp)+"/"+str(pokemon.hp)+")  "
            i+=1
        user_item_selected = int(input("Please choose a Pokemon to use "+self.name+" on. (Enter 0 to go back): \n"+prompt_message+"\n"))
        if(user_item_selected!=0):
            pokemon=player.pokemon_in_hand[user_item_selected-1]

            if(pokemon.current_hp>0):
                amount_restored = min(pokemon.hp - pokemon.current_hp, self.restore_amount)
                pokemon.current_hp += amount_restored
                print("Restored " + str(amount_restored) + " to " + pokemon.name + ". Current HP is now " + str(pokemon.current_hp))
                self.remove_item_from(player)
            else:
                print("Cannot use potions on Pokemon who have fainted. Use Revive first.")

class Revive(Item):

    def __init__(self,name):
        self.restore_amount=0
        super(self.__class__,self).__init__(name)
        if(self.name == "Revive"):
            self.health_restore=2
        elif(self.name == "Full Revive"):
            self.health_restore=1
 
    def invoke(self,player):

        prompt_message=""
        i=1
        for pokemon in player.pokemon_in_hand:
            prompt_message+=str(i)+":"+pokemon.name+" (HP: "+str(pokemon.current_hp)+"/"+str(pokemon.hp)+")  "
            i+=1
        user_item_selected = int(input("Please choose a Pokemon to use "+self.name+" on. (Enter 0 to go back): \n"+prompt_message+"\n"))
        if(user_item_selected!=0):
            pokemon=player.pokemon_in_hand[user_item_selected-1]

            if(pokemon.current_hp==0):
                pokemon.current_hp=int(pokemon.hp/self.health_restore)
                print(pokemon.name + " has been revived! Current HP is " + str(pokemon.current_hp))
                self.remove_item_from(player)
            else:
                print(pokemon.name + " is alive. Please select another Pokemon or use a different item")


class PokeBall(Item):

    def __init__(self,name):
        self.capture_chance = 0.5
        super(self.__class__,self).__init__(name)
        if(self.name == "Poke Ball"):
            self.capture_chance = 0.50
        elif(self.name == "Great Ball"):
            self.capture_chance = 0.70
        elif(self.name == "Ultra Ball"):
            self.capture_chance = 0.85
        elif(self.name == "Master Ball"):
            self.capture_chance = 1
        else:
            self.capture_chance = 0.5

    def invoke(self,player):
        pokemon = player.encountering_pokemon[0]
        #needs error handling if selected outside capture module.
        print("~~~~~~~~~~~~~~0~~~~~~~~~~~~~~~~")
        cap_chance = (pokemon.pokemon_level + 55)/100
        if cap_chance>1:
            cap_chance=1
        catch = random.uniform(pokemon.pokemon_level/100,cap_chance)
        if(catch < self.capture_chance * pokemon.catch_chance):
            print(pokemon.name + " has bee captured!")
            player.pokemon_in_hand.append(pokemon)
            player.increase_experience(pokemon.pokemon_level*10)
            #database.insert_player_pokemon(player,pokemon)
            #tables need to be created for above
            player.encountering_pokemon.remove(pokemon)
        else:
            print("It failed! "+pokemon.name+" could not be caught\n")
            run_chance = random.uniform(pokemon.catch_chance,1) - random.uniform(0,0.4)
            if catch > run_chance:
                print(pokemon.name + " has run away!")
                player.encountering_pokemon.remove(pokemon)
        self.remove_item_from(player)

class RazzBerry(Item):

    def __init__(self,name):
        self.catch_chance_modifier = 1.0
        super(self.__class__,self).__init__(name)
        if(self.name == "RazzBerry"):
            self.catch_chance_modifier = 1.1
        elif(self.name == "Great RazzBerry"):
            self.catch_chance_modifier = 1.2
        else:
            self.catch_chance_modifier = 1.0

    def invoke(self,player):
        pokemon=player.encounter_pokemon[0]
        print(pokemon.name + " is eating "+ self.name)
        pokemon.catch_chance*=self.catch_chance_modifier
        self.remove_item_from(player)

class Candy(Item):
    """Candy add experience to increase level instead of setting total number needed to evolve"""

    def __init__(self,name):
        self.xp_modifier = 0
        super(self.__class__,self).__init__(name)
        if(self.name == "Candy"):
            self.xp_modifier = 500
        if(self.name == "Rare Candy"):
            self.xp_modifier = 1000

    def invoke(self,player):

        prompt_message=""
        i=1
        for pokemon in player.pokemon_in_hand:
            prompt_message+=str(i)+":"+pokemon.name+" (HP: "+str(pokemon.current_hp)+"/"+str(pokemon.hp)+")  "
            i+=1

        user_item_selected = int(input("Please choose a Pokemon to use "+self.name+" on. (Enter 0 to go back): \n"+prompt_message+"\n"))
        if(user_item_selected!=0):
            pokemon=player.pokemon_in_hand[user_item_selected-1]
            pokemon.pokemon_increase_experience(self.xp_modifier)
            self.remove_item_from(player)

#Stardust for CP
