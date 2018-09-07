import os
import json

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
    room_descs = {
             "Library":{"neighbours":{"North":"Hallway"}},
             "Hallway":{"neighbours":{"South":"Library","North":"Kitchen"},"coord":(0,1),"npcs":["Bob"],"locks":[("North","Red Key")]},
             "Bedroom":{"coord":(1,1),"items":["Red Key"]},
             "Kitchen":{"coord":(0,2),"neigbours":{"South":"Hallway"},"items":["Book"],"locks":[("South","Red Key")]},
            }
    rooms = {}
    #for each room in the descriptions
    for room in room_descs:
        #create a new room with the name given in the descriptions
        rooms[room] = Room(room)
        #set all attributes required from the descriptions
        for arg in room_descs[room]:
           setattr(rooms[room],arg,room_descs[room][arg])
           
    npcs = {
            "Bob":Traveller("Bob",("Hallway","Bedroom")),
           }
    items = {
             "Red Key":Key("Red Key"),
             "Book":Item("Book"),
            }
    with open("test.json","w") as f:
        json.dump(room_descs,f)
    world = World("Test", "Library",Player("Japh","Male","Human"), rooms=rooms,items=items,npcs=npcs)
    world.save_world()
    sys.exit(0)
    def goal():
        return "Book" in [item.name for item in world.rooms["Library"].items]

    #PLAY GAME
    response = ""
    while not goal():
        os.system("clear")
        print(response if response else "")
        print_surroundings(world)
        command = input(">").split()
        action = command[0].lower()
        arg = " ".join(command[1:]).title()
        try:
            if arg:
                response = getattr(world,action)(arg)
            else:
                response = getattr(world,action)()
        except IndexError:
            pass
        """
        except AttributeError as e:
            response = "You don't understand how to \"{0}\".".format(" ".join(command))
        """    
    print("You Win!")
