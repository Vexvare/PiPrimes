"""Earliest PiPrimes appearances for every prime through a fixed bound."""
import argparse
import csv
from bisect import bisect_right
from collections import Counter
from math import comb
from random import Random

from sympy import primerange

from Fractal_Pi import constant_digits, digit_word


def first_appearance(digits, prime):
    """For a prime target, return its earliest (step, rule), or None."""
    target = str(prime)[::-1]
    end = 0
    for digit in target:
        pos = digits.find(digit, end)
        if pos < 0:
            return None
        end = pos + 1
    if end == len(target):
        rule = "fundamental"
    elif digits.endswith(target, 0, end):
        rule = "branch"
    else:
        rule = "pruned"
    return end, rule


def steps_for(digits, primes):
    digit_word(digits)
    return [first_appearance(digits, p) for p in primes]


def expected_covered(primes, fixed_prefix, step):
    """Sum target completion probabilities under independent uniform tail digits."""
    remaining = Counter()
    for prime in primes:
        target = str(prime)[::-1]
        for digit in fixed_prefix[:step]:
            if target.startswith(digit):
                target = target[1:]
        remaining[len(target)] += 1
    draws = max(0, step - len(fixed_prefix))
    outcomes = 10**draws
    successful = 0
    for needed, multiplicity in remaining.items():
        if needed <= draws:
            # Count digit strings with fewer than 'needed' successful matches.
            too_few = sum(comb(draws, i) * 9**(draws - i) for i in range(needed))
            successful += multiplicity * (outcomes - too_few)
    return successful / outcomes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--power", type=int, default=4, help="test primes through 10^power")
    parser.add_argument("--digits", type=int, default=100)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--csv", help="save pi first appearances, including missing targets")
    args = parser.parse_args()
    if args.digits < 2 or min(args.power, args.trials) < 1:
        parser.error("require at least two digits, positive power and positive trials")
    digits = constant_digits(args.digits)
    primes = list(primerange(2, 10**args.power + 1))
    hits = steps_for(digits, primes)
    if args.csv:
        with open(args.csv, "w", newline="") as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(("prime", "first_step", "rule"))
            for prime, hit in zip(primes, hits):
                writer.writerow((prime, *(hit or ("", ""))))

    def endpoints(rows):
        return sorted(row[0] for row in rows if row is not None)

    observed = endpoints(hits)
    rng = Random(args.seed)
    checkpoints = sorted({(args.digits * q + 3) // 4 for q in (1, 2, 3, 4)})
    counts = [bisect_right(observed, step) for step in checkpoints]
    totals = Counter()
    exceedances = Counter()
    finish = observed[-1] if len(observed) == len(primes) else None
    finished_by_pi = 0
    for _ in range(args.trials):
        stream = digits[:2] + "".join(str(rng.randrange(10)) for _ in digits[2:])
        sample = endpoints(steps_for(stream, primes))
        if finish is not None and len(sample) == len(primes) and sample[-1] <= finish:
            finished_by_pi += 1
        for step, count in zip(checkpoints, counts):
            covered = bisect_right(sample, step)
            totals[step] += covered
            exceedances[step] += covered >= count
    print(f"{len(primes)} targets, {args.digits} digits, {args.trials} controls, seed {args.seed}")
    if finish is not None:
        print(f"Pi covers all targets by step {finish}. {finished_by_pi}/{args.trials} controls finish by then")
    print("step\tpi covered\texact null mean\tcontrol mean covered\tcontrols >= pi")
    for step, count in zip(checkpoints, counts):
        expected = expected_covered(primes, digits[:2], step)
        print(f"{step}\t{count}\t{expected:.2f}\t{totals[step]/args.trials:.2f}\t"
              f"{exceedances[step]}/{args.trials}")


if __name__ == "__main__":
    main()
