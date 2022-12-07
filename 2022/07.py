import re
import sys

class Directory:
  def __init__(self, name='', parent=None):
    self.name = name
    self.files = {}
    self.subdirs = {}
    self.size = None
    self.parent = parent

  def AddFile(self, name, size):
    assert(name not in self.files)
    self.files[name] = size

  def AddDirectory(self, name):
    assert(name not in self.subdirs)
    subdir = Directory(name, self)
    self.subdirs[name] = subdir
    return subdir

  def ComputeSize(self):
    if self.size is None:
      self.size = (sum(self.files.values()) +
          sum(d.ComputeSize() for d in self.subdirs.values()))
    return self.size

  def __str__(self):
    return 'Directory{name="%s"}' % (self.name)


def ParseInput(lines):
  cwd = root = Directory()
  all_directories = [root]
  for line in lines:
    if re.match('^[$] cd /\n$', line):
      cwd = root
    elif re.match('^[$] cd ..\n$', line):
      cwd = cwd.parent
    elif m := re.match('^[$] cd ([a-z]+)\n$', line):
      cwd = cwd.AddDirectory(m[1])
      all_directories.append(cwd)
    elif re.match('^[$] ls\n$', line):
      pass
    elif re.match('^dir [a-z]+\n$', line):
      pass
    elif m := re.match('^(\d+) ([a-z.]+)\n$', line):
      cwd.AddFile(m[2], int(m[1]))
    else:
      raise Exception('Line not matched: ' + line)
  return all_directories


def SolvePart1(dir_sizes):
  return sum(size for size in dir_sizes if size < 100_000)


def SolvePart2(dir_sizes):
  total_size  = 70_000_000
  needed_size = 30_000_000
  need_to_delete = needed_size - (total_size - dir_sizes[0])
  for size in sorted(dir_sizes):
    if size >= need_to_delete:
      return size


directories = ParseInput(sys.stdin)
dir_sizes = [d.ComputeSize() for d in directories]
print(SolvePart1(dir_sizes))
print(SolvePart2(dir_sizes))
