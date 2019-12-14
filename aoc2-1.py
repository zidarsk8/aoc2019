from typing import List, Dict, Callable, Optional

puzzle_input_2 = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,19,9,23,1,23,13,27,1,10,27,31,2,31,13,35,1,10,35,39,2,9,39,43,2,43,9,47,1,6,47,51,1,10,51,55,2,55,13,59,1,59,10,63,2,63,13,67,2,67,9,71,1,6,71,75,2,75,9,79,1,79,5,83,2,83,13,87,1,9,87,91,1,13,91,95,1,2,95,99,1,99,6,0,99,2,14,0,0"


puzzle_input_5 = "3,225,1,225,6,6,1100,1,238,225,104,0,101,14,135,224,101,-69,224,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,102,90,169,224,1001,224,-4590,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1102,90,45,224,1001,224,-4050,224,4,224,102,8,223,223,101,5,224,224,1,224,223,223,1001,144,32,224,101,-72,224,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,36,93,225,1101,88,52,225,1002,102,38,224,101,-3534,224,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,1102,15,57,225,1102,55,49,225,1102,11,33,225,1101,56,40,225,1,131,105,224,101,-103,224,224,4,224,102,8,223,223,1001,224,2,224,1,224,223,223,1102,51,39,225,1101,45,90,225,2,173,139,224,101,-495,224,224,4,224,1002,223,8,223,1001,224,5,224,1,223,224,223,1101,68,86,224,1001,224,-154,224,4,224,102,8,223,223,1001,224,1,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,108,226,677,224,1002,223,2,223,1006,224,329,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,344,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,359,1001,223,1,223,107,226,677,224,1002,223,2,223,1005,224,374,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,389,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,404,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,419,101,1,223,223,1007,677,226,224,1002,223,2,223,1006,224,434,101,1,223,223,1107,226,226,224,1002,223,2,223,1006,224,449,101,1,223,223,8,677,226,224,102,2,223,223,1006,224,464,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,479,1001,223,1,223,1007,677,677,224,102,2,223,223,1005,224,494,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,509,101,1,223,223,1008,677,677,224,102,2,223,223,1005,224,524,1001,223,1,223,107,226,226,224,1002,223,2,223,1005,224,539,101,1,223,223,7,226,226,224,102,2,223,223,1005,224,554,101,1,223,223,1108,226,677,224,1002,223,2,223,1006,224,569,1001,223,1,223,107,677,677,224,102,2,223,223,1005,224,584,101,1,223,223,7,677,226,224,1002,223,2,223,1005,224,599,101,1,223,223,108,226,226,224,1002,223,2,223,1005,224,614,101,1,223,223,1008,677,226,224,1002,223,2,223,1005,224,629,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,644,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,659,1001,223,1,223,8,226,677,224,102,2,223,223,1006,224,674,1001,223,1,223,4,223,99,226"


