from random import randint
times = []
distances = []
for _ in range(100):
  t = randint(2, 1000)
  d = randint(0, (t // 2)*(t - t // 2) - 1)
  times.append(t)
  distances.append(d)

print('Time:', *times)
print('Distance:', *distances)

