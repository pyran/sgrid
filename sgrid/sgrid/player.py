# /usr/bin/env python3
from .gameobj import GameObj
from time import sleep

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

    def findObject(self, itemStr):
        """This function takes the string name of an item and searches
        through the current location and player inventory and returns the
        object.  If the object isn't found, then returns None."""
        mergedList = self.currLoc.getInv() + self.getInv()
        foundItem = False  # Keep track if item is found for player feedback
        # loop through merged list of player inventory and location inventory
        for item in mergedList:  # for every item object found
            # check if itemStr matches the item name or it's synonyms
            if (itemStr == item.getName()) or (itemStr in item.getSynonyms()):  
                foundItem = True  # if there is a match, then item found
                return item
        if not foundItem:  # give player feedback, if item wasn't found
            return None

    def simpleTake(self, args):
        "Private method for taking items directly from location inventory."
        itemStr = args[0]  # args[0] is the item string from user input
        # takes itemStr and returns the item if found, else returns None
        item = self.findObject(itemStr)
        if item:
            if item.checkCanTake(): # first check if item is takable
                # next check if the item is in the location inventory
                if item in self.currLoc.getInv(): 
                    self.addInv(item)  # first add item to player inv
                    self.currLoc.rmItem(item)  # then remove it from loc
                    print("I placed the {} into my inventory.".format(
                        item.getName()))
                elif item in self.getInv(): # if item already in inventory
                    print("I already have the {}.".format(itemStr))
            else:  # This means the item can't be taken, display message
                print(item.getCannotTakeMsg())                   
        else:  # give player feedback, if item wasn't found
            print("I don't see the {} here.".format(itemStr))

    def nestedTake(self, args):
        "Private method for taking an item from a container item's inventory."
        # Define the args and lists for readability
        nestedItemStr = args[0]
        preposition = args[1]
        containerItemStr = args[2]
        container = self.findObject(containerItemStr) # Find the container item
        if container: # if found object
            # Find nestedItem, by using search inventory function
            nestedItem = container.searchInventory(nestedItemStr)
            if nestedItem:
                if (preposition == 'from') or (preposition == 'in') or (preposition == 'on'):
                    self.addInv(nestedItem)
                    container.rmItem(nestedItem)
                    print("I took the {} from the {}".format(
                        nestedItem.getName(), container.getName()))
                else:
                    print("Uh... do you mean to take that 'from' something?")
            else:
                # If the nested item was not found in the container item...
                print("I didn't see the {} in the {}.".format(nestedItemStr, containerItemStr))
        # User feedback. If the container item in question was not found
        else:  # Didn't find container item (container == None)
            print("I didn't see the {} here.".format(containerItemStr))

    def take(self, args):
        # Local inventory + personal inventory
        if len(args) == 1:  # if a simple take; take directly from location
            self.simpleTake(args)
        # To take a nested item "Take subitem from item"
        elif len(args) > 2:
            self.nestedTake(args)
        else: # incomplete command
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
        itemStr = args[0]
        item = self.findObject(itemStr)
        if item:
            if item.checkIsContainer():
                item.open()
            else:
                print("You can't open that.")
        else:
            print("I don't see that here.")

    def close(self,args):
        itemStr = args[0]
        item = self.findObject(itemStr)
        if item:
            if item.checkIsContainer():
                item.close()
            else:
                print("You can't close that.")
        else: 
            print("I don't see that here.")

    def _quit(self, args):
        print("Thanks for playing.")
        return "quit game"

    def _save(self, args):
        return "save game"

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
        # can't use 'd' because of going down
        'inventory': self.inven, 'i': self.inven, 'items': self.inven, #'die': die,
        'quit': self._quit,
        'save': self._save,
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
            verb = line[0] # First item in line is usually the verb unless it's 'go'
            if verb not in verblist and verb != 'go':
                if len(line) > 1:
                    # second item following the verb is the game object
                    gameObject = self.findObject(line[1]) 
                    if gameObject:
                        gameObject.getEventManager().serve(line)
                    else:
                        print("I don't see {} here.".format(line[1]))
            elif verb == 'go':
                verb2 = line[1] # if the first verb is 'go' look to next argument
                if verb2 not in verblist:
                    print("I don't understand what you want me to go do.")
                else:
                    func = verblist[line[1]]
                    args = line[2:]
                    return func(args)
            else:
                func = verblist[line[0]]  # look for first word in verblist
                args = line[1:]  # What follows first word are arguments
                return func(args)  # use the arguments for the verb function

    # These are special player actions reserved for the event system and are not
    # included in the basic verb list above; they are optional

    def printText(self, textList, waitTime=0):
        """Function to print text to screen. Enter text as a list of paragraphs.
        The optional waitTime argument (seconds) allows display of text to be
        time delayed for dramatic effect. Use waitTime=0 for immediate."""
        for text in textList:
            print(text)
            sleep(waitTime)
            print("")


    # def combine(self):

    # def push(self):

    # def pull(self):

    # def sit(self):

    # def stand(self):

    # def crawl(self):


if __name__ == '__main__':
    # Test area
    print("Testing Player class")
