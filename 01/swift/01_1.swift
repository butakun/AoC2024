import Foundation

func read(_ path: String) -> ([Int], [Int]) {
    let buf = try! String(contentsOfFile: path, encoding: String.Encoding.utf8)
    var left: [Int] = [], right: [Int] = []

    buf.split(separator: "\n")
        .map({ $0.split(separator: " ").map({ Int($0)! }) })
        .forEach({
            left.append($0[0])
            right.append($0[1])
        })
    return (left, right)
}

func main() {
    let filename: String?
    if CommandLine.arguments.count > 1 {
        filename = CommandLine.arguments[1]
    } else {
        filename = "../input.txt"
    }

    var (left, right) = read(filename!)
    left.sort()
    right.sort()
    var count = 0
    for (l, r) in zip(left, right) {
        count += abs(l - r)
    }
    print(count)
}

main()