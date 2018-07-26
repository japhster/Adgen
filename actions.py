
from state_functions import reverse_direction

#("NextTo","Room1","Room2","east") defines that to get from Room1 to Room2 you must go east

all_actions = {
           "Move": (
                    ("Move", "From", "To", "DirectionFT", "DirectionTF"),
                    (("At","From"),("!At","To"),("NextTo","From","To","DirectionFT"),("NextTo","To","From","DirectionTF"),
                     ("!Lock","From","To"),("!Dark","To"),("!HiddenPath","To","From"),("!Occupied","From")),
                    (("At","To"),("!At","From"))
                   ),
           "Unlock": (
                      ("Unlock","Current","Neighbour","Direction","Key"),
                      (("At","Current"), ("!At","Neighbour"), ("NextTo","Current","Neighbour","Direction"), ("Has","Key"),
                       ("Lock","Current","Neighbour"), ("Lock","Neighbour","Current"),("LockNeeds","Neighbour","Current","Key"),
                       ("LockNeeds","Current","Neighbour","Key")),
                      (("!Lock","Current","Neighbour"), ("!Lock","Neighbour","Current"),("!LockNeeds","Neighbour","Current","Key"),
                       ("!LockNeeds","Current","Neighbour","Key"))
                     ),
           "Take": (
                    ("Take","Item","Room"),
                    (("At","Room"), ("In","Item","Room"),("!Has","Item"),("Takeable","Item")),
                    (("Has","Item"), ("!In","Item","Room"))
                   ),
           "Drop": (
                    ("Drop","Item","Room"),
                    (("At","Room"),("Has","Item"),("!In","Item","Room")),
                    (("!Has","Item"),("In","Item","Room"))
                   ),
           "Open": (
                    ("Open","Container","Item"),
                    (("Has","Container"),("Openable","Container"),("Contains","Container","Item"),("!Has","Item")),
                    (("!Has","Container"),("Has","Item"))
                   ),
           "ClearDarkness": (
                             ("ClearDarkness","From","To","DirectionFT","DirectionTF","Item"),
                             (("Has","Item"),("At","From"),("Purpose","Item","Light"),("Dark","To"),
                             ("NextTo","From","To","DirectionFT"),("NextTo","To","From","DirectionTF"),("!Lock","From","To"),
                             ("!Lock","To","From")),
                             (("!Dark","To"),)
                            ),
           "Talk": (
                    ("Talk","Person","PersonLocation","Room1","Room2","Direction12","Direction21"),
                    (("Knows","Person","Room1"), ("Knows","Person","Room2"),("HiddenPath","Room1","Room2"),
                     ("HiddenPath","Room2","Room1"),("In","Person","PersonLocation"),("At","PersonLocation"),
                     ("NextTo","Room1","Room2","Direction12"),("NextTo","Room2","Room1","Direction21")),
                    (("!HiddenPath","Room1","Room2"),("!HiddenPath","Room2","Room1"))
                   ),
           "CheatGain": (
                         ("CheatGain","Item"),
                         (("!Has","Item"),),
                         (("Has","Item"),)
                        ),
           "Fight": (
                     ("Fight","Monster","MonsterLocation","Weapon"),
                     (("At","MonsterLocation"),("Enemy","Monster"),("In","Monster","MonsterLocation"),("Has","Weapon"),
                     ("Purpose","Weapon","Fighting"),("Occupied","MonsterLocation")),
                     (("!In","Monster","MonsterLocation"),("!Occupied","MonsterLocation"))
                    ),
                     
          }
          
class Action(object):

    def __init__(self,state,name):
        self.state = state
        self.name = name.title()
        self.current_location = [item[1] for item in self.state if item[0] == "At"][0]
                
    def get_direction(self, room1, room2):
        for item in self.state:
            if item[0] == "NextTo" and item[1] == self.current_location and item[2] == self.room:
                return item[3]
                       
    def get_room(self):
        for item in self.state:
            if item[0] == "NextTo" and item[1] == self.current_location and item[3] == self.direction:
                return item[2]
            

