import re
from typing import Sequence

import aoc_utils as aoc

input_list = aoc.get_input_lines(2023, 1)

### Level 1 ###
test_expected = None
test_data = """""".splitlines()


def level_one(input: Sequence[str]):
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
