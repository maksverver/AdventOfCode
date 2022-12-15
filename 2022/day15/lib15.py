import re
import sys

def ParseLine(line):
  m = re.match('^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$', line)
  sx, sy, bx, by = map(int, m.groups())
  return (sx, sy, bx, by)

def ReadCoords(file=sys.stdin):
  '''Parses input as a list of tuples (sensor_x, sensor_y, nearest_beacon_x, nearest_beacon_y).'''
  return list(map(ParseLine, sys.stdin))

def MakeSensors(coords):
  '''Converts coords to a list of tuples (sensor_x, sensor_y, sensor_range)'''
  return [(sx, sy, abs(bx - sx) + abs(by - sy)) for sx, sy, bx, by in coords]

def MakeBeacons(coords):
  '''Converts coords to a set of tuples (beacon_x, beacon_y)'''
  return set([(bx, by) for sx, sy, bx, by in coords])

