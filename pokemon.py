from move import *
from type import *
from pokedex import pokemon_entries
import random

class Pokemon(object):

    """
    Attribute List
    name            : (string) name of the pokemon
    hp              : (int) total hit point of the pokemon
    current_hp      : (int) current hit point of pokemon, after attacks
    cp              : (int) combat power of the pokemon
    type1           : (string) primary type of pokemon
    type2           : (string) secondary type of pokemon
    weight          : (float) weight of pokemon
    height          : (float) height of pokemon
    sex             : (string) sex of pokemon
    move.name       : (string) name of the move performed by pokemon, parameter of move object 
    move.power      : (float) power of move performed parameter of move object
    """

    POKEMON_EXPERIENCE_LEVEL=range(1000,9999*1000,1000)

    def __init__(self, id_int=0, name='', hp_int=1, cp_int=1, type1='normal', type2='None', move=Move(), move2=Move(), weight=0.0, height=0.0, sex='Unknown', catch_chance=1.0, pokemon_level=0, pokemon_xp=0):
            if (hp_int<0 or cp_int<0):
                #additional validations should be added, sef, weight/height
                print("Values provided were not correct, default Pokemon instance has been created")
                self.pokedex_id   = 0
                self.name         = name
                self.hp           = 1
                self.current_hp   = self.hp
                self.cp           = 1
                self.type1        = 'normal'
                self.type2        = 'None'
                self.weight       = 0.0
                self.height       = 0.0
                self.sex          = 'Unknown'
                self.move         = move
                self.move2        = move2
                self.catch_chance = 1.0
                self.pokemon_xp   = 0
                self.pokemon_level= 0
            else:
                self.pokedex_id   = id_int
                self.name         = name
                self.hp           = hp_int
                self.current_hp   = self.hp
                self.cp           = cp_int
                self.type1        = type1
                self.type2        = type2
                self.weight       = weight
                self.height       = height
                self.sex          = sex
                self.move         = move
                self.move2        = move2
                self.catch_chance = catch_chance
                self.pokemon_xp   = pokemon_xp 
                self.pokemon_level= pokemon_level

    def change_name(self, new_name):
        """Change the name of the pokemon with new_name"""
        self.name   = new_name

    def attack(self, move, target_pokemon):
        """
        Accepts move select from battle menu, with type, to determine multiplier
        Damage dealt is multiplied based on effects of selected moves type compared to both types of target
        Adjusts HP and ends if hp has dropped to 0
        """
        
        print(self.name + " used " + str(move.name) + " against "+ target_pokemon.name + "!")
        
        type_multiplier = battle_type_eval(move.type, target_pokemon.type1, target_pokemon.type2)
        damage_dealt = int(max(1,int(move.power * (self.cp / target_pokemon.cp))) * type_multiplier)
        target_pokemon.current_hp -= damage_dealt

        print(self.name + ' dealt ' + str(damage_dealt) + " damage to " + target_pokemon.name + "!")

        if (target_pokemon.current_hp < 0):
            target_pokemon.current_hp=0
            print(target_pokemon.name + "'s HP has decreased to " + str(target_pokemon.current_hp) + "\n")
            print(target_pokemon.name, " has been defeated!")
        else:
            print(target_pokemon.name + "'s HP has decreased to " + str(target_pokemon.current_hp) + "\n")
       
                     
    def __str__(self):
        """defines string value returned when print function used for pokemon"""
        
        return str(self.name) +\
               ": \nLevel: "+ str(self.pokemon_level) +" (xp: "+str(self.pokemon_xp)+")"+\
               "\nSex: "+ str(self.sex) +\
               "\nCP: "+ str(self.cp) +\
               "\nHP: "+ str(int(self.current_hp)) +\
               "/" + str(int(self.hp)) +\
               "\nType: "+ str(self.type1)+ ", "+ str(self.type2) +\
               "\nPrimary Move: "+ str(self.move) + " (power: "+ str(self.move.power) +")"\
               "\nSecondary Move: "+ str(self.move2) + " (power: "+str(self.move2.power)+")"\
               "\nWeight: "+ str(self.weight) + " kg \nHeight: "+ str(self.height)+ " m"

    def randomize_status(self):
        """returns random values for pokemon's cp, hp, weight, heigh and sex"""
        
        self.cp         = random.randint(10*self.pokemon_level,10*(self.pokemon_level*2))
        self.hp         = random.randint(cp//10, 1.5*cp//10)
        self.current_hp = self.hp
        self.weight     = random.randint(0,100)
        self.height     = random.randint(0,10)
        self.sex        = random.choice(["M","F"])

    def is_evolvable(self):
        return self.__class__==EvolvablePokemon

    def pokemon_level_up(self):
        self.pokemon_level += 1
        scaling_ratio=1.2
        self.hp = int(self.hp*scaling_ratio)
        self.cp = int(self.cp*scaling_ratio)
        self.current_hp = self.hp
        
        print(self.name+" has increased to level "+str(self.pokemon_level)+"!\n")
        if(self.is_evolvable()):
            if(self.pokemon_level >= self.evolution_lvl):
                self.evolve()

    def pokemon_increase_experience(self,amount):
        self.pokemon_xp+=int(amount)
        print(self.name + " has gained " + str(amount) + " experience points\n")
        if(self.pokemon_xp >= self.POKEMON_EXPERIENCE_LEVEL[self.pokemon_level-1]):
            while(self.pokemon_xp >= self.POKEMON_EXPERIENCE_LEVEL[self.pokemon_level-1]):
                self.pokemon_level_up()


class EvolvablePokemon(Pokemon):

    def __init__(self, id_int, name, hp_int, cp_int, type1, type2, move, move2, weight, height, sex, catch_chance, pokemon_level, pokemon_xp, evolve_to_str, evolution_lvl):
        super(self.__class__, self).__init__(id_int, name, hp_int, cp_int, type1, type2, move, move2, weight, height, sex, catch_chance, pokemon_level, pokemon_xp)
        self.evolve_to=evolve_to_str
        self.evolution_lvl=evolution_lvl

    def __str__(self):
        return super(self.__class__,self).__str__()+"\nEvolves To: "+self.evolve_to +" at Level "+str(self.evolution_lvl)

    def evolve(self):
        print(self.name,"has evolved into",self.evolve_to,"!\n")
        evolved_pokemon=generate_pokemon_by_name(self.evolve_to)

        self.pokedex_id = evolved_pokemon.pokedex_id
        self.name       = evolved_pokemon.name
        self.type1      = evolved_pokemon.type1
        self.type2      = evolved_pokemon.type2
        self.move       = evolved_pokemon.move
        self.move2      = evolved_pokemon.move2
        self.weight     = evolved_pokemon.weight
        self.height     = evolved_pokemon.height

        if(evolved_pokemon.is_evolvable()):
            self.evolve_to=evolved_pokemon.evolve_to
            self.evolution_lvl=evolved_pokemon.evolution_lvl
        else:
            self.__class__=Pokemon
            self.evolve_to=""
            self.evolution_lvl=""

def generate_pokemon(player_lvl):

    pokemon=Pokemon()

    while (pokemon.pokemon_level > (player_lvl + 10) or pokemon.pokemon_level == 0):

        id=random.randint(1,151)

        if (id in pokemon_entries.keys()):

            name=pokemon_entries[id]["name"]
            type1=pokemon_entries[id]["type1"]
            type2=pokemon_entries[id]["type2"]
            move=pokemon_entries[id]["move"]
            move2=pokemon_entries[id]["move2"]
            initial_lvl=pokemon_entries[id]["initial_lvl"]
            gen_lvl_cap=pokemon_entries[id]["gen_lvl_cap"]
            catch_chance=pokemon_entries[id]["catch_chance"]
            evolution_lvl=pokemon_entries[id]["evolve_lvl"]
        
            gen_level  = random.randint(int(initial_lvl),int(gen_lvl_cap))
            cp         = random.randint(10*gen_level,10*(gen_level*2))
            hp         = random.randint(cp//10, (2*cp)//10)
            weight     = round(pokemon_entries[id]["weight"]*(1+0.5*random.uniform(-1,1)),2)
            height     = round(pokemon_entries[id]["height"]*(1+0.5*random.uniform(-1,1)),2)
            sex        = random.choice(["M","F"])
            pokemon_xp = (gen_level-1)*1000

            evolvable=pokemon_entries[id]["evolve_to"]!="None"

            if(evolvable):
                evolve_to=pokemon_entries[id]["evolve_to"]
                pokemon=EvolvablePokemon(id, name, hp, cp, type1, type2, move, move2, weight, height, sex, catch_chance, gen_level, pokemon_xp, evolve_to, evolution_lvl)
            else:
                pokemon=Pokemon(id,name,hp,cp,type1,type2,move,move2,weight,height,sex,catch_chance, gen_level, pokemon_xp)

        else:
            print("Pokemon does not exist in Pokedex. A default Pokemon will be created.")

    return pokemon



def generate_pokemon_by_name(name_str):
    """only used for evolutions or generation from preset list (ie creation of new user)"""

    pokemon=Pokemon()

    for id,pokemon_gen in pokemon_entries.items():
        if (pokemon_gen["name"].lower()==name_str.lower()):

            name=pokemon_entries[id]["name"]
            type1=pokemon_entries[id]["type1"]
            type2=pokemon_entries[id]["type2"]
            move=pokemon_entries[id]["move"]
            move2=pokemon_entries[id]["move2"]
            initial_lvl=pokemon_entries[id]["initial_lvl"]
            gen_lvl_cap=pokemon_entries[id]["gen_lvl_cap"]
            catch_chance=pokemon_entries[id]["catch_chance"]
            evolution_lvl=pokemon_entries[id]["evolve_lvl"]

            gen_level  = random.randint(int(initial_lvl),int(gen_lvl_cap))
            cp         = random.randint(10*gen_level,10*(gen_level*2))
            hp         = random.randint(cp//10, (2*cp)//10)
            weight     = round(pokemon_entries[id]["weight"]*(1+0.5*random.uniform(-1,1)),2)
            height     = round(pokemon_entries[id]["height"]*(1+0.5*random.uniform(-1,1)),2)
            sex        = random.choice(["M","F"])
            pokemon_xp = (gen_level-1)*1000

            evolvable=pokemon_entries[id]["evolve_to"]!="None"

            if(evolvable):
                evolve_to=pokemon_entries[id]["evolve_to"]
                pokemon=EvolvablePokemon(id, name, hp, cp, type1, type2, move, move2, weight, height, sex, catch_chance, gen_level, pokemon_xp, evolve_to, evolution_lvl)
            else:
                pokemon=Pokemon(id,name,hp,cp,type1,type2,move,move2,weight,height,sex,catch_chance, gen_level, pokemon_xp)

    return pokemon

def battle_type_eval(move_type, target_type1, target_type2):

    check1 = Type(move_type,target_type1)
    check2 = Type(move_type,target_type2)

    multiplier = check1.damage_multiplier * check2.damage_multiplier

    if multiplier == 0:
        print("It has no effect!")
    elif multiplier < 1:
        print("It's not very effective")
    elif multiplier >= 2:
        print("It's super effective!")
        
    return multiplier
