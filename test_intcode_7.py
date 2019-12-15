import pytest
from .intcode_pc import Intcode
from .intcode_pc import IntMainframe

amplifier_software = "3,8,1001,8,10,8,105,1,0,0,21,34,59,76,101,114,195,276,357,438,99999,3,9,1001,9,4,9,1002,9,4,9,4,9,99,3,9,102,4,9,9,101,2,9,9,102,4,9,9,1001,9,3,9,102,2,9,9,4,9,99,3,9,101,4,9,9,102,5,9,9,101,5,9,9,4,9,99,3,9,102,2,9,9,1001,9,4,9,102,4,9,9,1001,9,4,9,1002,9,3,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99"


def test_empty_input():
    program = "3,7,3,8,3,9,99,0,0,0"
    intcode = Intcode(program)
    intcode.run_partial(1)
    intcode.run_partial(2)
    intcode.run_partial(59)
    assert intcode.state == "3,7,3,8,3,9,99,1,2,59"


@pytest.mark.parametrize(
    "program, phase_settings, output",
    [
        ("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", [4, 3, 2, 1, 0], 43210),
        (
            "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
            [0, 1, 2, 3, 4],
            54321,
        ),
        (
            "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,"
            "1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
            [1, 0, 4, 3, 2],
            65210,
        ),
    ],
)
def test_run_chain(program, phase_settings, output):
    mainframe = IntMainframe(program, len(phase_settings))
    assert mainframe.run_chain(phase_settings) == output


@pytest.mark.parametrize(
    "program, phase_settings, output",
    [
        ("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", [4, 3, 2, 1, 0], 43210),
        (
            "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
            [0, 1, 2, 3, 4],
            54321,
        ),
        (
            "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,"
            "1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
            [1, 0, 4, 3, 2],
            65210,
        ),
    ],
)
def test_get_max_sequence(program, phase_settings, output):
    mainframe = IntMainframe(program, len(phase_settings))
    assert mainframe.get_max_sequence(sorted(phase_settings)) == (
        output,
        phase_settings,
    )


def test_part_1():
    phase_settings = [0, 1, 2, 3, 4]
    mainframe = IntMainframe(amplifier_software, len(phase_settings))
    max_signal, _ = mainframe.get_max_sequence(phase_settings)
    assert max_signal == 273814


@pytest.mark.parametrize(
    "program, phase_settings, output",
    [
        # (
        #     "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,"
        #     "27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
        #     [9, 8, 7, 6, 5],
        #     139629729,
        # ),
        (
            "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,"
            "-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,"
            "53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10",
            [9, 7, 8, 5, 6],
            18216,
        )
    ],
)
def test_run_loop(program, phase_settings, output):
    mainframe = IntMainframe(program, len(phase_settings))
    assert mainframe.run_loop(phase_settings) == output
    mainframe.reset()
    assert mainframe.run_loop(phase_settings) == output


@pytest.mark.parametrize(
    "program, phase_settings, output",
    [
        (
            "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,"
            "27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5",
            [9, 8, 7, 6, 5],
            139629729,
        ),
        (
            "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,"
            "-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,"
            "53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10",
            [9, 7, 8, 5, 6],
            18216,
        ),
    ],
)
def test_get_max_loop(program, phase_settings, output):
    phase_settings = [5, 6, 7, 8, 9]
    mainframe = IntMainframe(program, len(phase_settings))
    max_signal, _ = mainframe.get_max_loop(phase_settings)
    assert max_signal == output


def test_part_2():
    phase_settings = [5, 6, 7, 8, 9]
    mainframe = IntMainframe(amplifier_software, len(phase_settings))
    max_signal, _ = mainframe.get_max_loop(phase_settings)
    assert max_signal == 34579864
