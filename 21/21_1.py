import os
import logging
import numpy as np
from dijkstra import dijkstra


logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    grid = [ list(l.strip()) for l in open(inputfile) ]
    return np.array(grid)


DIRECTIONAL = np.array([
        [" ", "^", "A" ],
        ["<", "v", ">" ],
        ])

NUMERIC = np.array([
        ["7", "8", "9" ],
        ["4", "5", "6" ],
        ["1", "2", "3" ],
        [" ", "0", "A" ],
        ])

def generate_transitions(table):
    idim, jdim = table.shape[:2]
    T = {}
    for i in range(idim):
        for j in range(jdim):
            k = str(table[i, j])
            if k == " ":
                continue
            t = {}
            if i > 0 and table[i - 1, j] != " ":
                t["^"] = str(table[i - 1, j])
            if i < idim - 1 and table[i + 1, j] != " ":
                t["v"] = str(table[i + 1, j])
            if j > 0 and table[i, j - 1] != " ":
                t["<"] = str(table[i, j - 1])
            if j < jdim - 1 and table[i, j + 1] != " ":
                t[">"] = str(table[i, j + 1])
            T[k] = t
    return T


T_DIRECTIONAL = generate_transitions(DIRECTIONAL)
T_NUMERIC = generate_transitions(NUMERIC)


class Operator:
    def __init__(self, code):
        self.code = code

    def __getitem__(self, u):
        p1, p2, p3, c1, c2, c3, c4 = u
        vv = []
        for t in "^v<>":
            T = T_DIRECTIONAL[p1]
            if t in T:
                p1n = T[t]
                v = (p1n, p2, p3, c1, c2, c3, c4)
                vv.append(v)

        # what if the operator pressed A?
        if p1 == "A":
            # and robot 1 is pointing at A, pressing robot 2 in turn
            if p2 == "A":
                # and robot 2 is pointing at A, pressing robot 3 in turn
                cc = None
                if c1 is None:
                    assert c2 is None and c3 is None and c4 is None
                    cc = (p3, c2, c3, c4)
                elif c2 is None:
                    assert c3 is None and c4 is None
                    cc = (c1, p3, c3, c4)
                elif c3 is None:
                    assert c4 is None
                    cc = (c1, c2, p3, c4)
                elif c4 is None:
                    cc = (c1, c2, c3, p3)
                else:
                    assert ValueError(f"{c1=}, {c2=}, {c3=}, {c4=}")
                if cc is not None:
                    v = (p1, p2, p3) + cc
                    vv.append(v)
            else:
                assert p2 in "<>^v"
                # move p3 if allowed
                if p2 in T_NUMERIC[p3]:
                    p3n = T_NUMERIC[p3][p2]
                    vv.append((p1, p2, p3n, c1, c2, c3, c4))
        else:
            assert p1 in "<>^v"
            # move p2 if allowed
            if p1 in T_DIRECTIONAL[p2]:
                p2n = T_DIRECTIONAL[p2][p1]
                vv.append((p1, p2n, p3, c1, c2, c3, c4))

        vvw = [ (v, 1) for v in vv ]
        return vvw

    def is_goal(self, u):
        _, _, _, c1, c2, c3, c4 = u
        if c1 is None or c2 is None or c3 is None or c4 is None:
            return False
        cc = c1 + c2 + c3 + c4
        return cc == self.code


def main(inputfile):
    codes = [ l.strip() for l in open(inputfile)]

    total = 0
    for code in codes:
        operator = Operator(code)
        u0 = ("A", "A", "A", None, None, None, None)
        print(operator[u0])

        path, best_distance, _ = dijkstra(operator, u0, lambda u: operator.is_goal(u))
        print(path, best_distance)

        digits = int(code[:-1])
        total += digits * best_distance
    print(f"{total=}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
