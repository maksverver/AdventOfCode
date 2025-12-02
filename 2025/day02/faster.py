from heapq import heappush, heappop

#
# Part 1
#

def Solve1(lo, hi):
    period = 1
    total = 0
    start = 1
    pat = 11
    while pat*start <= hi:

        # a = start
        # while a < 10**n and a*pat < lo:
        #     a += 1
        # assert a == max(start, min(10**n, (lo + pat - 1)//pat))
        a = max(start, min(10**period, (lo + pat - 1)//pat))

        # b = a
        # while b < 10**n and b*pat <= hi:
        #     b += 1
        # assert b == min(10**n, hi//pat + 1)
        b = min(10**period, hi//pat + 1)

        #assert sum(range(a*pat, b*pat, pat)) == (a+b-1)*(b-a)//2*pat
        total += (a+b-1)*(b-a)//2*pat
        period += 1
        start *= 10
        pat = 10*start + 1

    return total

def Part1(ranges):
    return sum(Solve1(lo, hi) for (lo, hi) in ranges)


#
#  Part 2
#

def GenSeq(p):
    '''Generates sorted sequence of periodic integers with period at most p
        and length at least 2p'''
    pat = 1
    while True:
        pat = 10**p*pat + 1
        for i in range(10**(p-1)*pat, 10**p*pat, pat):
            yield i

def GenSeqs(max_period=10):
    '''Generates sorted sequence of all periodic integers with period up to
       max_period and length at least twice the period'''
    seqs = []
    for p in range(1, max_period + 1):
        seq = GenSeq(p)
        seqs.append((next(seq), p, seq))
    seqs.sort()

    last_i = 0
    while True:
        i, p, seq = seqs[0]

        # Reinsert in sorted sequence
        new_tuple = (next(seq), p, seq)
        j = 0
        while j + 1 < len(seqs) and seqs[j + 1] < new_tuple:
            seqs[j] = seqs[j + 1]
            j += 1
        seqs[j] = new_tuple

        if i != last_i:
            last_i = i
            yield i


def Part2(ranges):
    ranges.sort()
    total = 0
    ends = []
    pos = 0
    for i in GenSeqs():
        while pos < len(ranges) and ranges[pos][0] <= i:
            heappush(ends, ranges[pos][1])
            pos += 1
        while ends and ends[0] < i:
            heappop(ends)
        if ends:
            total += len(ends) * i
        elif pos == len(ranges):
            break
    return total


def ReadInput(file):
    ranges = []
    for part in file.read().strip().split(','):
        lo, hi = map(int, part.split('-'))
        ranges.append((lo, hi))
    return ranges


if __name__ == '__main__':

    # for testing
    if False:
        with open('../sampledata/02-sample.in') as f:
            sample = ReadInput(f)
        assert Part1(sample) == 1227775554
        assert Part2(sample) == 4174379265
        with open('../testdata/02.in') as f:
            official = ReadInput(f)
        assert Part1(official) == 28146997880
        assert Part2(official) == 40028128307

    import sys
    ranges = ReadInput(sys.stdin)
    #print('max=',max(hi for (_,hi) in ranges))
    print(Part1(ranges))
    print(Part2(ranges))
