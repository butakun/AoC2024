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
    def __init__(self, directionals=25):
        self.TT = [T_DIRECTIONAL] * directionals + [T_NUMERIC]

    def __getitem__(self, u):
        pp = u
        vv = []
        for t in "^v<>":
            T = T_DIRECTIONAL[pp[0]]
            if t in T:
                ppn = list(pp).copy()
                ppn[0] = T[t]
                vv.append(tuple(ppn))

        # what if the operator pressed A?
        try:
            index_not_A = next(i for i, p in enumerate(pp) if p != "A")
            button_pressed = pp[index_not_A]
            if index_not_A < len(pp) - 1:
                index_being_moved = index_not_A + 1
                p_being_moved = pp[index_being_moved]
                T = self.TT[index_being_moved]
                if button_pressed in T[p_being_moved]:
                    p_next = T[p_being_moved][button_pressed]
                    ppn = list(pp).copy()
                    ppn[index_being_moved] = p_next
                    vv.append(tuple(ppn))
            else:
                # the last numerical key is being pressed.
                pass

        except StopIteration:
            # all A's, no other state transition.
            pass

        vvw = [ (v, 1) for v in vv ]
        return vvw


def dump_path(path):
    path = path.copy()
    path.reverse()
    for p1, p2 in zip(path[:-1], path[1:]):
        a, b, t = p1[0], p2[0], None
        if a == b:
            t = "A"
        else:
            for t_, b_ in T_DIRECTIONAL[a].items():
                if b_ == b:
                    t = t_
                    break
        assert t, ValueError(f"{a=}, {b=}")
        print("".join(p1), t)
    print("".join(path[-1]))


def main(inputfile):
    codes = [ l.strip() for l in open(inputfile)]

    n_directionals = 2
    operator = Operator(n_directionals)

    total_complexities = 0
    for code in codes:
        u0 = ("A", ) * n_directionals + ("A",)
        steps = 0
        for letter in code:
            path, best_distance, _ = dijkstra(operator, u0, lambda u: "".join(u) == f"AA{letter}")
            print(path[0], best_distance + 1)  # +1 because pressing "A" is not included in the above dijkstra
            u0 = path[0]
            #dump_path(path)
            steps += best_distance + 1
        complexity = int(code[:3]) * steps
        print(f"{code=}: {steps=}, {complexity=}")
        total_complexities += complexity
    print(f"{total_complexities=}")



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
