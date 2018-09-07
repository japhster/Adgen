import copy

from helper_funcs import reverse_direction, get_coord_from_direction, get_direction_from_coords

class WorldPart(object):
    
    def __init__(self,name):
        self.name = name
        
    def get_dict_format(self):
        info = [i for i in dir(self) if not i.startswith("__") and not callable(getattr(self,i))]
        print(info)
        return_value = {}
        for i in info:
            print(i,getattr(self,i))
            return_value[i] = getattr(self,i)

        return return_value

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







