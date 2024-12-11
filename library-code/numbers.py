from math import floor, log10

def CountDigits(i):
    '''Returns the number of digits in the decimal representation of the nonnegative integer i.'''
    if i == 0: return 1  # not always necessary
    return floor(log10(i)) + 1

def SplitNumber(i):
    '''Splits a number in half, e.g. SplitNumber(1234) == (12, 34)'''
    digits = CountDigits(i)
    assert digits % 2 == 0
    div = 10**(digits // 2)
    return i // div, i % div
