import collections
import itertools
from typing import Callable
from typing import Dict
from typing import DefaultDict
from typing import List
from typing import Optional

puzzle_input_2: str = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,19,9,23,1,23,13,27,1,10,27,31,2,31,13,35,1,10,35,39,2,9,39,43,2,43,9,47,1,6,47,51,1,10,51,55,2,55,13,59,1,59,10,63,2,63,13,67,2,67,9,71,1,6,71,75,2,75,9,79,1,79,5,83,2,83,13,87,1,9,87,91,1,13,91,95,1,2,95,99,1,99,6,0,99,2,14,0,0"


puzzle_input_5: str = "3,225,1,225,6,6,1100,1,238,225,104,0,101,14,135,224,101,-69,224,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,102,90,169,224,1001,224,-4590,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1102,90,45,224,1001,224,-4050,224,4,224,102,8,223,223,101,5,224,224,1,224,223,223,1001,144,32,224,101,-72,224,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,36,93,225,1101,88,52,225,1002,102,38,224,101,-3534,224,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,1102,15,57,225,1102,55,49,225,1102,11,33,225,1101,56,40,225,1,131,105,224,101,-103,224,224,4,224,102,8,223,223,1001,224,2,224,1,224,223,223,1102,51,39,225,1101,45,90,225,2,173,139,224,101,-495,224,224,4,224,1002,223,8,223,1001,224,5,224,1,223,224,223,1101,68,86,224,1001,224,-154,224,4,224,102,8,223,223,1001,224,1,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,108,226,677,224,1002,223,2,223,1006,224,329,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,344,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,359,1001,223,1,223,107,226,677,224,1002,223,2,223,1005,224,374,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,389,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,404,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,419,101,1,223,223,1007,677,226,224,1002,223,2,223,1006,224,434,101,1,223,223,1107,226,226,224,1002,223,2,223,1006,224,449,101,1,223,223,8,677,226,224,102,2,223,223,1006,224,464,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,479,1001,223,1,223,1007,677,677,224,102,2,223,223,1005,224,494,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,509,101,1,223,223,1008,677,677,224,102,2,223,223,1005,224,524,1001,223,1,223,107,226,226,224,1002,223,2,223,1005,224,539,101,1,223,223,7,226,226,224,102,2,223,223,1005,224,554,101,1,223,223,1108,226,677,224,1002,223,2,223,1006,224,569,1001,223,1,223,107,677,677,224,102,2,223,223,1005,224,584,101,1,223,223,7,677,226,224,1002,223,2,223,1005,224,599,101,1,223,223,108,226,226,224,1002,223,2,223,1005,224,614,101,1,223,223,1008,677,226,224,1002,223,2,223,1005,224,629,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,644,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,659,1001,223,1,223,8,226,677,224,102,2,223,223,1006,224,674,1001,223,1,223,4,223,99,226"


