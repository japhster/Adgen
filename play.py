import sys
import copy
import os
import string
import json

from generate_world import make_actual_condition, get_positive_version
from actions import all_actions, actions, commands, requirements
from actions import Move, Unlock, Take, Open, ClearDarkness, Talk
from state_functions import deconstruct_literal, format_state


class World(object):
    
    def __init__(self,details):
        self.details = details
        
    def fill_in_assumptions(self):
        self.items = self.items + self.keys + self.containers

def get_items(state, room):
    """
    returns a list of items that can be found in the given room
    """
    return [item[1] for item in state if item[0] == "In" and item[-1] == room]

def get_exits(state, room):
    """
    returns a list of exits from the given room
    """
    return [(item[3], item[2]) for item in state if item[0] == "NextTo" and item[1] == room]
    
def get_neighbouring_blockages(state,room,blockage):
    """
    returns a list of rooms that are connected to the given room who's passage is blocked in some way
    could be "Lock", "HiddenPath"
    """
    return [item[2] for item in state if item[0] == blockage and item[1] == room]

def get_dark_neighbours(state,room):
    """
    returns a list of darkened rooms connected to the given room
    """
    return [item[1] for item in state if item[0] == "Dark"]

def get_inventory(state):
    """
    returns a list of items that the character has on them
    """
    return [item[1] for item in state if item[0] == "Has"]
    
def get_conflicts_with_action(state,preconditions):
    """
    tests to see if all the preconditions exist in the state therefore making it possible to perform the action
    returns a set of all conflicting precondition or an empty set if there are no conflicting preconditions
    """
    conflicts = set()
    for precond in preconditions:
        #if condition is negative and its positive is in the state the action can't happen
        negative_and_positive_in_state = precond[0][0] == "!" and get_positive_version(precond) in current_state
        #if condition is positive and is not in the state the action can't happen
        positive_and_not_in_state = precond[0][0] != "!" and precond not in current_state
        if negative_and_positive_in_state or positive_and_not_in_state:
            conflicts.add(precond[0])
            
    return conflicts

def perform_action(state,postconditions):
    """
    adds all the postconditions to the state (cancelling out conditions when it is negative) therefore having performed the action
    """
    for postcond in postconditions:
        positive = get_positive_version(postcond)
        if postcond[0][0] == "!" and positive in state:
            state.remove(positive)
        elif postcond[0][0] != "!":
            state.add(postcond)

def print_state(state):
    """
    prints out the information pertaining to the whereabouts of the character
    - where they are
    - what items are in the current room
    - what exits there are from the room (including whether or not they are blocked)
    """
    for item in state:
        if item[0] == "At":
            location = item[1]
            break
    inv = get_inventory(state)
    items = get_items(state,location)
    exits = get_exits(state,location)
    locked_doors = get_neighbouring_blockages(state,location,"Lock")
    dark_rooms = get_dark_neighbours(state,location)
    detailed = []
    for room in exits:
        if room[1] in locked_doors and room[1] in dark_rooms:
            detailed.append(room[0] + " (Locked, Dark)")
        elif room[1] in locked_doors:
            detailed.append(room[0] + " (Locked)")
        elif room[1] in dark_rooms:
            detailed.append(room[0] + " (Dark)")
        else:
            detailed.append(room[0])
    print("You are in a room.")
    print("You have: " + (", ".join(inv) if inv else "nothing"))
    print("You can see: " + (", ".join(items) if items else "nothing"))
    print("There are exits to the: " + ", ".join(sorted(detailed)))

def goal_reached(state,goal_state):
    """
    checks to see if the current state contains all the requirements of the goal state
    """ 
    for item in goal_state:
        if item[0][0] != "!" and item not in state:
            return False
        if item[0][0] == "!" and get_positive_version(item) in state:
            return False
    
    return True

def parse_input(instruction,actions,commands,requirements,world):
    #remove punctuation
    exclude = set(string.punctuation)
    instruction = "".join(ch for ch in instruction if ch not in exclude)
    #get action
    action = None
    instruction = instruction.split()
    for name,options in commands.items():
        for option in options:
            if set(option.split()).issubset(set(instruction)):
                action = name
                break
        if action:
            break
    #get required arguments
    if action:
        parsed = [action]
        #for each thing required by the action found
        for requirement in requirements[action]:
            #check if a defined item in details.txt is in the instruction and add it to parsed if it is
            found = False
            for item in world.details[requirement+"s"]:
                #print(set(item.lower().split()),set(instruction))
                if set(item.lower().split()).issubset(set(instruction)):
                    parsed.append(item)
                    found = True
                    break
            if not found:
                return "I need a{0} {1} to perform that action.".format("n" if requirement[0] in "aeiou" else "",requirement)
    else:
        return instruction     
    
    return parsed

