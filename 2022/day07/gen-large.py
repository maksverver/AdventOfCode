#!/usr/bin/env python3

# Generates a deeply nested directory hierarchy, with at most 1 subdir per
# directory.

from lib07 import Directory
from random import randint, shuffle
import sys

def shuffled(a):
  a = list(a)
  shuffle(a)
  return a

def RandomChar():
  return chr(randint(ord('a'), ord('z')))

def RandomName(n):
  return ''.join(RandomChar() for _ in range(n))

def RandomDirName():
  return RandomName(6)

def RandomFileName():
  return RandomName(4) + '.' + RandomName(3)

def MakePalindrome(i):
  while str(i) != ''.join(reversed(str(i))):
    i = i + 1
  return i

total_size  = 70_000_000
needed_size = 30_000_000
#target_occupied_size = 69_000_000
max_file_size = 100

def GenSubTree(name, size_left, last):
  assert size_left > 0
  print("$ cd {}".format(name))

  print("$ ls")
  dirsize = 0

  filecount = randint(0, 2)
  filesizes = []
  for _ in range(filecount):
    s = min(size_left, randint(1, max_file_size))
    size_left -= s
    filesizes.append(s)
    if size_left == 0:
      break

  subdircount = randint(1, 3) if size_left > 0 else 0
  subdirnames = []
  subdirsizes = []
  for i in range(subdircount):
    subdirnames.append(RandomDirName())
    if i < subdircount - 1:
      s = randint(1, size_left)
      subdirsizes.append(s)
      size_left -= s
    else:
      subdirsizes.append(size_left)
    if size_left == 0:
      break
  shuffle(subdirsizes)

  for subdirname in shuffled(subdirnames):
    print('dir {}'.format(subdirname))
  for filesize in shuffled(filesizes):
    dirsize += filesize
    print("{} {}".format(filesize, RandomFileName()))
  for i, (subdirname, subdirsize) in enumerate(zip(subdirnames, subdirsizes)):
    dirsize += GenSubTree(subdirname, subdirsize, last=(last and i == len(subdirnames) - 1))

  if not last:
    print("$ cd ..")

  return dirsize


subdirnames = [RandomDirName(), RandomDirName(), RandomDirName(), ]
print("$ cd /")
a = GenSubTree(RandomDirName(), 6_000_000, last=True)
print("$ cd /")
b = GenSubTree(RandomDirName(), 60_000_000, last=True)
print("$ cd /")
c = GenSubTree(RandomDirName(), 3_000_000, last=True)
print(a, b, c, a + b + c, file=sys.stderr)
print(a / needed_size, b / needed_size, c / needed_size, (a + b + c) / total_size, file=sys.stderr)
assert a + b + c < total_size
