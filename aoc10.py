astroids=""".#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##"""


astroids = """#.#.###.#.#....#..##.#....
.....#..#..#..#.#..#.....#
.##.##.##.##.##..#...#...#
#.#...#.#####...###.#.#.#.
.#####.###.#.#.####.#####.
#.#.#.##.#.##...####.#.##.
##....###..#.#..#..#..###.
..##....#.#...##.#.#...###
#.....#.#######..##.##.#..
#.###.#..###.#.#..##.....#
##.#.#.##.#......#####..##
#..##.#.##..###.##.###..##
#..#.###...#.#...#..#.##.#
.#..#.#....###.#.#..##.#.#
#.##.#####..###...#.###.##
#...##..#..##.##.#.##..###
#.#.###.###.....####.##..#
######....#.##....###.#..#
..##.#.####.....###..##.#.
#..#..#...#.####..######..
#####.##...#.#....#....#.#
.#####.##.#.#####..##.#...
#..##..##.#.##.##.####..##
.##..####..#..####.#######
#.#..#.##.#.######....##..
.#.##.##.####......#.##.##"""





positions = []

for y, line in enumerate(astroids.splitlines()):
    for x, char in enumerate(line):
        if char != ".":
            positions.append((x,y))
        print(y, line)

import math
import numpy as np
pos_len = []
for y, line in enumerate(astroids.splitlines()):
    for x, char in enumerate(line):
        if char != ".":
            same_line = []
            for position in positions:
                dx = position[0] - x
                dy = position[1] - y
                gcd = math.gcd(dx, dy)     
                if gcd:
                    same_line.append((dx/gcd, dy/gcd))
            pos_len.append((len(set(same_line)), x, y))
            # print(x, y, len(same_line))

best = sorted(pos_len)[-1]

print(astroids)
            
print(best)

count, bx, by = best
            

import collections
angles = collections.defaultdict(list)
for y, line in enumerate(astroids.splitlines()):
    for x, char in enumerate(line):
        if char == ".":
            continue
        dx = x - bx
        dy = y - by
        if dx == dy == 0:
            continue
        angle = round((math.degrees(np.arctan2(dy, dx)) + 90 + 360) % 360, 10)
        print(f"{angle:<20}, {dx:>5}, {dy:>5}")
        angles[angle].append((x,y, dx, dy))

angle_keys = sorted(angles)

for i in range(200):
    for angle in angle_keys:
        print(angles[angle])
