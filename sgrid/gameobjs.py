# /usr/bin/env python3

import sys

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

    def isVisible(self):
        """Set game object visible to player"""
        self.visible = True

    def invisible(self):
        """Set game object as invisible to player."""

    def checkSeen(self):
        """Checks to see if the item/location/player has been seen by the user before"""
        return self.seen

    def hasSeen(self):
        """Marks the location/item as seen"""
        self.seen = True


class Location(GameObj):
    """This class will hold a location object which will represent one room in 
    the dungeon map.  It will include an additional adjacent location dictionary
    that will be used to form a graph based game map."""

    def __init__(self, name, description, first_description, inventory, 
                    access = True, blocked_msg = "", 
                    unblocked_msg = ""):

        GameObj.__init__(self, name, description, first_description)
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


class Item(GameObj):
    """This class is for handling Items in the game"""
    def __init__(self, name, description, first_description, synonyms=[], 
                is_container = False, can_take = True, cannot_take_msg =""):
        GameObj.__init__(self, name, description, first_description)
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

    def checkContainer(self):
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


class Player(GameObj):
    """This class contains all the movement, current location and action
    functions for the player"""
    def __init__(self, name, description, first_description,
                 current_location, dungeon_map):
        GameObj.__init__(self, name, description, first_description)
        self.currLoc = current_location
        self.dmap = dungeon_map

    def describeLoc(self):
        """Check if the new current location has been visited, if False,
        then show first description, else show long description"""
        self.currLoc.printDesc()

    def describeSelf(self):
        if not self.checkSeen():
            self.printFirst()
            self.hasSeen()
        else:
            self.printDesc()

    def describeItem(self, arg):
        """Check if the new item has been seen, if False,
        then show first description, else show long description"""
        # combine the scope of the current location and your inventory
        mergedList = self.currLoc.getInv() + self.getInv()

        for item in mergedList:
            if arg in item.getSynonyms():
                item.printDesc()
                break # breaking out of loop skips the loops else statemnt **
            
        else:  # ** this one is skipped when breaking
            print("I don't see that here.")


    def examine(self, args):
        """This function allows the player to look at his surroundings
        and items (soon)"""
        if not args:  # a plain look should describe the room/location
            self.describeLoc()
        # elif(args[0] in ["in", "on"]):
        #     self.describeItem(args[1])

        elif(args[0] in ['me', 'self', self.getName()]):
            self.describeSelf()
        else:
            self.describeItem(args[0])

    def take(self, args):
        mergedList = self.currLoc.getInv() + self.getInv()
        if len(args) == 1:  # if a simple take item command
            foundItem = False
            for item in mergedList:
                if args[0] in item.getSynonyms():
                    foundItem = True
                    if item.checkCanTake():
                        if item in self.currLoc.getInv():
                            self.addInv(item)
                            self.currLoc.rmItem(item)
                            print("I placed the {} into my inventory.".format(
                                item.getName()))
                        elif item in self.getInv():
                            print("I already have the {}.".format(args[0]))
                        break
                    else:
                        print(item.getCannotTakeMsg())
                        
            if not foundItem:
                print("I don't see the {} here.".format(args[0]))
        # To take a nested item "Take subitem from item"
        elif len(args) > 2:
            foundItem = False
            foundSubitem = False
            for item in mergedList:
                if args[2] in item.getSynonyms():
                    foundItem = True
                    for subitem in item.getInv():
                        if args[0] in subitem.getSynonyms():
                            foundSubitem = True
                            if args[1] == 'from' or args[1] == 'in' or args[1] == 'on':
                                if args[2] in item.getSynonyms():
                                    self.addInv(subitem)
                                    item.rmItem(subitem)
                                    print("I took the {} from the {}".format(
                                        subitem.getName(), item.getName()))
                            else:
                                print("Uh... do you mean to take that 'from' something?")

            if not foundItem:
                print("I didn't see the {} here.".format(args[2]))
            if not foundSubitem and foundItem:
                print("I didn't see the {} in the {}.".format(args[0], args[2]))
        else:
            print("I don't understand. What do I need to take from?")

    def inven(self, args):
        print("I have:")
        if len(self.getInv()) < 1:
            print("...nothing...")
        else:
            for index, item in enumerate(self.getInv()):
                print("{}. {}".format(index+1, item.getName()))
                if item.isOpened:
                    subInv = item.getInv()
                    for subItem in subInv:
                        print("   - {}".format(subItem.getName()))

    # Functions related to movement
    def getCurrLoc(self):
        """Grabs current location of the player"""
        return self.currLoc

    def chgCurrLoc(self, dir):
        """Function to change current location to the new location."""
        curr = self.getCurrLoc()
        newLoc = self.dmap[curr][dir]
        self.currLoc = newLoc

    def move(self, dir):
        """function used to direct play to new locations on dungeon map."""
        if dir not in self.dmap[self.getCurrLoc()]:
            print("I can't go that way.")
        # elif newsect > 99:
        # # send this special value to decode function
        #     special_move(newsect)
        else:
            # Change to the new location
            self.chgCurrLoc(dir)
            print("I moved {} into {}.".format(dir, self.currLoc.getName()))
            if self.currLoc.checkSeen() == False:
                self.currLoc.printDesc()

    def north(self, args):
        self.move('north')

    def south(self, args):
        self.move('south')

    def east(self, args):
        self.move('east')

    def west(self, args):
        self.move('west')

    def northeast(self, args):
        self.move('northeast')

    def northwest(self, args):
        self.move('northwest')

    def southeast(self, args):
        self.move('southeast')

    def southwest(self, args):
        self.move('southwest')

    def up(self, args):
        self.move('up')

    def down(self, args):
        self.move('down')

    def _in(self, args):
        # 'in' is a delimeter, and cannot be used as a funcname without entailing
        # invalid syntax
        self.move('in')

    def out(self, args):
        self.move('out')

    def open(self, args):
        # TODO: Check for usage
        # combine the scope of the current location and your inventory
        mergedList = self.currLoc.getInv() + self.getInv()

        for item in mergedList:
            if args[0] in item.getSynonyms():
                if item.checkContainer():
                    item.open()
                else:
                    print("You can't open that.")
                break # breaking out of loop skips the loops else statemnt
            
        else:  # ** this one is skipped when breaking
            print("I don't see that here.")

    def close(self,args):
        # TODO: Check for usage
        # combine the scope of the current location and your inventory
        mergedList = self.currLoc.getInv() + self.getInv()

        for item in mergedList:
            if args[0] in item.getSynonyms():
                if item.checkContainer():
                    item.close()
                else:
                    print("You can't close that.")
                break # breaking out of loop skips the loops else statemnt **
            
        else:  # ** this one is skipped when breaking
            print("I don't see that here.")

    def _quit(self, args):
        print("Thanks for playing.")
        return sys.exit(0)

    def execprint(self, user_input):
        """This master function parses the user input, and passes the commands
        to their respective action and movement functions that the player can
        perform"""
        verblist = {
        'take': self.take, 'get': self.take, 'pick': self.take, 
        'hold': self.take,
        # 'drop': drop, 'throw': drop, 'toss': drop,
        'look': self.examine, 'l': self.examine, 'examine': self.examine,
        'x': self.examine, 'read': self.examine, 'r': self.examine,
        'describe': self.examine,
        # 'combine': combine, 'use': combine,
        # can't use 'd' because of going down
        'inventory': self.inven, 'i': self.inven, 'items': self.inven, #'die': die,
        'quit': self._quit,
        # 'help': _help,
        # 'save': save, 'restore': restore,
        'north': self.north, 'n': self.north,
        'south': self.south, 's': self.south,
        'east': self.east, 'e': self.east,
        'west': self.west, 'w': self.west,
        'northeast': self.northeast, 'ne': self.northeast,
        'southeast': self.southeast, 'se': self.southeast,
        'northwest': self.northwest, 'nw': self.northwest,
        'southwest': self.southwest, 'sw': self.southwest,
        'up': self.up, 'u': self.up,
        'down': self.down, 'd': self.down,
        'in': self._in, 'on': self._in, 'enter': self._in,
        'out': self.out,'off': self.out,  'exit': self.out,
        'open': self.open, 'close': self.close,
        }

        line = user_input.split()
        for c in ',:':
            line = c.join(line).split(
                c)  # Also, get rid of `c` that's been there first
        if line:
            if line[0] not in verblist and line[0] != 'go':
                print("I don't understand that.")
            elif line[0] == 'go':
                if line[1] not in verblist:
                    print("I don't understand what you want me to go do.")
                else:
                    func = verblist[line[1]]
                    args = line[2:]
                    func(args)
            else:
                func = verblist[line[0]]  # look for first word in verblist
                args = line[1:]  # What follows first word are arguments
                func(args)  # use the arguments for the verb function


#if __name__ == '__main__':
    # Test area