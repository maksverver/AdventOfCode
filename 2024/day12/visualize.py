from PIL import Image
import random
import sys

#
# Random color generation stolen from https://gist.github.com/adewes/5884820
#

def get_random_color(pastel_factor = 0.5):
    return [(x+pastel_factor)/(1.0+pastel_factor) for x in [random.uniform(0,1.0) for i in [1,2,3]]]

def color_distance(c1,c2):
    return sum([abs(x[0]-x[1]) for x in zip(c1,c2)])

def existing_colors(existing_colors, pastel_factor = 0.5):
    max_distance = None
    best_color = None
    for i in range(0,100):
        color = get_random_color(pastel_factor = pastel_factor)
        if not existing_colors:
            return color
        best_distance = min([color_distance(color,c) for c in existing_colors])
        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color
    return best_color


_, inpath, outpath = sys.argv

with open(inpath, 'rt') as f:
    grid = [line.strip() for line in f]
    H = len(grid)
    W = len(grid[0])
    assert all(len(row) == W for row in grid)

chars = list(set(''.join(grid)))
colors = []
while len(colors) < len(chars):
    colors.append(existing_colors(colors))
colors = [tuple(round(255*i) for i in rgb) for rgb in colors]

im = Image.new("RGB", (W, H))
pixels = im.load()
for r in range(H):
    for c in range(W):
        pixels[c, r] = colors[chars.index(grid[r][c])]
im.save(outpath)
