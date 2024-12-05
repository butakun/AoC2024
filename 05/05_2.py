import os
import logging
from collections import defaultdict

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    f = open(inputfile)
    rules = []
    for l in f:
        l = l.strip()
        if len(l) == 0:
            break
        p1, p2 = l.split("|")
        p1, p2 = int(p1), int(p2)
        rules.append((p1, p2))

    updates = []
    for l in f:
        update = [int(i) for i in l.split(",")]
        updates.append(update)

    return rules, updates


def check(update, graph):
    for page1, page2 in zip(update[:-1], update[1:]):
        if page2 in graph[page1][0]:
            return False
    return True


def reorder(update, graph):
    logger.debug(f"reordering: {update}")
    pages = set(update)

    # find the first page
    first = None
    for page in pages:
        rest = pages.copy()
        rest.remove(page)
        befores = graph[page][0]
        if not (rest & befores):
            first = page
            break
    assert first is not None

    logger.debug(f"first page is {first}")

    n = len(pages)
    imid = int(n / 2)
    page = first
    pages.remove(page)
    count = 1
    while count <= imid:
        next_candidates = graph[page][1] & pages
        for next_page in next_candidates:
            if graph[next_page][0] & pages:
                continue
            page = next_page
            pages.remove(page)
            count += 1
            break
    return page


def main(inputfile):
    rules, updates = read(inputfile)

    # Represent rules as a digraph.
    graph = defaultdict(lambda : [set(), set()].copy())
    for page1, page2 in rules:
        graph[page1][1].add(page2)
        graph[page2][0].add(page1)

    for p, (befores, afters) in graph.items():
        logger.debug(f"{p} <- {befores}")
        logger.debug(f"    -> {afters}")

    count = 0
    for update in updates:
        if check(update, graph):
            continue
        page = reorder(update, graph)
        count += page
    print(count)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
