import os
import logging
import re
import numpy as np

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    f = open(inputfile)
    registers = []
    for l in f:
        l = l.strip().split()
        if len(l) == 0:
            break
        r = l[1][:-1]
        v = int(l[2])
        registers.append(v)
    registers.append(0)

    asm = f.readline().strip().split()[-1].split(",")
    asm = [ [int(opcode), int(operand)] for opcode, operand in zip(asm[:-1:2], asm[1::2]) ]
    return registers, asm



def step(R, opcode, operand):
    def combo(o):
        if o < 4:
            return o
        elif o < 7:
            return R[o - 4]
        raise ValueError(f"operand {o}")

    output = None
    ipnext = R[3] + 2
    if opcode == 0:
        op = "adv"
        R[0] //= pow(2, combo(operand))
    elif opcode == 1:
        op = "bxl"
        R[1] = R[1] ^ operand
    elif opcode == 2:
        op = "bst"
        R[1] = combo(operand) % 8
    elif opcode == 3:
        op = "jnz"
        if R[0] != 0:
            ipnext = operand
    elif opcode == 4:
        op = "bxc"
        R[1] = R[1] ^ R[2]
    elif opcode == 5:
        op = "out"
        output = combo(operand) % 8
    elif opcode == 6:
        op = "bdv"
        R[1] = R[0] // pow(2, combo(operand))
    elif opcode == 7:
        op = "cdv"
        R[2] = R[0] // pow(2, combo(operand))
    else:
        raise ValueError(f"opcode {opcode}")
    print(f"{op=}, {operand=}")

    R[3] = ipnext

    return output


def main(inputfile, vis):
    R, code = read(inputfile)
    print(R, code)

    outputs = []
    while True:
        ip = R[3]
        assert ip % 2 == 0
        ip_ = ip // 2
        if ip_ >= len(code):
            break
        opcode, operand = code[ip_]
        output = step(R, opcode, operand)
        print(f"{opcode}, {operand}: {R=}")
        if output is not None:
            print(output)
            outputs.append(output)

    print(",".join(map(str, outputs)))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    parser.add_argument("--vis", action="store_true")
    args = parser.parse_args()
    main(args.input, args.vis)
