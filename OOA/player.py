from base import WorldPart

class Player(WorldPart):

    def __init__(self, name, gender, race, hp=0, level=1, gold=0, exp=0, inv=[], password=""):
        self.name = name #name of character
        """
        self.gender = gender #character's gender
        self.race = race #character's race object (e.g. Human)
        self.hp = hp if hp > 0 else sum([random.randint(1,i) for i in self.race.hp_dice]) #character's hit points
        self.level = level #character's level
        self.exp_requirement = self.race.base_exp*(self.level**self.race.level_factor) #the required exp to level up
        self.exp = exp #character's experience points
        self.gold = gold
        """
        self.inv = inv #character's inventory
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
            
    def get_details(self):
        return "{0} is a {1} level {2} that is currently carrying {3}".format(self.name.title(), self.level, self.race.name, "\n" + "\n".join(self.inv) if self.inv else "nothing")

    def print_inv(self):
        return "You are currently carrying:\n" + "\n".join(self.inv) if self.inv else "You don't have anything at the moment."










