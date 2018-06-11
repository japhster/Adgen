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

def action_is_possible(state,preconditions):
    for precond in preconditions:
        #if condition is negative and its positive is in the state the action can't happen
        #if condition is positive and is not in the state the action can't happen
        if (precond[0][0] == "!" and get_positive_version(precond) in current_state) or (precond[0][0] != "!" and precond not in current_state):
            print(precond)
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

    print("You are in a room.")
    print("You can see: " + (", ".join(items) if items else "nothing"))
    print("You can move: " + ", ".join([exit[0] for exit in exits]))

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
    performed = True
    while True:
        os.system("clear")
        if not performed:
            print("I cannot \"{0}\" at this point in time".format(" ".join(instruction)))
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
        except KeyError:
            print("Sorry, I don't understand that command.")
        definition = all_actions[action[0]]
        #check action can be performed
        preconditions = [make_actual_condition(action,definition,precond) for precond in definition[1]]
        if action_is_possible(current_state,preconditions):
            #perform action
            postconditions = [make_actual_condition(action,definition,postcond) for postcond in definition[2]]
            perform_action(current_state,postconditions)
            performed = True
        else:
            #action can't be performed so inform player
            performed = False
        #check if goal state has been reached
        if goal_reached(current_state,goal_state):
            print("You Win!")
            break
        
            
        
    
