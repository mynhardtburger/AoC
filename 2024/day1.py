from collections import Counter
from pprint import pprint

from aocd import get_data

DATA = get_data(day=1, year=2024).splitlines()


def data_to_lists() -> tuple[list[int], list[int]]:
    data_formatted = [x.split("   ") for x in DATA]

    left = [int(x[0]) for x in data_formatted]
    right = [int(x[1]) for x in data_formatted]

    return left, right


def total_distance(a: list[int], b: list[int]) -> int:
    a_sorted = sorted(a)
    b_sorted = sorted(b)
    pairs = ((x, y) for x, y in zip(a_sorted, b_sorted))
    result = sum(abs(x[0] - x[1]) for x in pairs)

    return result


def similarity(left: list[int], right: list[int]) -> int:
    b_counter = Counter(right)
    result = sum(x * b_counter.get(x, 0) for x in left)

    return result


def part_a():
    a, b = data_to_lists()
    return total_distance(a, b)


def part_b():
    left, right = data_to_lists()
    return similarity(left, right)


if __name__ == "__main__":
    pprint(part_a())

    pprint(part_b())
