f = 359282
t = 820401


count_part1 = 0
count_part2 = 0
for i in range(f, t + 1):
    if "".join(sorted(str(i))) == str(i):
        if len(set(str(i))) < 6:
            count_part1 += 1

        good = False
        for digit in str(i):
            if str(i).count(digit) == 2:
                good = True
        if good:
            count_part2 += 1

print(count_part1)
print(count_part2)
print("done")
