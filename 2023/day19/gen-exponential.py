from random import choice, randint

# in{x<2000:aa,ab}
# aa{m<500:b,b}
# ab{m<1500:b,b}
# b{a<2000:ba,bb}
# ba{a<500:c,c}
# bb{a<1500:c,c}
# c{s<2000:ca,cb}
# ca{s<500:d,d}
# cb{s<1500:d,d}
# d{x<2000:da,db}
# da{x<500:e,e}
# db{x<1000:e,e}
# e{x>1:A,x<4000:A,R}

# {x=1,m=1,a=1,s=1}

# Every doubling of size roughly multiplies the execution time by 16!
#
#  64 ->  ~4 seconds (challenge 3)
# 128 -> ~16 seconds (challenge 4)
# 256 -> ~64 seconds

fields = 'xmas'
size = 128   # may be up to 4000

def Gen(field, label, lo, hi, next_label):
  if hi - lo < 2:
    return next_label or choice(('A', 'R'))

  mid = lo + (hi - lo) // 2
  print(label + '{' + field + '<' + str(mid) + ':' + Gen(field, label + 'o', lo, mid, next_label) + ',' + Gen(field, label + 'l', mid, hi, next_label) + '}')
  return label

label = None
for field in fields:
  label = Gen(field, field, 1, size + 1, label)
print('in{%s,%s}'%(','.join('%s>%d:R' % (field, size) for field in fields), label))
print()
for _ in range(100):
  print('{x=%d,m=%d,a=%d,s=%d}' % tuple(randint(1, size) for _ in range(4)))
