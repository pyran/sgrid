# /usr/bin/env python3
from .gameobj import GameObj

class Player(GameObj):
    """This class contains all the movement, current location and action
    functions for the player"""
    def __init__(self, name, description, first_description,
                 current_location, dungeon_map):
        super().__init__(name, description, first_description)
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


if __name__ == '__main__':
    # Test area
    print("Testing Player class")
