import os
import re

import requests

AOC_URL = "https://adventofcode.com"
INT_PATTERN = r"-?\d+"


def get_input(year: int, day: int) -> str:
    """GET input data."""
    res = requests.get(
        url=f"{AOC_URL}/{year}/day/{day}/input",
        cookies={"session": os.environ["AOC_USER_SESSION_ID"]},
    )
    res.raise_for_status()
    return res.text


def get_input_lines(year: int, day: int) -> list[str]:
    """GET input data as a list."""
    return get_input(year, day).splitlines()


def ints(s: str) -> list[int]:
    """Extracts integer portion of all numbers from string."""
    return re.findall(r"-?\d+", s)
