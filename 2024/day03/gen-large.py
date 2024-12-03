from random import randint, uniform

def GenString(min_len):
    s = ''
    while len(s) < min_len:
        r = randint(0, 2)
        if r == 0:
            s += 'do()'
        elif r == 1:
            s += "don't()"
        elif r == 2:
            s += 'mul(%d,%d)' % (randint(0,999), randint(0, 999))
    return s

def Corrupt(s, p):
    return ''.join((chr(randint(32, 126)) if uniform(0, 1) < p else ch) for ch in s)

output = ''
for x in range(500):
    output += Corrupt(GenString(20480), uniform(0, 0.1)) * 100
print(output)
