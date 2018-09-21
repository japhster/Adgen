import random

from actions import all_actions
from state_functions import get_unique_neighbours, generate_map, reverse_direction, direction_of_coord, get_coord_neighbours, get_details
from visual import visualise_map
from save_plan import save_plan
from complexify import lock_door, darken

def basic_add_room(state,details,next_available_number):
    failed = set() #a set of rooms that already have 4 neighbours
    #generate a dictionary mapping each room to a coordinate relative to the starting room at (0,0)
    room_map = generate_map(state)
    #randomly select a room and get all surrounding coordinates that are not already assigned
    #if no non-assigned coordinates exist, choose another room
    while True:
        chosen = random.choice([i for i in room_map.keys() if i not in failed])
        valid = set([i for i in get_coord_neighbours(room_map[chosen]) if i not in room_map.values()])
        if (len(valid) == 0):
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
        
    return state, next_available_number+1

#start with basic, clear world        
state = [("At","Room0")]
nan = 1
game_name = "Auto Generated"
#add rooms and complexify
for i in range(20):
    details = get_details(state)
    state, nan = basic_add_room(state,details,nan)
#generate goal state (atm just select a room to get to)
goal_state = [("At", "Room{0}".format(random.randint(1,20)))]
#save the plan
details = get_details(state)
save_plan(list(state),list(goal_state),list(all_actions.values()),game_name,details)
#visualise world
visualise_map(generate_map(state),get_unique_neighbours(state),game_name)

