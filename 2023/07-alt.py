# Alternative solver for day 7.
#
# This simplifies the implementation and makes it faster using two observations:
#
#  1. We can rank the hands as a sorted list duplicate counts (e.g.,
#     5-of-a-kind is represented by [5], 4-of-a-kind by [4, 1], two pairs
#     by [2, 2, 1], etc.). This simplifies GetRank() a lot.
#
#  2. For part 2, the joker always substitutes for the most common other card!
#
#     The only special case we need to consider is if the hand consists of
#     5 jokers. In that case, there is no most-common other card, but we should
#     always consider this as a five-of-a-kind.
#

from collections import Counter

import sys

def ParseLine(chars, line):
  s, t = line.split()
  hand = tuple(chars.index(ch) for ch in s)
  bid = int(t)
  return (hand, bid)


def GetRank(hand):
  return tuple(count for card, count in Counter(hand).most_common())


def MaxRank(hand):
  counter = Counter(hand)
  jokers = counter[0]
  del counter[0]
  if not counter: return (jokers,)  # only jokers
  counter[counter.most_common()[0][0]] += jokers
  return tuple(count for card, count in counter.most_common())


def Solve(lines, chars, rank_func):
  hands = [ParseLine(chars, line) for line in lines]
  hands.sort(key=lambda a: (rank_func(a[0]), a[0]))
  return sum(rank * bid for rank, (hand, bid) in enumerate(hands, 1))


data = sys.stdin.readlines()
print(Solve(data, '23456789TJQKA', GetRank))
print(Solve(data, 'J23456789TQKA', MaxRank))
