import copy
import sys

from actions import all_actions
from output_plan import save_plan
from exceptions import SequenceError, SequenceMergeError
from complexify import complexify, generate_map, get_unique_neighbours, coordinate_modifier
from visual import visualise_map


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

def make_actual_condition(action, definition, cond):
    """
    removes variables from conditions replacing them with actual names
    e.g. (Move,From,To) might become (Move,Room1,Room2)
    """
    actual_cond = [cond[0]]
    for item in cond[1:]:
        #get the name from the action based on it's definition
        #e.g. action may be (Move, Room1, Room2) with definition (Move,From,To)
        #so literal should read At(Room1) not At(From)
        try:
            actual_cond.append(action[definition[0].index(item)])
        except ValueError:
            #item is already not a variable
            actual_cond.append(item)
            
    return tuple(actual_cond)

def cond_is_negative(cond):
    return cond[0][0] == "!"

def get_positive_version(cond):
    """
    returns a positive version of a condition if that condition is negative
    otherwise returns None
    """
    return tuple([cond[0][1:]] + list(cond[1:])) if cond_is_negative(cond) else None

def backtrack(goal_state,actions):
    """
    takes a list of literals defining the goal_state and a sequence of actions from initial to goal state
    e.g. {("InRoom","A")}, [("Take","Key"),("Unlock","B","A"),("Move","B","A")]
    reverses the sequence of actions and adds preconditions to the goal state
    to get back to the simplest initial state
    """
    actions.reverse()
    current_state = copy.copy(goal_state)
    for action in actions:
        #find action in list of all actions
        definition = all_actions[action[0]]
        for cond in definition[2]: #for each condition in the postconditions
            actual_cond = make_actual_condition(action,definition,cond)
            positive_cond = get_positive_version(actual_cond)
            if positive_cond in current_state:
                #if the condition is a negative and its positive is in the state the action couldn't have been performed 
                #so throw an exception
                print("Action requires a negative condition which is positive.")
                raise SequenceError("action sequence is not valid.")
            if actual_cond[0] == "At" and "At" in [c[0] for c in current_state] and actual_cond not in current_state:
                #if the condition is "At" and a different "At" is in the state the action couldn't have been performed
                #so throw an exception
                print("Conflicting location.") 
                raise SequenceError("action sequence is not valid.")
        #add preconditions of action to current state (cancelling out any negations)
        for cond in definition[1]: #for each condition in the preconditions
            actual_cond = make_actual_condition(action,definition,cond)
            positive_cond = get_positive_version(actual_cond)
            if cond_is_negative(actual_cond) and positive_cond in current_state:
                #if a condition is a negation and its positive literal is in the current state 
                current_state.remove(positive_cond)
            if not cond_is_negative(actual_cond):
                #if a condition is not a negation
                current_state.add(actual_cond) #add it to the current state
            #if a condition is a negation and its positive is not in the current state
            #nothing changes as this is assumed in the OWA anyway
                

    #current state must now be an initial state for this solution

    return current_state

def combine_states(initial_states):
    initial_state = set()
    for state in initial_states:
        for condition in state:
            initial_state.add(condition)
    #check that there is only one "At" variable
    if len([cond for cond in initial_state if cond[0] == "At"]) > 1:
        raise SequenceMergeError("At least two sequences start in different locations.")
    #check that the grid structure for the combination makes sense
    #includes if two rooms lead to the same room in the same direction and vice versa.
    room_map = generate_map(initial_state)
    neighbours = [cond for cond in initial_state if cond[0] == "NextTo"]
    for item in room_map: #for room in world
        for jtem in neighbours: # for condition in all "NextTo" conditions
            if item == jtem[1]: # if the room is in the from location
                if coordinate_modifier(room_map[item],jtem[3]) != room_map[jtem[2]]:
                    raise SequenceMergeError("Invalid grid structure of the rooms.")
    return list(initial_state)

if __name__ == "__main__":
    """
    args:
    filename of input file
    followed by filename of output file 
    """
    filename = sys.argv[1]
    with open(filename, "r") as f:
        line = f.readline().strip()
        #capture goal state (line 1)
        goal_state = set([deconstruct_literal(literal) for literal in line.split(", ")])
        #for the remaining lines, each line is a sequence of actions to the goal state
        actions = []
        for line in f:
            line = line.strip()
            #capture actions from sequence
            actions.append([deconstruct_literal(action) for action in line.split(", ")])

    initial_states, used_actions = [], set()
    for sequence in actions:
        initial_states.append(backtrack(goal_state,sequence))
        for action in sequence:
            used_actions.add(all_actions[action[0]])
    #combine initial states from each sequence of actions
    initial_state = combine_states(initial_states)
    #increase the difficulty of the state    
    initial_state = complexify(initial_state, goal_state)
    #save the planning problem to a file with the name of the second filename given on command line
    print("Initial State:")
    print(initial_state)
    save_plan(list(initial_state),list(goal_state),list(all_actions.values()),sys.argv[2])
    visualise_map(generate_map(initial_state),get_unique_neighbours(initial_state))
    print("Plan has been saved to {0}".format(sys.argv[2]))
        
