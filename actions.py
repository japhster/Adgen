from complexify import reverse_direction

#("NextTo","Room1","Room2","east") defines that to get from Room1 to Room2 you must go east

all_actions = {
           "Move": (
                    ("Move", "From", "To", "DirectionFT", "DirectionTF"),
                    (("At","From"),("!At","To"),("NextTo","From","To","DirectionFT"),("NextTo","To","From","DirectionTF"),
                     ("!Lock","From","To"),
                     ("!Dark","To"),("!HiddenPath","To","From")),
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
                    (("At","Room"), ("In","Item","Room"),("!Has","Item")),
                    (("Has","Item"), ("!In","Item","Room"))
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
          }
          
          

class Move(object):

    def __init__(self,state,direction):
        self.name = "Move"
        self.direction = direction
        self.required = {"From":self.get_from(state),"To":self.get_To(state),"DirectionFT":direction,"DirectionTF":reverse_direction(direction)}        
    
    def get_from(state):
        for item in state:
            if item[0] == "At":
                return item[1]
    
    def get_To(state):
        for item in state:
            if item[0] == "NextTo" and item[1] == get_from(state) and item[3] == self.direction:
                return item[2]
          
if __name__ == "__main__":
    print(all_actions["ClearDarkness"])
