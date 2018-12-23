INPUT = 704321


def part1(input):
    scores = '37'
    elf1_index = 0
    elf2_index = 1
    for _ in range(input + 10):
        elf1_score = int(scores[elf1_index])
        elf2_score = int(scores[elf2_index])
        result = str(elf1_score + elf2_score)
        scores += result[0]
        if len(result) > 1:
            scores += result[1]
        elf1_index = (elf1_index + elf1_score + 1) % len(scores)
        elf2_index = (elf2_index + elf2_score + 1) % len(scores)
    return scores[input:input + 10]


def main():
    assert part1(9) == '5158916779'
    assert part1(5) == '0124515891'
    assert part1(18) == '9251071085'
    assert part1(2018) == '5941429882'

    print(part1(INPUT))


if __name__ == "__main__":
    main()