def perform_pre_actions(state,all_actions,conflicts,move_action):
    """
    is used when a move command is given with a lock on a door or the room being moved to is dark
    will attempt to perform all the necessary actions leading up to the action, and return if it was successful or not
    """
    if "!Lock" in conflicts:
        pass
        #build unlock action from scratch
         #needs a direction and a key
        print(move_action)
        #find the key required for the action
        for item in state:
            if item[0] == "LockNeeds" and item == ("LockNeeds",move_action[1],move_action[2],item[3]):
                key = item[3]
                break
        instruction = ["Unlock",move_action[3],key]
        action = actions["unlock"](current_state,*instruction).action
        definition = all_actions[action[0]]
        #check the action can be performed
        unlock_preconds = [make_actual_condition(action,definition,precond) for precond in definition[1]]
        conflicts = get_conflicts_with_action(state,unlock_preconds)
        if conflicts:
            #if it can't perform the action return False
            print("lock: {0}".format(conflicts))
            return False
        unlock_postconds = [make_actual_condition(action,definition,postcond) for postcond in definition[2]]
        #perform the action
        perform_action(state,unlock_postconds)

    if "!Dark" in conflicts:
        pass
        #build cleardarkness action from scratch
        #find all light sources in the world and check if the player has any of them
        #if it doesn't find one the player has then that is okay, it will fail on the next step
        for item in state:
            if item[0] == "Purpose" and item[2] == "Light":
                light_source = item[1]
                #check the player has the light source
                if ("Has",light_source) in state:
                    #can jump out early knowing the player has this light source
                    break
        instruction = ["ClearDarkness",move_action[3],light_source]
        action = actions["clear darkness"](current_state,*instruction).action
        definition = all_actions[action[0]]
        #check the action can be performed
        light_preconds = [make_actual_condition(action,definition,precond) for precond in definition[1]]
        conflicts = get_conflicts_with_action(state,light_preconds)
        if conflicts:
            #if it can't perform the action return False
            print("dark: {0}".format(conflicts))
            return False
        light_postconds = [make_actual_condition(action,definition,postcond) for postcond in definition[2]]
        perform_action(state,light_postconds)
        
    return True

if __name__ == "__main__":
    """
    takes argument of the name of the adventure
    """
    adventure = "Games/" + " ".join(sys.argv[1:]).title()
    world_path = adventure + "/world.txt"
    details_path = adventure + "/details.json"
    with open(world_path, "r") as f:
        #capture initial state
        initial_state = format_state(f.readline().strip(), "Initial state:")
        #capture goal state
        goal_state = format_state(f.readline().strip(), "Goal state:")
        with open(details_path,"r") as f:
            #this file is for details
            #defines what type of object anything in the world is
            details = json.load(f)
        world = World(details)
            
        
    current_state = copy.copy(initial_state)
    non_functional_commands = ["inv"]
    multi_action_commands = ["Move"]
    performed = True
    response = None
    while True:
        os.system("clear")
        #check if goal state has been reached
        if goal_reached(current_state,goal_state):
            print("You Win!")
            break
        if response:
            print(response)
        performed = False
        response = None
        action = None
        print_state(current_state)
        #get instruction
        instruction = input(">")
        real_instruction = parse_input(instruction, actions, commands, requirements, world)
        if type(real_instruction) != list:
            #action was missing a requirement
            response = real_instruction
        if not "".join(instruction):
            quit = input("Do you really want to quit (Y/n)?")
            if quit.lower() in ["","y","yes"]:
                break
        #get action for instruction
        if not response:
            try:
                action = actions[real_instruction[0]](current_state,*real_instruction).action
                print(action)
                response = "You {0}".format(instruction)
            except TypeError:
                response = "Sorry, I couldn't \"{0}\"".format(instruction)
            #if no action so far then check in non_functional_commands
            if not action and real_instruction[0].lower() in non_functional_commands:
                if real_instruction[0].lower() == "inv":
                    response = "You have: " + ", ".join(get_inventory(current_state))
            elif not action:
                response = "Sorry, I don't understand the command \"{0}\".".format(instruction) 

        if action:
            definition = all_actions[action[0]]
            #check action can be performed
            preconditions = [make_actual_condition(action,definition,precond) for precond in definition[1]]
            while not performed:
                conflicts = get_conflicts_with_action(current_state,preconditions)
                if  conflicts == set():
                    #perform action
                    postconditions = [make_actual_condition(action,definition,postcond) for postcond in definition[2]]
                    perform_action(current_state,postconditions)
                    performed = True
                elif action[0] in multi_action_commands and conflicts.issubset({"!Lock","!Dark"}):
                    if not perform_pre_actions(current_state,all_actions,conflicts,action):
                        response = "Sorry, I can't \"{0}\" at this point in time".format(instruction)
                        break
                else:
                    print(conflicts)
                    response = "Sorry, I can't \"{0}\" at this point in time".format(instruction)
                    break
        
            
        
    
