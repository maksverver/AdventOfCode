from lib07 import Directory
import re
import sys

pattern = re.compile(r'''
^
(\$\ cd\ (?P<subdir> / | [.][.] | [a-z]+)) |
(\$\ ls) |
((?P<filesize>\d+)\ (?P<filename>[a-z.]+)) |
(dir\ [a-z]+)
\n$
''', re.VERBOSE)

def ParseInput(lines):
  cwd = root = Directory()
  all_directories = [root]
  for line in lines:
    m = pattern.match(line)
    if not m:
      raise Exception('Line not matched: ' + line)
    if filename := m.group("filename"):
      cwd.AddFile(filename, int(m.group("filesize")))
    elif dirname := m.group("subdir"):
      if dirname == '/':
        cwd = root
      elif dirname == '..':
        cwd = cwd.parent
      else:
        cwd = cwd.AddDirectory(m[1])
        all_directories.append(cwd)
  return all_directories


def SolvePart1(dir_sizes):
  return sum(size for size in dir_sizes if size <= 100_000)


def SolvePart2(dir_sizes):
  total_size  = 70_000_000
  needed_size = 30_000_000
  need_to_delete = needed_size - (total_size - dir_sizes[0])
  for size in sorted(dir_sizes):
    if size >= need_to_delete:
      return size


print('Parsing', file=sys.stderr)
directories = ParseInput(sys.stdin)
print('Computing sizes', file=sys.stderr)
dir_sizes = [d.ComputeSize() for d in directories]
print('Solving', file=sys.stderr)
print(SolvePart1(dir_sizes))
print(SolvePart2(dir_sizes))