class Intcode:
    def __init__(self, program: str):
        self.program = program
        self.ram: Dict[int, int] = dict(enumerate(int(i) for i in program.split(",")))
        self.position = 0
        self.running = True
        self.next_input = None
        self.outputs: List[int] = []

    def reset(self):
        self.ram: Dict[int, int] = dict(
            enumerate(int(i) for i in self.program.split(","))
        )
        self.position = 0
        self.running = True
        self.next_input = None

    def relative(self, relative: int, mode: int = 0) -> int:
        if self.mode[relative - 1]:
            return self.ram[self.position + relative]

        return self.ram[self.ram[self.position + relative]]

    def add(self) -> None:  # 1
        self.ram[self.ram[self.position + 3]] = self.relative(1) + self.relative(2)
        self.position += 4

    def mul(self) -> None:  # 2
        self.ram[self.ram[self.position + 3]] = self.relative(1) * self.relative(2)
        self.position += 4

    def read(self) -> None:  # 3
        if self.next_input is None:
            raise Exception("Missing input value")
        self.ram[self.ram[self.position + 1]] = self.next_input
        self.next_input = None
        self.position += 2

    def write(self) -> None:  # 4
        self.outputs.append(self.ram[self.ram[self.position + 1]])
        self.position += 2

    def jt(self) -> None:  # 5
        pass

    def jf(self) -> None:  # 6
        pass

    def lt(self) -> None:  # 7
        pass

    def eq(self) -> None:  # 8
        pass

    def stop(self) -> int:  # 99
        self.running = False
        return self.outputs[-1] if self.outputs else self.ram[0]

    @property
    def commands(self) -> Dict[int, Callable[[], Optional[int]]]:
        return {
            1: self.add,
            2: self.mul,
            3: self.read,
            4: self.write,
            5: self.jt,
            6: self.jf,
            7: self.lt,
            8: self.eq,
            99: self.stop,
        }

    @property
    def pos(self) -> int:
        return self.ram[self.position]

    @property
    def current_code(self) -> int:
        return self.pos % 100

    @property
    def mode(self) -> List[int]:
        return [
            self.pos % 1000 // 100,
            self.pos % 10000 // 1000,
            self.pos % 100000 // 10000,
        ]

    def run(self):
        while self.running:
            result = self.commands[self.current_code]()
            if result is not None:
                return result

    def set_program_state(self, program_state: int):
        self.ram[1] = program_state // 100
        self.ram[2] = program_state % 100

    def get_program_state(self, desired_result) -> int:
        for i in range(10000):
            self.reset()
            self.set_program_state(i)
            if self.run() == desired_result:
                return i
        return -1

    @property
    def state(self) -> str:
        return ",".join(str(v) for k, v in sorted(self.ram.items()))


### aoc 5


def test_mode():
    intcode = Intcode("2")
    assert intcode.mode == [0, 0, 0]
    intcode = Intcode("102")
    assert intcode.mode == [1, 0, 0]
    intcode = Intcode("101")
    assert intcode.mode == [1, 0, 0]
    intcode = Intcode("1002")
    assert intcode.mode == [0, 1, 0]
    intcode = Intcode("1102")
    assert intcode.mode == [1, 1, 0]


def test_instruction_mode():
    program = "1002,4,3,4,33"
    intcode = Intcode(program)
    intcode.run()
    assert intcode.state == "1002,4,3,4,99"


def test_day5_part_1():
    intcode = Intcode(puzzle_input_5)
    intcode.next_input = 1
    assert intcode.run() == 6731945


### aoc 2


def test_pos():
    program = "1,23,4501"
    intcode = Intcode(program)
    intcode.position = 2
    assert intcode.pos == 4501
    assert intcode.current_code == 1


def test_state():
    program = "1,2,3,4,5"
    intcode = Intcode(program)
    intcode.ram[1] = 55
    intcode.ram[4] = 0
    assert intcode.state == "1,55,3,4,0"


def test_intcode_init():
    program = "1,9,10,3,2,3,11,0,99,30,40,50"
    intcode = Intcode(program)
    assert intcode.position == 0
    assert intcode.ram
    assert intcode.run


def test_empty_run():
    intcode = Intcode("99")
    assert intcode.running
    intcode.run()
    assert not intcode.running


def test_add():
    intcode = Intcode("1,4,4,0,99")
    intcode.run()
    assert intcode.state == "198,4,4,0,99"


def test_mul():
    intcode = Intcode("2,4,4,0,99")
    intcode.run()
    assert intcode.state == "9801,4,4,0,99"


def test_first_program():
    program = "1,9,10,3,2,3,11,0,99,30,40,50"
    intcode = Intcode(program)
    intcode.run()
    assert intcode.state == "3500,9,10,70,2,3,11,0,99,30,40,50"


def test_part_1():
    intcode = Intcode(puzzle_input_2)
    intcode.set_program_state(1202)
    assert intcode.run() == 3085697


def test_part_2():
    intcode = Intcode(puzzle_input_2)
    assert intcode.get_program_state(19690720) == 9425