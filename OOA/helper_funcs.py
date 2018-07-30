

def reverse_direction(direction):
    return {"North":"South","South":"North","East":"West","West":"East"}[direction]
    
def get_coord_from_direction(coord,direction):
    modifier = {"North":(0,1),"South":(0,-1),"East":(1,0),"West":(-1,0)}[direction]
    return (coord[0]+modifier[0],coord[1]+modifier[1])
    
def get_direction_from_coords(c1,c2):
    direction = (c2[0]-c1[0],c2[1]-c1[1])
    try:
        return {(0,1):"North",(0,-1):"South",(1,0):"East",(-1,0):"West"}[direction]
    except KeyError:
        return None
        
        
if __name__ == "__main__":
    print(get_direction_from_coords((0,0),(1,0)))
    print(get_direction_from_coords((0,0),(2,0)))
