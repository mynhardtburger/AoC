import re
from typing import Sequence

import aoc_utils as aoc

input_list = aoc.get_input_lines(2023, 1)


def get_calibration_value(s) -> int:
    digits = re.findall(r"\d", s)
    return int(f"{digits[0]}{digits[-1]}")


### Level 1 ###
test_expected = 142
test_data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""".splitlines()


def level_one(input: Sequence[str]) -> int:
    return sum(map(get_calibration_value, input))


test_actual = level_one(test_data)
assert test_actual == test_expected, f"expected '{test_expected}' got '{test_actual}'"

print(f"Level 1 result: {level_one(input_list)}")

### Level 2 ###
test_expected2 = 281
test_data2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""".splitlines()

number_map = dict(
    one=1,
    two=2,
    three=3,
    four=4,
    five=5,
    six=6,
    seven=7,
    eight=8,
    nine=9,
    zero=0,
)


def get_calibration_value2(s: str) -> int:
    split_pattern = r"(?=(one|two|three|four|five|six|seven|eight|nine|zero|\d))"
    words = re.findall(pattern=split_pattern, string=s, flags=re.IGNORECASE)
    cleaned_words = [str(number_map.get(word, word)) for word in words if word]
    return int(f"{cleaned_words[0]}{cleaned_words[-1]}")


def level_two(input: Sequence[str]) -> int:
    return sum(map(get_calibration_value2, input))


test_actual = level_two(test_data)
assert test_actual == test_expected, f"expected '{test_expected}' got '{test_actual}'"

test_actual2 = level_two(test_data2)
assert (
    test_actual2 == test_expected2
), f"expected '{test_expected2}' got '{test_actual2}'"

print(f"Level 2 result: {level_two(input_list)}")
