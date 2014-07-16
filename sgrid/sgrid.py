# /usr/bin/env python3

from sgrid.location import Location
from sgrid.player import Player
from sgrid.item import Item
import json
import sys

HEADING = \
"""\n*****This is a 2 location demo. You can only go north/south, look, look item, 
open item, close item, take item, take 'nestedItem' from 'containerItem',
inventory and quit. Not all items can be opened, or taken.*****\n"""

# Function to run the game
def run_game(player):
    print(HEADING)
    player.getCurrLoc().printFirst()
    while True:
        reply = input('\n>').lower().split(';') or ['']
        first = True
        for i in reply:
            if not first:
                print('\n>')
            rc = player.execprint(i)
            # Quit if execprint returns a 'quit' code.
            if (rc == -1):
                sys.exit(0) 
            first = False

    if __name__ == '__main__':
        input('\n>')

if __name__ == '__main__':
    # Test code
    twig = Item('twig', 'a nice sized twig', 'hmm... a twig',
                    ['wood', 'twig', 'stick'])
    berries = Item('berries', 'two small berries', 'two tiny berries', 
                    ['round', 'circles','berry', 'berries, balls'])

    undies = Item('undies', 'white undies', 'white undies with skid-marks', 
                    ['underwear', 'undies', 'boxers'], is_container = True)
    chest = Item('chest', 'an ornate chest', 'a beautiful crusty chest',
                    ['chest', 'box', 'container'], is_container = True, can_take = False, 
                    cannot_take_msg = "This thing is heavy. I ain't takin' it no where. ")
    sword = Item("sword", 'a small sword', 'a tiny sword made for tiny dudes',
                    ['sword', 'needle', 'prick', 'knife', 'dagger'])
    note = Item("note", 
        """The note says:
        Hi Dick,

        I hope you enjoyed playing with yourself.

        -Dick""",
        "This note looks familiar... it may warrant another inspection.",
        ['note', 'letter', 'message', 'paper'])
    
    undies.addInv(twig)
    undies.addInv(berries)
    chest.addInv(note)
    caveInv = [chest]
    clearingInv = [sword]

    Cave = Location('Cave', 
        'A dimly lit cave. You can see a clearing South of here.', 
        'This cave sucks.', caveInv)
    Clearing = Location('Clearing', 
        'This clearing looks stupid. It looks as if there is a cave North of here.', 
        'You are in an expansive clearing. It looks as if there is a cave North of here.', clearingInv)
    
    dungeon_map = {
    Clearing:  {'north': Cave},
    Cave: {'south': Clearing}
    }

    gameItems = {}
    hero = Player("Dick", "I am a detective with a phallic name.", 
        "Whoa, I can see myself.", Clearing, dungeon_map)
    hero.addInv(undies)

    # myVar = {'name':'Room 2', 'description':'a big ass ROOM.', 
    # 'firstDescription':'wow such big.'}
    # testFile = open("/home/brian/testfile", 'r')
    #testFile.write(json.dumps(myVar))

    # newVar = json.load(testFile)
    # testFile.close()
    # print(newVar)

    # Maybe can add a look self
    run_game(hero)
