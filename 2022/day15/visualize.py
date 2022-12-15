#!/usr/bin/env python3

from lib15 import *
import sys
import subprocess
from PIL import Image, ImageDraw, ImageShow

class FehViewer(ImageShow.UnixViewer):
  def get_command_ex(self, file, **options):
    command = executable = 'feh'
    return command, executable

  def show_file(self, path=None, **options):
    assert path is not None
    subprocess.Popen(["feh", path])
    return 1

ImageShow.register(FehViewer(), 0)

def DrawImage(coords, scale=4000, max_x=4_000_000, max_y=4_000_000, solution=None):
  im = Image.new('RGB', ((max_x + 1) // scale, (max_y + 1) // scale), (0, 0, 0))
  draw = ImageDraw.Draw(im, 'RGBA')
  beacons = set()
  for x, y, bx, by in coords:
    beacons.add((bx, by))
    r = abs(bx - x) + abs(by - y)
    bx //= scale
    by //= scale
    x //= scale
    y //= scale
    r //= scale
    draw.polygon([(x - r, y), (x, y - r), (x + r, y), (x, y + r)],
      fill=(128, 128, 255, 16), outline=(0, 255, 0, 160))
    if 0 <= x <= max_x and 0 <= y <= max_y:
      draw.line((x - 3, y, x + 3, y), fill=(0, 255, 0, 255))
      draw.line((x, y - 3, x, y + 3), fill=(0, 255, 0, 255))
    draw.line((x, y, bx, by), fill=(255, 255, 0, 240))

  for x, y in beacons:
    x //= scale
    y //= scale
    if 0 <= x <= max_x and 0 <= y <= max_y:
      draw.line((x - 12, y, x + 12, y), fill=(255, 64, 0, 255))
      draw.line((x, y - 12, x, y + 12), fill=(255, 64, 0, 255))

  if solution:
    x, y = solution
    x //= scale
    y //= scale
    fill = (255, 0, 0, 255)
    if x >= 5:
      draw.line((x - 75, y, x - 5, y), fill=fill)
    if x + 5 <= max_x:
      draw.line((x + 5, y, x + 75, y), fill=fill)
    if y >= 5:
      draw.line((x, y - 75, x, y - 5), fill=fill)
    if y + 5 <= max_y:
      draw.line((x, y + 5, x, y + 75), fill=fill)

  return im

# Usage: visualize.py < input [<solution> [<output.png>]]
if __name__ == "__main__":
  solution = None
  if len(sys.argv) > 1:
    arg = int (sys.argv[1])
    solution = (arg // 4_000_000, arg % 4_000_000)
  coords = ReadCoords()
  im = DrawImage(coords, solution=solution)
  if len(sys.argv) > 2:
    im.save(sys.argv[2])
  else:
    im.show()
