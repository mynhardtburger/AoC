import pprint
import re
from collections import defaultdict, namedtuple
from typing import Sequence

import aoc_utils as aoc

input_list = aoc.get_input_lines(2023, 3)

### Level 1 ###
test_expected = 4361
test_data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".splitlines()


def contains_symbol(match: re.Match, context: Sequence[str], index: int) -> bool:
    index_start = max([0, index - 1])
    index_end = min([len(context) - 1, index + 1])

    char_start = max([0, match.start() - 1])
    char_end = min([len(match.string) - 1, match.end() + 1])

    search_ranges = (
        context[index_start][char_start:char_end]
        + context[index][char_start:char_end]
        + context[index_end][char_start:char_end]
    )
    return re.search(r"[!#$%&'()*+,\-/:;<=>?@[\]^_`{|}~]", search_ranges) is not None


def level_one(input: Sequence[str]) -> int:
    parts = []
    for i, s in enumerate(input):
        for number in re.finditer(r"\d+", s):
            if contains_symbol(number, input, i):
                print(number[0])
                parts.append(int(number[0]))
    return sum(parts)


test_actual = level_one(test_data)
assert test_expected == test_actual, f"expected '{test_expected}' got '{test_actual}'"
print(f"Level 1 test passed :{test_actual}")

print(f"Level 1 result: {level_one(input_list)}")

### Level 2 ###
test_expected2 = 467835
test_data2 = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".splitlines()

Point = namedtuple("Point", ["x", "y"])


def point_region(point: Point) -> set[Point]:
    return {
        # top row
        Point(point.x - 1, point.y - 1),
        Point(point.x, point.y - 1),
        Point(point.x + 1, point.y - 1),
        # sides
        Point(point.x - 1, point.y),
        Point(point.x + 1, point.y),
        # bottom row
        Point(point.x - 1, point.y + 1),
        Point(point.x, point.y + 1),
        Point(point.x + 1, point.y + 1),
    }


def match_to_points(index: int, number: re.Match) -> set[Point]:
    return {Point(x, index) for x in range(number.start(), number.end())}


def level_two(input: Sequence[str]):
    star_points = {
        Point(x=star.start(), y=i)
        for i, s in enumerate(input)
        for star in re.finditer(r"\*", s)
    }
    numbers = {
        i: {number for number in re.finditer(r"\d+", s)} for i, s in enumerate(input)
    }

    # Record numbers in the region of each star
    star_number_map: dict[Point, list[int]] = defaultdict(list)
    for star in star_points:
        min_y = max(0, star.y - 1)
        max_y = min(len(input) - 1, star.y + 1)
        for i in range(min_y, max_y + 1):
            region_numbers = [
                int(number[0])
                for number in numbers[i]
                if match_to_points(i, number).intersection(point_region(star))
            ]
            star_number_map[star].extend(region_numbers)

    # filter for stars with only two numbers
    gear_map = {i: x for i, x in star_number_map.items() if len(x) == 2}

    return sum([x[0] * x[1] for x in gear_map.values()])


test_actual2 = level_two(test_data2)
assert (
    test_expected2 == test_actual2
), f"expected '{test_expected2}' got '{test_actual2}'"
print(f"Level 2 test passed :{test_actual2}")

print(f"Level 2 result: {level_two(input_list)}")
