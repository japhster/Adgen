# Text-based Adventure Game Generator (Adgen)

To generate a text-based adventure game world run generate_world.py with two arguments:
first argument: the name of the file that stores the goal state and action sequences
second argument: a name of the adventure that will be generated (used later to retrieve the game)

e.g. python generate_world.py input.txt adventure

To play the generated text-based adventure game run play.py with the name of the adventure you wish to play

e.g. python play.py adventure

To run the code Python 3 must be installed.
To view the visualisation of the generated map Pygame must also be installed.
See https://www.pygame.org/wiki/GettingStarted for instruction on how to install pygame

## Designing the adventure

To make the adventure you need to create the file that will describe what the goal state of the adventure is
(this could include being in a location, having an item, or making sure an item is in a particular room).
As well as this the file must contain the sequence of actions that are used to get from the start of the 
adventure (you can leave the start state unspecified) to the goal state.
A sequence of actions must take up only one line of the file and you may provide more that one action sequence,
provided all sequences take the player from the same starting point to the same ending point.
To get an idea of what the adventure looks like, have a look at the example given in the file "input.txt" and
for a full selection of the actions that can be used in the action sequence and what each action requires,
read the actions.py file.

