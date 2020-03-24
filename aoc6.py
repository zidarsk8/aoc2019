orbits = """J1C)J1M
N2W)2DM
DST)VZL
555)45Q
S4C)DGK
G4Z)GKJ
598)L58
6R1)34Z
DVN)6KR
VMM)687""".splitlines()


# orbits = """COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
# K)YOU
# I)SAN""".splitlines()


d = dict(l.split(")")[::-1] for l in orbits)


def walk(k, d):
    count = 0
    while k in d:
        count += 1
        k = d[k]
    return count


print(sum(walk(k, d) for k in d))


import collections


def walk_path(k, d):
    path = collections.OrderedDict()
    count = 0
    while k in d:
        count += 1
        k = d[k]
        path[k] = count

    return path


you = walk_path("YOU", d)
san = walk_path("SAN", d)

while len(set(you).intersection(set(san))) > 1:
    last_key = list(you.keys())[-1]
    you.pop(last_key)
    san.pop(last_key)

print(list(you.values())[-1] + list(san.values())[-1] -2 )
