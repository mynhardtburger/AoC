import re
from dataclasses import dataclass, field
from functools import reduce
from typing import Sequence

import aoc_utils as aoc

input_list = aoc.get_input_lines(2023, 2)

### Level 1 ###
test_expected = 8
test_data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".splitlines()


@dataclass()
class CubeSet:
    red: int
    green: int
    blue: int

    @property
    def cube_count(self) -> int:
        return self.red + self.blue + self.green

    def is_possible(self, max_red: int, max_green: int, max_blue: int) -> bool:
        return (
            self.red <= max_red
            and self.blue <= max_blue
            and self.green <= max_green
            and self.cube_count <= (max_red + max_green + max_blue)
        )


@dataclass()
class Game:
    id: int
    cube_sets: list[CubeSet] = field(default_factory=list)

    def is_possible(self, max_red: int, max_green: int, max_blue: int) -> bool:
        return all(
            (cs.is_possible(max_red, max_green, max_blue) for cs in self.cube_sets)
        )

    def _minimum_required_cubes(self) -> tuple[int, int, int]:
        red = max([x.red for x in self.cube_sets], default=0)
        green = max([x.green for x in self.cube_sets], default=0)
        blue = max([x.blue for x in self.cube_sets], default=0)
        return red, green, blue

    @property
    def power(self) -> int:
        return reduce(lambda x, y: x * y, self._minimum_required_cubes())


def parse_game_string(s: str) -> Game:
    game_part, _, sets_part = s.partition(":")
    game_id = re.search(r"\d+", game_part)
    assert game_id, f"No game ID found in {s}"

    game = Game(id=int(game_id[0]))
    for cube_set in sets_part.split(";"):
        red = re.search(r"(\d+) red", cube_set)
        blue = re.search(r"(\d+) blue", cube_set)
        green = re.search(r"(\d+) green", cube_set)
        game.cube_sets.append(
            CubeSet(
                red=int(red[1]) if red else 0,
                blue=int(blue[1]) if blue else 0,
                green=int(green[1]) if green else 0,
            )
        )
    return game


def level_one(input: Sequence[str]) -> int:
    possible_games = [
        parse_game_string(s)
        for s in input
        if parse_game_string(s).is_possible(12, 13, 14)
    ]
    return sum([game.id for game in possible_games])


test_actual = level_one(test_data)
assert test_actual == test_expected, f"expected '{test_expected}' got '{test_actual}'"

print(f"Level 1 result: {level_one(input_list)}")

### Level 2 ###
test_expected2 = 2286
test_data2 = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".splitlines()


def level_two(input: Sequence[str]):
    games = [parse_game_string(s) for s in input]

    return sum([game.power for game in games])


test_actual2 = level_two(test_data2)
assert (
    test_actual2 == test_expected2
), f"expected '{test_expected2}' got '{test_actual2}'"

print(f"Level 2 result: {level_two(input_list)}")
