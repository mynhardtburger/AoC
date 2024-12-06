from dataclasses import dataclass
from pprint import pprint
from typing import Protocol

from aocd import get_data

DATA = get_data(day=4, year=2024)
A1 = """..X...
.SAMX.
.A..A.
XMAS.S
.X...."""

A2 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

B1 = """M.S
.A.
M.S"""

B2 = """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
.........."""


@dataclass
class Coord:
    x: int
    y: int

    def padded(self, padding: int) -> "Coord":
        return Coord(self.x + padding, self.y + padding)


class SpanMatch(Protocol):
    def match(
        self, word: str, padded_anchor: Coord, padded_grid: list[list[str]]
    ) -> bool: ...


@dataclass
class Span(SpanMatch):
    """Definition of an unachored line of continuous coordinates starting at the anchor point"""

    direction: Coord
    length: int

    def match(
        self, word: str, padded_anchor: Coord, padded_grid: list[list[str]]
    ) -> bool:
        span_letters = [
            padded_grid[padded_anchor.y + offset.y][padded_anchor.x + offset.x]
            for offset in self._offsets()
        ]
        # pprint(span_letters)

        span_word = "".join(span_letters)

        return word == span_word

    def _offsets(self) -> list[Coord]:
        return [
            Coord(self.direction.x * pos, self.direction.y * pos)
            for pos in range(self.length)
        ]


@dataclass
class SpanCenter(SpanMatch):
    """Definition of an unachored line of continuous coordinates around a center anchor point"""

    direction: Coord
    radius: int

    def match(
        self, word: str, padded_anchor: Coord, padded_grid: list[list[str]]
    ) -> bool:
        span_letters = [
            padded_grid[padded_anchor.y + offset.y][padded_anchor.x + offset.x]
            for offset in self._offsets()
        ]
        # pprint(span_letters)

        span_word = "".join(span_letters)

        return word == span_word

    def _offsets(self) -> list[Coord]:
        return [
            Coord(self.direction.x * pos, self.direction.y * pos)
            for pos in range(-self.radius, self.radius + 1)
        ]


@dataclass
class SpanGroupAll:
    spans: list[SpanMatch]

    def match(
        self, word: str, padded_anchor: Coord, padded_grid: list[list[str]]
    ) -> bool:
        results = []
        for span in self.spans:
            results.append(span.match(word, padded_anchor, padded_grid))
        return all(results)


@dataclass
class SpanGroupAny:
    spans: list[SpanMatch]

    def match(
        self, word: str, padded_anchor: Coord, padded_grid: list[list[str]]
    ) -> bool:
        results = []
        for span in self.spans:
            results.append(span.match(word, padded_anchor, padded_grid))
        return any(results)


def count_any_matches(word: str, grid: list[list[str]], spans: list[SpanMatch]) -> int:
    padding = len(word) - 1
    padded_grid = pad_grid(grid, padding)
    # pprint(padded_grid, width=200)
    count = 0

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            padded_anchor = Coord(x, y).padded(padding)
            for span in spans:
                if span.match(word, padded_anchor, padded_grid):
                    # pprint(f"Found {word} at {padded_anchor}")
                    count += 1
    return count


def count_group_matches(
    word: str, grid: list[list[str]], span_groups: list[list[SpanMatch]]
) -> int:
    padding = len(word) - 1
    padded_grid = pad_grid(grid, padding)
    count = 0

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            padded_anchor = Coord(x, y).padded(padding)
            group_results: list[bool] = []
            for group in span_groups:
                for span in group:
                    if span.match(word, padded_anchor, padded_grid):
                        group_results.append(True)
                        break  # Move onto next collection on a match

            if all(group_results):
                count += 1

    return count


def text_to_grid(text: str) -> list[list[str]]:
    return [list(line) for line in text.splitlines()]


