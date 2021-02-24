"""
A simple home map, to be used for Lab4 of the "AI for Civil Engineers" course at ORU
It contains a set of rooms, a set of doors, and a set of points p1, p2, ..., pn (nodes)
Each point p is located in some room
Doors are associated with two locations, on the two sides of the door
Robot navigates between nodes, but it can only move between nodes in the same
room, or between the nodes on the two sides of a door
"""


# The map
nodes = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9']
rooms = {'room1': ['p1', 'p2', 'p3'], 'room2': ['p4', 'p5', 'p6'], 'room3': ['p7', 'p8', 'p9']}
doors = {'door1': ['p2', 'p8'], 'door2': ['p6', 'p7'], 'door3': ['p3', 'p4']}




# A few helper functions, that can be used in the methods' preconditions

def room_of(p):
    """
    Tell in what room a given node is located
    :param p: a point name (node)
    :return: a room name
    """
    for r in rooms.keys():
        if p in rooms[r]:
            return r
    return False

def side_of(d, r):
    """
    Look at the pair of nodes around a door d, and return the one which is located in room r
    :param d: a door
    :param r: a room
    :return: a node
    """
    p1, p2 = doors[d]
    if p1 in rooms[r]:
        return p1
    if p2 in rooms[r]:
        return p2
    return False

def other_side_of(d, r):
    """
    Like 'side_of' but it returns the other node
    :param d: a door
    :param r: a room
    :return: the node beside d that is located opposite to r
    """
    p1, p2 = doors[d]
    if p1 in rooms[r]:
        return p2
    if p2 in rooms[r]:
        return p1
    return False

def doors_of(r):
    """
    Returns the list of doors connected to room r
    :param r: a room
    :return: a list of doors
    """
    res = []
    for d in doors.keys():
        if side_of(d, r):
            res.append(d)
    return res

def door_of_node(b):
    #Returns the door adjacent to input node, if any.
    for d in doors.keys():
        if b in doors[d]:
            return d
    print("no door found for node " + b)
    return False


def which_door(a, b):
    """
    Determines which door connects two rooms
    """
    for door in doors_of(a):
        if door in doors_of(b):
            return door
    return False


# test that the helper functions work ok
"""
for p in nodes:
    print("Node", p, "is in", room_of(p))

for d in doors:
    for r in rooms:
        if side_of(d, r):
            print("Door", d, "has", side_of(d, r), "on the", r, "side, and", other_side_of(d, r), "on the other side")

for r1 in rooms:
    print("Room", r1, "has doors:", doors_of(r1))

"""

import pyhop

""" State variables 
state1 = State('state1')
state1.node = p1

"""

###Task a

# Create moveto and cross operators
# Create different navigate to methods

def moveto(state, b): 
    #If in the same room, move to that position
    if room_of(state.robot_pos) == room_of(b):
        state.robot_pos = b
        return state 
    else: return False

def cross(state, d):
    robot_room = room_of(state.robot_pos)
    #If the robot is next to the door, cross to the other side
    if state.robot_pos == side_of(d, robot_room) and state.door[d] == 'open':
        state.robot_pos = other_side_of(d, robot_room)
        return state
    else: return False

def open(state, d):
    #If the door isn't already opened, and the robot is next to it, open it.
    if state.door[d] != 'open' and state.robot_pos == side_of(d, room_of(state.robot_pos)):
        state.door[d] ='open'
        return state


def close(state, d):
    #If the door isn't already closed, and the robot is next to it, close it.
    if state.door[d] != 'closed' and state.robot_pos == side_of(d, room_of(state.robot_pos)):
        state.door[d] = 'closed'
        return state

def pickup(state, box):
    if state.boxes[box] == state.robot_pos:  # If the robot is by the box
        state.carrying = box #pickup the box
        state.boxes[box] = None #The box gets removed from its current position (since it got picked up)
        return state
    else:
        print("Can't pick-up the box!")
        return False

def putdown(state, box):
    if state.carrying == box: #If you carry the box
        state.carrying = None #drop it
        state.boxes[box] = state.robot_pos #Put it down where the robot is
        return state
    else:
        print("Can't putdown this box!")
        return False


pyhop.declare_operators(moveto, cross, open, close, pickup, putdown)
pyhop.print_operators()

def go_through(state, d):
    if state.door[d] != 'open':
        return [('open', d), ('cross', d), ('close', d)]
    else: return [('cross', d), ('close', d)]

pyhop.declare_methods('go_through', go_through)

def move_in_room(state, b):
    return [('moveto', b)] 

def move_to_another_room(state, b):
    goal_room = room_of(b)
    my_room = room_of(state.robot_pos)
    door_to_cross = which_door(my_room, goal_room)
    
    return [('moveto',side_of(door_to_cross,my_room)), ('go_through', door_to_cross), ('moveto',b)]


pyhop.declare_methods('navigate_to', move_in_room, move_to_another_room)

def fetch(state, box): #Go to the box, then pick it up
    return [('navigate_to', state.boxes[box]), ('pickup', box)]

pyhop.declare_methods('fetch', fetch)

def transport(state, box, position):
    #First, get the box
    # Then go to the position
    # then put the box down
    return[('fetch', box), ('navigate_to', position), ('putdown', box)]

pyhop.declare_methods('transport', transport)


state1 = pyhop.State('state1')
state1.robot_pos = 'p1'
state1.door = {'door1': 'closed', 'door2': 'closed','door3': 'closed'}
state1.boxes = {'box1': 'p9', 'box2': 'p5'}
state1.carrying = None

pyhop.pyhop(state1,[('transport', 'box1', 'p1')], verbose=1)

pyhop.pyhop(state1,[('transport', 'box2', 'p9')], verbose=1)
    
state1.robot_pos = 'p8'
pyhop.pyhop(state1,[('transport', 'box2', 'p9')], verbose=1)

pyhop.pyhop(state1,[('fetch', 'box2')], verbose=1)
pyhop.pyhop(state1,[('fetch', 'box1')], verbose=1)

state1.robot_pos = 'p3'
pyhop.pyhop(state1,[('fetch', 'box2')], verbose=1)
pyhop.pyhop(state1,[('fetch', 'box1')], verbose=1)

pyhop.pyhop(state1,[('navigate_to', 'p9')], verbose=1)
pyhop.pyhop(state1,[('navigate_to', 'p4')], verbose=1)
pyhop.pyhop(state1,[('navigate_to', 'p6')], verbose=1)