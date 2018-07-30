import os

from world import World,Room
from items import Item,Lightsource,Key,Container,Money
from npcs import Merchant,Traveller
from enemies import Enemy
from player import Player

def print_surroundings(world):
    print("You are in a {0}".format(world.current_location.name))
    print("You can see: {0}".format(", ".join(world.current_location.get_visible())))
    print("There are exits: {0}".format(",".join(world.get_detailed_neighbours(world.current_location.name))))

if __name__ == "__main__":
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

    def goal():
        return "Book" in [item.name for item in world.rooms["Library"].items]

    #PLAY GAME
    while not goal():
        os.system("clear")
        print_surroundings(world)
        command = input(">").split()
        action = command[0].lower()
        arg = " ".join(command[1:]).title()
        if arg:
            getattr(world,action)(arg)
        else:
            getattr(world,action)()
            
    print("You Win!")
