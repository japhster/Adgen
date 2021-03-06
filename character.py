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

    def __init__(self, name, gender, race, hp=0, level=1, gold=0, exp=0, inv=[], password=""):
        self.name = name #name of character
        self.gender = gender #character's gender
        self.race = race #character's race object (e.g. Human)
        self.hp = hp if hp > 0 else sum([random.randint(1,i) for i in self.race.hp_dice]) #character's hit points
        self.level = level #character's level
        self.exp_requirement = self.race.base_exp*(self.level**self.race.level_factor) #the required exp to level up
        self.exp = exp #character's experience points
        self.gold = gold
        self.inv = self.race.inv + inv #character's inventory
        self.password = password #a password to "protect" the character (not currently used)
        
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
                "gender": self.gender,
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
        with open("Characters/characters.txt","a") as f:
            f.write(self.name)
            
    def get_details(self):
        return "{0} is a {1} level {2} that is currently carrying {3}".format(self.name.title(), self.level, self.race.name, "\n" + "\n".join(self.inv) if self.inv else "nothing")

#FUNCTIONS#
           
def load_character(name):
    try:
        with open("Characters/"+name.title()+"/info.json","r") as f:
            info = json.load(f)
        character = Character(info["name"],info["gender"],races[info["race"]],info["hp"],info["level"],info["exp"],info["inv"],info["password"])
    except FileNotFoundError:
        print("Character \"{0}\" does not exist.".format(name))
        return None
        
    return character


                 
        
if __name__ == "__main__":
    #test that a character can be created
    character = Character("Japhster",races["Human"])
    #test that a characters details work properly and that it can be saved
    print(character.get_details())
    character.save()
    #test that a character can be loaded
    new_char = load_character("Japhster")
    print(new_char.get_details())
    #test that the program can deal with non-existant characters
    new_char = load_character("Noone")
    

