# /usr/bin/env python3
from .gameobj import GameObj

class Location(GameObj):
    """This class will hold a location object which will represent one room in 
    the dungeon map.  It will include an additional adjacent location dictionary
    that will be used to form a graph based game map."""

    def __init__(self, name, description, first_description, inventory = None, 
                    access = True, blocked_msg = "", 
                    unblocked_msg = ""):

        super().__init__(name, description, first_description)
        self.access = access
        self.inventory = inventory
        self.blockedMsg = blocked_msg
        self.unblockedMsg = unblocked_msg

    def blockLoc(self, blockedMsg):
        """If you want to block a player from entering a location"""
        self.access = False
        self.blockedMsg = blockedMsg

    def rmBlock(self):
        """Removing the block from the location"""
        self.access = True
        self.blockedMsg = ""

if __name__ == '__main__':
    # Test area
    print("Testing Location class")
