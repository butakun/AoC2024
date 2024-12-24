import os
import logging
from collections import defaultdict
from pyfiglet import Figlet

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    f = open(inputfile)
    wires = {}
    for l in f:
        if not l.strip():
            break
        wire, value = l.strip().split(": ")
        wires[wire] = bool(int(value))

    gates = []
    for l in f:
        input1, logic, input2, _, output = l.strip().split()
        gates.append((logic, input1, input2, output))
        if input1 not in wires:
            wires[input1] = None
        if input2 not in wires:
            wires[input2] = None
        if output not in wires:
            wires[output] = None
    return wires, gates


def process(gate, wires):
    logic, i1, i2, o = gate
    assert wires[o] is None
    if logic == "AND":
        wires[o] = wires[i1] & wires[i2]
    elif logic == "OR":
        wires[o] = wires[i1] | wires[i2]
    elif logic == "XOR":
        wires[o] = wires[i1] ^ wires[i2]
    else:
        raise ValueError


def run_circuit(Go, zz, wires, gates):
    Q = [ Go[z] for z in zz ]
    while Q:
        gate = Q.pop(0)
        _, i1, i2, o = gate
        if wires[i1] is not None and wires[i2] is not None:
            if wires[o] is None:
                process(gate, wires)
        else:
            if wires[i1] is None:
                Q.append(Go[i1])
            if wires[i2] is None:
                Q.append(Go[i2])
            Q.append(gate)

    Z = 0
    for z in zz:
        v = wires[z]
        i = int(z[1:])
        Z += int(v) * pow(2, i)
    return Z


def eval_register(letter, wires):
    rr = [ r for r in wires.keys() if r.startswith(letter) ]
    R = 0
    for r in rr:
        v = wires[r]
        i = int(r[1:])
        R += int(v) * pow(2, i)
    return R


def dump_graphviz(gates, filename="circuit.dot"):
    with open(filename, "w") as f:
        print("digraph {", file=f)
        ins = set()
        for ig, (logic, i1, i2, o) in enumerate(gates):
            print(f"{i1} -> {o}", file=f)
            print(f"{i2} -> {o}", file=f)

            attr = dict()
            if o[0] == "z":
                attr["style"] = "bold"
            if logic == "AND":
                attr["shape"] = "box"
            elif logic == "OR":
                attr["shape"] = "egg"
            elif logic == "XOR":
                attr["shape"] = "diamond"
            attr_str = ",".join([ f"{k}=\"{v}\""for k, v in attr.items() ])
            print(f"{o} [{attr_str}]", file=f)
            for i in [i1, i2]:
                if i in ins:
                    continue
                if i[0] == "x":
                    print(f"{i} [color=\"red\"]", file=f)
                    ins.add(i)
                elif i[0] == "y":
                    print(f"{i} [color=\"blue\"]", file=f)
                    ins.add(i)
        print("}", file=f)


def upstream_gates(gate, Go):
    upstreams = dict()
    Q = [ gate ]
    while Q:
        g = Q.pop(0)
        _, i1, i2, o = g
        if o not in upstreams:
            upstreams[o] = gate
        if i1 in Go:
            Q.append(Go[i1])
        if i2 in Go:
            Q.append(Go[i2])
    return upstreams


def main(inputfile):
    wires, gates = read(inputfile)
    wires0 = wires.copy()

    Go = dict()
    for gate in gates:
        logic, i1, i2, o = gate
        assert o not in Go
        Go[o] = gate

    dump_graphviz(gates)

    X = eval_register("x", wires)
    Y = eval_register("y", wires)
    Zcorrect = X + Y
    print(f"{X=}, {Y=}, {Zcorrect=}")

    zz = sorted([ z for z in wires.keys() if z.startswith("z") ])

    Z = run_circuit(Go, zz, wires, gates)
    print(Z)

    print(f"{Zcorrect:046b}")
    print(f"{Z:046b}")
    nbits = 46

    wrong_zs = []
    xor = Z^Zcorrect
    print(f"{xor:{nbits}b}")
    for i in range(nbits):
        wrong = xor >> i & 1
        if wrong:
            print(f"{i}(z{i:02d}) is wrong")
            wrong_zs.append(f"z{i:02d}")

    print("now do dot -Tpng input.txt > circuit.png, and swap 4 pairs of outputs by hand.")
    print(Figlet(font="cosmic").renderText("God  Jul  !"))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
