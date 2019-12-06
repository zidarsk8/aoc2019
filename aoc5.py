code = "1,9,10,3,2,3,11,0,99,30,40,50"


code = "1,0,0,0,99"
code = "2,3,0,3,99"
code = "2,4,4,5,99,0"
code = "1,1,1,4,99,5,6,0,99"


code = "1,9,10,3,2,3,11,0,99,30,40,50"


def run(system_id):
    code = "1101,100,-1,4,0"
    code = "3,225,1,225,6,6,1100,1,238,225,104,0,101,14,135,224,101,-69,224,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,102,90,169,224,1001,224,-4590,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1102,90,45,224,1001,224,-4050,224,4,224,102,8,223,223,101,5,224,224,1,224,223,223,1001,144,32,224,101,-72,224,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,36,93,225,1101,88,52,225,1002,102,38,224,101,-3534,224,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,1102,15,57,225,1102,55,49,225,1102,11,33,225,1101,56,40,225,1,131,105,224,101,-103,224,224,4,224,102,8,223,223,1001,224,2,224,1,224,223,223,1102,51,39,225,1101,45,90,225,2,173,139,224,101,-495,224,224,4,224,1002,223,8,223,1001,224,5,224,1,223,224,223,1101,68,86,224,1001,224,-154,224,4,224,102,8,223,223,1001,224,1,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,108,226,677,224,1002,223,2,223,1006,224,329,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,344,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,359,1001,223,1,223,107,226,677,224,1002,223,2,223,1005,224,374,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,389,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,404,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,419,101,1,223,223,1007,677,226,224,1002,223,2,223,1006,224,434,101,1,223,223,1107,226,226,224,1002,223,2,223,1006,224,449,101,1,223,223,8,677,226,224,102,2,223,223,1006,224,464,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,479,1001,223,1,223,1007,677,677,224,102,2,223,223,1005,224,494,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,509,101,1,223,223,1008,677,677,224,102,2,223,223,1005,224,524,1001,223,1,223,107,226,226,224,1002,223,2,223,1005,224,539,101,1,223,223,7,226,226,224,102,2,223,223,1005,224,554,101,1,223,223,1108,226,677,224,1002,223,2,223,1006,224,569,1001,223,1,223,107,677,677,224,102,2,223,223,1005,224,584,101,1,223,223,7,677,226,224,1002,223,2,223,1005,224,599,101,1,223,223,108,226,226,224,1002,223,2,223,1005,224,614,101,1,223,223,1008,677,226,224,1002,223,2,223,1005,224,629,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,644,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,659,1001,223,1,223,8,226,677,224,102,2,223,223,1006,224,674,1001,223,1,223,4,223,99,226"

    computer = {i: int(c) for i, c in enumerate(code.split(","))}
    pos = 0

    opcode = computer[pos] % 100
    mode = list(str(1000 + computer[pos] // 100))[1:]
    mode.reverse()

    while computer[pos] != 99:
        opcode = computer[pos] % 100
        mode = [int(i) for i in str(1000 + computer[pos] // 100)][1:]
        mode.reverse()
        if mode[2] == 1:
            print("WRONGE MODE")
            break
        if opcode == 1:
            par1 = computer[pos + 1] if mode[0] else computer[computer[pos + 1]]
            par2 = computer[pos + 2] if mode[1] else computer[computer[pos + 2]]
            write_pos = computer[pos + 3]
            print(
                f"{pos:>5} - {computer[pos]:>10} {opcode:>5}    {mode} "
                f"- {par1:>7} {par2:>7} , write_pos: {write_pos:>7} "
            )
            computer[write_pos] = par1 + par2
            print(f"                            result: {computer[write_pos]}")
            pos += 4
        elif opcode == 2:
            par1 = computer[pos + 1] if mode[0] else computer[computer[pos + 1]]
            par2 = computer[pos + 2] if mode[1] else computer[computer[pos + 2]]
            write_pos = computer[pos + 3]
            print(
                f"{pos:>5} - {computer[pos]:>10} {opcode:>5}    {mode} "
                f"- {par1:>7} {par2:>7} , write_pos: {write_pos:>7} "
            )
            computer[write_pos] = par1 * par2
            print(f"                            result: {computer[write_pos]}")
            pos += 4
        elif opcode == 3:
            write_pos = computer[pos + 1]
            print(
                f"{pos:>5} - {computer[pos]:>10} {opcode:>5}    {mode} "
                f"-                 , write_pos: {write_pos:>7} "
            )
            computer[write_pos] = system_id
            print(f"                            result: {computer[write_pos]}")
            pos += 2
        elif opcode == 4:
            par1 = computer[pos + 1] if mode[0] else computer[computer[pos + 1]]
            print(
                f"{pos:>5} - {computer[pos]:>10} {opcode:>5}    {mode} "
                f"- {par1:>7}                "
            )
            print(par1)
            pos += 2
        elif opcode == 5:
            par1 = computer[pos + 1] if mode[0] else computer[computer[pos + 1]]
            par2 = computer[pos + 2] if mode[1] else computer[computer[pos + 2]]
            if par1:
                pos = par2
            else:
                pos += 3
        elif opcode == 6:
            par1 = computer[pos + 1] if mode[0] else computer[computer[pos + 1]]
            par2 = computer[pos + 2] if mode[1] else computer[computer[pos + 2]]
            if not par1:
                pos = par2
            else:
                pos += 3
        elif opcode == 7:
            par1 = computer[pos + 1] if mode[0] else computer[computer[pos + 1]]
            par2 = computer[pos + 2] if mode[1] else computer[computer[pos + 2]]
            write_pos = computer[pos + 3]
            computer[write_pos] = 1 if par1 < par2 else 0
            pos += 4
        elif opcode == 8:
            par1 = computer[pos + 1] if mode[0] else computer[computer[pos + 1]]
            par2 = computer[pos + 2] if mode[1] else computer[computer[pos + 2]]
            write_pos = computer[pos + 3]
            computer[write_pos] = 1 if par1 == par2 else 0
            pos += 4
        else:
            print("WRONG")
            print(computer[pos])
            break

    print("Success")
    # print(computer.values())
    return computer[0]


run(5)