class Intcode:
    def __init__(self, program: str):
        self.program = program
        self.ram: DefaultDict[int, int] = collections.defaultdict(
            int, dict(enumerate(int(i) for i in program.split(",")))
        )
        self.position = 0
        self.running: bool = True
        self.finished: bool = False
        self._next_input: Optional[int] = None
        self._outputs: List[int] = []
        self.relative_base = 0

    def reset(self):
        self.ram: Dict[int, int] = dict(
            enumerate(int(i) for i in self.program.split(","))
        )
        self.position = 0
        self.running = True
        self._next_input = None

    def par_pos(self, parameter):
        if self.mode[parameter - 1] == 2:
            return self.ram[self.position + parameter] + self.relative_base
        else:
            return self.ram[self.position + parameter]

    def parameter(self, parameter: int, mode: int = 0) -> int:
        if self.mode[parameter - 1] == 1:
            return self.ram[self.position + parameter]

        return self.ram[self.par_pos(parameter)]

    def add(self) -> None:  # 1
        self.ram[self.par_pos(3)] = self.parameter(1) + self.parameter(2)
        self.position += 4

    def mul(self) -> None:  # 2
        self.ram[self.par_pos(3)] = self.parameter(1) * self.parameter(2)
        self.position += 4

    def read(self) -> None:  # 3
        if self._next_input is None:
            self.running = False
            return
        self.ram[self.par_pos(1)] = self._next_input
        self._next_input = None
        self.position += 2

    def write(self) -> int:  # 4
        output = self.parameter(1)
        self._outputs.append(output)
        self.position += 2
        return output

    def jt(self) -> None:  # 5
        par1 = self.parameter(1)
        par2 = self.parameter(2)
        if par1:
            self.position = par2
        else:
            self.position += 3

    def jf(self) -> None:  # 6
        par1 = self.parameter(1)
        par2 = self.parameter(2)
        if not par1:
            self.position = par2
        else:
            self.position += 3

    def lt(self) -> None:  # 7
        self.ram[self.par_pos(3)] = int(self.parameter(1) < self.parameter(2))
        self.position += 4

    def eq(self) -> None:  # 8
        self.ram[self.par_pos(3)] = int(self.parameter(1) == self.parameter(2))
        self.position += 4

    def set_relative_base(self) -> None:  # 9
        self.relative_base += self.parameter(1)
        self.position += 2

    def stop(self) -> int:  # 99
        self.running = False
        self.finished = True
        return self._outputs[-1] if self._outputs else self.ram[0]

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
            9: self.set_relative_base,
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

    def run_partial(self, next_input: Optional[int] = None):
        """Run the intcode computer until the first output."""
        self._next_input = next_input
        self.running = True
        while self.running:
            result = self.commands[self.current_code]()
            if result is not None:
                return result, self.running

    def run(self, next_input: Optional[int] = None):
        """Run the intcode computer until it finishes and return the last output."""
        while self.running:
            result, _ = self.run_partial(next_input)
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

    @property
    def outputs(self) -> str:
        return ",".join(str(i) for i in self._outputs)

    def print_stack(self):
        for i in range(min(self.ram), max(self.ram) + 1):
            print(f"{i:>10}: {self.ram[i]:>10}")


class IntMainframe:
    def __init__(self, program: str, amp_count: int):
        self.program = program
        self.amps: List[Intcode] = []
        self.init_amps(amp_count)

    def reset(self):
        self.init_amps(len(self.amps))

    def init_amps(self, amp_count: int) -> None:
        self.amps = [Intcode(self.program) for _ in range(amp_count)]

    def run_chain(self, phase_settings):
        last_output = 0
        for amp, phase_setting in zip(self.amps, phase_settings):
            amp.run_partial(phase_setting)
            last_output, _ = amp.run_partial(last_output)
        return last_output

    def get_max_sequence(self, phase_settings):

        max_phase_setting: List[int] = []
        max_result: int = 0
        for phase_setting in itertools.permutations(phase_settings):
            self.reset()
            result = self.run_chain(phase_setting)
            if result > max_result:
                max_result = result
                max_phase_setting = phase_setting

        return max_result, list(max_phase_setting)

    def run_loop(self, phase_settings):
        last_output = 0

        for amp, phase_setting in zip(self.amps, phase_settings):
            amp.run_partial(phase_setting)
            last_output, _ = amp.run_partial(last_output)
        while not self.amps[-1].finished:
            for amp, phase_setting in zip(self.amps, phase_settings):
                last_output, _ = amp.run_partial(last_output)
        return last_output

    def get_max_loop(self, phase_settings):

        max_phase_setting: List[int] = []
        max_result: int = 0
        for phase_setting in itertools.permutations(phase_settings):
            self.reset()
            result = self.run_loop(phase_setting)
            if result > max_result:
                max_result = result
                max_phase_setting = phase_setting

        return max_result, list(max_phase_setting)
