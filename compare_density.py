"""Compare distinct fundamental hits against matched random digit streams."""
import argparse
from concurrent.futures import ProcessPoolExecutor
from math import fsum, log
from random import Random
from statistics import mean

from Fractal_Pi import constant_digits, discoveries


def baselines(n):
    """Raw length heuristic and distinct-hit version conditional on the initial 31."""
    raw = fsum(2.5 / (i * log(10)) for i in range(1, n + 1))
    distinct = 2 + 0.9 * fsum(2.5 / (i * log(10)) for i in range(3, n + 1))
    return raw, distinct


def hit_count(stream):
    return sum(1 for _ in discoveries(stream, mode="fundamental"))


def compare(digits, trials, seed, jobs=1):
    """Preserve the first two digits, length, and nested-prefix search."""
    rng = Random(seed)

    def streams():
        yield digits
        for _ in range(trials):
            suffix = "".join(str(rng.randrange(10)) for _ in range(len(digits) - 2))
            yield digits[:2] + suffix

    if jobs == 1:
        observed, *controls = map(hit_count, streams())
    else:
        with ProcessPoolExecutor(max_workers=min(jobs, trials + 1)) as pool:
            observed, *controls = pool.map(hit_count, streams())
    return observed, controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, default=100)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--jobs", type=int, default=1, help="parallel streams")
    args = parser.parse_args()
    if args.digits < 3 or min(args.trials, args.jobs) < 1:
        parser.error("supply at least three digits and positive trial and job counts")
    observed, controls = compare(constant_digits(args.digits), args.trials, args.seed, args.jobs)
    raw, distinct = baselines(args.digits)
    print(f"Heuristic sums: raw {raw:.2f}, matched distinct {distinct:.2f}")
    upper = sum(count >= observed for count in controls)
    print(f"{args.digits} digits, {args.trials} controls, seed {args.seed}")
    print(f"Distinct fundamental hits: pi {observed}, control mean {mean(controls):.2f}")
    print(f"Controls with at least as many hits as pi: {upper}/{args.trials}")


if __name__ == "__main__":
    main()
