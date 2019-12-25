from intcode import ReadInts, Machine, MachineState
import re
import sys

# Set to true to print game input/output
VERBOSE = False

# Picking up these items ends the game prematurely, so leave these where you found them.
LEAVE_ITEMS = ('escape pod', 'giant electromagnet', 'infinite loop', 'molten lava', 'photons')

# The answer is a multi-digit code.
ANSWER_PATTERN = re.compile(r'\w\d+\w')

machine = Machine(ReadInts())
answer = None
edges = {}  # {room -> {direction -> room}}
inventory = set()

def Continue(command=None):
    if command:
        command += '\n'
        if VERBOSE:
            sys.stdout.write(command)
        for ch in command:
            machine.PutInput(ord(ch))
    outputs = []
    while True:
        state = machine.Run()
        if state != MachineState.OUTPUT:
            break
        outputs.append(machine.GetOutput())
    output = ''.join(map(chr, outputs))
    if VERBOSE:
        sys.stdout.write(output)
    match = ANSWER_PATTERN.search(output)
    if match:
        global answer
        assert answer is None
        answer = match[0]
    return output

def EnterRoom(command=None):
    name = None
    doors = []
    items = []
    state = 0
    for line in Continue(command).split('\n'):
        if line.startswith('== '):
            name = line.strip('= ')
        if line.startswith('Doors here lead'):
            state = 1
        if line.startswith('Items here:'):
            state = 2
        if line.startswith('- '):
            word = line.strip('- ')
            if state == 1:
                doors.append(word)
            elif state == 2:
                items.append(word)
            else:
                assert False
    if name not in edges:
        assert name not in edges
        edges[name] = dict((door, None) for door in doors)
    for item in items:
        if item not in LEAVE_ITEMS:
            assert item not in inventory
            Continue('take ' + item)
            inventory.add(item)
    return name

def FindPath(start, is_finish):
    todo = [start]
    prev = {}  # room -> (room, dir)
    for room in todo:
        if is_finish(room):
            dirs = []
            while room != start:
                room, dir = prev[room]
                dirs.append(dir)
            dirs.reverse()
            return dirs
        for next_dir, next_room in edges[room].items():
            if next_room not in prev:
                prev[next_room] = (room, next_dir)
                todo.append(next_room)

def ExploreShip():
    room = EnterRoom(None)
    while True:
        path = FindPath(room, lambda room: None in edges[room].values())
        if path is None:
            break
        for dir in path:
            room = EnterRoom(dir)
        next_dir = [next_dir for (next_dir, next_room) in edges[room].items() if next_room is None][0]
        next_room = EnterRoom(next_dir)
        edges[room][next_dir] = next_room
        room = next_room
    return room

def GetPastSecurityCheckpoint(room):
    # The security checkpoint is the one that has an edge back to itself.
    [(final_room, final_dir)] = [(room, next_dir)
        for (room, room_edges) in edges.items()
        for (next_dir, next_room) in room_edges.items()
        if room == next_room]

    # Move to the security checkpoint
    for dir in FindPath(room, final_room.__eq__):
        room = EnterRoom(dir)
    assert room == final_room

    all_items = list(inventory)
    mask = 1 << len(all_items)
    while mask > 0:
        mask -= 1
        for i, item in enumerate(all_items):
            if (mask & (1 << i)) == 0:
                if item in inventory:
                    Continue('drop ' + item)
                    inventory.remove(item)
            else:
                if item not in inventory:
                    Continue('take ' + item)
                    inventory.add(item)
        room = EnterRoom(final_dir)
        if room != final_room:
            return room

GetPastSecurityCheckpoint(ExploreShip())
assert machine.Run() == MachineState.HALT
print(answer)
