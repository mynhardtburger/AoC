from collections import namedtuple
from functools import reduce
from math import ceil, floor
import re
from typing import Sequence


import aoc_utils as aoc

input_list = aoc.get_input(2023, 6)

### Level 1 ###
test_expected = 288
test_data = """Time:      7  15   30
Distance:  9  40  200"""

Race = namedtuple("Race", ["time", "distance"])

def parse(s:str) -> tuple[Race, ...]:
    lines = s.splitlines()
    times = re.findall(r"\d+", lines[0])
    distances = re.findall(r"\d+", lines[1])
    return tuple(Race(int(t), int(d)) for t,d in zip(times,distances))


def calc_record_hold_times(r: Race) -> tuple[int, int]:
    a = 1
    b = r.time * -1
    c = r.distance
    solution_a = (b*-1 - (b**2 - 4*a*c)**0.5) / (2*a)
    solution_b = (b*-1 + (b**2 - 4*a*c)**0.5) / (2*a)
    return min([solution_a, solution_b]), max([solution_a, solution_b])

def race_margin(r:Race) -> int:
    # t_max = r.time / 2
    record_low, record_high =  calc_record_hold_times(r)
    t_low = max([floor(record_low), 0])
    t_high = min([ceil(record_high), r.time])

    return max([t_high - t_low - 1, 0])


def level_one(input: str):
    return reduce(lambda x, y: x*y,  ([race_margin(r) for r in parse(input)]))


test_actual = level_one(test_data)
assert test_expected == test_actual, f"expected '{test_expected}' got '{test_actual}'"

print(f"Level 1 result: {level_one(input_list)}")

### Level 2 ###
test_expected2 = 71503
test_data2 = """Time:      7  15   30
Distance:  9  40  200"""

def parse_nospace(s:str) -> tuple[Race, ...]:
    lines = s.replace(" ", "").splitlines()
    times = re.findall(r"\d+", lines[0])
    distances = re.findall(r"\d+", lines[1])
    return tuple(Race(int(t), int(d)) for t,d in zip(times,distances))

def level_two(input: str):
    return reduce(lambda x, y: x*y,  ([race_margin(r) for r in parse_nospace(input)]))


test_actual2 = level_two(test_data2)
assert (
    test_expected2 == test_actual2
), f"expected '{test_expected2}' got '{test_actual2}'"

print(f"Level 2 result: {level_two(input_list)}")
