import string
import collections
import heapq


class Vertex:
    def __init__(self, node, pos=None, dl=0):
        self.pos = pos
        self.id = node
        self.adjacent = {}
        self.distance = 100000000
        self.previous = None
        self.dl = dl

    def __str__(self):
        return f"{self.id} {self.previous and self.previous.id} {self.distance} adjacent: {[x.id for x in self.adjacent]}"

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def get_adjacent_repr(self):
        return {k.id: v for k, v in self.adjacent.items()}

    def __gt__(self, other):
        return self.distance > other.distance


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node, pos=None, dl=0):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node, pos, dl)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, vertex_id: str) -> Vertex:
        return self.vert_dict[vertex_id]

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()


class Maze:
    moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    def __init__(self, input_number):
        self.current = set()
        self.visited = set()
        self.input_file: str = f"aoc_20_input_{input_number}.txt"
        self.data: Dict[Point, str] = {}
        self.width = 0
        self.height = 0
        self.read_data()
        self.close_dead_ends()
        self.thickness = self.get_maze_thickness()
        self.portals: Dict[str, Tuple[int, int]] = self.all_portals()
        self.portal_map: Dict[Tuple[int, int], str] = {
            v: k for k, v in self.portals.items()
        }

    def get_maze_thickness(self):
        if not self.data:
            return 0

        for i in range(2, self.height // 2):
            if self.data[(i, i)] != "#":
                break

        return i - 2

    def read_data(self):

        with open(self.input_file) as f:
            for y, line in enumerate(f.read().splitlines()):
                for x, char in enumerate(line):
                    self.data[(x, y)] = char

        self.width = x
        self.height = y

    def _count_walls(self, x, y):
        return self._count_chars(x, y, "#")

    def _count_chars(self, x, y, char):
        return sum(1 for dx, dy in self.moves if self.data[(x + dx, y + dy)] == char)

    def close_dead_ends(self):
        grid = ""
        new_grid = self.get_grid()
        while grid != new_grid:
            grid = new_grid
            for _ in range(10):
                self._close_wall_step()
            new_grid = self.get_grid()

    def _close_wall_step(self):
        for y in range(1, self.height):
            for x in range(1, self.width):
                if self._count_walls(x, y) == 3:
                    self.data[(x, y)] = "#"

    def get_grid(self):
        def ch(x, y):
            if (x, y) in self.current:
                return "*"
            if (x, y) in self.visited:
                return " "
            return self.data[(x, y)]

        return "\n".join(
            "".join(ch(x, y) for x in range(self.width + 1))
            for y in range(self.height + 1)
        )

    def print(self):
        print(self.get_grid().replace("#", "░"))
        print()

    def _add_graph_vertices(self, g):
        for portal, pos in self.portals.items():
            g.add_vertex(portal, pos)
        return g

    def _get_possible_steps(self, position):
        x, y = position
        return [
            (x + dx, y + dy)
            for dx, dy in self.moves
            if self.data[(x + dx, y + dy)] == "."
        ]

    def _walk_from_portal(self, start_position):
        visited_portals = {}
        self.current = {start_position}
        self.visited = {start_position}
        steps = 0
        while self.current:
            possible_positions = set(
                sum([self._get_possible_steps(cur) for cur in self.current], [])
            )
            self.visited = self.visited.union(self.current)
            self.current = possible_positions.difference(self.visited)
            steps += 1
            for pos in self.current:
                if pos in self.portal_map:
                    visited_portals[self.portal_map[pos]] = (steps, pos)
            # print(steps)
            # self.print()
        self.visited = set()
        self.current = set()
        return visited_portals

    def _add_graph_edges(self, g):
        for portal, position in self.portals.items():
            visited_portals = self._walk_from_portal(position)
            for visited_portal, dist_pos in visited_portals.items():
                distance, _ = dist_pos
                g.add_edge(portal, visited_portal, cost=distance)

        for portal in self.portals:
            base = portal[:2]
            p1, p2 = f"{base}o", f"{base}i"
            if p1 in self.portals and p2 in self.portals:
                g.add_edge(f"{base}o", f"{base}i", 1)
        return g

    def to_graph(self):
        g = Graph()
        g = self._add_graph_vertices(g)
        g = self._add_graph_edges(g)

        return g

    def _find_dot_around(self, x, y):
        for dx, dy in self.moves:
            if self.data.get((x + dx, y + dy), "") == ".":
                return (x + dx, y + dy)

    def _get_portal_position(self, x1, y1, x2, y2):
        return self._find_dot_around(x1, y1) or self._find_dot_around(x2, y2)

    def _get_portal_name(self, x1, y1, x2, y2):
        chars = self.data[(x1, y1)] + self.data[(x2, y2)]
        rim = "i" if 3 < x1 < self.width - 3 and 3 < y1 < self.height - 3 else "o"
        return chars + rim

    def all_portals(self):
        portals = {}
        for x in range(self.width):
            for y in range(self.height):
                if (
                    self.data[(x, y)] in string.ascii_uppercase
                    and self.data[(x + 1, y)] in string.ascii_uppercase
                ):
                    portal_name = self._get_portal_name(x, y, x + 1, y)
                    portal_position = self._get_portal_position(x, y, x + 1, y)

                    portals[portal_name] = portal_position
                if (
                    self.data[(x, y)] in string.ascii_uppercase
                    and self.data[(x, y + 1)] in string.ascii_uppercase
                ):
                    portal_name = self._get_portal_name(x, y, x, y + 1)
                    portal_position = self._get_portal_position(x, y, x, y + 1)
                    portals[portal_name] = portal_position
        return portals

    def _dl(self, pos):
        return -1 if min(pos) < 3 or max(pos) > self.width - 3 else 1


def dikstra(g: Graph, frm, to):
    print("Dikstra")
    distances = 1000000000000
    frm = g.get_vertex(frm)
    to = g.get_vertex(to)
    frm.distance = 0
    unvisited: List[Vertex] = list(g.vert_dict.values())
    heapq.heapify(unvisited)

    while unvisited:
        closest: Vertex = heapq.heappop(unvisited)
        for neighbor, distance in closest.adjacent.items():
            alt = closest.distance + distance
            if neighbor.distance > alt:
                neighbor.distance = alt
                neighbor.previous = closest
        heapq.heapify(unvisited)


def test_dikstra_1():
    maze = Maze(1)
    g = maze.to_graph()
    dikstra(g, "AAo", "ZZo")
    assert g.get_vertex("ZZo").distance == 23


def test_dikstra_2():
    maze = Maze(2)
    g = maze.to_graph()
    dikstra(g, "AAo", "ZZo")
    assert g.get_vertex("ZZo").distance == 58


def test_dikstra():
    maze = Maze(0)
    g = maze.to_graph()
    dikstra(g, "AAo", "ZZo")
    assert g.get_vertex("ZZo").distance == 578


def test_graph():
    g = Graph()

    g.add_vertex("a")
    g.add_vertex("b")
    g.add_vertex("c")
    g.add_vertex("d")
    g.add_vertex("e")
    g.add_vertex("f")

    g.add_edge("a", "b", 7)
    g.add_edge("a", "c", 9)
    g.add_edge("a", "f", 14)
    g.add_edge("b", "c", 10)
    g.add_edge("b", "d", 15)
    g.add_edge("c", "d", 11)
    g.add_edge("c", "f", 2)
    g.add_edge("d", "e", 6)
    g.add_edge("e", "f", 9)

    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print("( %s , %s, %3d)" % (vid, wid, v.get_weight(w)))

    for v in g:
        print("g.vert_dict[%s]=%s" % (v.get_id(), g.vert_dict[v.get_id()]))
    assert g.vert_dict["a"].get_adjacent_repr() == {"b": 7, "c": 9, "f": 14}


def test_maze_thickness():
    maze = Maze(2)
    assert maze.thickness == 7
    maze = Maze(1)
    assert maze.thickness == 5
    maze = Maze(3)
    assert maze.thickness == 5
    # maze = Maze(0)
    # assert maze.thickness == 31


def test_maze_to_graph_2():
    maze = Maze(2)
    maze.print()
    g = maze.to_graph()
    assert set(g.vert_dict.keys()) == {
        "AAo",
        "ASo",
        "ASi",
        "BUo",
        "BUi",
        "CPo",
        "CPi",
        "DIo",
        "DIi",
        "JOo",
        "JOi",
        "JPo",
        "JPi",
        "LFo",
        "LFi",
        "QGo",
        "QGi",
        "VTo",
        "VTi",
        "YNo",
        "YNi",
        "ZZo",
    }
    print(maze.portals)
    assert set(maze.portals) == set(g.vert_dict.keys())


def test_graph_edges():
    maze = Maze(1)
    maze.print()
    g = maze.to_graph()
    assert "ZZo" in {v.id for v in g.vert_dict["AAo"].adjacent}
    assert g.vert_dict["AAo"].adjacent[g.get_vertex("ZZo")] == 26
    assert g.vert_dict["ZZo"].adjacent[g.get_vertex("AAo")] == 26

    assert g.vert_dict["AAo"].adjacent[g.get_vertex("BCi")] == 4
    assert g.vert_dict["BCi"].adjacent[g.get_vertex("AAo")] == 4

    assert g.vert_dict["BCo"].adjacent[g.get_vertex("DEi")] == 6
    assert g.vert_dict["DEi"].adjacent[g.get_vertex("BCo")] == 6

    assert g.vert_dict["FGo"].adjacent[g.get_vertex("DEo")] == 4

    assert g.vert_dict["FGi"].adjacent[g.get_vertex("ZZo")] == 6


def test_maze_to_graph():
    # maze = Maze(0)
    # g = maze.to_graph()
    # assert set(maze.portals) == set(g.vert_dict.keys())
    maze = Maze(1)
    g = maze.to_graph()
    assert set(maze.portals) == set(g.vert_dict.keys())
    maze = Maze(2)
    g = maze.to_graph()
    assert set(maze.portals) == set(g.vert_dict.keys())


def test_read_data():
    maze = Maze(1)
    maze.print()
