from itertools import combinations
import sys

weapons = [
	("Dagger",      8, 4, 0),
	("Shortsword", 10, 5, 0),
	("Warhammer",  25, 6, 0),
	("Longsword",  40, 7, 0),
	("Greataxe",   74, 8, 0) ]

armors = [
	("Leather",     13, 0, 1),
	("Chainmail",   31, 0, 2),
	("Splintmail",  53, 0, 3),
	("Bandedmail",  75, 0, 4),
	("Platemail",  102, 0, 5) ]

rings = [
	("Damage +1",   25, 1, 0),
	("Damage +2",   50, 2, 0),
	("Damage +3",  100, 3, 0),
	("Defense +1",  20, 0, 1),
	("Defense +2",  40, 0, 2),
	("Defense +3",  80, 0, 3) ]

cost   = lambda outfit: sum(c for _, c, _, _ in outfit)
damage = lambda outfit: sum(d for _, _, d, _ in outfit)
armor  = lambda outfit: sum(a for _, _, _, a in outfit)

def hits(my_damage, his_armor, his_health):
	damage_per_hit = max(1, my_damage - his_armor)
	# Return his_health divided by damage_per_hit, rounded up.
	return (his_health // damage_per_hit) + (his_health % damage_per_hit != 0)

def winning(outfit):
	return (hits(damage(outfit), boss_stats['Armor'], boss_stats['Hit Points']) <=
		hits(boss_stats['Damage'], armor(outfit), 100))

boss_stats = {}
for line in sys.stdin:
	stat, value = line.split(': ')
	boss_stats[stat] = int(value)

weapons = [[w] for w in weapons]
armors = [[]] + [[a] for a in armors]
rings = [[]] + [[r] for r in rings] + [list(t) for t in combinations(rings, 2)]
outfits = [w + a + r for w in weapons for a in armors for r in rings]

print(min(cost(outfit) for outfit in outfits if winning(outfit)))      # Part 1
print(max(cost(outfit) for outfit in outfits if not winning(outfit)))  # Part 2
