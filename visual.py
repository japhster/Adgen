import pygame

def visualise_map(room_map,neighbours):
    stop = False
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("monospace",15)
    screen = pygame.display.set_mode((1000,1000))
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
    
    #display the world until either escape is pressed or the window is closed
    while not stop:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
                stop = True

    
if __name__ == "__main__":
    room_map = {'Room7': (1, -2), 'Room2': (0, -1), 'Library': (0, 0), 'Room5': (1, 1), 'Room8': (0, -2), 'Room3': (2, 0),
                'Office': (0, 1), 'Room6': (-2, -1), 'Room11': (-1, 0), 'Room1': (1, -1), 'Room10': (3, 0), 'Room9': (1, 2),
                'Kitchen': (1, 0), 'Room4': (-1, -1)}
    neighbours = set([('Kitchen', 'Library', "West"), ('Room1', 'Kitchen', "North"), ('Room3', 'Kitchen', "West"),
                     ('Room4', 'Room2', "East"), ('Room10', 'Room3', "West"), ('Room11', 'Library', "East"),
                     ('Room6', 'Room4', "East"), ('Room7', 'Room1', "North"), ('Room11', 'Room4', "South"),
                     ('Room9', 'Room5', "South"), ('Room8', 'Room7', "East"), ('Room2', 'Library', "North"),
                     ('Room5', 'Kitchen', "South"), ('Library', 'Office', "North"), ('Room8', 'Room2', "North"),
                     ('Room2', 'Room1', "East"), ('Room5', 'Office', "West")])

    visualise_map(room_map,neighbours)
    """
    room_map = {"Room1": (0,0),"Room2": (0,1)}
    neighbours = set([("Room1", "Room2", "north")])
    visualise_map(room_map,neighbours)
    """
