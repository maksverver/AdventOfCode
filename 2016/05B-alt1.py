from hashlib import md5
import sys

def solve(door_id):
  password = ['?']*8
  i = 0
  while '?' in password:
    digest = md5(bytes(door_id + str(i), 'ascii')).digest()
    if digest[0] == 0 and digest[1] == 0 and digest[2] < 8:
      if password[digest[2]] == '?':
        password[digest[2]] = '%x'%(digest[3] >> 4)
    i += 1
  return ''.join(password)

print(solve(sys.stdin.readline().strip()))
