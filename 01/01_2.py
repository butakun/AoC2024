from collections import Counter


def main(filename):
    lists = [l.split() for l in open(filename)]
    listL = [int(l[0]) for l in lists]
    listR = [int(l[1]) for l in lists]

    counter = Counter(listR)
    s = 0
    for l in listL:
        s += l * counter[l]
    print(s)


if __name__ == "__main__":
    main("input.txt")
