import re
import sys

def ParseRuleTable(lines):
    rules = [None]*len(lines)
    for line in lines:
        num, rest = line.split(': ')
        if rest[0] == '"' and rest[-1] == '"':
            # "foo"  --> "foo"
            rules[int(num)] = rest[1:-1]
        else:
            # 2 3 | 4 5  -->  ((2, 3), (4, 5))
            rules[int(num)] = tuple(tuple(map(int, alt.split(' '))) for alt in rest.split(' | '))
    return rules

def MatchEntirely(line):
    def Match(start_pos, rule_idx):
        rule = rules[rule_idx]
        ends = set()
        if isinstance(rule, str):
            if line.startswith(rule, start_pos):
                ends.add(start_pos + len(rule))
        else:
            for seq in rule:
                def Search(seq_idx, pos):
                    if seq_idx == len(seq):
                        ends.add(pos)
                        return
                    for end_pos in Match(pos, seq[seq_idx]):
                        Search(seq_idx + 1, end_pos)
                Search(0, start_pos)
        return ends
    return len(line) in Match(0, 0)

part1, part2 = sys.stdin.read().split('\n\n')
rules = ParseRuleTable(part1.split('\n'))
messages = part2.strip().split('\n')

print(len(list(filter(MatchEntirely, messages))))  # Part 1

assert rules[8] == ((42,),)
assert rules[11] ==  ((42, 31),)
rules[8] = ((42,), (42, 8))
rules[11] = ((42, 31), (42, 11, 31))

print(len(list(filter(MatchEntirely, messages))))  # Part 2
