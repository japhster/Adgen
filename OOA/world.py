import copy
import os
import json

from helper_funcs import reverse_direction, get_coord_from_direction, get_direction_from_coords
from player import Player
from base import WorldPart


class World(object):

    def __init__(self,name,start_location,player,rooms={},items={},npcs={},enemies={}):
        self.name = name
        self.rooms = rooms #dictionary mapping the name of a room to the object representing the room
        self.items = items
        self.npcs = npcs
        self.enemies = enemies
        self.current_location = self.rooms[start_location]
        self.player = player                
        
    def move(self,direction):
        if self.can_move(direction):
            self.current_location = self.rooms[self.current_location.neighbours[direction]]
            return "You moved {0}".format(direction)

        return "You can't move {0} right now".format(direction)
            
    def can_move(self,direction):
        room = self.current_location
        locks = [i[0] for i in room.locks]
        if direction not in room.neighbours:
            return False
        return (not room.enemies) and (not direction in locks) and (not self.rooms[room.neighbours[direction]].is_dark)

    def take(self,item_name):
        for item in self.current_location.items:
            if item_name == item:
                item = self.items[item]
                break
        try:
            self.current_location.items.remove(item_name)
            if item.category != "Money":
                self.player.inv.append(item_name)
            else:
                self.player.gold += item.value
        except ValueError:
            return "You can't see the {0}".format(item_name)

        return "You picked up the {0}".format(item_name)
                    
    def drop(self,item_name):
        for item in self.player.inv:
            if item == item_name:
                self.player.inv.remove(item_name)
                self.current_location.items.append(item)
                
                return "You dropped the {0}".fomat(item_name)
        
        return "You don't have the {0}".format(item_name)
            
    def talk(self,person):
        npc = ""
        for npc in self.current_location.npcs:
            if person in self.npcs:
                if npc == person:
                    npc = self.npcs[npc]
                    break
        try:
            response = npc.talk()
        except AttributeError:
            return "You can't see {0}".format(person)
        if npc.category == "Merchant":
            self.player.inventory = response
        if npc.category == "Traveller":
            room1, room2 = self.rooms[response[0]],self.rooms[response[1]]
            direction = get_direction_from_coords(room1.coord,room2.coord)
            room1.neighbours[direction] = room2.name
            room2.neighbours[reverse_direction(direction)] = room1.name
            return "You talk to {0} and he shows you a shortcut between The {1} and The {2}".format(person,npc.knowledge[0],npc.knowledge[1])
            
                    
    def inv(self):
        return self.player.print_inv()
        
    def unlock(self,direction):
        for lock in self.current_location.locks:
            if direction == lock[0]:
                if lock[1] in self.player.inv:
                    self.current_location.locks.remove(lock)
                    #find room the direction leads to and remove the lock on that door as well
                    coord = get_coord_from_direction(self.current_location.coord,direction)
                    for room in self.rooms:
                        if self.rooms[room].coord == coord:
                            self.rooms[room].locks.remove((reverse_direction(direction),lock[1]))
                    return "You unlock the door to the {0}".format(direction)
                
        return "There isn't a lock to the {0}".format(direction)
                
            
    def get_detailed_neighbours(self,room):
        details = []
        room = self.rooms[room]
        for neighbour in room.neighbours:
            detailed = neighbour
            locked = neighbour in [i[0] for i in room.locks]
            dark = self.rooms[room.neighbours[neighbour]].is_dark
            if locked and dark:
                detailed += " (Lock, Dark)"
            elif locked:
                detailed += " (Lock)"
            elif dark:
                detailed += " (Dark)"
            details.append(detailed)
        
        return details


    def save_world(self):
        directory = "Games/" + self.name + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        fixed_info = ["rooms","items","npcs","enemies"]
        flexible_info = ["player","current_location"]

        for name in fixed_info:
            with open(directory + name + ".json","w+") as f:
                to_save = {}
                for item,obj in getattr(self,name).items():
                    to_save[item] = obj.get_dict_format()
                json.dump(to_save,f)
        directory += "Saves/" + self.player.name + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory + "player.json","w+") as f:
            json.dump(self.player.get_dict_format(),f)
        with open(directory + "current_location.json","w+") as f:
            json.dump(self.current_location.get_dict_format(),f)



class Room(WorldPart):

    def __init__(self,name,coord=(0,0),locks=[],neighbours={},items=[],npcs=[],enemies=[]):
        super(Room,self).__init__(name)
        self.coord = coord #where the room is located in the world relative to the initial room at (0,0)
        self.is_dark = False
        self.neighbours = neighbours #dictionary of a compass direction mapped to the name of the room in that direction
        self.locks = copy.copy(locks) #a list of tuples of directions in which the door has a lock on it and the key required to unlock it
        self.npcs = copy.deepcopy(npcs) #list of NPCs that are found in the room
        self.enemies = copy.deepcopy(enemies) #list of enemies that are found in the room
        self.items = copy.deepcopy(items) #list of items that are found in the room

        self.description = "" #included for expansion
        
    def get_visible(self):
        return self.npcs + self.enemies + self.items
        lists_to_return = [self.npcs,self.enemies,self.items]
        return_values = []
        for item in lists_to_return:
            for jtem in item:
                return_values.append(jtem.name)
        return return_values

if __name__ == "__main__":
    from player import Player
    from items import Item,Lightsource,Key,Container,Money
    from npcs import Merchant,Traveller
    from enemies import Enemy
    room_descs = {
             "Library":{"neighbours":{"North":"Hallway"}},
             "Hallway":{"neighbours":{"South":"Library","North":"Kitchen"},"coord":(0,1),"npcs":["Bob"],"locks":[("North","Red Key")]},
             "Bedroom":{"coord":(1,1),"items":["Red Key"]},
             "Kitchen":{"coord":(0,2),"neigbours":{"South":"Hallway"},"items":["Book"],"locks":[("South","Red Key")]},
            }
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


