"""Landon Wells's PiPrimes game on reversed finite decimal prefixes."""
import argparse
from decimal import Decimal
from itertools import combinations

import gmpy2
from mpmath.ctx_iv import MPIntervalContext
from sympy import isprime


_SMALL_FACTORS = gmpy2.primorial(10000)


def passes_prime_test(value):
    """Use deterministic small-integer tests and a sieved strong BPSW for large values."""
    if value < 2**64:
        return isprime(value)
    return gmpy2.gcd(value, _SMALL_FACTORS) == 1 and gmpy2.is_strong_bpsw_prp(value)


def constant_digits(count, constant="pi"):
    """Return count truncated digits, including the units digit."""
    if count < 1:
        raise ValueError("count must be positive")
    ctx = MPIntervalContext()
    ctx.dps = count + 12
    scale = 10 ** (count - 1)
    while True:
        value = {"pi": lambda: ctx.pi, "e": lambda: ctx.exp(1),
                 "sqrt2": lambda: ctx.sqrt(2)}[constant]() * scale
        lower, upper = int(value.a), int(value.b)
        if lower == upper:
            return str(Decimal(lower))
        ctx.dps += 16


def digit_word(value):
    word = str(Decimal(value)) if isinstance(value, int) else value
    if not isinstance(word, str) or not word.isascii() or not word.isdecimal():
        raise ValueError("expected a nonempty string of ASCII digits or a nonnegative integer")
    return word


def fundamental_prime(pi_reversed):
    return passes_prime_test(gmpy2.mpz(digit_word(pi_reversed), 10))


def branch_primes(pi_reversed):
    """Yield every prime proper prefix, shortest first."""
    word = digit_word(pi_reversed)
    value = 0
    for digit in word[:-1]:
        value = 10 * value + int(digit)
        if passes_prime_test(value):
            yield value


def branch_prime(pi_reversed):
    """Original single-result interface."""
    return next(branch_primes(pi_reversed), False)


def pruned_prime(pi_reversed):
    """Distinct prime values from gapped prefixes, including the full word."""
    word = digit_word(pi_reversed)
    found = set()
    for end in range(2, len(word)):
        # Keep both endpoints and omit at least one interior position.
        if word[end] in "024568" and word[0] != "0":
            continue
        for size in range(end - 1):
            for interior in combinations(word[1:end], size):
                value = int(Decimal(word[0] + "".join(interior) + word[end]))
                if value not in found and passes_prime_test(value):
                    found.add(value)
    return sorted(found)


def discoveries(digits, mode="all", at_end=False):
    """Yield (source length, rule, value) at the first eligible discovery."""
    digits = digit_word(digits)
    if mode not in ("all", "fundamental"):
        raise ValueError("mode must be all or fundamental")
    seen = set()
    value = 0
    place = 1
    for length, digit in enumerate(digits, 1):
        value += int(digit) * place
        place *= 10
        if at_end and length != len(digits):
            continue
        if mode == "fundamental" and digit == "0" and not at_end:
            continue
        if value not in seen and passes_prime_test(value):
            seen.add(value)
            yield length, "fundamental", value
        if mode == "all":
            word = digits[:length][::-1]
            for rule, candidates in (("branch", branch_primes), ("pruned", pruned_prime)):
                for prime in candidates(word):
                    if prime not in seen:
                        seen.add(prime)
                        yield length, rule, prime


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, default=12, help="includes the units digit")
    parser.add_argument("--constant", choices=["pi", "e", "sqrt2"], default="pi")
    parser.add_argument("--mode", choices=["all", "fundamental"], default="all")
    parser.add_argument("--at-end", action="store_true", help="inspect only the final prefix")
    parser.add_argument("--force", action="store_true", help="allow exponential pruning above 18 digits")
    args = parser.parse_args(argv)
    if args.digits < 1:
        parser.error("--digits must be positive")
    if args.mode == "all" and args.digits > 18 and not args.force:
        parser.error("all-rule pruning is exponential. Select --mode fundamental or supply --force")
    digits = constant_digits(args.digits, args.constant)
    print("length\trule\tstatus\tvalue")
    for length, rule, prime in discoveries(digits, args.mode, args.at_end):
        status = "prime" if prime < 2**64 else "probable-prime"
        print(length, rule, status, Decimal(prime), sep="\t")


if __name__ == "__main__":
    main()
