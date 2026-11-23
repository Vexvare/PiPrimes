"""Exact modular and exploratory Gaussian-integer analyses for PiPrimes.

The modular computation is integer-only. Complex phases are a visualization
of those exact residues, not a floating-point primality test.
"""
import argparse
import csv
import math
from random import Random
from statistics import mean, pstdev

from sympy import primerange

from Fractal_Pi import constant_digits, passes_prime_test


def checked_digits(digits):
    if not isinstance(digits, str) or not digits or any(d not in "0123456789" for d in digits):
        raise ValueError("digits must be a nonempty ASCII decimal string")
    return digits


def reversed_prefixes(digits):
    """Generate exact R_n, including repeated integers after a zero digit."""
    value, power = 0, 1
    for digit in checked_digits(digits):
        value += int(digit) * power
        yield value
        power *= 10


def modular_scan(digits, moduli, start=1):
    """Count divisibility and small-prime survivors from index start through N.

    A survivor is *not* necessarily prime. The first few R_n may themselves
    equal one of the tested moduli. No huge R_n integers are constructed.
    """
    checked_digits(digits)
    moduli = tuple(moduli)
    if len(set(moduli)) != len(moduli) or any(not isinstance(p, int) or p < 2 for p in moduli):
        raise ValueError("moduli must be distinct integers >= 2")
    if not 1 <= start <= len(digits):
        raise ValueError("start must lie between 1 and the digit count")
    residues = [0] * len(moduli)
    powers = [1] * len(moduli)
    counts = [0] * len(moduli)
    survivors = 0
    for n, digit in enumerate(digits, 1):
        digit = ord(digit) - 48
        has_divisor = False
        for i, p in enumerate(moduli):
            residues[i] = (residues[i] + digit * powers[i]) % p
            powers[i] = powers[i] * 10 % p
            if n >= start and residues[i] == 0:
                counts[i] += 1
                has_divisor = True
        if n >= start and not has_divisor:
            survivors += 1
    return {"tested": len(digits) - start + 1,
            "counts": dict(zip(moduli, counts)),
            "survivors": survivors,
            "last_residues": dict(zip(moduli, residues))}


def root_of_unity_filter(value, modulus):
    """Numerical check of the exact roots-of-unity divisibility identity.

    Use value % modulus == 0 for actual decisions; floating sums are
    intended only for teaching and diagnostics.
    """
    if not isinstance(modulus, int) or modulus < 2:
        raise ValueError("modulus must be >= 2")
    residue = value % modulus
    return sum(complex(math.cos(2 * math.pi * j * residue / modulus),
                       math.sin(2 * math.pi * j * residue / modulus))
               for j in range(modulus)) / modulus


def compare_modular(digits, moduli, start=1, trials=100, seed=0):
    """Match π against entire random streams with identical first two digits.

    The control distribution is empirical. Prefix tests within each stream
    are dependent; never interpret them as independent Bernoulli trials.
    """
    checked_digits(digits)
    if not isinstance(trials, int) or trials < 1:
        raise ValueError("trials must be positive")
    if len(digits) < 2:
        raise ValueError("at least two source digits are required")
    observed = modular_scan(digits, moduli, start)
    moduli = tuple(observed["counts"])
    rng = Random(seed)
    rows = []
    for _ in range(trials):
        stream = digits[:2] + "".join(str(rng.randrange(10)) for _ in range(len(digits) - 2))
        rows.append(modular_scan(stream, moduli, start))
    summary = {}
    for key in (*moduli, "survivors"):
        measured = observed["survivors"] if key == "survivors" else observed["counts"][key]
        samples = [r["survivors"] if key == "survivors" else r["counts"][key] for r in rows]
        summary[key] = {"observed": measured, "control_mean": mean(samples),
                        "control_sd": pstdev(samples),
                        "control_ge": sum(v >= measured for v in samples),
                        "control_le": sum(v <= measured for v in samples),
                        "trials": trials}
    return observed, summary


