import os
import logging
import numpy as np

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

    print(rules)
    print(updates)

    return rules, updates


def check(update, rules):
    for page1, page2 in rules:
        try:
            i1 = update.index(page1)
        except:
            i1 = -1
        try:
            i2 = update.index(page2)
        except:
            i2 = -1
        if i1 >= 0 and i2 >= 0:
            if i1 > i2:
                return False
    return True


def apply(ii, rule, update, indices):
    page1, page2 = rule
    print(f"** rule {page1}|{page2}")
    page = update[indices[ii]]
    if page2 != page:
        return ii

    # page1 must be before page2 which is page
    for j in indices[ii+1:]:
        pagej = update[j]
        if pagej == page1:
            # put j in front of indices[ii]
            print(f"  removing {j} and inserting it at {ii}: before: {indices=}")
            indices.remove(j)
            indices.insert(ii, j)
            return ii + 1
    return ii


def apply2(rule, update, indices):
    page1, page2 = rule
    print(f"** rule {page1}|{page2}: {indices=}")
    for ii, i in enumerate(indices):
        page = update[i]
        if page2 != page:
            continue
        for j in indices[ii+1:]:
            pagej = update[j]
            if page1 == pagej:
                print(f"  removing {j} and inserting it at {ii}: before: {indices=}")
                indices.remove(j)
                indices.insert(ii, j)
                return True
    return False

def reorder(update, rules):
    indices = [i for i in range(len(update))]
    N = len(indices)

    while True:
        for rule in rules:
            applied = apply2(rule, update, indices)
            if applied:
                print(f"rule {rule[0]}|{rule[1]} applied: {indices=}, {[update[k] for k in indices]}")
                break
        if not applied:
            break

    reordered = [update[k] for k in indices]
    return reordered

    """
    ii = 0
    while ii < N:
        for rule in rules:
            ii_new = apply(ii, rule, update, indices)
            if ii_new != ii:
                print(f"rule {rule[0]}|{rule[1]} applied: {indices=}, {[update[k] for k in indices]}")
            #ii = ii_new
        ii += 1

    reordered = [update[k] for k in indices]
    return reordered
    """


def main(inputfile):
    rules, updates = read(inputfile)
    #updates = updates[-1:]

    count = 0
    for i, update in enumerate(updates):
        if check(update, rules):
            continue
        print(f"reordering {i}: {update}")
        reordered = reorder(update, rules)

        l = len(reordered)
        assert l % 2 == 1
        imid = int(l / 2)
        print(reordered[imid])
        count += reordered[imid]
    print(count)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
