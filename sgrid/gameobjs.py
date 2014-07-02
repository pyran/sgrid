# /usr/bin/env python3

# Classes for the game
class GameObj(object):
    """This parent class contains the descriptions and inventory methods that
    we plan to use for all subclasses

    name = a short name or description of the object, item, player, or location
    long_description = more detailed summary description
    first_description = first encounter description, can be funny or more
    elaborate. This distinction was made because it might be annoying to read
    the same joke over and over."""

    def __init__(self, name, long_description, first_description):
        self.name = name
        self.longDesc = long_description
        self.firstDesc = first_description
        self.inventory = []
        self.seen = False

    def getName(self):
        return self.name

    def printLong(self):
        print(self.longDesc)

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


    def checkSeen(self):
        return self.seen

    def hasSeen(self):
        self.seen = True


class Location(GameObj):
    """This class will hold a location object which will represent one room in 
    the dungeon map.  It will include an additional adjacent location dictionary
    that will be used to form a graph based game map."""

    def __init__(self, name, long_description, first_description):
        GameObj.__init__(self, name, long_description, first_description)
        self.access = True
        self.blockedMsg = ""
        self.unblockedMsg = ""


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
    def __init__(self, name, long_description, first_description):
        GameObj.__init__(self, name, long_description, first_description)
        self.combine = []


class Player(GameObj):
    """This class contains all the movement, current location and action
    functions for the player"""
    def __init__(self, name, long_description, first_description,
                 current_location, dungeon_map):
        GameObj.__init__(self, name, long_description, first_description)
        self.currLoc = current_location
        self.dmap = dungeon_map

    def describeLoc(self):
        """Check if the new current location has been visited, if False,
        then show first description, else show long description"""
        if self.currLoc.checkSeen() == False:
            self.currLoc.printFirst()
            self.currLoc.hasSeen()
        else:
            self.currLoc.printLong()

    # def describeItem(self, item):
    #     """Check if the new item has been seen, if False,
    #     then show first description, else show long description"""
    #     if self.currLoc.checkSeen() == False:
    #         self.currLoc.printFirst()
    #         self.currLoc.hasSeen()
    #     else:
    #         self.currLoc.printLong()

    def examine(self, args):
        """This function allows the player to look at his surroundings
        and items (soon)"""
        if not args:  # a plain look should describe the room/location
            self.describeLoc()
        # elif args[0] not in self.currLoc.getInv():
        #     print("I'm not sure what to look at...")
        else:
            print("I can't look at items yet... D:")

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
                self.currLoc.printFirst()
                self.currLoc.hasSeen()

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

    def execprint(self, user_input):
        """This master function parses the user input, and passes the commands
        to their respective action and movement functions that the player can
        perform"""
        verblist = {
        # 'take': take, 'get': take, 'pick': take, 'hold': take,
        # 'drop': drop, 'throw': drop, 'toss': drop,
        'look': self.examine, 'l': self.examine, 'examine': self.examine,
        'x': self.examine, 'read': self.examine, 'r': self.examine,
        'describe': self.examine,
        # 'combine': combine, 'use': combine,
        # can't use 'd' because of going down
        # 'inventory': inven, 'i': inven, 'items': inven, #'die': die,
        # 'quit': _quit,
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