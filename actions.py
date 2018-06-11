#("NextTo","Room1","Room2","east") defines that to get from Room1 to Room2 you must go east

all_actions = {
           "MoveEast": (
                    ("MoveEast", "From", "To"),
                    (("At","From"),("!At","To"),("NextTo","From","To","east"),("NextTo","To","From","west"),("!Lock","From","To"),
                     ("!Dark","To"),("!HiddenPath","To","From")),
                    (("At","To"),("!At","From"))
                   ),
           "MoveWest": (
                    ("MoveWest", "From", "To"),
                    (("At","From"),("!At","To"),("NextTo","From","To","west"),("NextTo","To","From","east"),("!Lock","From","To"),
                     ("!Dark","To"),("!HiddenPath","To","From")),
                    (("At","To"),("!At","From"))
                   ),
           "MoveNorth": (
                    ("MoveNorth", "From", "To"),
                    (("At","From"),("!At","To"),("NextTo","From","To","north"),("NextTo","To","From","south"),("!Lock","From","To"),
                     ("!Dark","To"),("!HiddenPath","To","From")),
                    (("At","To"),("!At","From"))
                   ),
           "MoveSouth": (
                    ("MoveSouth", "From", "To"),
                    (("At","From"),("!At","To"),("NextTo","From","To","south"),("NextTo","To","From","north"),("!Lock","From","To"),
                     ("!Dark","To"),("!HiddenPath","To","From")),
                    (("At","To"),("!At","From"))
                   ),
           "Unlock": (
                      ("Unlock","Current","Neighbour","Direction"),
                      (("At","Current"), ("!At","Neighbour"), ("NextTo","Current","Neighbour","Direction"), ("Has","Key"),
                       ("Lock","Current","Neighbour"), ("Lock","Neighbour","Current")),
                      (("!Lock","Current","Neighbour"), ("!Lock","Neighbour","Current"))
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
                             (("!Dark","Room"),)
                            ),
           "Talk": (
                    ("Talk","Person","PersonLocation","Room1","Room2","Direction12","Direction21"),
                    (("Knows","Person","Room1"), ("Knows","Person","Room2"),("HiddenPath","Room1","Room2"),
                     ("HiddenPath","Room2","Room1"),("In","Person","PersonLocation"),("At","PersonLocation"),
                     ("NextTo","Room1","Room2","Direction12"),("NextTo","Room2","Room1","Direction21")),
                    (("!HiddenPath","Room1","Room2"),("!HiddenPath","Room2","Room1"))
                   ),
          }
          
          
if __name__ == "__main__":
    print(all_actions["ClearDarkness"])
