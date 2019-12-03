code = "1,9,10,3,2,3,11,0,99,30,40,50"


code = "1,0,0,0,99"
code = "2,3,0,3,99"
code = "2,4,4,5,99,0"
code = "1,1,1,4,99,5,6,0,99"


code = "1,9,10,3,2,3,11,0,99,30,40,50"


def run(value):
    code = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,19,9,23,1,23,13,27,1,10,27,31,2,31,13,35,1,10,35,39,2,9,39,43,2,43,9,47,1,6,47,51,1,10,51,55,2,55,13,59,1,59,10,63,2,63,13,67,2,67,9,71,1,6,71,75,2,75,9,79,1,79,5,83,2,83,13,87,1,9,87,91,1,13,91,95,1,2,95,99,1,99,6,0,99,2,14,0,0"
    computer = {i: int(c) for i, c in enumerate(code.split(","))}
    pos = 0

    computer[1] = value // 100
    computer[2] = value % 100

    while computer[pos] != 99:
        if computer[pos] == 1:
            computer[computer[pos + 3]] = (
                computer[computer[pos + 1]] + computer[computer[pos + 2]]
            )
            pos += 4
        elif computer[pos] == 2:
            computer[computer[pos + 3]] = (
                computer[computer[pos + 1]] * computer[computer[pos + 2]]
            )
            pos += 4
        else:
            print("WRONG")
            print(computer[pos])

    # print(computer.values())
    return computer[0]


for i in range(10000):
    r = run(i)
    print(i, r)
    if r == 19690720:
        break
