import copy
import re
from collections import defaultdict
import random

from state_functions import get_unique_neighbours, generate_map, reverse_direction, direction_of_coord

"""
rewrite algorithm steps:
 - add room
 - random chance that a key will be placed (.1)
 - generate connections
 - for each door random chance that the door will be locked (.2)
   - random key (that already exists in the world) required to open the door
 - random chance that (if it is not already placed) a torch is placed (.005)
 - random chance that (if a torch exists in the world) the generated room is made dark
"""

def complexify(initial_state, goal_state, room_complexity=10, item_complexity=10):
    initial_complexity = measure_complexity(initial_state,"both")
    #print(initial_complexity)
    state = copy.copy(initial_state)
    #understand what each literal means
    #get a list of room names and item names
    rooms, items = breakdown(state)
    #add new rooms in with appropriate neighbours and unique names
    state = add_rooms(state, goal_state, room_complexity)        
    new_complexity = measure_complexity(state,"both")
    #add new items into the rooms with appropriate features
    options = {lock_doors,darken}
    for option in options:
        new_state = option(state)
        if new_state != None:
            state = new_state

    return state

def breakdown(state,returns="both"):
    """
    returns a list of strings representing the names of the rooms and a list of strings representing the names of items
    """
    rooms = set()
    items = set()
    for item in state:
        if item[0] == "NextTo":
            rooms.add(item[1])
            rooms.add(item[2])
        elif item[0] == "In":
            items.add(item[1])
        elif item[0] == "Contains":
            items.add(item[1])
            items.add(item[2])
        
    return rooms if returns=="rooms" else (items if returns=="items" else rooms,items) 

def count_blockages(state):
    blockages = 0
    for item in state:
        if item[0] == "HiddenPath" or item[0] == "Lock":
            blockages += 0.5
        elif item[0] == "Dark":
            blockages += 1
            
    return blockages

def add_rooms(state, goal, room_complexity):
    """
    get the highest unnamed room number (HRN) from form "Room11"
    add new rooms as named "Room*" where * represents a number higher than the highest number so far
    """
    failed = set() #a set of rooms that already have 4 neighbours
    next_available_number = -1
    while measure_complexity(state, "rooms") < room_complexity:
        #generate a dictionary mapping each room to a coordinate relative to the starting room at (0,0)
        room_map = generate_map(state)
        #randomly select a room and get all surrounding coordinates that are not already assigned
        #if no non-assigned coordinates exist, choose another room
        while True:
            chosen = random.choice([i for i in room_map.keys() if i not in failed])
            valid = set([i for i in get_coord_neighbours(room_map[chosen]) if i not in room_map.values()])
            if (len(valid) == 0) or (("At",chosen) in state) or (("At",chosen) in goal):
                failed.add(chosen)
            else:
                break
        #randomly select a coordinate from valid coords and find all rooms connected to it
        new_room = random.choice(list(valid))
        coord_neighbours = get_coord_neighbours(new_room)
        named_neighbours = [pair[0] for pair in room_map.items() if pair[1] in coord_neighbours]
        #find the next available room name in form Room* where * > 0
        current_rooms = list(breakdown(state,"rooms"))
        if next_available_number == -1:
            next_available_number = get_next_available_number(current_rooms)
        new_room_name = "Room"+str(next_available_number)
        next_available_number += 1
        #randomly generate a number of neighbours that will be added
        num_neighbours = random.randint(1,len(named_neighbours))
        neighbours_to_add = set()
        while len(neighbours_to_add) < num_neighbours:
            neighbours_to_add.add(random.choice(named_neighbours))
        #add new tuples to the state describing the neighbours of the new room
        for neighbour in neighbours_to_add:
            direction = direction_of_coord(new_room,room_map[neighbour]) #from new room to neighbour
            state.append(("NextTo",new_room_name,neighbour,direction))
            state.append(("NextTo",neighbour,new_room_name,reverse_direction(direction)))
        
    return state

def add_item(state):
    items = breakdown(state,"items")
    return state

def lock_doors(state,percent=0.2):
    """
    ***currently only has an effect if the player already has a key***
    ***also could break the initial path through the world***
    adds locked doors to the state
    will lock a percentage of the neighbours that aren't already locked in the state based on arg percent
    """
    if ("Has","Key") in state:
        new_state = copy.copy(state)
        neighbours = get_unique_neighbours(state)
        not_locked_neighbours = []
        for pair in neighbours:
            if not ("Lock",pair[0],pair[1]) in state:
                not_locked_neighbours.append(pair)                
        locked = random.sample(not_locked_neighbours, int(len(not_locked_neighbours)*percent))
        for pair in locked:
            new_state.append(("Lock",pair[0],pair[1]))
            new_state.append(("Lock",pair[1],pair[0]))
        return new_state
    return None
    
