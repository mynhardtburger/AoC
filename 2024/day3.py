import re
from enum import StrEnum, auto
from pprint import pprint

from aocd import get_data

DATA = get_data(day=3, year=2024)

MUL_PATTERN = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
DO_DONT_PATTERN = re.compile(r"(do\(\))|(don't\(\))")


class Command(StrEnum):
    DO = auto()
    DONT = auto()


def find_muls(s: str) -> list[tuple[str, str]]:
    return re.findall(MUL_PATTERN, s)


def sumproduct(list: list[tuple[str, str]]) -> int:
    muls = [int(a) * int(b) for a, b in list]
    return sum(muls)


def do_muls(s: str) -> int:
    muls = find_muls(s)
    return sumproduct(muls)


def filter_do_inputs(s: str) -> list[str]:
    command: Command | None = Command.DO
    to_do_muls: list[str] = []

    splits = ["do()"] + re.split(DO_DONT_PATTERN, s)
    for x in splits:
        match x:
            case "do()":
                command = Command.DO
            case "don't()":
                command = Command.DONT
            case "" | None:
                pass
            case _ if command == Command.DO:
                to_do_muls.append(x)

    return to_do_muls


def do_muls_on_list(commands: list[str]):
    return sum([do_muls(c) for c in commands])


def part_a():
    return do_muls(DATA)


def part_b():
    commands = filter_do_inputs(DATA)
    return do_muls_on_list(commands)


if __name__ == "__main__":
    pprint(DATA)

    pprint(part_a())

    pprint(part_b())
