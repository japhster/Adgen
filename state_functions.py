from collections import defaultdict


def get_unique_neighbours(state):
    """
    returns a set of tuples containing a pair of rooms if they are next to eachother and the direction from 0 to 1
    removes duplicates. e.g. (room2,room3), (room3,room2)
    """
    neighbours = set()
    for item in state:
        if item[0] == "NextTo" and (item[2],item[1],reverse_direction(item[3])) not in neighbours:
            neighbours.add((item[1],item[2],item[3]))
            
    return neighbours

def generate_map(state):
    """
    returns a dictionary mapping each room to an x,y coordinate relative to the starting room at (0,0)
    """
    rooms = {}
    #get the starting room and give it coordinate (0,0)
    for i in state:
        if i[0] == "At":
            rooms[i[1]] = (0,0)
    #for each other room that is next to the initial room, give it a coordinate
    considered = set()
    while len(considered) != len(get_unique_neighbours(state)):
        for room1,room2,direction in get_unique_neighbours(state):
            #if the neighbours haven't already been considered
            if not tuple(sorted((room1,room2))) in considered:
                #EITHER:
                #first room already assigned so assign second room a coordinate
                if room1 in rooms.keys():
                    rooms[room2] = coordinate_modifier(rooms[room1],direction)
                    considered.add(tuple(sorted((room1,room2))))
                #OR:
                #second room already assigned so assign first room a coordinate
                elif room2 in rooms.keys():
                    rooms[room1] = coordinate_modifier(rooms[room2],reverse_direction(direction))
                    considered.add(tuple(sorted((room1,room2))))

    return rooms

def coordinate_modifier(coord, direction):
    mod = {"East":(1,0),"West":(-1,0),"South":(0,-1),"North":(0,1)}[direction]
    return (coord[0]+mod[0],coord[1]+mod[1])
    
def direction_of_coord(start,end):
    mod = {(1,0):"East",(-1,0):"West",(0,-1):"South",(0,1):"North"}
    return mod[(end[0]-start[0],end[1]-start[1])]


def format_state(line,remove_from_front):
        """
        takes in a state as saved in an output file and removes the front part
        usually either "Initial state: " or "Goal state: "
        returns a set of literals from the state
        """
        line = line[len(remove_from_front)+1:].split("),")
        line[-1] = line[-1][:-1]
        return set([deconstruct_literal(literal + ")") for literal in line])


def deconstruct_literal(literal):
    """
    takes input of a literal in natural form and converts it to a storable tuple
    e.g.
    "Neighbour(Room1,Room2)"
    will be returned as:
    ("Neighbour","Room1","Room2")
    """
    literal = literal.split("(")
    return_list = tuple([literal[0]] + literal[1][:-1].split(","))
    return return_list
    
    
def reverse_direction(direction):
    dirs = {"East":"West","West":"East","South":"North","North":"South"}
    try:
        return dirs[direction]
    except KeyError as e:
        print("{0} is not a direction.".format(e))
        return None

def get_details(state):
    """
    returns a dictionary of details mapping the type of interactable object to a list of objects in the world of that type.
    types include:
     - keys
     - containers
     - lightsources
     - items (including all of the above)
     - people
     - directions
    """
    details = defaultdict(set)
    details["directions"] = {"north","east","south","west"}
    for item in state:
        if item[0] == "LockNeeds":
            details["keys"].add(item[3])
        elif item[0] == "Openable":
            details["containers"].add(item[1])
        elif item[0] == "Purpose" and item[2] == "Light":
            details["lightsources"].add(item[1])
        elif item[0] == "Knows":
            details["people"].add(item[1])
        elif item[0] == "In":
            is_item = True
            for jtem in state:
                if jtem[0] == "Knows" and item[1] in jtem:
                    is_item = False
                    break
            if is_item:
                details["items"].add(item[1])
        elif item[0] == "Contains":
            details["items"].add(item[2])
    print(details)
    return details














