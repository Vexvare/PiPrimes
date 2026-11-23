import unittest
from decimal import Decimal
from itertools import product
from math import isqrt
from pathlib import Path

from Fractal_Pi import branch_prime, branch_primes, constant_digits, discoveries, pruned_prime


class PiPrimesTests(unittest.TestCase):
    def test_original_example(self):
        self.assertEqual(list(discoveries("314")), [
            (1, "fundamental", 3), (2, "fundamental", 13),
            (3, "branch", 41), (3, "pruned", 43)])

    def test_multiple_proper_prefixes(self):
        self.assertEqual(list(branch_primes(237)), [2, 23])
        self.assertEqual(branch_prime(237), 2)
        self.assertIs(branch_prime(13), False)

    def test_rules_against_masks(self):
        # Independent enumeration of every anchored position mask.
        for digits in product("023", repeat=5):
            word = "".join(digits)
            expected = {}
            for mask in range(1, 1 << len(word), 2):
                indices = [i for i in range(len(word)) if mask & (1 << i)]
                value = int("".join(word[i] for i in indices))
                if value < 2 or any(value % d == 0 for d in range(2, isqrt(value) + 1)):
                    continue
                if len(indices) == len(word):
                    rank = 0
                elif indices[-1] + 1 == len(indices):
                    rank = 1
                else:
                    rank = 2
                expected[value] = min(rank, expected.get(value, 2))
            rows = list(discoveries(word[::-1], at_end=True))
            actual = {v: ("fundamental", "branch", "pruned").index(r) for _, r, v in rows}
            self.assertEqual(len(actual), len(rows))
            self.assertEqual(expected, actual, word)

    def test_combined_branch_and_prune(self):
        self.assertIn(47, pruned_prime("4173"))
        self.assertEqual(pruned_prime("413"), [43])

    def test_zero_steps(self):
        self.assertEqual(list(discoveries("310", "fundamental")),
                         [(1, "fundamental", 3), (2, "fundamental", 13)])
        self.assertEqual(list(discoveries("310", "fundamental", at_end=True)),
                         [(3, "fundamental", 13)])

    def test_decimal_truncation(self):
        self.assertEqual(constant_digits(4), "3141")
        self.assertEqual(constant_digits(5, "e"), "27182")
        self.assertEqual(constant_digits(5, "sqrt2"), "14142")

    def test_archived_digits(self):
        for length in (712, 7599):
            path = Path(__file__).parent / "records" / f"{length}.txt"
            self.assertEqual(constant_digits(length)[::-1], path.read_text().strip())

    def test_712_digit_prp(self):
        word = constant_digits(712)
        self.assertEqual(list(discoveries(word, "fundamental", at_end=True)),
                         [(712, "fundamental", int(Decimal(word[::-1])))])


if __name__ == "__main__":
    unittest.main()
