from collections import defaultdict
from heapq import heappush, heappop
import sys

class Player:
	def __init__(player, health, mana, armor = 0, enchantments = {}):
		player.health = health
		player.mana = mana
		player.armor = armor
		player.enchantments = enchantments

	def clone(player):
		return Player(player.health, player.mana, player.armor, dict(player.enchantments))

	def enchant(player, boss):
		player.armor = 0
		for spell in player.enchantments:
			spell.effect(player, boss)
		player.enchantments = dict((spell, turns - 1)
			for (spell, turns) in player.enchantments.items() if turns > 1)

	def key(player):
		# Armor isn't a key attribute because it resets every turn.
		return (player.health, player.mana,
			tuple(sorted(player.enchantments.items())))

class Boss:
	def __init__(boss, health, damage):
		boss.health = health
		boss.damage = damage

	def clone(boss):
		return Boss(boss.health, boss.damage)

	def key(boss):
		# Damage isn't a key attribute because it is constant.
		return boss.health

	def attack(boss, player):
		if boss.health > 0:
			player.health -= max(1, boss.damage - player.armor)

class Spell:
	'A spell has an immediate effect when cast.'

	def __init__(spell, name, cost, effect):
		spell.name = name
		spell.cost = cost
		spell.effect = effect

	def __repr__(spell):
		return spell.name

	def castable(spell, player):
		return spell.cost <= player.mana

	def cast(spell, player, boss):
		player.mana -= spell.cost
		spell.effect(player, boss)

class Enchantment(Spell):
	'''An enchantement is a spell that has no immediate effect, but applies
	   its effect over the duration of several turns instead.'''

	def __init__(spell, name, cost, duration, effect):
		Spell.__init__(spell, name, cost, effect)
		spell.duration = duration

	def castable(spell, player):
		return Spell.castable(spell, player) and spell not in player.enchantments

	def cast(spell, player, boss):
		player.mana -= spell.cost
		player.enchantments[spell] = spell.duration

def Effect(damage = 0, heal = 0, armor = 0, charge = 0):
	def apply(player, boss):
		boss.health -= damage
		player.health += heal
		player.armor += armor
		player.mana += charge
	return apply

class State:
	def __init__(state, player, boss):
		state.player = player
		state.boss = boss

	def winning(state):
		return state.boss.health <= 0

	def key(state):
		return (state.player.key(), state.boss.key())

spells = [
	Spell('Magic Missile', 53, Effect(damage = 4)),
	Spell('Drain', 73, Effect(damage = 2, heal = 2)),
	Enchantment('Shield', 113, 6, Effect(armor = 7)),
	Enchantment('Poison', 173, 6, Effect(damage = 3)),
	Enchantment('Recharge', 229, 5, Effect(charge = 101))]

def successors(state, hard_mode):
	player = state.player.clone()
	boss = state.boss.clone()
	# Player's turn
	if hard_mode:
		player.health -= 1
		if player.health <= 0:
			return
	player.enchant(boss)
	for spell in spells:
		if spell.castable(player):
			temp_player = player.clone()
			temp_boss = boss.clone()
			spell.cast(temp_player, temp_boss)
			# Boss' turn
			temp_player.enchant(temp_boss)
			temp_boss.attack(temp_player)
			if temp_player.health > 0:
				yield (spell.cost, State(temp_player, temp_boss))

def solve(initial_state, hard_mode):
	# Maps state keys to minimum cost to reach it.
	min_cost = defaultdict(lambda: float('inf'), [(initial_state.key(), 0)])
	# Lists unexpanded (cost, state) pairs.
	fringe = [(0, initial_state)]
	# Dijkstra's algorithm:
	while fringe:
		prev_cost, prev_state = heappop(fringe)
		if prev_state.winning():
			return prev_cost
		for add_cost, next_state in successors(prev_state, hard_mode):
			next_cost = prev_cost + add_cost
			next_key = next_state.key()
			if next_cost < min_cost[next_key]:
				min_cost[next_key] = next_cost
				heappush(fringe, (next_cost, next_state))

boss_stats = {}
for line in sys.stdin:
	stat, value = line.split(': ')
	boss_stats[stat] = int(value)

initial_state = State(Player(health = 50, mana = 500),
	Boss(health = boss_stats['Hit Points'], damage = boss_stats['Damage']))
print solve(initial_state, 0)  # Part 1
print solve(initial_state, 1)  # Part 2
