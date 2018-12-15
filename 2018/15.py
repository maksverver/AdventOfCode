import sys

class Unit(object):
    def __init__(self, type):
        self.type = type
        self.hp = 200

    def __repr__(self):
        return self.type + '(' + str(self.hp) + ')'

def Adjacent(r, c):
    return [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]

def Solve(lines, attack_power):
    wall = [[ch == '#' for ch in line] for line in lines]
    occupied = [[Unit(ch) if ch in 'EG' else None for ch in line] for line in lines]

    # Track total HP per type to detect end-of-game.
    total_hp = {'E': 0, 'G': 0}
    for u in (u for row in occupied for u in row if u):
        total_hp[u.type] += u.hp

    # Simulate rounds one-by-one.
    rounds = 0
    while True:
        # Simulate one round.
        for ur, uc, u in [(r, c, u) for r, row in enumerate(occupied) for c, u in enumerate(row) if u]:
            if u.hp <= 0:
                # I'm dead.
                continue
            # Check if there are any enemies left.
            if total_hp[u.type] == sum(total_hp.values()):
                units_left = sum(1 for row in occupied for u in row if u)
                return (rounds, u.type, total_hp[u.type], units_left)
            # Breadth-first search to find nearest targets.
            dist = {(ur, uc): 0}
            prev = {}
            todo = [(ur, uc)]
            todo_next = []
            targets = []
            while todo and not targets:
                for r, c in todo:
                    for rr, cc in Adjacent(r, c):
                        t = occupied[rr][cc]
                        if t:
                            if t.type != u.type:
                                targets.append((r, c))
                        elif not wall[rr][cc]:
                            if (rr, cc) in dist:
                                continue
                            dist[rr, cc] = dist[r, c] + 1
                            prev[rr, cc] = (r, c)
                            todo_next.append((rr, cc))
                todo = todo_next
                todo_next = []
            # Take a step towards the nearest target.
            if targets:
                tr, tc = min(targets)
                if dist[tr, tc] > 0:
                    occupied[ur][uc] = None
                    ur, uc = tr, tc
                    while dist[ur, uc] > 1:
                        ur, uc = prev[ur, uc]
                    occupied[ur][uc] = u
            # Find enemies within reach.
            adjacent_enemies = []
            for r, c in Adjacent(ur, uc):
                t = occupied[r][c]
                if t and t.type != u.type:
                    adjacent_enemies.append((r, c, t))
            # Attack enemy with lowest HP.
            if adjacent_enemies:
                tr, tc, t = min(adjacent_enemies, key=lambda x: x[2].hp)
                damage = min(attack_power[u.type], t.hp)
                t.hp -= damage
                total_hp[t.type] -= damage
                if t.hp == 0:
                    occupied[tr][tc] = None
        rounds += 1

# Part 1
lines = [line.strip() for line in sys.stdin]
attack_power = {'E': 3, 'G': 3}
rounds, winner, hp_left, units_left = Solve(lines, attack_power)
print(rounds*hp_left)

# Part 2 (continues from above)
total_elves = sum(ch == 'E' for line in lines for ch in line)
while winner != 'E' or units_left < total_elves:
    attack_power['E'] += 1
    rounds, winner, hp_left, units_left = Solve(lines, attack_power)
print(rounds*hp_left)

# Used for debugging.
def DebugPrint():
    for r, row in enumerate(grid):
        line = ''
        desc = ''
        for c in range(len(row)):
            if wall[r][c]:
                line += '#'
            elif occupied[r][c]:
                u = occupied[r][c]
                line += u.type
                if desc != '':
                    desc += ', '
                desc += str(u)
            else:
                line += '.'
        print(line + '   ' + desc)
