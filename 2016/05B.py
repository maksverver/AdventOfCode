import md5
import sys

def solve(door_id):
  prefix = '0'*5
  password = ['?']*8
  i = 0
  while '?' in password:
    digest = md5.new(door_id + str(i)).hexdigest()
    if digest.startswith(prefix):
      position = int(digest[len(prefix)], 16)
      if 0 <= position < len(password) and password[position] == '?':
        password[position] = digest[len(prefix) + 1]
    i += 1
  return ''.join(password)

print solve(sys.stdin.readline().strip())
