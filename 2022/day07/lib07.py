import re
import sys

def ComputeDirectorySizes(start):
  needed = [start]
  for d in needed:
    for s in d.subdirs.values():
      if s.size is None:
        needed.append(s)
  for d in reversed(needed):
    d.size = (sum(d.files.values()) +
        sum(s.size for s in d.subdirs.values()))

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
      ComputeDirectorySizes(self)
    return self.size

  def __str__(self):
    return 'Directory{name="%s"}' % (self.name)