class Move(Action):

    def __init__(self, state, name, direction):
        super(Move,self).__init__(state,"Move")
        self.direction = direction.title()
        self.action = (self.name, self.current_location,self.get_To(),self.direction,reverse_direction(self.direction))        
    
    def get_To(self):
        for item in self.state:
            if item[0] == "NextTo" and item[1] == self.current_location and item[3] == self.direction:
                return item[2]
                
                
class Unlock(Action):
    
    def __init__(self, state, name, direction, key):
        super(Unlock,self).__init__(state,"Unlock")
        self.direction = direction.title()
        self.room = self.get_room()
        self.key = key
        self.action = (self.name, self.current_location, self.room, self.direction,
                       self.key)
                
class Take(Action):
    
    def __init__(self, state, name, item):
        super(Take,self).__init__(state,"Take")
        self.item = item
        self.action = (self.name, self.item, self.current_location)
        
class Drop(Action):

    def __init__(self, state, name, item):
        super(Drop,self).__init__(state,"Drop")
        self.item = item
        self.action = (self.name, self.item, self.current_location)
        
class Open(Action):

    def __init__(self, state, name, container):
        super(Open,self).__init__(state,"Open")
        self.container = container.title()
        self.action = (self.name, self.container, self.get_item())
        
    def get_item(self):
        for item in self.state:
            if item[0] == "Contains" and item[1] == self.container:
                return item[2]
                
class ClearDarkness(Action):
    
    def __init__(self, state, name, direction, item):
        super(ClearDarkness,self).__init__(state,"irrelevant")
        self.name = "ClearDarkness"
        self.direction = direction.title()
        self.room_from = self.current_location
        self.room_to = self.get_room()
        self.item = item.title()
        self.action = (self.name, self.room_from, self.room_to, self.direction, reverse_direction(self.direction), self.item)


class Talk(Action):

    def __init__(self, state, name, person):
        super(Talk,self).__init__(state,"Talk")
        self.person = person
        self.person_knows = self.get_person_knows()
        self.direction = self.get_direction(self.person_knows[0], self.person_knows[1])
        self.action = (self.name, self.person, self.current_location, self.person_knows[0], self.person_knows[1],
                            self.direction, reverse_direction(self.direction))
                            
    
    def get_person_knows(self):
        person_knows = []
        for item in self.state:
            if item[0] == "Knows" and item[1] == self.person:
                person_knows.append(item[2])
        
            if len(person_knows) == 2:
               return person_knows

        
class Fight(Action):
    
    def __init__(self, state, name, monster):
        super(Fight,self).__init__(state,"Fight")
        self.monster = monster
        self.action = (self.name,self.monster,self.current_location,self.get_weapon())
        
    def get_weapon(self):
        for item in self.state:
            if item[0] == "Has" and  ("Purpose",item[1],"Fighting") in self.state:
                return item[1]
            
        
class CheatGain(Action):
    
    def __init__(self, state, name, item):
        super(CheatGain,self).__init__(state,"irrelevant")
        self.name = "CheatGain"
        self.item = item
        self.action = (self.name, self.item)


actions = {
           "move":Move,
           "clear darkness": ClearDarkness,
           "unlock": Unlock,
           "take": Take,
           "drop": Drop,
           "open": Open,
           "talk": Talk,
           "fight": Fight,
           "cheat gain": CheatGain,
          }

commands = {
            "move": ["move","go"],
            "clear darkness": ["cleardarkness","clear darkness","light","shine"],
            "unlock": ["unlock"],
            "take": ["take","pick up","get","acquire"],
            "drop": ["drop","let go of"],
            "open": ["open","smash","break"],
            "talk": ["talk","speak"],
            "fight": ["fight","attack","kill"],
           }
           
commands["cheat gain"] = ["reach into the nethersphere and receive"]

requirements = {
                "move": ["direction"],
                "unlock": ["direction","key"],
                "take": ["item"],
                "drop": ["item"],
                "open": ["container"],
                "clear darkness": ["direction","item"],
                "talk": ["person"],
                "fight": ["monster"],
                "cheat gain": ["item"],
               }

if __name__ == "__main__":
    print(all_actions["ClearDarkness"])






















