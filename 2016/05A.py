import md5
import sys

def solve(door_id):
  prefix = '0'*5
  password = ''
  i = 0
  while len(password) < 8:
    digest = md5.new(door_id + str(i)).hexdigest()
    if digest.startswith(prefix):
      password += digest[len(prefix)]
    i += 1
  return password

print solve(sys.stdin.readline().strip())
