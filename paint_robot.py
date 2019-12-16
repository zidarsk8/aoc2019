from typing import DefaultDict, Tuple, Set
import collections
from .intcode_pc import Intcode


class Robot:
    direction_marker = {0: "^", 1: ">", 2: "v", 3: "<"}
    directions = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}

    def __init__(self, robot_brain: str):
        self.panel: DefaultDict[Tuple[int, int], str] = collections.defaultdict(
            lambda: "."
        )
        self.panel[(0, 0)] = "."
        self.robot_brain: str = robot_brain
        self.position: Tuple[int, int] = (0, 0)
        self.direction: int = 0  # 0 up 1 right 2 down 3 left
        self.brain: Intcode = Intcode(robot_brain)
        self.painted: Set[Tuple[int, int]] = {(0, 0)}

    def single_step(self):
        paint, running = self.brain.run_partial(int(self.panel[self.position] == "#"))
        if not running:
            return False
        turn, running = self.brain.run_partial()
        self.painted.add(self.position)
        self.panel[self.position] = "#" if paint else "."
        self.direction = (self.direction + (turn * 2 - 1)) % 4
        delta = self.directions[self.direction]
        self.position = (self.position[0] + delta[0], self.position[1] + delta[1])
        return running

    def run_robot(self):
        for i in range(10000):
            running = self.single_step()
            if not running:
                break

    def get_panel(self, show_robot=True):
        min_x = min(x for x, y in self.painted) - 3
        max_x = max(x for x, y in self.painted) + 3
        min_y = min(y for x, y in self.painted) - 3
        max_y = max(y for x, y in self.painted) + 3

        def get_char(x, y):
            if (x, y) == self.position and show_robot:
                return self.direction_marker[self.direction]
            return self.panel[(x, y)]

        return "\n".join(
            ("".join(get_char(x, y) for x in range(min_x, max_x)))
            for y in range(max_y, min_y, -1)
        )

    def print_panel(self, show_robot=True):
        print(self.get_panel(show_robot))
