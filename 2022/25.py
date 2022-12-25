import sys

SNAFU_DIGITS = "=-012"

def ParseDigits(string):
  'Converts the SNAFU string to a list of base-5 digits, ordered from least to most significant.'
  return list(reversed([SNAFU_DIGITS.index(ch) - 2 for ch in string]))

def FormatDigits(digits):
  'Inverse of ParseDigits(): converts a sequence of base-5 digits to a SNAFU string.'
  return ''.join(SNAFU_DIGITS[d + 2] for d in reversed(digits))

def AddDigits(a, b):
  result = []
  carry = 0
  pos = 0
  while pos < len(a) or pos < len(b) or carry:
    digit = (a[pos] if pos < len(a) else 0) + (b[pos] if pos < len(b) else 0) + carry
    if digit < -2:
      carry = -1
      digit += 5
    elif digit > 2:
      digit -= 5
      carry = 1
    else:
      carry = 0
    result.append(digit)
    pos += 1
  return result

total = []
for line in sys.stdin:
  total = AddDigits(total, ParseDigits(line.strip()))
print(FormatDigits(total))
