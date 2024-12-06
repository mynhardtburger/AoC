import re
from pprint import pprint
from typing import NamedTuple, Self

from aocd import get_data

DATA = get_data(day=5, year=2024)

A1 = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


class Rule(NamedTuple):
    a: int
    b: int


PageRules = list[Rule]
Pages = list[int]


class Node:
    def __init__(
        self,
        _prev: Self | None = None,
        val: int | None = None,
        _next: Self | None = None,
    ) -> None:
        self._prev: Self | None = _prev
        self.val: int | None = val
        self._next: Self | None = _next

    def __str__(self) -> str:
        mylist = []
        mylist.append(str(self._prev.val) if self._prev else "_")
        mylist.append(str(self.val) if self.val else "_")
        mylist.append(str(self._next.val) if self._next else "_")

        return f"({">".join(mylist)})"

    def __repr__(self):
        return f"Node({self._prev}, {self.val}, {self._next})"


def split_data(input: str) -> tuple[PageRules, list[Pages]]:
    rules_text, pages_text = re.split(r"\n\n", input, maxsplit=1)

    page_rules: PageRules = []
    for line in rules_text.splitlines():
        a, b = line.split("|", maxsplit=1)
        page_rules.append(Rule(int(a), int(b)))

    pages: list[Pages] = []
    for line in pages_text.splitlines():
        pages.append([int(page) for page in line.split(",")])

    return page_rules, pages


### linked list
def get_head(rules: PageRules) -> Node:
    a_list, b_list = list(zip(*rules))

    earliest: int = (set(a_list) - set(b_list)).pop()
    latest: int = (set(b_list) - set(a_list)).pop()

    head = Node(None, earliest, None)
    tail = Node(None, latest, None)

    head._next = tail
    tail._prev = head

    return head


def ll_from_rules(rules: PageRules) -> Node:
    """Returns the head of a linked list built from the rules"""
    head = get_head(rules)

    for rule in rules:
        ll_insert_asc(rule, head)


def ll_insert_asc(rule: Rule, head: Node) -> None:
    r = Node(None, rule.a, None)  # rule node to be inserted
    current = head

    # Walk linked list up to insertion point
    # while current


### Sort normal list
def unique_pages(rules: PageRules) -> set[int]:
    unique_pages = set()
    for rule in rules:
        unique_pages.add(rule.a)
        unique_pages.add(rule.b)

    print(f"unique_pages: {unique_pages}")

    return unique_pages


def rules_to_map(rules: PageRules, unique_pages: set[int]) -> dict[int, set[int]]:
    map: dict[int, set[int]] = {k: set() for k in unique_pages}

    for rule in rules:
        map[rule.a].add(rule.b)

    pprint(f"rules_to_map: {map}", width=500)

    return map


def create_rule_order(
    unique_pages: set[int], rule_map: dict[int, set[int]]
) -> list[int]:
    pages = list(unique_pages)
    # ordered = False

    # while not ordered:
    # all_valid = True
    for page, next_pages in rule_map.items():
        page_idx: int | None = None
        first_next_page_idx: int | None = None
        breakpoint()

        for i, v in enumerate(pages):
            if v == page:
                page_idx = i
                if first_next_page_idx is None:
                    # rule_page is prior to all next_pages. Valid
                    break  # nothing to do. Go to next rule set

            if v in next_pages and first_next_page_idx is None:
                first_next_page_idx = i

            if page_idx is not None and first_next_page_idx is not None:
                # Move page from page_idx to prior to first_next_page_idx
                pages.pop(page_idx)  # remove from latter portion
                pages.insert(
                    first_next_page_idx, page
                )  # insert prior to first_next_page
                # all_valid = False
                break  # Go to next rule set

        # print(f"create_rule_order WIP: {pages}")
        # ordered = all_valid

    print(f"create_rule_order: {pages}")

    return pages


def is_correct_order(pages: Pages, rule_order: list[int]) -> bool:
    last_rule_idx: int | None = None
    for v in pages:
        try:
            last_rule_idx = rule_order.index(v, last_rule_idx or 0)
        except ValueError:
            # page not found in remaining rule_order
            # Therefore not ordered
            return False

    return True


def middle_page(pages: Pages) -> int:
    i = int(len(pages) / 2)
    return pages[i]


def tests():
    rules, page_lists = split_data(A1)
    pprint((rules, page_lists))
    # head = get_head(rules)
    # pprint(head)

    uniq_pages = unique_pages(rules)
    rule_map = rules_to_map(rules, uniq_pages)

    rule_order = create_rule_order(uniq_pages, rule_map)

    for pages in page_lists:
        print(f"{pages} | {is_correct_order(pages, rule_order)} | {middle_page(pages)}")


def part_a(data: str):
    rules, page_lists = split_data(data)
    uniq_pages = unique_pages(rules)
    rule_map = rules_to_map(rules, uniq_pages)
    rule_order = create_rule_order(uniq_pages, rule_map)

    total = 0
    for pages in page_lists:
        valid = is_correct_order(pages, rule_order)
        center = ""
        if valid:
            center = middle_page(pages)
            total += center

        print(f"{valid}\t| {center}\t| {pages}")

    print(f"Total of center pages from valid print orders: {total}")


def part_b(data: str):
    pass


if __name__ == "__main__":
    # pprint(DATA)

    # tests()

    part_a(DATA)

    part_b(DATA)
