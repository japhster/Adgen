from actions import all_actions

def print_actions(actions, filename):
    """
    action will be a list of tuples defining, input variables, precondtions, postconditions
    e.g.
    [("Move", "From", "To"), [("At","From"),("!At","From"),("Neighbour","From","To"),("!Lock","From","To")],[("At","To"),("!At","From")]]
    should output in the form:
    Move(From, To)
    Preconditions: At(From), !At(To)
    Postconditions: At(To), !At(From)    
    """
    with open(filename, "a") as f:
        f.write("\nActions:\n\n")
        for action in actions:
            #print action name and input variables
            f.write(format_literal(action[0]) + "\n")
            #print preconditions and postconditions
            titles = ["Preconditions:", "Postconditions:"]
            for title in titles:
                f.write(title)
                items = action[titles.index(title) + 1] #either items from preconditions or postconditions
                for item in items: #e.g. ("At","From") first iteration or ("At","To") second iteration
                    f.write(format_literal(item) + "," if last_item(item,items) else format_literal(item))
                f.write("\n")
            f.write("\n")
            
def format_literal(var):
    """
    takes in a tuple and returns it's proper form
    e.g.
    ("Move", "From", "To")
    will return:
    "Move(From, To)"
    """
    return_var = var[0] + "("
    for item in var[1:]:
        return_var += item+"," if last_item(item,var[1:]) else item
        
    return return_var + ")"
        
def last_item(item, group):
    return group.index(item) != len(group) -1

def concatenate_literals(items):
    return_string = ""
    for item in items:
        return_string += format_literal(item) + "," if last_item(item,items) else format_literal(item)
    return return_string
        
        
def save_plan(initial, goal, actions, filename):
    with open(filename, "w") as f:
        #print the initial state of the game world
        f.write("Initial state: ")
        f.write(concatenate_literals(initial) + "\n")
        #print the goal state of the game world
        f.write("Goal state: ")
        f.write(concatenate_literals(goal) + "\n")     
    #print the actions of the game world
    print_actions(actions, filename)
        
if __name__ == "__main__":
    initial = [("At","Room1"), ("NextTo","Room1","Room2"), ("NextTo","Room2","Room1"), ("Lock","Room1","Room2"), ("Lock","Room2","Room1"), ("In","Key","Room1")]
    goal = [("At","Room2")]
    actions = [all_actions["Move"], all_actions["Take"], all_actions["Unlock"]]
    save_plan(initial,goal,actions,"testing.txt")
    visualise_map(generate_map(state))
