import pygame
import sys

from state_functions import generate_map, get_unique_neighbours,format_state

def visualise_map(room_map,neighbours,gamename):
    stop = False
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("monospace",15)
    screen = pygame.display.set_mode((500,500))
    screen.fill((255,255,255))
    #get the minimum values of x and y
    min_x, min_y = min([i[0] for i in room_map.values()]), min([i[1] for i in room_map.values()])
    #change all coordinates so that they are all positive
    coordinates = {}
    for room,coord in room_map.items():
        coordinates[room] = (coord[0]-min_x,coord[1]-min_y)
    #calculate how big each section in the grid is and what multipler is required to convert a room coordinate to its screen coord
    max_x, max_y = max([i[0] for i in coordinates.values()]), max([i[1] for i in coordinates.values()])
    multiplier_x, multiplier_y = 500/(max_x+1), 500/(max_y+1)
    center_offset = (multiplier_x/2,multiplier_y/2)
    x,y = 0,0
    #draw out the grid
    while x < 500:
        pygame.draw.line(screen, (0,0,0), (x,0),(x,500),10)
        x += multiplier_x
    while y < 500:
        pygame.draw.line(screen, (0,0,0), (0,y),(500,y),10)
        y += multiplier_y
    #place all labels onto the grid in their places
    for room,coord in coordinates.items():
        label = font.render(room,1,(0,0,0))
        size = font.size(room)
        adj = (size[0]/2,size[1]/2)
        x,y = (coord[0]*multiplier_x+center_offset[0], coord[1]*multiplier_y+center_offset[1])
        screen.blit(label,(x-adj[0],500-(y-adj[1])))
    #black out any unused squares
    for i in range(max_x+1):
        for j in range(max_y+1):
            if (i,j) not in coordinates.values():
                pygame.draw.rect(screen,(0,0,0),(i*multiplier_x,500-(j*multiplier_y),multiplier_x,-multiplier_y))
    #draw a line to represent doors
    for room1,room2,direction in neighbours:
        start = coordinates[room1]
        end = coordinates[room2]
        multipliers = {"East":(1.8,1,0.2,1),"West":(0.2,1,1.8,1),"North":(1,1.8,1,0.2),"South":(1,0.2,1,1.8)}[direction]
        world_start = (start[0]*multiplier_x+center_offset[0]*multipliers[0],500-(start[1]*multiplier_y+center_offset[1]*multipliers[1]))
        world_end = (end[0]*multiplier_x+center_offset[0]*multipliers[2],500-(end[1]*multiplier_y+center_offset[1]*multipliers[3]))
        pygame.draw.line(screen, (0,0,0), world_start, world_end, 10)
    
    pygame.image.save(screen, "Games/" + gamename + "/map.jpeg")
    #display the world until either escape is pressed or the window is closed
    while not stop:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
                stop = True

    
if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        #get first line (remove "initial state: " and split into a list of literals
        initial_state = format_state(f.readline().strip(), "Initial state: ")
        visualise_map(generate_map(initial_state), get_unique_neighbours(initial_state))
