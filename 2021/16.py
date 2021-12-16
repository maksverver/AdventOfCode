from functools import reduce
from operator import mul
import sys

data = sys.stdin.readline().strip()

def DecodeBits(hex):
    bits = []
    for c in hex:
        i = int(c, 16)
        for b in reversed(range(4)):
            bits.append((i >> b) & 1)
    return bits


class BitReader:
    def __init__(self, bits):
        self.bits = bits
        self.pos = 0

    def NextInt(self, length):
        result = self.GetInt(self.pos, length)
        self.pos += length
        return result

    def GetInt(self, start, length):
        end = start + length
        assert end < len(self.bits)
        res = 0
        for bit in self.bits[start:end]:
            res += res + bit
        return res

    def NextVarInt(self):
        res = 0
        while True:
            i = self.NextInt(5)
            res = (res << 4) | (i & 0xf)
            if (i & 0x10) == 0:
                return res


class Packet:
    def __init__(self, version):
        self.version = version


class LiteralPacket(Packet):
    def __init__(self, version, value):
        super().__init__(version)
        self.value = value

    def Part1(self):
        return self.version

    def Part2(self):
        return self.value


class OperatorPacket(Packet):
    def __init__(self, version, op, subpackets):
        super().__init__(version)
        self.op = op
        self.subpackets = subpackets

    def Part1(self):
        return self.version + sum(subpacket.Part1() for subpacket in self.subpackets)

    def Part2(self):
        return self.op(subpacket.Part2() for subpacket in self.subpackets)


def Product(values):
    return reduce(mul, values)


def Gt(values):
    a, b = values
    return int(a > b)


def Lt(values):
    a, b = values
    return int(a < b)


def Eq(values):
    a, b = values
    return int(a == b)


OPS = {
    0: sum,
    1: Product,
    2: min,
    3: max,
    5: Gt,
    6: Lt,
    7: Eq}


def ParsePacket(reader):
    version = reader.NextInt(3)
    type_id = reader.NextInt(3)
    if type_id == 4:
        return LiteralPacket(version, reader.NextVarInt())
    else:
        return OperatorPacket(version, OPS[type_id], ParseSubpackets(reader))


def ParseSubpackets(reader):
    if reader.NextInt(1) == 0:
        end_pos = reader.NextInt(15) + reader.pos
        subpackets = []
        while reader.pos < end_pos:
            subpackets.append(ParsePacket(reader))
        return subpackets
    else:
        return [ParsePacket(reader) for _ in range(reader.NextInt(11))]


root_packet = ParsePacket(BitReader(DecodeBits(data)))
print(root_packet.Part1())
print(root_packet.Part2())
