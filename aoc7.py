code = "3,8,1001,8,10,8,105,1,0,0,21,34,59,76,101,114,195,276,357,438,99999,3,9,1001,9,4,9,1002,9,4,9,4,9,99,3,9,102,4,9,9,101,2,9,9,102,4,9,9,1001,9,3,9,102,2,9,9,4,9,99,3,9,101,4,9,9,102,5,9,9,101,5,9,9,4,9,99,3,9,102,2,9,9,1001,9,4,9,102,4,9,9,1001,9,4,9,1002,9,3,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99"

code = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"

amplifiers = {
    amp: {"code": {i: int(c) for i, c in enumerate(code.split(","))}, "pos": 0}
    for amp in ["A", "B", "C", "D", "E"]
}


def run_system(amplifier, phase_setting, input_signal):
    computer = amplifiers[amplifier]["code"]

    pos = amplifiers[amplifier]["pos"]

    opcode = computer[pos] % 100
    mode = list(str(1000 + computer[pos] // 100))[1:]
    mode.reverse()

    inputs = [input_signal, phase_setting]
    output = 0

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
            # print(
            #     f"{pos:>5} - {computer[pos]:>10} {opcode:>5}    {mode} "
            #     f"- {par1:>7} {par2:>7} , write_pos: {write_pos:>7} "
            # )
            computer[write_pos] = par1 + par2
            # print(f"                            result: {computer[write_pos]}")
            pos += 4
        elif opcode == 2:
            par1 = computer[pos + 1] if mode[0] else computer[computer[pos + 1]]
            par2 = computer[pos + 2] if mode[1] else computer[computer[pos + 2]]
            write_pos = computer[pos + 3]
            # print(
            #     f"{pos:>5} - {computer[pos]:>10} {opcode:>5}    {mode} "
            #     f"- {par1:>7} {par2:>7} , write_pos: {write_pos:>7} "
            # )
            computer[write_pos] = par1 * par2
            # print(f"                            result: {computer[write_pos]}")
            pos += 4
        elif opcode == 3:
            write_pos = computer[pos + 1]
            # print(
            #     f"{pos:>5} - {computer[pos]:>10} {opcode:>5}    {mode} "
            #     f"-                 , write_pos: {write_pos:>7} "
            # )
            computer[write_pos] = inputs.pop()
            # print(f"                            result: {computer[write_pos]}")
            pos += 2
        elif opcode == 4:
            par1 = computer[pos + 1] if mode[0] else computer[computer[pos + 1]]
            # print(
            #     f"{pos:>5} - {computer[pos]:>10} {opcode:>5}    {mode} "
            #     f"- {par1:>7}                "
            # )
            print(par1)
            output = par1
            inputs.insert(0, output)
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
    return output


# import itertools
#
# order_max = []
# for order in itertools.permutations(range(5)):
#     previous = 0
#     for phase_setting in order:
#         previous = run_system(phase_setting, previous)
#         print(previous)
#     order_max.append(previous)
#
#
# print(max(order_max))


seq = [9, 7, 8, 5, 6]

previous_value = 0
import ipdb

ipdb.set_trace()
for i in range(2):
    for amp, s in zip(amplifiers, seq):
        previous_value = run_system(amp, s, previous_value)
        print(f"{amp:>5} {s:>5}  {previous_value:>10}")
