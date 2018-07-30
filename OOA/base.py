import copy

from helper_funcs import reverse_direction, get_coord_from_direction, get_direction_from_coords

class Player(object):

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
        print("I am currently carrying:\n" + "\n".join(self.inv))





if __name__ == "__main__":
    from world import World,Room
    from items import Item,Lightsource,Key,Container,Money
    from npcs import Merchant,Traveller
    from enemies import Enemy
    #CREATE WORLD
    rooms = {
             "Library":Room("Library",neighbours={"North":"Hallway"}),
             "Hallway":Room("Hallway",neighbours={"South":"Library","North":"Kitchen"},coord=(0,1)),
             "Bedroom":Room("Bedroom",coord=(1,1)),
             "Kitchen":Room("Kitchen",coord=(0,2),neighbours={"South":"Hallway"}),
            }
    rooms["Hallway"].npcs.append(Traveller("Bob",("Hallway","Bedroom")))
    rooms["Bedroom"].items.append(Key("Red Key"))
    rooms["Kitchen"].items.append(Item("Book"))
    rooms["Hallway"].locks.append(("North","Red Key"))
    rooms["Kitchen"].locks.append(("South","Red Key"))
    world = World("Test", "Library",Player("Japh","Male","Human"), rooms=rooms)

    #TEST WORLD CAN BE COMPLETED
    actions = [(world.move,"North"),(world.talk,"Bob"),(world.move,"East"),(world.take,"Red Key"),(world.move,"West"),
               (world.unlock,"North"),(world.move,"North"),(world.take,"Book"),(world.move,"South"),(world.move,"South"),
               (world.drop,"Book")
              ]

    def goal():
        return "Book" in [item.name for item in world.rooms["Library"].items]

    for action in actions:
        if goal():
            print(world.rooms["Kitchen"].items)
            break
        print(world.current_location.name)
        action[0](action[1])

    print("You Win")







