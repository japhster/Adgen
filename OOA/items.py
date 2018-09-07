from base import WorldPart

class Item(WorldPart):

    def __init__(self,name,category="Item"):
        self.category = category
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Lightsource(Item):

    def __init__(self,name):
        super(Lightsource,self).__init__(name,"Lightsource")
        self.on = False
        
    def light(self):
        self.on = True


class Key(Item):

    def __init__(self,name):
        super(Key,self).__init__(name,"Key")


class Container(Item):
    
    def __init__(self,name,contents):
        super(Container,self).__init__(name,"Container")
        self.contents = contents #an item object that is in the container

    def open(self):
        return self.contents


class Money(Item):

    def __init__(self,name,value):
        super(Money,self).__init__(name,"Money")
        self.value = value

