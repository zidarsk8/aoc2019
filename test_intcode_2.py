from .intcode_pc import Intcode

puzzle_input = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,19,9,23,1,23,13,27,1,10,27,31,2,31,13,35,1,10,35,39,2,9,39,43,2,43,9,47,1,6,47,51,1,10,51,55,2,55,13,59,1,59,10,63,2,63,13,67,2,67,9,71,1,6,71,75,2,75,9,79,1,79,5,83,2,83,13,87,1,9,87,91,1,13,91,95,1,2,95,99,1,99,6,0,99,2,14,0,0"


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
    intcode = Intcode(puzzle_input)
    intcode.set_program_state(1202)
    assert intcode.run() == 3085697


def test_part_2():
    intcode = Intcode(puzzle_input)
    assert intcode.get_program_state(19690720) == 9425
