#! /usr/bin/env python3

from .events import EventManager 

# Classes for the game
class GameObj(object):
    """This parent class contains the descriptions and inventory methods that
    we plan to use for all subclasses

    name = a short name or description of the object, item, player, or location
    description = more detailed summary description
    first_description = first encounter description, can be funny or more
    elaborate. This distinction was made because it might be annoying to read
    the same joke over and over."""

    def __init__(self, name, description, first_description):
        self.name = name
        self.desc = description
        self.firstDesc = first_description
        self.inventory = []
        self.visible = True
        self.seen = False
        self.eventManager = EventManager()

    def getEventManager(self):
        return self.eventManager

    def getName(self):
        return self.name

    def printDesc(self):
        extraDesc = ""
        count = 0
        invSize = len(self.getInv())
        if invSize > 0:
            extraDesc = "  I see "
            for item in self.getInv():
                extraDesc += item.desc
                if (count == (invSize - 2)):
                    extraDesc += ", and "
                elif (count < (invSize - 1)):
                    extraDesc += ", "
                count += 1
            extraDesc += "."

        if (self.seen):
        # If the player has been here before, print the normal description.
            print(self.desc + extraDesc)
        else:
        # If the player hasn't been here before, give them the first description.
            print (self.firstDesc + extraDesc)
            self.seen = True

    def printFirst(self):
        print(self.firstDesc)

    def addInv(self, item):
        self.inventory.append(item)

    def rmItem(self, item):
        try:
            self.inventory.remove(item)
        except:
            print("You do not have that item")

    def getInv(self):
        return self.inventory

    def checkVisible(self):
        """Checks to see if game object is visible to player"""
        return self.visible

    def setVisible(self):
        """Set game object visible to player"""
        self.visible = True

    def setInvisible(self):
        """Set game object as invisible to player."""
        self.visible = False

    def checkSeen(self):
        """Checks to see if the item/location/player has been seen by the user before"""
        return self.seen

    def hasSeen(self):
        """Marks the location/item as seen"""
        self.seen = True

if __name__ == '__main__':
    # Test area
    print("Testing GameObj class")
