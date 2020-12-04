import re
import sys

REQUIREMENTS = {
    'byr': lambda s: len(s) == 4 and 1920 <= int(s) <= 2002,
    'iyr': lambda s: len(s) == 4 and 2010 <= int(s) <= 2020,
    'eyr': lambda s: len(s) == 4 and 2020 <= int(s) <= 2030,
    'hgt': lambda s: (
        (s.endswith('cm') and 150 <= int(s[:-2]) <= 193) or
        (s.endswith('in') and 59 <= int(s[:-2]) <= 76)),
    'hcl': lambda s: re.match('^#[0-9a-f]{6}$', s) is not None,
    'ecl': lambda s: s in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
    'pid': lambda s: re.match('^[0-9]{9}$', s),
}

passports = [
    dict(entry.split(':', 1) for entry in record.split())
    for record in sys.stdin.read().split('\n\n')]

def HasAllRequiredFields(passport):
    for key in REQUIREMENTS:
        if key not in passport:
            return False
    return True

def IsValid(passport):
    for key, validator in REQUIREMENTS.items():
        value = passport.get(key)
        if value is None or not validator(value):
            return False
    return True

# Part 1
print(sum(map(HasAllRequiredFields, passports)))

# Part 2
print(sum(map(IsValid, passports)))
