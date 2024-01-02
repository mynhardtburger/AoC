from collections import namedtuple
import re
from typing import Sequence, TypeAlias

import aoc_utils as aoc

input_list = aoc.get_input_lines(2023, 10)

### Level 1 ###
test_expected = 8
test_data = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...""".splitlines()

Coord = namedtuple("Coord", ["row", "char"])
Direction = namedtuple("Direction", ["row", "char"])
UP = Direction(-1, 0)
DOWN = Direction(1, 0)
LEFT = Direction(0, -1)
RIGHT = Direction(0, 1)

def get_start(input: Sequence[str]) -> Coord:
    for i, s in enumerate(input):
        char = s.find("S")
        if char != -1:
            return Coord(row=i, char=char)
    raise ValueError("No 'S' start found")

def move(position: Coord, direction:Direction) -> Coord:
    return Coord(position.row + direction.row, position.char + direction.char)

def find_connected(position:Coord, map: Sequence[str]) -> set[Direction]:
    connected:set[Direction] = set()
    for direction in (UP, DOWN, LEFT, RIGHT):
        coord = move(position, direction)
        try:
            _ = map[coord.row][coord.char]
        except IndexError:
            pass
        else:
            connected.add(direction)
    return connected


def level_one(input: Sequence[str]):
    start = get_start(input)

    a = Coord(*start)
    b = Coord(*start)
    possible_directions = find_connected(start, input)
    for direction in possible_directions:
        pass




test_actual = level_one(test_data)
assert test_expected == test_actual, f"expected '{test_expected}' got '{test_actual}'"

print(f"Level 1 result: {level_one(input_list)}")

### Level 2 ###
test_expected2 = None
test_data2 = """""".splitlines()


def level_two(input: Sequence[str]):
    pass


test_actual2 = level_two(test_data2)
assert (
    test_expected2 == test_actual2
), f"expected '{test_expected2}' got '{test_actual2}'"

print(f"Level 2 result: {level_two(input_list)}")