def darken(state,percent=0.2):
    """
    ***currently only has an effect if the player already has a torch***
    ***also could break the initial path through the world***
    adds darkness to a percentage of the rooms in the state based on arg percent
    """
    if ("Has","Torch") in state:
        new_state = copy.copy(state)
        rooms = breakdown(state,"rooms")
        light_rooms = []
        for room in rooms:
            if not ("Dark",room) in state:
                light_rooms.append(room)
        make_dark = random.sample(light_rooms, int(len(light_rooms)*percent))
        for room in make_dark:
            new_state.append(("Dark",room))
        return new_state
    return None    
    
    
def get_start_location(state):
    """
    returns the name of the room the player will start in
    """
    for item in state:
        if item[0] == "At":
            return item[1]

def get_neighbour_counts(state):
    """
    returns a dictionary with each room as a key and the number of neighbours that room has as the value
    """
    neighbours = get_unique_neighbours(state)
    neighbour_counts = defaultdict(int)
    for neighbour in neighbours:
        neighbour_counts[neighbour[0]] += 1
        neighbour_counts[neighbour[1]] += 1
        
    return neighbour_counts
        
def get_next_available_number(rooms):
    """
    returns the next number to be used for a room name (e.g. Room2)
    """
    unnamed_rooms = [i for i in rooms if re.match("^Room[1-9]{1}[0-9]*$",i)] #matches to "Room*" where * is any number > 0
    try:
        next_available_number = int(sorted(unnamed_rooms, key=lambda a:int(a[4:]))[-1][4:]) + 1
    except IndexError:
        #no rooms in initial state are of the form Room*
        next_available_number = 1
        
    return next_available_number

def get_coord_neighbours(coord):
    return set([(coord[0]+i[0],coord[1]+i[1]) for i in [(0,1),(1,0),(0,-1),(-1,0)]])
    
        
def measure_complexity(state, measure="both"):
    """
    room complexity will be calculated as the sum of the number of branches from each room
    i.e. number of neighbours of each room -2 for every room that is not the starting room else -1
         -1 for everything is so that if the room only has 1 neighbour then there are no branches
         so the difficulty does not increase
         -1 for non-starting rooms as each room must have had an entrance, which shouldn't be considered as a branch (probably?)
    """
    rooms = breakdown(state)[0]
    num_blockages = count_blockages(state)
    if measure == "rooms" or measure == "both":
        neighbour_counts = get_neighbour_counts(state)
        branches = 0
        start_loc = get_start_location(state)
        for room, count in neighbour_counts.items():
            if ("At",room) in state:
                room_branches = count
            else:
                room_branches = count - 2
            if room_branches > 0:
                branches += room_branches

        return branches if measure == "rooms" else branches + num_blockages
    elif measure == "items":
        return num_blockages


if __name__ == "__main__":
    original_state = [('At', 'Library'), ('NextTo', 'Office', 'Library', "South"), ('NextTo', 'Kitchen', 'Office', "West"),
                      ('NextTo', 'Office', 'Kitchen', "East"), ('NextTo', 'Library', 'Office', "North"), ]


    count = 0
    state = copy.copy(original_state)
    measure_complexity(original_state,"items")
    print(measure_complexity([("At", "Kitchen"), ('NextTo', 'Kitchen', 'Office', "West"),('NextTo', 'Office', 'Kitchen', "East")], "rooms"))
    print(measure_complexity([("At", "Kitchen"), ('NextTo', 'Kitchen', 'Office', "West"),('NextTo', 'Office', 'Kitchen', "East"),('NextTo', 'Kitchen', 'Library', "East"),('NextTo', 'Library', 'Kitchen', "West")], "rooms"))
    print(measure_complexity([("At", "Kitchen"), ('NextTo', 'Kitchen', 'Office', "East"),('NextTo', 'Office', 'Kitchen', "West"),
                                  ('NextTo', 'Kitchen', 'Library', "South"),('NextTo', 'Library', 'Kitchen', "North"),
                                  ("NextTo", "Office", "Room1", "East"), ("NextTo", "Room1","Office", "West"),
                                  ("NextTo", "Office", "Room2", "North"), ("NextTo", "Room2", "Office", "South")], "rooms"))
    while measure_complexity(state,"rooms") < 10:
        try:
            state = add_room(state)
        except ValueError:
            count += 1
            break
        break
    """
    print(measure_complexity(state,"rooms"))
    print(state)
    print(measure_complexity(state,"items"))
    state = lock_doors(state)
    state = darken(state)
    print(state, measure_complexity(state, "items"))
    """

    















