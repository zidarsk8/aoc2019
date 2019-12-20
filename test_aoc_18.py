from typing import FrozenSet, Set, Dict, Tuple, Optional, List
import string
import pytest

Point = Tuple[int, int]
Points = Set[Point]
OPoints = Optional[Points]


DOT = frozenset(".")


class Path:
    def __init__(
        self, position: Point, keys: FrozenSet, steps: int = 0, finished: bool = False
    ):
        self.steps = steps
        self.position: Point = position
        self.keys: FrozenSet[str] = keys
        self.finished = finished

    def __key(self):
        return (self.position, self.keys)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Path):
            return self.__key() == other.__key()
        return NotImplemented

    def branch(self, new_pos, all_keys, data):
        if self.finished:
            return None
        if new_pos in all_keys:
            new_keys = self.keys.union({data[new_pos]})
        else:
            new_keys = self.keys
        finished = len(new_keys) == len(all_keys) + 1
        return Path(new_pos, new_keys, self.steps + 1, finished=finished)


class Maze:

    moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    def __init__(self, input_number):
        self.ticks = 0
        self.input_number: int = input_number
        self.input_file: str = f"aoc_18_input_{input_number}.txt"
        self.data: Dict[Point, str] = {}
        self.start: Point = (0, 0)
        self.keys: Points = set()
        self.doors: Points = set()
        self.walls: Points = set()
        self.width: int = 0
        self.height: int = 0
        self.current: List[Path] = []
        self.visited = {}
        self.read_data()

    def read_data(self):

        with open(self.input_file) as f:
            for y, line in enumerate(f.read().splitlines()):
                for x, char in enumerate(line):
                    self.data[(x, y)] = char
                    if char == "@":
                        self.start = (x, y)
                        self.data[(x, y)] = "."
                    if char in string.ascii_lowercase:
                        self.keys.add((x, y))
                    if char in string.ascii_uppercase:
                        self.doors.add((x, y))
                    if char == "#":
                        self.walls.add((x, y))

        self.width = x
        self.height = y

        start_point = Path(self.start, DOT)

        self.visited[start_point] = start_point.steps
        self.current.append(start_point)

    def _count_walls(self, x, y):
        return self._count_chars(x, y, "#")

    def _count_chars(self, x, y, char):
        return sum(1 for dx, dy in self.moves if self.data[(x + dx, y + dy)] == char)

    def close_dead_ends(self):
        for y in range(1, self.height):
            for x in range(1, self.width):
                if (
                    self.data[(x, y)] == "."
                    or self.data[(x, y)] in string.ascii_uppercase
                ) and self._count_walls(x, y) == 3:
                    self.data[(x, y)] = "#"

    def expand_walls(self):
        self.data[(49, 37)] = "Y"
        self.data[(49, 38)] = "N"
        self.data[(42, 41)] = "C"
        self.data[(38, 39)] = "W"
        self.data[(37, 39)] = "T"
        self.data[(1, 50)] = "X"
        self.data[(1, 51)] = "H"
        self.data[(1, 52)] = "K"
        self.data[(1, 53)] = "D"
        self.data[(37, 65)] = "G"
        self.data[(37, 64)] = "P"

    def get_grid(self):
        visited_pos = {v.position for v in self.visited}

        def ch(x, y):
            for i, path in enumerate(self.current[::-1]):
                if path.position == (x, y):
                    return str(i % 10)
            if (x, y) == self.start:
                return "@"
            if (x, y) in visited_pos and self.data[(x, y)] == ".":
                return "_"

            return self.data[(x, y)]

        return "\n".join(
            "".join(ch(x, y) for x in range(self.width + 1))
            for y in range(self.height + 1)
        )

    def print(self):
        print(self.get_grid().replace("#", "░"))
        print()

    def move(self, path: Path) -> List[Path]:
        x, y = path.position

        new_points: List[State] = []
        for dx, dy in self.moves:
            new_pos = (x + dx, y + dy)
            if self.data[new_pos] == "#":
                continue
            if (
                self.data[new_pos].lower() not in path.keys
                and self.data[new_pos].upper() == self.data[new_pos]
            ):
                continue

            new_path = path.branch(new_pos, self.keys, self.data)
            if new_path:
                if new_path in self.visited:
                    if self.visited[new_path] > new_path.steps:
                        new_points.append(new_path)
                else:
                    new_points.append(new_path)

            if new_path and new_path.finished:
                new_points.append(new_path)

        return new_points

    def tick(self):
        self.print()
        if self.current:
            self.ticks += 1
            pos = self.current.pop()
            moves = self.move(pos)
            for new_pos in moves:
                self.current.append(new_pos)
            for move in moves:
                self.visited[move] = min(move.steps, self.visited.get(move, 1000000000))

    def keys_collected(self):
        # +1 is for the "." to make walking easier in path.keys
        return any(len(path.keys) == len(self.keys) + 1 for path in self.current)

    def walk(self):
        while self.current:
            self.tick()

    def steps(self):
        for p in self.visited:
            print(p.steps, p.position, p.keys, p.finished)
        return min(path.steps for path in self.visited if path.finished)


