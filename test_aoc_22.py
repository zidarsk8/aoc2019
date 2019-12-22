import pytest


def read_data(input_number):

    input_file: str = f"aoc_22_input_{input_number}.txt"
    data = []
    with open(input_file) as f:
        for line in f.read().splitlines():
            if line == "deal into new stack":
                data.append(("reverse", 0))
            else:
                data.append((line.split()[0], int(line.split()[-1])))

    return data


def reverse(l: list, pos):
    return l[::-1]


def cut(l: list, pos):
    return l[pos:] + l[:pos]


def deal(l: list, step):
    new_list = l.copy()
    ll = len(l)

    for i in range(ll):
        new_list[i * step % ll] = l[i]
    return new_list


functions = {
    "reverse": reverse,
    "cut": cut,
    "deal": deal,
}


def shuffle(deck_size, steps):
    cards = list(range(deck_size))
    for fun_name, par in steps:
        cards = functions[fun_name](cards, par)
    return cards


def shuffle_single(deck_size, card, steps):
    cards = list(range(deck_size))
    for fun_name, par in steps:
        cards = functions[fun_name](cards, par)
    return cards[card]


def test_read():
    data = read_data(4)
    assert data[0] == ("reverse", 0)
    assert data[1] == ("cut", -2)
    assert data[2] == ("deal", 7)


@pytest.mark.parametrize(
    "operation, result",
    [
        [("reverse", 0), [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]],
        [("cut", 3), [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]],
        [("cut", -4), [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]],
        [("reverse", 0), [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]],
    ],
)
def test_reverse(operation, result):
    data = [operation]
    assert shuffle(10, data) == result


@pytest.mark.parametrize(
    "input_number, result",
    [
        [4, [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]],
        [3, [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]],
        [2, [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]],
        [1, [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]],
    ],
)
def test_shuffle(input_number, result):
    data = read_data(input_number)
    assert shuffle(10, data) == result


def test_shuffle_4():
    data = read_data(0)
    assert shuffle(10007, data).index(2019) == 4703


@pytest.mark.parametrize(
    "operation", [("reverse", 0), ("cut", 3), ("cut", -4), ("reverse", 0),],
)
def test_reverse(operation):
    data = [operation]
    deck_size = 10
    for card in range(deck_size):
        assert shuffle_single(deck_size, card, data) == shuffle(deck_size, data)[card]
