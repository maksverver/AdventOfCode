from hashlib import md5
import sys

def solve(door_id):
  password = ''
  i = 0
  while len(password) < 8:
    digest = md5(bytes(door_id + str(i), 'ascii')).digest()
    if digest[0] == 0 and digest[1] == 0 and digest[2] < 16:
      password += '%x' % digest[2]
    i += 1
  return password

print(solve(sys.stdin.readline().strip()))
