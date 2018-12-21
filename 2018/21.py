# Manually decoded from testdata/21.in
# See 21-decoded.txt for details.
def Next(a):
    b = a | 65536
    a = 6152285
    while b > 0:
        a += b & 255
        a &= 16777215
        a *= 65899
        a &= 16777215
        b >>= 8
    return a

first = a = Next(0)
seen = set()
while a not in seen:
    last = a
    seen.add(a)
    a = Next(a)
print(first)
print(last)
