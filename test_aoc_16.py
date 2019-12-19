from typing import List
import math
import numpy as np
import pytest
import functools

fft = "59776034095811644545367793179989602140948714406234694972894485066523525742503986771912019032922788494900655855458086979764617375580802558963587025784918882219610831940992399201782385674223284411499237619800193879768668210162176394607502218602633153772062973149533650562554942574593878073238232563649673858167635378695190356159796342204759393156294658366279922734213385144895116649768185966866202413314939692174223210484933678866478944104978890019728562001417746656699281992028356004888860103805472866615243544781377748654471750560830099048747570925902575765054898899512303917159138097375338444610809891667094051108359134017128028174230720398965960712"
fftl = len(fft)

base_pattern = [0, 1, 0, -1]


def pattern_on(x, y):
    return base_pattern[(x + 1) // (y + 1) % 4]


def generate_pattern(y: int, length: int) -> List[int]:
    return [pattern_on(x, y) for x in range(length)]


def pattern_grid(number):
    length = len(str(number))
    return np.array([generate_pattern(y, length) for y in range(length)])


def single_phase(number, grid):
    numbers = [int(i) for i in str(number)]
    narr = np.array([numbers] * len(numbers))
    res = (narr * grid).sum(axis=1)
    return "".join(str(i)[-1] for i in res)


def run_phases(number: str, phases: int, return_value: List[int] = None) -> str:
    grid = pattern_grid(number)
    if return_value is not None:
        return_value.append(number)
    for i in range(phases):
        print(number)
        number = single_phase(number, grid)
        if return_value is not None:
            return_value.append(number)
    print(number)
    return number


def run_100(number):
    return run_phases(number, 100)[:8]


def get_pos(number, pos, phase):
    if pos == len(number) - 1:
        return number


@pytest.mark.parametrize(
    "position, length, output",
    [
        (0, 6, [1, 0, -1, 0, 1, 0]),
        (1, 10, [0, 1, 1, 0, 0, -1, -1, 0, 0, 1]),
        (2, 10, [0, 0, 1, 1, 1, 0, 0, 0, -1, -1]),
    ],
)
def test_generate_pattern_one(position, length, output):
    assert generate_pattern(position, length) == output


def test_generate_grid():
    grid = [
        [1, 0, -1, 0, 1, 0, -1, 0],
        [0, 1, 1, 0, 0, -1, -1, 0],
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1],
    ]
    assert pattern_grid(48226158).tolist() == grid


def test_phase_1():
    assert single_phase("12345678", pattern_grid("12345678")) == "48226158"
    assert single_phase("48226158", pattern_grid("48226158")) == "34040438"


def test_run_phases():
    assert run_phases("12345678", 1) == "48226158"
    assert run_phases("12345678", 3) == "03415518"
    assert run_phases("12345678", 4) == "01029498"


def test_run_100():
    assert run_100("80871224585914546619083218645595") == "24176176"
    assert run_100("19617804207202209144916044189917") == "73745418"
    assert run_100("69317163492948606335995924319873") == "52432133"


def test_part_1():
    # assert run_100(fft) == "89576828"
    pass


def test_partern_on():
    grid = pattern_grid("1234567890").tolist()
    for y, line in enumerate(grid):
        for x, value in enumerate(line):
            assert pattern_on(x, y) == value


def test_single_phase_double_input():
    # assert run_phases(fft * 4, 10)[-2:] == "48226158"
    pass


@functools.lru_cache(None)
def recursive(pos: int, phase: int, number: str, multiplier: int) -> int:
    if phase == 0:
        return int(number[pos % len(number)])
    partial_sums = 0
    for i in range(pos, len(number) * multiplier):
        pattern = pattern_on(i, pos)
        if not pattern:
            continue
        rec = recursive(i, phase - 1, number, multiplier)
        partial_sums += rec * pattern
        if phase == 2:
            print(phase, i, pos, rec, pattern_on(i, pos), partial_sums)
    return abs(partial_sums) % 10


def test_recursive_zero_phase():
    num = "75319024"
    for pos in range(200):
        assert recursive(pos, 0, num, 100) == int((num * 100)[pos])


def test_recursive_phase_1():
    multiplier = 2
    num = "12345"
    correct_result = run_phases(num * multiplier, 1)

    for i in range(len(num)):
        assert recursive(i, 1, num, multiplier) == int(correct_result[i])


def test_recursive_phase_2():
    multiplier = 10
    num = "12345"
    phase = 2
    correct_result = run_phases(num * multiplier, phase)

    for i in range(len(num)):
        assert recursive(i, phase, num, multiplier) == int(correct_result[i])


def test_recursive_phase_100():
    multiplier = 100
    num = "12345678"
    phase = 100
    correct_result = [0]  # run_phases(num * multiplier, phase)

    for i in range(12):
        recursive(i, phase, num, multiplier)
