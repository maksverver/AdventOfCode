import md5
import sys

def solve(door_id):
  prefix = '0'*5
  password = ''
  i = 0
  while len(password) < 8:
    digest = md5.new(door_id + str(i)).digest()
    if (ord(digest[0]) == 0 and ord(digest[1]) == 0 and ord(digest[2]) < 16:
      password += digest[2].encode('hex')[-1]
    i += 1
  return password

print solve(sys.stdin.readline().strip())
