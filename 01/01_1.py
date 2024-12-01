def main(filename):
    lists = [l.split() for l in open(filename)]
    listL = [int(l[0]) for l in lists]
    listR = [int(l[1]) for l in lists]
    distances = [abs(l - r) for l, r in zip(sorted(listL), sorted(listR))]
    print(sum(distances))


if __name__ == "__main__":
    main("input_1.txt")
