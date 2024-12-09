import sys

class Span:
    def __init__(self, start, size):
        self.start = start
        self.size = size

    def __repr__(self):
        return f'Span({self.start},{self.size})'


def DecodeInput(input):
    files = []
    spaces = []
    disk_size = 0
    for i, size in enumerate(input):
        if i % 2 == 0:
            files.append(Span(disk_size, size))
        else:
            spaces.append(Span(disk_size, size))
        disk_size += size
    return files, spaces, disk_size


def Checksum(disk_layout):
    return sum(i * j for i, j in enumerate(disk_layout) if j >= 0)


# Calculates a list that maps each block index to the correspodning file index,
# or -1 if the block is free space.
def CalculateDiskLayout(files, disk_size):
    disk_layout = [-1]*disk_size
    for i, f in enumerate(files):
        for j in range(f.start, f.start + f.size):
            assert disk_layout[j] == -1
            disk_layout[j] = i
    return disk_layout


def SolvePart1(input):
    files, spaces, disk_size = DecodeInput(input)

    # Calculate the initial disk layout
    disk_layout = CalculateDiskLayout(files, disk_size)

    # Find list of occupied block indices. These will be used to move from.
    occupied = []
    for block, file in enumerate(disk_layout):
        if file != -1:
            occupied.append(block)

    # Find free spaces, and move occupied file blocks into them from the right.
    for dst, file in enumerate(disk_layout):
        if file == -1:
            if not occupied or (src := occupied.pop()) <= dst:
                break
            disk_layout[dst] = disk_layout[src]
            disk_layout[src] = -1

    return Checksum(disk_layout)



def SolvePart2(input):
    files, spaces, disk_size = DecodeInput(input)

    # Move files, starting from the right. Note it's never needed to merge adjacent
    # spaces because we move files left only, and we start from the right, so any
    # space created by moving files away can never be used to place another file.
    #
    # The loop below is O(n^2) which is slow but good enough for the official input.
    for f in reversed(files):
        for s in spaces:
            if s.start >= f.start:
                break
            if f.size <= s.size:
                # Put file in this space, and shrink space accordingly
                f.start = s.start
                s.start += f.size
                s.size -= f.size
                break

    return Checksum(CalculateDiskLayout(files, disk_size))


input = list(map(int, sys.stdin.readline().strip()))
print(SolvePart1(input))
print(SolvePart2(input))
