from base import WorldPart

class Enemy(WorldPart):
    
    def __init__(self,name,species):
        """
        will fight the player
        player cannot proceed to the next room without defeating (or fleeing from) the enemy
        """
        super(Enemy,self).__init__(name)
        self.species = species
        
        
