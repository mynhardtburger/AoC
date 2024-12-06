from collections import namedtuple
from functools import reduce
from itertools import cycle
from math import gcd, lcm
import re
from typing import Sequence, TypedDict

import aoc_utils as aoc

input_list = aoc.get_input(2023, 8)

### Level 1 ###
test_expected = 2
test_data = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

test_expected3 = 6
test_data3 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


class Node(TypedDict):
    L: str
    R: str


def parse(s: str) -> tuple[str, dict[str, Node]]:
    lines = s.splitlines()
    moves = lines[0]
    network: dict[str, Node] = {}
    for line in lines[2:]:
        node_name, left, right = re.findall(r"\w+", line)
        network[node_name] = Node(L=left, R=right)
    return moves, network


def level_one(input: str):
    moves, network = parse(input)
    current_node = "AAA"
    for i, move in enumerate(cycle(moves)):
        if current_node == "ZZZ":
            return i

        current_node = network[current_node][move]


test_actual = level_one(test_data)
assert test_expected == test_actual, f"expected '{test_expected}' got '{test_actual}'"

test_actual3 = level_one(test_data3)
assert (
    test_expected3 == test_actual3
), f"expected '{test_expected3}' got '{test_actual3}'"

print(f"Level 1 result: {level_one(input_list)}")

### Level 2 ###
test_expected2 = 6
test_data2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def level_two(input: str):
    moves, network = parse(input)
    starting_nodes = tuple(x for x in network if x[-1] == "A")

    history: dict[str, dict[str, int]] = {}
    for n, node in enumerate(starting_nodes):
        current_node = node
        history[node] = {}
        for i, move in enumerate(cycle(moves)):
            if current_node[-1] == "Z":
                print(f"Node {n}: Z node '{current_node}' found at {i}.")
                history[node][current_node] = i
                break

            current_node = network[current_node][move]
    return lcm(*[y for x in history.values() for y in x.values()])


test_actual2 = level_two(test_data2)
assert (
    test_expected2 == test_actual2
), f"expected '{test_expected2}' got '{test_actual2}'"

print(f"Level 2 result: {level_two(input_list)}")
