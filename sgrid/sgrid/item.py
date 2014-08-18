# /usr/bin/env python3
from .gameobj import GameObj

class Item(GameObj):
    """This class is for handling Items in the game"""
    def __init__(self, name, description, first_description, synonyms=[], 
                is_container = False, can_take = True, cannot_take_msg =""):
        super().__init__(name, description, first_description)
        self.synonyms = synonyms
        self.isContainer = is_container
        self.combine = []
        self.isOpened = False
        self.canTake = can_take
        self.cannotTakeMsg = cannot_take_msg

    def getSynonyms(self):
        return self.synonyms

    def printDesc(self):
        extraDesc = ""
        if (self.isOpened):
            invSize = len(self.getInv())
            if invSize > 0:
                extraDesc = " has:\n"
                for index, item in enumerate(self.getInv()):
                    extraDesc += "{}. {}\n".format(index+1, item.getName())
                #extraDesc += "."

        if (self.seen):
        # If the player has been here before, print the normal description.
            print(self.desc + extraDesc)
        else:
        # If the player hasn't been here before, give them the first description.
            print (self.firstDesc + extraDesc)
            self.seen = True

    def checkIsContainer(self):
        return self.isContainer

    def open(self):
        if self.isOpened:
            print("It's already been opened.")
        else:    
            self.isOpened = True
            print("It's open.")

    def close(self):
        if not self.isOpened:
            print("It's already closed.")
        else:
            self.isOpened = False
            print("It's closed.")
    
    def checkCanTake(self):
        return self.canTake

    def getCannotTakeMsg(self):
        return self.cannotTakeMsg

    
if __name__ == '__main__':
    # Test area
    print("Testing Item class")
