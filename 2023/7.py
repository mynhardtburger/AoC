from collections import Counter, namedtuple
from enum import auto, Enum
from typing import Sequence
from functools import cmp_to_key, partial

import aoc_utils as aoc

input_list = aoc.get_input_lines(2023, 7)
CARDS = tuple(reversed("AKQJT98765432"))
CARDS_MODIFIED = tuple(reversed("AKQT98765432J"))

### Level 1 ###
test_expected = 6440
test_data = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".splitlines()


class HandType(Enum):
    HighCard = auto()
    OnePair = auto()
    TwoPair = auto()
    ThreeKind = auto()
    FullHouse = auto()
    FourKind = auto()
    FiveKind = auto()


def parse(s: str) -> tuple[tuple[str, ...], int]:
    hand, bid = s.split()
    assert len(hand) == 5
    return (tuple(hand), int(bid))


def hand_type(hand: tuple[str, ...]) -> HandType:
    frequency = Counter(hand).most_common()
    if frequency[0][1] == 5:
        return HandType.FiveKind
    if frequency[0][1] == 4:
        return HandType.FourKind
    if frequency[0][1] == 3:
        if frequency[1][1] == 2:
            return HandType.FullHouse
        else:
            return HandType.ThreeKind
    if frequency[0][1] == 2:
        if frequency[1][1] == 2:
            return HandType.TwoPair
        else:
            return HandType.OnePair
    return HandType.HighCard


ClassifiedHand = namedtuple("ClassifiedHand", ["hand", "original_hand", "type", "bid"])


def compare_hands(x: ClassifiedHand, y: ClassifiedHand, ranking: tuple) -> int:
    if x.type.value != y.type.value:
        return 1 if x.type.value > y.type.value else -1

    for i in range(5):
        x_rank = ranking.index(x.original_hand[i])
        y_rank = ranking.index(y.original_hand[i])
        if x_rank > y_rank:
            return 1
        if x_rank < y_rank:
            return -1

    return 0


def level_one(input: Sequence[str]):
    hands_parsed = (parse(s) for s in input)
    hands_classified = (
        ClassifiedHand(hand, hand, hand_type(hand), bid) for hand, bid in hands_parsed
    )

    comparer = partial(compare_hands, ranking=CARDS)
    hands_sorted = sorted(hands_classified, key=cmp_to_key(comparer))
    winnings = [(v.bid * (i + 1)) for i, v in enumerate(hands_sorted)]
    return sum(winnings)


test_actual = level_one(test_data)
assert test_expected == test_actual, f"expected '{test_expected}' got '{test_actual}'"

print(f"Level 1 result: {level_one(input_list)}")

### Level 2 ###
test_expected2 = 5905
test_data2 = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".splitlines()


def apply_jokers(hand: tuple[str, ...]) -> tuple[str, ...]:
    normal_cards = tuple(c for c in hand if c != "J")
    if len(normal_cards) == 0 or len(normal_cards) == 5:
        return hand

    counter = Counter(normal_cards)
    freq = counter.most_common()
    if freq[0][1] == 1:
        return tuple(c.replace("J", normal_cards[0]) for c in hand)
    if freq[0][1] == 2 and len(freq) >= 2 and freq[1][1] == 2:
        i_best_pair = min([hand.index(freq[0][0]), hand.index(freq[1][0])])
        return tuple(c.replace("J", normal_cards[i_best_pair]) for c in hand)
    else:
        return tuple(c.replace("J", freq[0][0]) for c in hand)


def level_two(input: Sequence[str]):
    hands_parsed = tuple(parse(s) for s in input)
    hands_modified = tuple((apply_jokers(h), b) for h, b in hands_parsed)
    hands_classified = tuple(
        ClassifiedHand(z[0][0], z[1][0], hand_type(z[0][0]), z[0][1])
        for z in zip(hands_modified, hands_parsed)
    )

    comparer = partial(compare_hands, ranking=CARDS_MODIFIED)
    hands_sorted = sorted(hands_classified, key=cmp_to_key(comparer))
    winnings = [(v.bid * (i + 1)) for i, v in enumerate(hands_sorted)]
    return sum(winnings)


test_actual2 = level_two(test_data2)
assert (
    test_expected2 == test_actual2
), f"expected '{test_expected2}' got '{test_actual2}'"

print(f"Level 2 result: {level_two(input_list)}")
