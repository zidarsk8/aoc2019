import math


class FuelCell:
    def __init__(self, part, generate_amount, input_cells):
        self.part = part
        self.generate_amount = generate_amount
        self.input_cells = input_cells
        self.multiplier = 0
        self.remaining = 0
        self.requirement = 0
        self.ore_required = 0

    def reset(self):
        self.multiplier = 0
        self.remaining = 0
        self.requirement = 0
        self.ore_required = 0

    def get(self, amount):
        pass

    @property
    def require_types(self):
        return [i[1] for i in self.input_cells]

    @property
    def quantity(self):
        return self.multiplier * self.generate_amount

    def add_requirement(self, amount):
        self.requirement += amount
        current_multiplier = math.ceil(
            max(0, (amount - self.remaining)) / self.generate_amount
        )
        self.multiplier += current_multiplier
        self.remaining = self.quantity - self.requirement

        for require_amount, require_type in self.input_cells:
            if require_type == "ORE":
                self.ore_required = require_amount * self.multiplier
            else:
                fuel_map[require_type].add_requirement(
                    require_amount * current_multiplier
                )

    def __str__(self):
        return (
            f"{self.part:>6}:    r: {self.requirement:>6}    m: {self.multiplier:>6}"
            f"    rem: {self.remaining:>6}    ore: {self.ore_required:>6}"
        )

    def print_map(self):
        for _, f in sorted(fuel_map.items()):
            print(f)


def _make_tuple(ore):
    ore = ore.strip().split()
    ore[0] = int(ore[0])
    return tuple(ore)


def parse_input(n):
    input_name = f"aoc14-{n}.txt"
    conversion = {}
    for line in open(input_name):
        if line.strip():
            ore_in, ore_out = line.strip().split("=>")
            conversion[_make_tuple(ore_out)] = [
                _make_tuple(part) for part in ore_in.split(",")
            ]
    return conversion


fuel_input = parse_input(0)
fuel_map = {f[1]: FuelCell(f[1], f[0], items) for f, items in fuel_input.items()}


def get_requirement(fuel):
    for fuel_cell in fuel_map.values():
        fuel_cell.reset()
    fuel_map["FUEL"].add_requirement(fuel)
    return sum(f.ore_required for f in fuel_map.values())


limit = 1000000000000
low = 1
high = limit
while low < high:
    middle = (high + low) // 2
    req = get_requirement(middle)
    print(f"{low:>15}  {high:>15}  {middle:>15} {req:>20}")
    if req > limit:
        low = middle
    else:
        high = middle
