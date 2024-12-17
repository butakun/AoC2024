import os
import logging
import numpy as np
from collections import defaultdict

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

    code = f.readline().strip().split()[-1].split(",")
    code = [ int(c) for c in code ]
    return registers, code


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

    R[3] = ipnext

    return output


def run(R, code):
    outputs = []
    logger.debug(f"_,_:{R}")
    while True:
        ip = R[3]
        if ip >= len(code):
            break
        opcode, operand = code[ip], code[ip+1]
        output = step(R, opcode, operand)
        logger.debug(f"{opcode},{operand}:{R}")
        if output is not None:
            outputs.append(output)

    return outputs


def pattern_to_bits(p):
    bits = {}
    for i, v in enumerate(reversed(list(p))):
        if v == ".":
            continue
        bits[i] = int(v)
    return bits


def conflict(bits1, bits2):
    common = set(bits1.keys())
    common &= set(bits2.keys())
    for b in common:
        if bits1[b] != bits2[b]:
            return True
    return False


def merge(bits1, bits2):
    merged = bits1.copy()
    merged.update(bits2)
    return merged


def bits_compact(bits):
    if not bits:
        return "." * 55
    nbits = 55
    return "".join(reversed([str(bits[i]) if i in bits else "." for i in range(nbits)]))

def bits_to_value(bits):
    nbits = max(bits.keys()) + 1
    buf = []
    for i in range(nbits):
        if i in bits:
            buf.append(str(bits[i]))
        else:
            buf.append("0")
    buf.reverse()
    value = int("".join(buf), 2)
    return value


def verify_table(table, R0, code):
    for target, pats in table.items():
        for pat in pats:
            nslots = pat.count(".")
            pat = np.array(list(pat))
            slots = np.where(pat == ".")[0]
            for i in range(pow(2, nslots)):
                a = pat.copy()
                bb = f"{i:0{nslots}b}"
                for j, b in enumerate(list(bb)):
                    a[slots[j]] = b
                a = "".join(a)
                A = int(a, 2)
                R = R0.copy()
                R[0] = A
                outputs = run(R, code)
                logger.debug(f"{a=}, {A=}, {outputs[0]} == {target}?")
                assert(outputs[0] == target)


def search(R0, code):
    table = {
        #    bits
        #    11             11             11             11             11             11             11             11
        #    10987654321    10987654321    10987654321    10987654321    10987654321    10987654321    10987654321    10987654321
        0: [ ".010...000",  "011....001",  "...000.010",  "..001..011",                 "....111101",                              ],
        1: [ ".011...000",  "010....001",  "...001.010",  "..000..011",  ".....11100",  "....110101",                              ],
        2: [ ".000...000",  "001....001",  "...010.010",  "..011..011",                 "....101101",  ".......110",  "......1111" ],
        3: [ ".001...000",  "000....001",  "...011.010",  "..010..011",  ".....10100",  "....100101",                              ],
        4: [ ".110...000",  "111....001",  "...100.010",  "..101..011",                 "....011101",                              ],
        5: [ ".111...000",  "110....001",  "...101.010",  "..100..011",  ".....01100",  "....010101",                              ],
        6: [ ".100...000",  "101....001",  "...110.010",  "..111..011",                 "....001101",                 "......0111" ],
        7: [ ".101...000",  "100....001",  "...111.010",  "..110..011",  ".....00100",  "....000101",                              ],
        }

    #verify_table(table, R0, code)

    candidates = [{}]
    for i, target in enumerate(code[:15]):
        i0 = i * 3
        print(f"TARGET {target=}")

        new_candidates = []
        for pattern in table[target]:
            bits = pattern_to_bits(pattern)
            # shift bits
            bits = { i0+i: v for i, v in bits.items() }
            print(f"testing {pattern=}, {bits_compact(bits)}")

            for candidate in candidates:
                if conflict(bits, candidate):
                    print(f"***< {bits_compact(candidate)}")
                    print(f"***> {bits_compact(bits)}")
                    continue
                print(f"===< {bits_compact(candidate)}")
                print(f"===> {bits_compact(bits)}")
                merged = merge(bits, candidate)
                new_candidates.append(merged)

        print("new candidates")
        for c in new_candidates:
            print(f"  {bits_compact(c)}")

        candidates = new_candidates
    print(candidates)

    print("verifying the solutions")
    AA = []
    for bits in candidates:
        A = bits_to_value(bits)
        print(f"{bits_compact(bits)}, {A=}")
        R = R0.copy()
        R[0] = A
        outputs = run(R, code)
        assert np.all(np.array(outputs) == np.array(code))
        print(f"{outputs=}")
        AA.append(A)
    print(min(AA))


def main(inputfile, vis):
    R0, code = read(inputfile)
    print(R0, code)
    code0 = ",".join(map(str, code))
    search(R0, code)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    parser.add_argument("--vis", action="store_true")
    args = parser.parse_args()
    main(args.input, args.vis)
