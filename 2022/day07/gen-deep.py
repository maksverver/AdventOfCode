#!/usr/bin/env python3

# Generates a deeply nested directory hierarchy, with at most 1 subdir per
# directory.

from lib07 import Directory
from random import randint
import sys

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
target_occupied_size = 69_000_000
min_files_per_dir = 1
max_files_per_dir = 1
max_depth = 5000000
palindromic = False

file_counts = [randint(min_files_per_dir, max_files_per_dir) for _ in range(max_depth + 1)]
total_files = sum(file_counts)
avg_file_size = target_occupied_size // total_files
file_sizes = [[randint(0, 2*avg_file_size) for _ in range(cnt)] for cnt in file_counts]
dir_sizes = [sum(sizes) for sizes in file_sizes]

# Update dir_sizes to include files in subdirectories.
for i in reversed(range(max_depth)):
  dir_sizes[i] += dir_sizes[i + 1]
  if palindromic and dir_sizes[i] <= 100_000 and dir_sizes[i] + dir_sizes[i - 1] > 100_000:
    # For part 1, we print the sizes of directories up to this point.
    # Massage the file sizes so the answer is a palindrome.
    part1 = sum(dir_sizes[i:])
    extra = MakePalindrome(part1) - part1
    file_sizes[i][0] += extra
    dir_sizes[i] += extra
    # This sometimes fails. We could fix that by smearing out the extra size
    # over all the directories in the subtree (instead just the root) but
    # it's easier to just rerun the script when that happens.
    assert dir_sizes[i] <= 100_000

# Minimum size of directory to delete.
deleted_size = needed_size - (total_size - dir_sizes[0])

# Find index `i` of the directory to delete.
i = 0
while dir_sizes[i + 1] >= deleted_size:
  i += 1
if palindromic:
  # Massage the file sizes in this directory so the answer is a
  # palindrome.
  extra = MakePalindrome(dir_sizes[i]) - dir_sizes[i]
  file_sizes[i][0] += extra
# Technically we should recalculate all dir_sizes, but let's not bother
# because we won't use them afterwards
#while i >= 0:
#  dir_sizes[i] += extra
#  i -= i
dir_sizes = None

cwd = root = Directory()
depth = 0
dir_name = '/'
while depth <= max_depth:
  print('$ cd %s' % dir_name)
  print('$ ls')

  if depth < max_depth:
    dir_name = RandomDirName()
    print('dir %s' % dir_name)
    cwd = cwd.AddDirectory(dir_name)

  for size in file_sizes[depth]:
    name = RandomFileName()
    cwd.AddFile(name, size)
    print('%d %s' % (size, name))

  depth += 1

print(root.ComputeSize(), file=sys.stderr)
