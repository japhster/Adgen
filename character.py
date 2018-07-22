import json
import random
import os

#RACES#

class Race(object):

    def __init__(self, name, weapon_classes, armour_classes, hp_dice=[8], level_factor=1, base_exp=100, inv=[]):
        """
        name defines the race type (e.g. human, elf)
        weapon_classes is a list of all classes of weapons (long_bows, cross_bows, short_swords, long_swords, etc.) the race can use
        armour_classes is a list of all classes of armours (plate, chain, leather, etc.) the race can use
        hp_dice defines the list of dice that will be thrown each level to increase the hp of the character
        level_factor defines the xp increase between levels ((level**lf)*base_exp)
         - a lf of 1 will require 100,200,300,400,etc.
         - a lf of 2 will require 100,200,400,800,etc.
        base_exp defines the required amout of exp for level 1 and is also the multiplier for calculating further levels
        inv defines any items the character may have because of their race (included for expansion)
        """
        self.name = name
        self.weapon_clases = weapon_classes
        self.armour_classes = armour_classes
        self.hp_dice = hp_dice
        self.level_factor = level_factor
        self.base_exp = base_exp
        self.inv = inv
        

class Human(Race):

    def __init__(self):
        super().__init__("Human",["long bows", "long swords"], ["plate","chain","leather"])


races = {
         "Human": Human(),
        }

#CHARACTER#

class Character(object):

    def __init__(self, name, race, hp=0, level=1, exp=0, inv=[], password=""):
        self.name = name
        self.race = race
        self.hp = hp if hp > 0 else sum([random.randint(1,i) for i in self.race.hp_dice])
        self.level = level
        self.exp_requirement = self.race.base_exp*(self.level**self.race.level_factor)
        self.exp = exp
        self.inv = self.race.inv + inv
        self.password = password
        
    def level_up(self):
        """
        updates according to race details
         - the characters level
         - the characters hp
         - how much exp the character requires for the next level
        call at the end of an adventure
        """
        while self.exp > self.exp_requirement:
            self.level += 1
            self.hp += sum([random.randint(1,i) for i in self.race.hp_dice])
            self.exp_requirement = self.race.base_hp*(self.level ** self.race.level_factor)
            
            
    def save(self):
        info = {
                "name": self.name,
                "race": self.race.name,
                "hp": self.hp,
                "level": self.level,
                "exp": self.exp,
                "inv": self.inv,
                "password": self.password
               }
        folderpath = "Characters/{0}/".format(self.name.title())
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
        with open(folderpath+"/info.json","w+") as f:
            json.dump(info,f)
            
    def get_details(self):
        return "{0} is a {1} level {2} that is currently carrying {3}".format(self.name.title(), self.level, self.race.name, "\n" + "\n".join(self.inv) if self.inv else "nothing")

#FUNCTIONS#
           
def load_character(name):
    try:
        with open("Characters/"+name.title()+"/info.json","r") as f:
            info = json.load(f)
        character = Character(info["name"],races[info["race"]],info["hp"],info["level"],info["exp"],info["inv"],info["password"])
    except FileNotFoundError:
        print("Character \"{0}\" does not exist.".format(name))
        return None
        
    return character


                 
        
if __name__ == "__main__":
    character = Character("Japhy",races["Human"])
    print(character.get_details())
    character.save()
    new_char = load_character("Japhy")
    print(new_char.get_details())
    new_char = load_character("Noone")
    

