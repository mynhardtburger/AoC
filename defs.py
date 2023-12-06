from dataclasses import dataclass
from math import inf
from typing import Optional


@dataclass()
class AlmanacRange:
    destination_start: int
    source_start: int
    range_length: int

    def plot(self, source: int) -> Optional[int]:
        if self.source_start <= source <= self.source_start + (self.range_length - 1):
            offset = source - self.source_start
            return self.destination_start + offset


@dataclass()
class AlmanacMap:
    name: str
    ranges: list[AlmanacRange]

    def plot(self, source: int) -> int:
        for rng in self.ranges:
            destination = rng.plot(source)
            if isinstance(destination, int):
                return destination

        return source


def get_min_location_queue(seed_batch: tuple[int, int, list[AlmanacMap]]):
    seed_start, seed_range, maps = seed_batch
    print("starting batch")
    min_location = inf
    for seed in range(int(seed_start), int(seed_start) + int(seed_range)):
        plot_location = maps[6].plot(
            maps[5].plot(
                maps[4].plot(
                    maps[3].plot(maps[2].plot(maps[1].plot(maps[0].plot(int(seed)))))
                )
            )
        )
        if plot_location < min_location:
            min_location = plot_location
    print(f"Done. min_location = {min_location}")
    return min_location
