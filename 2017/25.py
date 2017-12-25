from collections import defaultdict
import sys
import re

class State:
    def __init__(self):
        self.write = None
        self.move = None
        self.next_state = None

class Machine:
    def __init__(self, start_state, states):
        self.states = states
        self.tape = defaultdict(lambda: 0)
        self.cursor_pos = 0
        self.current_state = start_state

    def run(self, iterations):
        for _ in range(iterations):
            self.step()

    def step(self):
        current_value = self.tape[self.cursor_pos]
        state = self.states[self.current_state, current_value]
        self.tape[self.cursor_pos] = state.write
        self.cursor_pos += state.move
        self.current_state = state.next_state

start_state = None
iterations = None
states = {}
for line in sys.stdin:
    line = line.strip()
    m = re.match('Begin in state (\w+)\.', line)
    if m:
        start_state = m.group(1)
        continue
    m = re.match('Perform a diagnostic checksum after (\d+) steps.', line)
    if m:
        iterations = int(m.group(1))
        continue
    m = re.match('In state (\w+):', line)
    if m:
        current_state = m.group(1)
        continue
    m = re.match('If the current value is (\d+):', line)
    if m:
        current_value = int(m.group(1))
        states[current_state, current_value] = state = State()
        continue
    m = re.match('- Write the value (\d+).', line)
    if m:
        state.write = int(m.group(1))
        continue
    m = re.match('- Move one slot to the (left|right)', line)
    if m:
        state.move = 1 if m.group(1) == 'right' else -1
        continue
    m = re.match('- Continue with state (\w+)\.', line)
    if m:
        state.next_state = m.group(1)
        continue
    assert not line

machine = Machine(start_state, states)
machine.run(iterations)
print(sum(machine.tape.values()))
