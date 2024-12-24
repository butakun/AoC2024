import os
import logging
from collections import defaultdict

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


def main(inputfile):
    wires, gates = read(inputfile)
    print(wires)
    print(gates)

    Go = dict()
    for gate in gates:
        logic, i1, i2, o = gate
        assert o not in Go
        Go[o] = gate
    print(Go)

    zz = sorted([ z for z in wires.keys() if z.startswith("z") ])
    Q = [ Go[z] for z in zz ]
    while Q:
        gate = Q.pop(0)
        print(f"gate = {gate}")
        _, i1, i2, o = gate
        if wires[i1] is not None and wires[i2] is not None:
            if wires[o] is None:
                print(f"processing {gate}")
                process(gate, wires)
        else:
            if wires[i1] is None:
                Q.append(Go[i1])
            if wires[i2] is None:
                Q.append(Go[i2])
            Q.append(gate)

    zz = sorted([ z for z in wires.keys() if z.startswith("z") ])
    Z = 0
    for z in zz:
        v = wires[z]
        i = int(z[1:])
        Z += int(v) * pow(2, i)
    print(f"{Z:b}")
    print(Z)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
