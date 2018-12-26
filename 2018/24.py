import re
import sys

pattern1 = re.compile(r'^(\d+) units each with (\d+) hit points( [(](.*)[)])? with an attack that does (\d+) (\w+) damage at initiative (\d+)$')
pattern2 = re.compile(r'^(immune|weak) to (\w+(, \w+)*)$')

class Group:
    def __init__(self, army, line):
        self.army = army
        m = pattern1.match(line)
        assert m
        units, hitpoints, _, attributes, damage, weapon, initiative = m.groups()
        self.units = int(units)
        self.hitpoints = int(hitpoints)
        self.damage = int(damage)
        self.weapon = weapon
        self.initiative = int(initiative)
        self.weaknesses = set()
        self.immunities = set()
        if attributes:
            for attribute in attributes.split('; '):
                m = pattern2.match(attribute)
                assert m
                attr, weapons, _ = m.groups()
                if attr == 'immune':
                    self.immunities.update(weapons.split(', '))
                else:
                    assert attr == 'weak'
                    self.weaknesses.update(weapons.split(', '))

def ParseGroups(lines, boosts=(0, 0)):
    groups = []
    groups_per_army = [0, 0]
    army = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line == 'Immune System:':
            army = 0
            continue
        if line == 'Infection:':
            army = 1
            continue
        groups_per_army[army] += 1
        boost = boosts[army]
        groups.append(Group(army, line))
    return groups

def Battle(groups, boosts=(0, 0)):
    units = dict((group, group.units) for group in groups)
    def TotalDamage(group):
        return units[group] * (group.damage + boosts[group.army])
    while True:
        # Targeting phase.
        attacked = set()
        targets = {}
        for a in sorted(groups, key=lambda group: (TotalDamage(group), group.initiative), reverse=True):
            b = max((b for b in groups if a.army != b.army and a.weapon not in b.immunities and b not in attacked),
                    key=lambda b: (a.weapon in b.weaknesses, TotalDamage(b), b.initiative), default=None)
            targets[a] = b
            if b is not None:
                attacked.add(b)

        # Attacking phase.
        total_killed = 0
        for group in sorted(groups, key=lambda group: group.initiative, reverse=True):
            target = targets[group]
            if target:
                damage = TotalDamage(group)
                if group.weapon in target.weaknesses:
                    damage *= 2
                killed = min(units[target], damage // target.hitpoints)
                units[target] -= killed
                total_killed += killed

        if total_killed == 0:
            return units

        groups = [group for group in groups if units[group] != 0]

def Winners(units):
    return set(group.army for group in units if units[group] != 0)

def UnitsLeft(units):
    return sum(units.values())

def Part1(groups):
    units = Battle(groups)
    assert len(Winners(units)) == 1  # Only 1 army remains.
    return UnitsLeft(units)

def Part2(groups):
    def CanWin(boost):
        return Winners(Battle(groups, boosts=(boost, 0))) == {0}
    hi = 1
    while not CanWin(hi):
        hi *= 2
    lo = 0
    while lo < hi:
        mid = lo + (hi - lo)//2
        if CanWin(mid):
            hi = mid
        else:
            lo = mid + 1
    return UnitsLeft(Battle(groups, boosts=(lo, 0)))

groups = ParseGroups(sys.stdin)
print(Part1(groups))
print(Part2(groups))
