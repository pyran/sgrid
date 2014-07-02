# /usr/bin/env python3

from gameobjs import Location
from gameobjs import Player
#from gameobjs import Item


HEADING = \
"""This is a 2 room demo. Spoiler, you can only go north and south.
you can also use the examine/look command"""

# Function to run the game
def run_game(player):
    print(HEADING)
    global playing
    while playing:
        reply = input('\n>').lower().split(';') or ['']
        first = True
        for i in reply:
            if not first:
                print('\n>')
            player.execprint(i)
            first = False
    if __name__ == '__main__':
        input('\n>')

if __name__ == '__main__':
    # Test code
    playing = True
    Loc2 = Location('Room 2', 'a big ass ROOM', 'wow such big')
    Loc = Location('Room 1', 'a small ass ROOM', 'wow such small')
    # stick = Item('stick', 'a nice sized stick', 'such small stick')
    # ball = Item('ball', 'a big ball', 'first ball ever')
    # Loc.addInv(stick)
    # Loc2.addInv(ball)
    dungeon_map = {
    Loc:  {'north': Loc2},
    Loc2: {'south': Loc}
    }
    gameItems = {}
    hero = Player("Brian", "Asian Brian", "Whoa", Loc, dungeon_map)
    # Maybe can add a look self
    run_game(hero)