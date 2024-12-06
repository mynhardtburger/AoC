from functools import reduce
import re
import numpy as np
from typing import Sequence

import aoc_utils as aoc

input_list = aoc.get_input_lines(2023, 9)

### Level 1 ###
test_expected = 114
test_data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".splitlines()

def parse(s: str) -> np.ndarray:
    return np.asarray(re.findall(aoc.INT_PATTERN, s)).astype(int)

def get_diffs(arr: np.ndarray) -> list[np.ndarray]:
    diffs:list[np.ndarray] = [arr]

    def recurse(a: np.ndarray):
        diffs.append(np.diff(a, 1))
        if np.any(diffs[-1]):
            recurse(diffs[-1])
    recurse(diffs[-1])

    return diffs

def predict(diffs: list[np.ndarray]) -> int:
    return sum(a[-1] for a in diffs)

def level_one(input: Sequence[str]):
    return sum(predict(get_diffs(parse(s))) for s in input)


test_actual = level_one(test_data)
assert test_expected == test_actual, f"expected '{test_expected}' got '{test_actual}'"

print(f"Level 1 result: {level_one(input_list)}")

### Level 2 ###
test_expected2 = 2
test_data2 = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".splitlines()

def lookback(diffs:list[np.ndarray]) -> int:
    left_side =tuple(x[0] for x in  reversed(diffs))
    return reduce(lambda x,y: y-x, left_side)

def level_two(input: Sequence[str]):
        return sum(lookback(get_diffs(parse(s))) for s in input)



test_actual2 = level_two(test_data2)
assert (
    test_expected2 == test_actual2
), f"expected '{test_expected2}' got '{test_actual2}'"

print(f"Level 2 result: {level_two(input_list)}")
