import copy
import re
from collections import defaultdict
import random

from state_functions import get_unique_neighbours, generate_map, reverse_direction, direction_of_coord, get_coord_neighbours

def complexify(initial_state, goal_state, details, room_complexity=10, item_complexity=10):
    initial_complexity = measure_complexity(initial_state,"both")
    #print(initial_complexity)
    state = copy.copy(initial_state)
    #understand what each literal means
    #get a list of room names and item names
    rooms, items = breakdown(state)
    nan = get_next_available_number(rooms)
    while room_complexity > measure_complexity(state,"rooms"):
        #add new rooms in with appropriate neighbours and unique names
        state,nan,added_room_name = add_room(state, goal_state, details, nan)

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

def add_room(state, goal, details, next_available_number):
    """
    get the highest unnamed room number (HRN) from form "Room11"
    add new rooms as named "Room*" where * represents a number higher than the highest number so far
    """
    failed = set() #a set of rooms that already have 4 neighbours
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
    #randomly select a coordinate from valid coords and find all rooms adjacent to it
    new_room = random.choice(list(valid))
    coord_neighbours = get_coord_neighbours(new_room)
    named_neighbours = [pair[0] for pair in room_map.items() if pair[1] in coord_neighbours]
    #find the next available room name in form Room* where * > 0
    new_room_name = "Room"+str(next_available_number)
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
    
    #maybe lock a door
    state = lock_door(state,details,new_room_name)
    #maybe darken the room
    state = darken(state,details,new_room_name)
        
    return state, next_available_number+1, new_room_name

def lock_door(state,details,room_name,percent=0.4):
    """
    adds locked doors to the state
    will lock a percentage of the neighbours that aren't already locked in the state based on arg percent
    """
    colours = ["Red","Blue","Purple","Orange","Yellow","Pink","White","Black","Green"]
    for n in get_neighbours(state,room_name):
        if random.uniform(0,1) < percent:
            if len(details["keys"]) == 0:
                new_key = random.choice(colours) + " Key"
                #place a key in the world
                place = random.choice(list(breakdown(state,"rooms")))
                state.append(("In",new_key,place))
                state.append(("Takeable",new_key))
                details["keys"].add(new_key)
            if random.uniform(0,1) < .2:
                #add a new key and use that
                while True:
                    new_key = random.choice(colours) + " Key"
                    if not new_key in details["keys"]:
                        place = random.choice(list(breakdown(state,"rooms")))
                        state.append(("In",new_key,place))
                        state.append(("Takeable",new_key))
                        details["keys"].add(new_key)
                        break
                key_required = new_key
                print("A new key has entered the world")
            else:
                key_required = random.choice(list(details["keys"]))
            state.append(("Lock",room_name,n))
            state.append(("LockNeeds",room_name,n,key_required))
            state.append(("Lock",n,room_name))
            state.append(("LockNeeds",n,room_name,key_required))
        
    return state
    
def darken(state,details,room_name,percent=0.2):
    """
    adds darkness to a percentage of the rooms in the state based on arg percent
    """
    if random.uniform(0,1) < percent:
        if len(details["lightsources"]) == 0:
            #place a lightsource in the world somewhere
            place = random.choice(list(breakdown(state,"rooms")))
            state.append(("In","Torch",place))
            state.append(("Takeable","Torch"))
            state.append(("Purpose","Torch","Light"))
            details["lightsources"].add("Torch")
        #add the dark room to the state
        state.append(("Dark",room_name))
    
    return state

def get_start_location(state):
    """
    returns the name of the room the player will start in
    """
    for item in state:
        if item[0] == "At":
            return item[1]

def get_neighbours(state,room):
    return [n[1] for n in get_unique_neighbours(state) if n[0] == room]

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

