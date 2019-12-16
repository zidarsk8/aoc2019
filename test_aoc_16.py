from typing import List
import math
import numpy as np
import pytest

fft = "59776034095811644545367793179989602140948714406234694972894485066523525742503986771912019032922788494900655855458086979764617375580802558963587025784918882219610831940992399201782385674223284411499237619800193879768668210162176394607502218602633153772062973149533650562554942574593878073238232563649673858167635378695190356159796342204759393156294658366279922734213385144895116649768185966866202413314939692174223210484933678866478944104978890019728562001417746656699281992028356004888860103805472866615243544781377748654471750560830099048747570925902575765054898899512303917159138097375338444610809891667094051108359134017128028174230720398965960712"


def generate_pattern(position: int, length: int) -> List[int]:
    base_pattern = [0, 1, 0, -1]
    return [base_pattern[(i + 1) // position % 4] for i in range(length)]


def pattern_grid(number):
    length = len(str(number))
    return [generate_pattern(i + 1, length) for i in range(length)]


def single_phase(number, grid):
    numbers = [int(i) for i in str(number)]
    narr = np.array([numbers] * len(numbers))
    garr = np.array(grid)
    res = (narr * garr).sum(axis=1)
    return "".join(str(i)[-1] for i in res)


def run_phases(number, phases):
    grid = pattern_grid(number)
    for i in range(phases):
        number = single_phase(number, grid)
    return number


def run_100(number):
    return run_phases(number, 100)[:8]


@pytest.mark.parametrize(
    "position, length, output",
    [
        (1, 6, [1, 0, -1, 0, 1, 0]),
        (2, 10, [0, 1, 1, 0, 0, -1, -1, 0, 0, 1]),
        (3, 10, [0, 0, 1, 1, 1, 0, 0, 0, -1, -1]),
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
    assert pattern_grid(48226158) == grid


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
    assert run_100(fft) == "52432133"


