import sys

codes = [line.strip() for line in sys.stdin]

def Part1():
    a = 0
    b = 0
    for col in zip(*codes):
        num0 = col.count('0')
        num1 = col.count('1')
        assert num0 != num1
        a = 2*a + (num1 > num0)
        b = 2*b + (num1 < num0)
    return a * b

def Part2():

    def MostCommon(num0, num1):
        return '1' if num1 >= num0 else '0'

    def LeastCommon(num0, num1):
        return '0' if num1 >= num0 else '1'

    def Search(codes, predicate):
        i = 0
        while len(codes) > 1:
            col = [code[i] for code in codes]
            num0 = col.count('0')
            num1 = col.count('1')
            keep = predicate(num0, num1)
            codes = [code for code in codes if code[i] == keep]
            i += 1
        return codes[0]

    a = int(Search(codes, MostCommon), 2)
    b = int(Search(codes, LeastCommon), 2)
    return a * b

print(Part1())
print(Part2())
