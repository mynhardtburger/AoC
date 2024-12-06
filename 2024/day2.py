from enum import StrEnum, auto
from pprint import pprint
from typing import NamedTuple

from aocd import get_data

DATA = get_data(day=2, year=2024).splitlines()
TEST_DATA = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""".splitlines()
SAMPLE = "40 42 44 47 49 50 48".splitlines()


class Direction(StrEnum):
    INCREASING = auto()
    DECREASING = auto()
    EVEN = auto()


class SafetyStatus(StrEnum):
    SAFE = auto()
    UNSAFE = auto()


class PairEval(NamedTuple):
    status: SafetyStatus
    direction: Direction


def eval_direction(a: int, b: int) -> Direction:
    if a > b:
        return Direction.DECREASING
    if a < b:
        return Direction.INCREASING
    if a == b:
        return Direction.EVEN
    raise ValueError("Can't determine direction")


def eval_pair_safety(a: int, b: int) -> SafetyStatus:
    if 3 >= abs(a - b) >= 1:
        return SafetyStatus.SAFE
    else:
        return SafetyStatus.UNSAFE


def eval_pair(a: int, b: int) -> PairEval:
    pair_safety = eval_pair_safety(int(a), int(b))
    pair_direction = eval_direction(int(a), int(b))

    return PairEval(pair_safety, pair_direction)


def is_safe(report: list[str]) -> bool:
    # Initialize starting direction
    record_direction = eval_direction(int(report[0]), int(report[1]))

    for i in range(0, len(report) - 1):
        pair = eval_pair(int(report[i]), int(report[i + 1]))
        if pair.status == SafetyStatus.SAFE and pair.direction == record_direction:
            continue
        else:
            return False
    else:
        return True


def is_safe_with_dampener(report: list[str]) -> bool:
    if is_safe(report):
        print(f"SAFE: {report}")
        return True

    for i in range(len(report)):
        damp_report = report[:i] + report[i + 1 :]
        if is_safe(damp_report):
            print(f"SAFE: {report[:i] + [f"<{report[i]}>"] + report[i + 1:]}")
            return True

    print(f"UNSAFE: {report}")
    return False


def part_a():
    return sum(is_safe(line.split()) for line in DATA)


def part_b():
    return sum(is_safe_with_dampener(line.split()) for line in DATA)


if __name__ == "__main__":
    pprint(DATA)

    pprint(part_a())

    pprint(part_b())