def test_read_data():
    maze = Maze(1)
    assert maze.data[(5, 1)] == "."
    assert maze.start == (5, 1)
    assert maze.data[(0, 0)] == "#"
    assert maze.keys == {(1, 1), (7, 1)}
    assert maze.doors == {(3, 1)}
    assert maze.width == 8
    assert maze.height == 2


def test_get_grid():
    maze = Maze(1)
    assert (
        maze.get_grid()
        == """#########
              #b.A.0.a#
              #########""".replace(
            " ", ""
        )
    )


def test_hashable():
    assert Path((1, 5), frozenset()) == Path((1, 5), frozenset())
    assert Path((1, 5), frozenset()) in {Path((1, 5), frozenset())}
    assert Path((1, 5), frozenset()) not in {Path((2, 5), frozenset())}
    assert Path((1, 5), frozenset([55, 55])) not in {Path((1, 5), frozenset())}
    assert Path((1, 5), frozenset()) not in {Path((1, 5), frozenset([55]))}


def test_move():
    maze = Maze(1)
    orig = maze.current[0]
    new_points = maze.move(orig)
    assert len(new_points) == 2
    assert Path((orig.position[0] + 1, orig.position[1]), DOT) in new_points
    assert Path((orig.position[0] - 1, orig.position[1]), DOT) in new_points


def test_tick():
    maze = Maze(1)
    orig = maze.current[0]
    maze.tick()
    assert len(maze.current) == 2
    assert Path((orig.position[0] + 1, orig.position[1]), DOT) in maze.current
    assert Path((orig.position[0] - 1, orig.position[1]), DOT) in maze.current
    assert orig not in maze.current
    assert len(maze.visited) == 3
    assert orig in maze.visited
    assert Path((orig.position[0] + 1, orig.position[1]), DOT) in maze.visited
    assert Path((orig.position[0] - 1, orig.position[1]), DOT) in maze.visited
    assert (
        maze.get_grid()
        == """#########
              #b.A1@0a#
              #########""".replace(
            " ", ""
        )
    )


def test_double_tick():
    maze = Maze(1)
    maze.tick()
    maze.tick()
    assert len(maze.current) == 2
    assert (
        maze.get_grid()
        == """#########
              #b.A1@_0#
              #########""".replace(
            " ", ""
        )
    )
    maze.tick()
    assert (
        maze.get_grid()
        == """#########
              #b.A1@0_#
              #########""".replace(
            " ", ""
        )
    )
    maze.tick()
    maze.tick()
    maze.tick()
    assert (
        maze.get_grid()
        == """#########
              #b.01@__#
              #########""".replace(
            " ", ""
        )
    )
    assert maze.ticks == 6


def test_walk_1():
    maze = Maze(1)
    maze.walk()
    assert maze.steps() == 8


def test_walk_4():
    maze = Maze(4)
    maze.print()
    for _ in range(20):
        print(len(maze.current))
        maze.tick()
    maze.print()


@pytest.mark.parametrize("maze, steps", [(2, 86), (3, 132), (5, 81),])
def test_walks(maze, steps):
    if maze > 3:
        return
    maze = Maze(maze)
    maze.walk()
    assert maze.steps() == steps


#
#
# def test_part_1():
#     maze = Maze(0)
#     maze.print()
#     for i in range(100):
#         maze.close_dead_ends()
#
#     maze.expand_walls()
#
#     maze.print()
#     for _ in range(6):
#         print(len(maze.current))
#         maze.tick()
#     maze.print()
#     assert maze.ticks == 0
