from nose.tools import *
from planisphere import *

def test_room():
    gold = Room("GoldRoom",
                """This room has gold in it you can grab. There's a
                door to the north.""", 'help text')
    assert_equal(gold.name, "GoldRoom")
    assert_equal(gold.paths, {})

def test_room_paths():
    center = Room("Center", "Test room in the center.", "Center help text")
    north = Room("North", "Test room in the north.", "North help text")
    south = Room("South", "Test room in the south.", "South help text")
    
    center.add_paths({'north': north, 'south': south})
    assert_equal(center.go('north'), north)
    assert_equal(center.go('south'), south)

    # Test help function
    assert_equal(center.helptext, "Center help text")

def test_map():
    start = Room("Start", "You can go west and down a hole.", "Start help text")
    west = Room("Trees", "There are trees here, you can go east.", "West help text")
    down = Room("Dungeon", "It's dark down here, you can go up.", "Down help text")
    
    start.add_paths({'west': west, 'down': down})
    west.add_paths({'east': start})
    down.add_paths({'up': start})

    assert_equal(start.go('west'), west)
    assert_equal(start.go('west').go('east'), start)
    assert_equal(start.go('down').go('up'), start)

def test_gothon_game_map():
    start_room = load_room(START)
    assert_equal(start_room.go('shoot!'), generic_death)
    assert_equal(start_room.go('dodge!'), generic_death)
    room = start_room.go('tell a joke')
    assert_equal(room, laser_weapon_armory)

    assert_equal(room.go('*'), generic_death)
    next_room = room.go('1234')
    assert_equal(next_room, the_bridge)

    assert_equal(next_room.go('throw the bomb'), generic_death)
    next_room2 = next_room.go('slowly place the bomb')
    assert_equal(next_room2, escape_pod)

    assert_equal(next_room2.go('*'), the_end_loser)
    assert_equal(next_room2.go('2'), the_end_winner)