def star_spans(word: str) -> list[SpanMatch]:
    if not word:
        raise ValueError("word cannot be empty")

    length = len(word)
    spans: list[SpanMatch] = [
        Span(Coord(0, -1), length),  # degree 0
        Span(Coord(1, -1), length),  # degree 45
        Span(Coord(1, 0), length),  # degree 90
        Span(Coord(1, 1), length),  # degree 135
        Span(Coord(0, 1), length),  # degree 180
        Span(Coord(-1, 1), length),  # degree 225
        Span(Coord(-1, 0), length),  # degree 270
        Span(Coord(-1, -1), length),  # degree 315
    ]

    return spans


def forward_slash_spans(word: str) -> list[SpanMatch]:
    if not word:
        raise ValueError("word cannot be empty")

    radius = int(len(word) / 2)

    spans: list[SpanMatch] = [
        SpanCenter(Coord(1, -1), radius),  # degree 45
        SpanCenter(Coord(-1, 1), radius),  # degree 225
    ]

    return spans


def backward_slash_spans(word: str) -> list[SpanMatch]:
    if not word:
        raise ValueError("word cannot be empty")

    radius = int(len(word) / 2)

    spans: list[SpanMatch] = [
        SpanCenter(Coord(1, 1), radius),  # degree 135
        SpanCenter(Coord(-1, -1), radius),  # degree 315
    ]

    return spans


def pad_grid(grid: list[list[str]], padding: int) -> list[list[str]]:
    if padding < 0:
        raise ValueError("padding must be >= 0")

    padded_grid = []
    pad_value = "."

    # Add top padding
    for _ in range(padding):
        padded_grid.append([pad_value] * (len(grid[0]) + 2 * padding))

    # Add side padding
    for row in grid:
        padded_grid.append([pad_value] * padding + row + [pad_value] * padding)

    # Add bottom padding
    for _ in range(padding):
        padded_grid.append([pad_value] * (len(grid[0]) + 2 * padding))

    return padded_grid


def tests():
    assert pad_grid([[]], 0) == [[]], "no padding should match original grid"
    assert pad_grid([["a"]], 2) == [
        [".", ".", ".", ".", "."],
        [".", ".", ".", ".", "."],
        [".", ".", "a", ".", "."],
        [".", ".", ".", ".", "."],
        [".", ".", ".", ".", "."],
    ], "2 padding added"
    assert Coord(1, 2).padded(3) == Coord(4, 5)
    assert Span(Coord(0, 0), 1)._offsets() == [Coord(0, 0)]
    assert Span(Coord(1, -1), 4)._offsets() == [
        Coord(0, 0),
        Coord(1, -1),
        Coord(2, -2),
        Coord(3, -3),
    ]

    assert text_to_grid("123\n456\n789") == [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
    ]

    word = "XMAS"
    assert Span(Coord(1, 0), 4).match(word, Coord(0, 3), text_to_grid(A1))
    assert Span(Coord(1, 1), 4).match(word, Coord(2, 0), text_to_grid(A1))

    word = "XMAS"
    spans = star_spans(word)
    assert count_any_matches(word, text_to_grid(A1), spans) == 4
    assert count_any_matches(word, text_to_grid(A2), spans) == 18

    word = "MAS"
    forward = SpanGroupAny(forward_slash_spans(word))
    backward = SpanGroupAny(backward_slash_spans(word))
    x_group = [SpanGroupAll([forward, backward])]
    assert count_any_matches(word, text_to_grid(B1), x_group) == 1
    assert count_any_matches(word, text_to_grid(B2), x_group) == 9


def part_a(text: str):
    word = "XMAS"
    spans = star_spans(word)
    grid = text_to_grid(text)

    return count_any_matches(word, grid, spans)


def part_b(text: str):
    word = "MAS"
    forward = SpanGroupAny(forward_slash_spans(word))
    backward = SpanGroupAny(backward_slash_spans(word))
    x_group = [SpanGroupAll([forward, backward])]

    grid = text_to_grid(text)

    return count_any_matches(word, grid, x_group)


if __name__ == "__main__":
    pprint(DATA)

    tests()

    pprint(part_a(DATA))

    pprint(part_b(DATA))
