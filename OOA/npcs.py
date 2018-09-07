from base import WorldPart

class NPC(WorldPart):

    def __init__(self,name,category="NPC"):
        super(NPC,self).__init__(name)
        self.name = name
        self.category = category
        
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.__str__()


class Merchant(NPC):

    def __init__(self,name):
        """
        can sell wares to the player for a price
        can also purchase items from the player for a reduced price
        """
        super(Merchant,self).__init__(name,"Merchant")
        self.wares = []

    def talk(self):
        pass
        
        
class Traveller(NPC):

    def __init__(self,name,knowledge):
        """
        knows a secret passage between two adjacent rooms yet to be discovered by the player
        """
        super(Traveller,self).__init__(name,"Traveller")
        self.knowledge = tuple(knowledge) #a tuple of two rooms that are connected
        
    def talk(self):
        """returns the traveller's knowledge"""
        print("I know a shortcut between The {0} and The {1}, I'll show you on your map".format(self.knowledge[0],self.knowledge[1]))
        
        return self.knowledge
        
    def get_save_info(self):
        return [self.category,self.name,self.knowledge]
        
