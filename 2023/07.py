import sys

NUM_CARDS = 13


def GetRank(hand):
  assert len(hand) == 5
  cards = sorted(hand)

  if cards[0] == cards[4]:
    return 6  # five of a kind

  if cards[0] == cards[3] or cards[1] == cards[4]:
    return 5  # four or a kind

  if ((cards[0] == cards[2] and cards[3] == cards[4]) or
      (cards[0] == cards[1] and cards[2] == cards[4])):
    return 4  # full house

  if cards[0] == cards[2] or cards[1] == cards[3] or cards[2] == cards[4]:
    return 3  # three of a kind

  pairs = sum(cards[i] == cards[j] for i in range(5) for j in range(i + 1, 5))
  return pairs


def MaxRank(input_hand):
  hand = list(input_hand)

  def Dfs(i):
    if i == len(hand):
      return GetRank(hand)

    if hand[i] != 0:
      return Dfs(i + 1)

    res = 0
    for j in range(NUM_CARDS):
      hand[i] = j
      res = max(res, Dfs(i + 1))
    hand[i] = 0
    return res

  return Dfs(0)


def ParseLine(chars, line):
  s, t = line.split()
  hand = tuple(chars.index(ch) for ch in s)
  bid = int(t)
  return (hand, bid)


def Solve(data, chars, rank_func):
  assert len(chars) == NUM_CARDS
  hands = [ParseLine(chars, line) for line in data.splitlines()]
  hands.sort(key=lambda a: (rank_func(a[0]), a[0]))
  return sum(rank * bid for rank, (hand, bid) in enumerate(hands, 1))


data = sys.stdin.read()
print(Solve(data, '23456789TJQKA', GetRank))
print(Solve(data, 'J23456789TQKA', MaxRank))
