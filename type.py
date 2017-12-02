class Type(object):
"""
Initially implemented as a class but can be a function
Will require updates elsewhere so leaving as is for now
"""

    def __init__(self,pokemon_type = "", target_type=""):
        self.pokemon_type = pokemon_type
        self.target_type = target_type
        
        if (pokemon_type == "Normal"):
            if (self.target_type == "Rock" or self.target_type == "Steel"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Ghost"):
                self.damage_multiplier = 0
            else:
                self.damage_multiplier = 1
                
        elif (pokemon_type == "Fire"):
            if (self.target_type == "Fire" or self.target_type == "Water" or self.target_type == "Rock" or self.target_type == "Dragon"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Grass" or self.target_type == "Ice" or self.target_type == "Bug" or self.target_type == "Steel"):
                self.damage_multiplier = 2
            else:
                self.damage_multiplier = 1
                
        elif (pokemon_type == "Water"):
            if (self.target_type == "Fire" or self.target_type == "Ground" or self.target_type == "Rock"):
                self.damage_multiplier = 2
            elif (self.target_type == "Water" or self.target_type == "Grass" or self.target_type == "Dragon"):
                self.damage_multiplier = 0.5
            else:
                self.damage_multiplier = 1
                
        elif (pokemon_type == "Electric"):
            if (self.target_type == "Water" or self.target_type == "Flying"):
                self.damage_multiplier = 2
            elif (self.target_type == "Electric" or self.target_type == "Grass" or self.target_type == "Dragon"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Ground"):
                self.damage_multiplier = 0
            else:
                self.damage_multiplier = 1
                
        elif (pokemon_type == "Grass"):
            if (self.target_type == "Fire" or self.target_type == "Grass" or self.target_type == "Poison" or self.target_type == "Flying" or self.target_type == "Bug" or self.target_type == "Dragon" or self.target_type == "Steel"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Water" or self.target_type == "Ground" or self.target_type == "Rock"):
                self.damage_multiplier = 2
            else:
                self.damage_multiplier = 1
                
        elif (pokemon_type == "Ice"):
            if (self.target_type == "Fire" or self.target_type == "Water" or self.target_type == "Ice" or self.target_type == "Steel"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Grass" or self.target_type == "Ground" or self.target_type == "Flying" or self.target_type == "Dragon"):
                self.damage_multiplier = 2
            else:
                self.damage_multiplier = 1
                
        elif (pokemon_type == "Fighting"):
            if (self.target_type == "Normal" or self.target_type == "Ice" or self.target_type == "Rock" or self.target_type == "Dark" or self.target_type == "Steel"):
                self.damage_multiplier = 2
            elif (self.target_type == "Poison" or self.target_type == "Flying" or self.target_type == "Psychic" or self.target_type == "Bug" or self.target_type == "Fairy"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Ghost"):
                self.damage_multiplier = 0
            else:
                self.damage_multiplier = 1
                
        elif (pokemon_type == "Poison"):
            if (self.target_type == "Grass" or self.target_type == "Fairy"):
                self.damage_multiplier = 2
            elif (self.target_type == "Poison" or self.target_type == "Ground" or self.target_type == "Rock" or self.target_type == "Ghost"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Steel"):
                self.damage_multiplier = 0
            else:
                self.damage_multiplier = 1
                
        elif (pokemon_type == "Ground"):
            if (self.target_type == "Fire" or self.target_type == "Electric" or self.target_type == "Poison" or self.target_type == "Rock" or self.target_type == "Steel"):
                self.damage_multiplier = 2
            elif (self.target_type == "Grass" or self.target_type == "Bug"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Flying"):
                self.damage_multiplier = 0
            else:
                self.damage_multiplier = 1
                
        elif (pokemon_type == "Flying"):
            if (self.target_type == "Electric" or self.target_type == "Rock" or self.target_type == "Steel"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Grass" or self.target_type == "Fighting" or self.target_type == "Bug"):
                self.damage_multiplier = 2
            else:
                self.damage_multiplier = 0
                
        elif (pokemon_type == "Psychic"):
            if (self.target_type == "Fighting" or self.target_type == "Poison"):
                self.damage_multiplier = 2
            elif (self.target_type == "Psychic" or self.target_type == "Steel"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Dark"):
                self.damage_multiplier = 0
            else:
                self.damage_multiplier = 1

        elif (pokemon_type == "Bug"):
            if (self.target_type == "Fire" or self.target_type == "Fighting" or self.target_type == "Poison" or self.target_type == "Flying" or self.target_type == "Ghost" or self.target_type == "Steel" or self.target_type == "Fairy"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Grass" or self.target_type == "Psychic" or self.target_type == "Dark"):
                self.damage_multiplier = 2
            else:
                self.damage_multiplier = 1 

        elif (pokemon_type == "Rock"):
            if (self.target_type == "Fire" or self.target_type == "Ice" or self.target_type == "Flying" or self.target_type == "Bug"):
                self.damage_multiplier = 2
            elif (self.target_type == "Fighting" or self.target_type == "Ground" or self.target_type == "Steel"):
                self.damage_multiplier = 0.5
            else:
                self.damage_multiplier = 1

        elif (pokemon_type == "Ghost"):
            if (self.target_type == "Normal"):
                self.damage_multiplier = 0
            elif (self.target_type == "Psychic" or self.target_type == "Ghost"):
                self.damage_multiplier = 2
            elif (self.target_type == "Dark"):
                self.damage_multiplier = 0.5
            else:
                self.damage_multiplier = 1

        elif (pokemon_type == "Dragon"):
            if (self.target_type == "Dragon"):
                self.damage_multiplier = 2
            elif (self.target_type == "Steel"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Fairy"):
                self.damage_multiplier = 0
            else:
                self.damage_multiplier = 1

        elif (pokemon_type == "Dark"):
            if (self.target_type == "Fighting" or self.target_type == "Dark" or self.target_type == "Fairy"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Psychic" or self.target_type == "Ghost"):
                self.damage_multiplier = 2
            else:
                self.damage_multiplier = 1

        elif (pokemon_type == "Steel"):
            if (self.target_type == "Fire" or self.target_type == "Water" or self.target_type == "Electric" or self.target_type == "Steel"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Ice" or self.target_type == "Rock" or self.target_type == "Fairy"):
                self.damage_multiplier = 2
            else:
                self.damage_multiplier = 1

        elif (pokemon_type == "Fairy"):
            if (self.target_type == "Fire" or self.target_type == "Poison" or self.target_type == "Steel"):
                self.damage_multiplier = 0.5
            elif (self.target_type == "Fighting" or self.target_type == "Dragon" or self.target_type == "Dark"):
                self.damage_multiplier = 2
            else:
                self.damage_multiplier = 1 
                
        else:
            self.damage_multiplier = 1
