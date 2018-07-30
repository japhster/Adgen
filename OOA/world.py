import copy

from helper_funcs import reverse_direction, get_coord_from_direction, get_direction_from_coords
from player import Player


class World(object):

    def __init__(self,name,start_location,player,rooms={},items={},npcs={},enemies={}):
        self.name = name
        self.rooms = rooms #dictionary mapping the name of a room to the object representing the room
        self.current_location = self.rooms[start_location]
        self.player = player                
        
    def move(self,direction):
        if self.can_move(direction):
            self.current_location = self.rooms[self.current_location.neighbours[direction]]
        else:
            print("I can't do that right now")
    
    def can_move(self,direction):
        room = self.current_location
        if direction not in room.neighbours:
            return False
        return (not room.enemies) and (not direction in room.locks) and (not self.rooms[room.neighbours[direction]].is_dark)

    def take(self,item_name):
        for item in self.current_location.items:
            if item_name == item.name:
                self.current_location.items.remove(item)
                if item.category != "Money":
                    self.player.inv.append(item)
                else:
                    self.player.gold += item.value
                break
                    
    def drop(self,item_name):
        for item in self.player.inv:
            if item.name == item_name:
                self.player.inv.remove(item)
                self.current_location.items.append(item)
                break
            
    def talk(self,person):
        for npc in self.current_location.npcs:
            if npc.name == person:
                response = npc.talk()
                if npc.category == "Merchant":
                    self.player.inventory = response
                if npc.category == "Traveller":
                    room1, room2 = self.rooms[response[0]],self.rooms[response[1]]
                    direction = get_direction_from_coords(room1.coord,room2.coord)
                    room1.neighbours[direction] = room2.name
                    room2.neighbours[reverse_direction(direction)] = room1.name
                    
    def inv(self):
        self.player.print_inv()
        
    def unlock(self,direction):
        for lock in self.current_location.locks:
            if direction == lock[0]:
                if lock[1] in self.player.inv:
                    self.current_location.locks.remove(lock)
                    #find room the direction leads to and remove the lock on that door as well
                    coord = get_coord_from_direction(self.current_location.coord,direction)
                    for room in self.rooms:
                        if room.coord == coord:
                            room.locks.remove((reverse_direction(direction),lock[1]))
                break
                
            
    def get_detailed_neighbours(self,room):
        details = []
        room = self.rooms[room]
        for neighbour in room.neighbours:
            detailed = neighbour
            locked = neighbour in room.locks
            dark = self.rooms[room.neighbours[neighbour]].is_dark
            if locked and dark:
                detailed += "(Lock, Dark)"
            if locked:
                detailed += "(Lock)"
            if dark:
                detailed += "(Dark)"
            details.append(detailed)
        
        return details

class Room(object):

    def __init__(self,name,coord=(0,0),locks=[],neighbours={},items=[],npcs=[],enemies=[]):
        self.name = name
        self.coord = coord #where the room is located in the world relative to the initial room at (0,0)
        self.is_dark = False
        self.neighbours = neighbours #dictionary of a compass direction mapped to the name of the room in that direction
        self.locks = copy.copy(locks) #a list of tuples of directions in which the door has a lock on it and the key required to unlock it
        self.npcs = copy.deepcopy(npcs) #list of NPCs that are found in the room
        self.enemies = copy.deepcopy(enemies) #list of enemies that are found in the room
        self.items = copy.deepcopy(items) #list of items that are found in the room

        self.description = "" #included for expansion
        
    def get_visible(self):
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


