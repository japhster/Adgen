import sys
import copy
import os

from generate_world import deconstruct_literal, make_actual_condition, get_positive_version
from actions import all_actions
from actions import Move, Unlock, Take, Open, ClearDarkness, Talk



def get_items(state, room):        
    return [item[1] for item in state if item[0] == "In" and item[-1] == room]

def get_exits(state, room):
    return [(item[3], item[2]) for item in state if item[0] == "NextTo" and item[1] == room]
    
def get_neighbouring_blockages(state,room,blockage):
    #could be "Lock", "Dark", "HiddenPath"
    return [item[2] for item in state if item[0] == blockage and item[1] == room]

def get_inventory(state):
    return [item[1] for item in state if item[0] == "Has"]
    
def action_is_possible(state,preconditions):
    for precond in preconditions:
        #if condition is negative and its positive is in the state the action can't happen
        negative_and_positive_in_state = precond[0][0] == "!" and get_positive_version(precond) in current_state
        #if condition is positive and is not in the state the action can't happen
        positive_and_not_in_state = precond[0][0] != "!" and precond not in current_state
        if negative_and_positive_in_state or positive_and_not_in_state:
            return False
            
    return True

def perform_action(state,postconditions):
    for postcond in postconditions:
        positive = get_positive_version(postcond)
        if postcond[0][0] == "!" and positive in state:
            state.remove(positive)
        elif postcond[0][0] != "!":
            state.add(postcond)

def print_state(state):
    for item in state:
        if item[0] == "At":
            location = item[1]
            break

    items = get_items(state,location)
    exits = get_exits(state,location)
    locked_doors = get_neighbouring_blockages(state,location,"Lock")
    dark_rooms = get_neighbouring_blockages(state,location,"Dark")
    detailed = []
    for room in exits:
        if room[1] in locked_doors and dark_rooms:
            detailed.append(room[0] + " (Locked, Dark)")
        elif room[1] in locked_doors:
            detailed.append(room[0] + " (Locked)")
        elif room[1] in dark_rooms:
            detailed.append(room[0] + " (Dark)")
        else:
            detailed.append(room[0])
    print("You are in a room.")
    print("You can see: " + (", ".join(items) if items else "nothing"))
    print("There are exits to the: " + ", ".join(sorted(detailed)))

def goal_reached(state,goal_state):
    for item in goal_state:
        if item[0][0] != "!" and item not in state:
            return False
        if item[0][0] == "!" and get_positive_version(item) in state:
            return False
    
    return True
    

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        #capture initial state
        line = f.readline().strip()[15:].split("),")
        line[-1] = line[-1][:-1]
        initial_state = set([deconstruct_literal(literal + ")") for literal in line])
        #capture goal state
        line = f.readline().strip()[12:].split("),")
        line[-1] = line[-1][:-1]
        goal_state = set([deconstruct_literal(literal + ")") for literal in line])
        
    current_state = copy.copy(initial_state)
    non_functional_commands = ["inv"]
    performed = True
    while True:
        os.system("clear")
        if not performed:
            if error:
                print(error)
            else:
                print("I cannot \"{0}\" at this point in time".format(" ".join(instruction)))
        performed = False
        error = None
        print_state(current_state)
        #get instruction
        instruction = tuple(input(">").split())
        
        if not instruction:
            break
        #get action for instruction
        try:
            action = {"move":Move,"unlock":Unlock,"take":Take,
                           "cleardarkness":ClearDarkness,"open":Open,
                           "talk":Talk}[instruction[0].lower()](current_state, *instruction).action
        except KeyError as e:
            action = None
            if instruction[0].lower() in non_functional_commands:
                if instruction[0].lower() == "inv":
                    error = "You have: " + ", ".join(get_inventory(current_state))
            else:
                error = "Sorry, I don't understand the command: {0}.".format(e)
        except TypeError as e:
            action = None
            error = "That command is missing a {0}".format(str(e).split()[-1])
        if action:
            definition = all_actions[action[0]]
            #check action can be performed
            preconditions = [make_actual_condition(action,definition,precond) for precond in definition[1]]
            if action_is_possible(current_state,preconditions):
                #perform action
                postconditions = [make_actual_condition(action,definition,postcond) for postcond in definition[2]]
                perform_action(current_state,postconditions)
                performed = True
        #check if goal state has been reached
        if goal_reached(current_state,goal_state):
            print("You Win!")
            break
        
            
        
    
