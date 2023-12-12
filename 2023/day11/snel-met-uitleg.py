# Advent of Code 2013 Dag 11 -- O(N) oplossing met uitleg.
# https://adventofcode.com/2023/day/11
#
# Om een efficiënte oplossing te schrijven zijn drie observaties nodig.
#
#
# Observatie 0:
#
# Je kunt de nieuwe coördinaten van de sterrenstelsels berekenen door voor elke
# rij/kolom de nieuwe breedte/hoogte te bereken. Ik neem aan dat iedereen die
# deel 2 opgelost heeft dit bedacht heeft, dus wijdt ik daar verder niet over
# uit.
#
# Vervolgens moeten we de som van afstanden tussen sterrenstelsels berekenen. De
# afstand tussen punten p en q is gedefinieerd als de som:
#
#     |p.x - q.x| + |p.y - q.y|
#
# En het eindantwoord is simpelweg de som van die afstanden voor alle paren van
# punten p en q:
#
#     som(|p.x - q.x| + |p.y - q.y| voor alle p, q)
#
# Als er N sterrenstelsels zijn, dan tel je op deze manier O(N^2) waarden op.
# Dit werkt voor de officiële testdata, maar is te traag voor grotere invoer.
# Om dit te optimaliseren hebben we nog twee observaties nodig.
#
#
# Observatie 1:
#
# De bovenstaande som bevat zelf een som. Omdat optellen een associatieve en
# commutatieve operatie is, kun je de som net zo goed schrijven als:
#
#     som(|p.x - q.x| voor alle p, q) +
#     som(|p.y - q.y| voor alle p, q)
#
# Aha! We kunnen de x en y coordinaten dus apart beschouwen.
#
# Dat betekent dat we de x en y coordinaten afzonderlijk kunnen sorteren (merk
# op dat dit niet kan met 2D punten), en de abs() weghalen, zodat we de som
# kunnen versimpelen naar:
#
#   som(xs[j] - xs[i] voor alle i < j) +
#   som(ys[j] - ys[i] voor alle i < j).
#
# Dit levert niet meteen snelheidswinst op, maar helpt om de implementatie
# verder te optimaliseren.
#
#
# Observatie 2:
#
# De bovenstaande som kan in lineaire tijd uitgerekend worden. Dat is het
# makkelijkst uit te leggen aan de hand van een voorbeeld:
#
#  xs = [1, 5, 7, 8]
#
# Op de trage manier bereken we de afstand tussen alle paren van punten:
#
#   (5 - 1) + (7 - 1) + (7 - 5) + (8 - 1) + (8 - 5) + (8 - 7) =
#      4    +    6    +    2    +    7    +    3    +    1    = 23.
#
# Het helpt om dit te visualiseren op de nummerlijn. Feitelijk nemen we de som
# van een aantal intervallen:
#
#  x = 1 2 3 4 5 6 7 8
#      o-------o                   5 - 1 = 4
#      o-----------o               7 - 1 = 6
#              o---o               7 - 5 = 2
#      o-------------o             8 - 1 = 7
#              o-----o             8 - 5 = 3
#                  o-o             8 - 7 = 1
#
# Maar zoals je ziet zit er veel overlap tussen de intervallen! Bijvoorbeeld het
# stukje tussen 5 en 7 komt voor in de intervallen 1..7, 5..7, 1..8 en 5..8.
#
# Laten we de kleinst mogelijke segmenten van intervallen bekijken. Dat zijn de
# segmenten tussen opvolgende punten in de invoer: 1..5, 5..7, en 7..8:
#
#  x = 1 2 3 4 5 6 7 8
#      o-------o                   5 - 1 + 4
#      o-------|---o               7 - 1 + 6
#              o---o               7 - 5 + 2
#      o-------|---|-o             8 - 1 + 7
#              o---|-o             8 - 5 + 3
#                  o-o             8 - 7 + 1
#
# Het interval 1..5 van lengte 4 wordt 3 keer geteld.
# Het interval 5..7 van lengte 2 wordt 4 keer geteld.
# Het interval 7..8 van lengte 1 wordt 3 keer geteld.
#
# We kunnen de som dus ook schrijven als: 4×3 + 2×4 + 1×3 = 23.
#
# Het aantal minimale segmenten is O(N). Als we kunnen bepalen hoe vaak elk
# segment in een interval geteld wordt kunnen we de som van de lengte van de
# intervallen dus tellen in O(N) in plaats van O(N^2). Gelukkig is dat niet
# moeilijk. Het aantal keer dat een interval a..b geteld wordt is gelijk aan het
# product:
#
#  (aantal getallen kleiner dan of gelijk aan a) *
#  (aantal getallen  groter dan of gelijk aan b)
#
# Als we een gesorteerde array xs[] hebben met indices van 0 tot en met n - 1,
# dan komt het segment xs[i-1..i] precies i×(n - i) keer voor.
#
# En daarmee hebben we alles wat we nodig hebben: elk deel van de oplossing
# loopt in O(N) tijd.

from itertools import accumulate
import sys

# Stap 0: invoer inlezen
grid = [s.strip() for s in sys.stdin]
H = len(grid)     # hoogte
W = len(grid[0])  # breedte

for expand in (2, 1_000_000):

  # Stap 1: berekenen getransleerde coordinaten (observatie 1)
  x_sizes = [expand if all(grid[y][x] == '.' for y in range(H)) else 1 for x in range(W)]
  y_sizes = [expand if all(grid[y][x] == '.' for x in range(W)) else 1 for y in range(H)]
  new_x = list(accumulate(x_sizes, initial=0))
  new_y = list(accumulate(y_sizes, initial=0))
  xs = [new_x[x] for x in range(W) for y in range(H) if grid[y][x] == '#']
  ys = [new_y[y] for y in range(H) for x in range(W) if grid[y][x] == '#']

  # Stap 2: bereken voor x- en y-coordinaten afzonderlijk de som van de
  # verschillen (observatie 2 en 3). `xs` en `ys` moeten gesorteerd zijn!
  print(
    sum((xs[i] - xs[i - 1]) * i * (len(xs) - i) for i in range(1, len(xs))) +
    sum((ys[i] - ys[i - 1]) * i * (len(ys) - i) for i in range(1, len(ys))))
