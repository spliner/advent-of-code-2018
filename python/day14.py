INPUT = 704321


def part1(recipes):
    scores = '37'
    score_gen = generate_scores(scores)
    for _ in range(recipes + 10):
        scores += next(score_gen)
    return scores[recipes:recipes + 10]


def generate_scores(initial_scores):
    scores = initial_scores
    elf1 = 0
    elf2 = 1
    while True:
        score1 = int(scores[elf1])
        score2 = int(scores[elf2])
        result = str(score1 + score2)
        scores += result
        yield result
        elf1 = (elf1 + score1 + 1) % len(scores)
        elf2 = (elf2 + score2 + 1) % len(scores)


def part2(recipes):
    scores = '37'
    score_gen = generate_scores(scores)
    length = len(recipes)
    while recipes not in scores[-length:]:
        scores += next(score_gen)
    return scores.index(recipes)


def main():
    assert part1(9) == '5158916779'
    assert part1(5) == '0124515891'
    assert part1(18) == '9251071085'
    assert part1(2018) == '5941429882'
    print(part1(INPUT))

    assert part2('51589') == 9
    assert part2('01245') == 5
    assert part2('92510') == 18
    assert part2('59414') == 2018
    print(part2(str(INPUT)))


if __name__ == "__main__":
    main()
