import concurrent.futures
import re
from dataclasses import dataclass

# from itertools import batched
from math import inf
from multiprocessing import Pool
from typing import Optional

import aoc_utils as aoc
from defs import AlmanacMap, AlmanacRange, get_min_location_queue

# from defs import AlmanacMap, AlmanacRange, get_min_location_queue

if __name__ == "__main__":
    input_list = aoc.get_input(2023, 5)

    def batched(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    ### Level 1 ###
    test_data = """seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4"""
    test_expected = 35

    def parse_almanac(s: str):
        matches: list[str] = re.findall(r":\n?([\s|\d]*)(?:\n|$)", s)
        return dict(
            seeds=matches[0].strip().split(),
            seed_to_soil=matches[1].strip().splitlines(),
            soil_to_fertilizer=matches[2].strip().splitlines(),
            fertilizer_to_water=matches[3].strip().splitlines(),
            water_to_light=matches[4].strip().splitlines(),
            light_to_temperature=matches[5].strip().splitlines(),
            temperature_to_humidity=matches[6].strip().splitlines(),
            humidity_to_location=matches[7].strip().splitlines(),
        )

    # @dataclass()
    # class AlmanacRange:
    #     destination_start: int
    #     source_start: int
    #     range_length: int

    #     def plot(self, source: int) -> Optional[int]:
    #         if self.source_start <= source <= self.source_start + (self.range_length - 1):
    #             offset = source - self.source_start
    #             return self.destination_start + offset

    # @dataclass()
    # class AlmanacMap:
    #     name: str
    #     ranges: list[AlmanacRange]

    #     def plot(self, source: int) -> int:
    #         for rng in self.ranges:
    #             destination = rng.plot(source)
    #             if isinstance(destination, int):
    #                 return destination

    #         return source

    def create_almanac_maps(almanacs: dict[str, list[str]]) -> list[AlmanacMap]:
        maps = []
        for key, lines in almanacs.items():
            if key == "seeds":
                # don't create map for seeds
                continue

            ranges: list[AlmanacRange] = []
            for line in lines:
                dest, source, length = line.strip().split()
                ranges.append(AlmanacRange(int(dest), int(source), int(length)))
            maps.append(AlmanacMap(key, ranges))

        return maps

    def level_one(input: str):
        almanacs = parse_almanac(input)
        maps = create_almanac_maps(almanacs)

        min_location = inf
        for seed in almanacs["seeds"]:
            temp_location = int(seed)
            for map in maps:
                temp_location = map.plot(temp_location)
            min_location = min([min_location, temp_location])

        return min_location

    test_actual = level_one(test_data)
    assert (
        test_expected == test_actual
    ), f"expected '{test_expected}' got '{test_actual}'"

    print(f"Level 1 result: {level_one(input_list)}")

    ### Level 2 ###
    test_data2 = test_data
    test_expected2 = 46

    def get_min_location(seed_batch: tuple[int, int, list[AlmanacMap]]):
        seed_start, seed_range, maps = seed_batch
        min_location = inf
        for seed in prange(int(seed_start), int(seed_start) + int(seed_range)):
            plot_location = maps[6].plot(
                maps[5].plot(
                    maps[4].plot(
                        maps[3].plot(
                            maps[2].plot(maps[1].plot(maps[0].plot(int(seed))))
                        )
                    )
                )
            )
            if plot_location < min_location:
                min_location = plot_location
        return int(min_location)

    def level_two(input: str):
        almanacs = parse_almanac(input)
        maps = create_almanac_maps(almanacs)

        # min_locations: list[int] = []
        seed_batches = [
            (int(seed_start), int(seed_range), maps)
            for seed_start, seed_range in batched(almanacs["seeds"], 2)
        ]
        for batch in seed_batches:
            print(get_min_location(batch))
            # for seed in range(int(seed_start), int(seed_start) + int(seed_range)):
            #     plot_location = maps[6].plot(
            #         maps[5].plot(
            #             maps[4].plot(
            #                 maps[3].plot(
            #                     maps[2].plot(maps[1].plot(maps[0].plot(int(seed))))
            #                 )
            #             )
            #         )
            #     )
            #     if plot_location < min_location:
            #         min_location = plot_location
            # plot_location = int(seed)
            # for map in maps:
            #     plot_location = map.plot(plot_location)
            # min_location = min([min_location, plot_location])

        # return min(min_locations)

    # def get_min_location_queue(seed_batch: tuple[int, int, list[AlmanacMap], int]):
    #     seed_start, seed_range, maps, i = seed_batch
    #     print(f"{i}: starting batch")
    #     min_location = inf
    #     for seed in range(int(seed_start), int(seed_start) + int(seed_range)):
    #         plot_location = maps[6].plot(
    #             maps[5].plot(
    #                 maps[4].plot(
    #                     maps[3].plot(
    #                         maps[2].plot(maps[1].plot(maps[0].plot(int(seed))))
    #                     )
    #                 )
    #             )
    #         )
    #         if plot_location < min_location:
    #             min_location = plot_location
    #     print(f"{i}: Done. min_location = {min_location}")
    #     return min_location

    def level_two_threaded(input: str):
        almanacs = parse_almanac(input)
        maps = create_almanac_maps(almanacs)

        min_locations = []
        seed_batches = [
            (int(seed_start), int(seed_range), maps, min_locations)
            for seed_start, seed_range in batched(almanacs["seeds"], 2)
        ]
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            executor.map(get_min_location, seed_batches)

        return min(min_locations)

    def level_two_multiprocess(input: str):
        almanacs = parse_almanac(input)
        maps = create_almanac_maps(almanacs)

        seed_batches = [
            (int(seed_start), int(seed_range), maps)
            for seed_start, seed_range in batched(almanacs["seeds"], 2)
        ]
        with Pool(processes=11) as pool:
            pool.map(get_min_location_queue, seed_batches, chunksize=1)

    test_actual2 = level_two_multiprocess(test_data2)
    # assert (
    #     test_expected2 == test_actual2
    # ), f"expected '{test_expected2}' got '{test_actual2}'"

    print(f"Level 2 result: {level_two_multiprocess(input_list)}")


# starting batch
# starting batch
# starting batch
# starting batch
# starting batch
# starting batch
# starting batch
# starting batch
# starting batch
# starting batch
# Done. min_location = 469381783
# Done. min_location = 1531539628
# Done. min_location = 1880769172
# Done. min_location = 95181345 too high
# Done. min_location = 1165763062
# Done. min_location = 318728750
# Done. min_location = 384658003
# Done. min_location = 1314084048
# Done. min_location = 190399026
# Done. min_location = 37384986
