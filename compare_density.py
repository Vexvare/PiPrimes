"""Compare distinct fundamental hits against matched random digit streams."""
import argparse
from random import Random
from statistics import mean

from Fractal_Pi import constant_digits, discoveries


def compare(digits, trials, seed):
    """Preserve the first two digits, length, and nested-prefix search."""
    rng = Random(seed)

    def hits(stream):
        return sum(1 for _ in discoveries(stream, mode="fundamental"))

    observed = hits(digits)
    controls = []
    for _ in range(trials):
        suffix = "".join(str(rng.randrange(10)) for _ in digits[2:])
        controls.append(hits(digits[:2] + suffix))
    return observed, controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, default=100)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if args.digits < 3 or args.trials < 1:
        parser.error("supply at least three digits and one trial")
    observed, controls = compare(constant_digits(args.digits), args.trials, args.seed)
    upper = sum(count >= observed for count in controls)
    print(f"{args.digits} digits, {args.trials} controls, seed {args.seed}")
    print(f"Distinct fundamental hits: pi {observed}, control mean {mean(controls):.2f}")
    print(f"Controls with at least as many hits as pi: {upper}/{args.trials}")


if __name__ == "__main__":
    main()