def gaussian_pair(left, right):
    """Normalize (left + i*right)/(1+i) in the Gaussian integers.

    Returns a rigorous prime/composite classification below 2**64 and a
    probable-prime indication beyond that bound, as in Fractal_Pi.py.
    For non-real values, Gaussian primality iff the norm is rational prime.
    On an axis, a Gaussian prime has magnitude p = 3 (mod 4).
    """
    if not isinstance(left, int) or not isinstance(right, int) or left < 0 or right < 0:
        raise ValueError("components must be nonnegative integers")
    if (left - right) % 2:
        raise ValueError("components must have the same parity")
    real, imag = (left + right) // 2, (right - left) // 2
    norm = real * real + imag * imag
    if real == 0 or imag == 0:
        candidate = abs(real or imag)
        passed = candidate % 4 == 3 and passes_prime_test(candidate)
    else:
        candidate = norm
        passed = passes_prime_test(norm)
    status = ("composite" if not passed else
              "prime" if candidate < 2**64 else "probable-prime")
    return {"real": real, "imag": imag, "norm": norm, "status": status}


def gaussian_adjacent(digits, pairs=20):
    """Examine W_(n,n+1) for the first pairs adjacent prefixes."""
    checked_digits(digits)
    if not 0 <= pairs < len(digits):
        raise ValueError("pairs must lie between 0 and the digit count minus 1")
    values = reversed_prefixes(digits)
    previous = next(values)
    result = []
    for n in range(1, pairs + 1):
        following = next(values)
        result.append({"left_step": n, "right_step": n + 1,
                       **gaussian_pair(previous, following)})
        previous = following
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, default=1000)
    parser.add_argument("--start", type=int, default=100,
                        help="first prefix included in modular counts")
    parser.add_argument("--max-prime", type=int, default=97)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--pairs", type=int, default=20,
                        help="adjacent Gaussian pairs starting at R_1 (0 disables)")
    parser.add_argument("--csv", help="optional CSV file of modulus statistics")
    args = parser.parse_args(argv)
    if not (2 <= args.digits and 1 <= args.start <= args.digits and
            args.max_prime >= 3 and 0 <= args.pairs < args.digits and args.trials >= 1):
        parser.error("require digits >= 2, 1 <= start <= digits, max-prime >= 3, "
                     "0 <= pairs < digits, trials >= 1")
    digits = constant_digits(args.digits)
    moduli = list(primerange(3, args.max_prime + 1))
    observed, result = compare_modular(digits, moduli, args.start, args.trials, args.seed)
    print(f"π digits={args.digits}; prefix lengths={args.start}..{args.digits}; "
          f"random controls={args.trials}; seed={args.seed}")
    print("p\tπ divisible\tcontrol mean\tcontrol SD\tcontrols >= π")
    for p in moduli:
        r = result[p]
        print(f"{p}\t{r['observed']}\t{r['control_mean']:.2f}\t"
              f"{r['control_sd']:.2f}\t{r['control_ge']}/{args.trials}")
    r = result["survivors"]
    print(f"No divisor in tested primes: π {r['observed']}/{observed['tested']}; "
          f"control mean {r['control_mean']:.2f}, SD {r['control_sd']:.2f}; "
          f"controls >= π {r['control_ge']}/{args.trials}")
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["modulus", "pi_divisible", "control_mean", "control_sd", "control_ge", "trials"])
            for p in moduli:
                stat = result[p]
                writer.writerow([p, stat["observed"], stat["control_mean"],
                                 stat["control_sd"], stat["control_ge"], args.trials])
    if args.pairs:
        print("\nNormalized adjacent Gaussian pairs (small samples):")
        print("steps\tW=a+bi\tnorm\tstatus")
        for row in gaussian_adjacent(digits, args.pairs):
            print(f"{row['left_step']},{row['right_step']}\t"
                  f"{row['real']}{row['imag']:+d}i\t{row['norm']}\t{row['status']}")
    print("\nExploratory only: neither survivors nor probable-prime hits prove infinitely many primes.")


if __name__ == "__main__":
    main()