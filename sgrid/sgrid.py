# /usr/bin/env python3

from sgrid.location import Location
from sgrid.player import Player
from sgrid.item import Item
import json
import sys
import pickle
import argparse

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
            elif (rc == -2):
                with open("save.p", "wb") as f:
                    pickle.dump(player, f)
                sys.exit(0)

            first = False

    if __name__ == '__main__':
        input('\n>')

def new_game():
    # Test code
    twig = Item(name = 'twig', description = 'a nice sized twig',
                    first_description = 'hmm... a twig',
                    synonyms = ['wood', 'twig', 'stick'])
    berries = Item(name = 'berries', description = 'two small berries',
                    first_description = 'two tiny berries', 
                    synonyms = ['round', 'circles','berry', 'berries', 'balls'])

    undies = Item(name = 'undies', description = 'white undies',
                    first_description = 'white undies with skid-marks', 
                    synonyms = ['underwear', 'undies', 'boxers'],
                    is_container = True)
    chest = Item(name = 'chest', description = 'an ornate chest',
                    first_description = 'a beautiful crusty chest',
                    synonyms = ['chest', 'box', 'container'],
                    is_container = True, can_take = False, 
                    cannot_take_msg = "This thing is heavy. I ain't takin' it no where. ")
    sword = Item(name = "sword", description = 'a small sword',
                    first_description = 'a tiny sword made for tiny dudes',
                    synonyms = ['sword', 'needle', 'prick', 'knife', 'dagger'])

    note = Item(name = "note", 
        description = """The note says:
        Hi Dick,

        I hope you enjoyed playing with yourself.

        -Dick""",
        first_description = "This note looks familiar... it may warrant another inspection.",
        synonyms = ['note', 'letter', 'message', 'paper'])
    
    undies.addInv(twig)
    undies.addInv(berries)
    chest.addInv(note)
    caveInv = [chest]
    clearingInv = [sword]

    Cave = Location(name = 'Cave', 
        description = 'A dimly lit cave. You can see a clearing South of here.', 
        first_description = 'This cave sucks.',
        inventory = caveInv)
    Clearing = Location(name = 'Clearing', 
        description = 'This clearing looks stupid. It looks as if there is a cave North of here.', 
        first_description = 'You are in an expansive clearing. It looks as if there is a cave North of here.',
        inventory = clearingInv)
    
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

def load_game(loadfile):
    with open(loadfile, "rb") as f:
        hero = pickle.load(f)
        run_game(hero)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--load", help="load a game from the specified file")
    args = parser.parse_args()

    # Load a game if specified
    if args.load:
        load_game(args.load)

    # Start a new game by default
    new_game()
