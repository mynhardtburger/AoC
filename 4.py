import re
from collections import namedtuple
from typing import Sequence

import aoc_utils as aoc

input_list = aoc.get_input_lines(2023, 4)

### Level 1 ###
test_expected = 13
test_data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".splitlines()

CardData = namedtuple("CardData", ["card", "winning_numbers", "my_numbers"])
CardScore = namedtuple("CardData", ["card", "score"])
re_ints = re.compile(aoc.INT_PATTERN)


def format_line(s: str) -> CardData:
    card_part, _, numbers_part = s.partition(":")
    winning_part, _, my_numbers_part = numbers_part.partition("|")

    card = re_ints.search(card_part)
    assert card is not None
    card_number = int(card[0])

    winning_numbers = {int(x) for x in re_ints.findall(winning_part)}
    my_numbers = {int(x) for x in re_ints.findall(my_numbers_part)}

    return CardData(
        card=card_number, winning_numbers=winning_numbers, my_numbers=my_numbers
    )


def score_line(card: int, winning_numbers: set[int], my_numbers: set[int]) -> CardScore:
    my_winning_numbers = winning_numbers.intersection(my_numbers)
    if len(my_winning_numbers) == 0:
        score = 0
    else:
        score = 2 ** (len(my_winning_numbers) - 1)
    return CardScore(card, score)


def level_one(input: Sequence[str]) -> int:
    scores = (score_line(*format_line(s)).score for s in input)
    return sum(scores)


test_actual = level_one(test_data)
assert test_expected == test_actual, f"expected '{test_expected}' got '{test_actual}'"

print(f"Level 1 result: {level_one(input_list)}")

### Level 2 ###
test_expected2 = 30
test_data2 = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".splitlines()


def score_line_by_count(
    card: int, winning_numbers: set[int], my_numbers: set[int]
) -> CardScore:
    my_winning_numbers = winning_numbers.intersection(my_numbers)
    return CardScore(card, len(my_winning_numbers))


def update_card_counts(card_count: dict[int, int], card_score: CardScore) -> None:
    card_count[card_score.card] = card_count.get(card_score.card, 0) + 1
    multiplier = card_count[card_score.card]
    new_counts = {
        card: card_count.get(card, 0) + 1 * multiplier
        for card in range(card_score.card + 1, card_score.card + 1 + card_score.score)
    }
    card_count.update(new_counts)


def level_two(input: Sequence[str]):
    card_counts: dict[int, int] = {}
    card_scores = (score_line_by_count(*format_line(s)) for s in input)
    for card_score in card_scores:
        update_card_counts(card_counts, card_score)
    total_cards = sum(card_counts.values())

    return total_cards


test_actual2 = level_two(test_data2)
assert (
    test_expected2 == test_actual2
), f"expected '{test_expected2}' got '{test_actual2}'"

print(f"Level 2 result: {level_two(input_list)}")
