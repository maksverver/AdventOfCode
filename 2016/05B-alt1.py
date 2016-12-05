import md5
import sys

def solve(door_id):
  prefix = '0'*5
  password = ['?']*8
  i = 0
  while '?' in password:
    digest = md5.new(door_id + str(i)).digest()
    if ord(digest[0]) == 0 and ord(digest[1]) == 0 and ord(digest[2]) < 8:
      if password[ord(digest[2])] == '?':
        password[ord(digest[2])] = digest[3].encode('hex')[0]
    i += 1
  return ''.join(password)

print solve(sys.stdin.readline().strip())
