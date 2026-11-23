"""Regression tests for exact complex/modular PiPrimes computations."""
import unittest

from complex_analysis import (compare_modular, gaussian_adjacent, gaussian_pair,
                              modular_scan, reversed_prefixes, root_of_unity_filter)


class ComplexAnalysisTests(unittest.TestCase):
    def test_prefix_recurrence_with_zeros(self):
        self.assertEqual(list(reversed_prefixes("31415")), [3, 13, 413, 1413, 51413])
        self.assertEqual(list(reversed_prefixes("310")), [3, 13, 13])

    def test_exact_residues_and_sieve(self):
        digits = "314159265358979323846"
        values = list(reversed_prefixes(digits))
        for start in (1, 3, 8):
            data = modular_scan(digits, (3, 7, 11, 13, 17), start)
            for p, count in data["counts"].items():
                self.assertEqual(count, sum(v % p == 0 for v in values[start - 1:]))
                self.assertEqual(data["last_residues"][p], values[-1] % p)
            self.assertEqual(data["survivors"], sum(
                all(v % p for p in (3, 7, 11, 13, 17)) for v in values[start - 1:]))
            self.assertEqual(data["tested"], len(digits) - start + 1)

    def test_rejects_invalid_inputs(self):
        for digits in ("", "31x", "٣١", "31.4"):
            with self.assertRaises(ValueError):
                modular_scan(digits, [3])
        for moduli in ((3, 3), (1, 3), (0,), (-1,)):
            with self.assertRaises(ValueError):
                modular_scan("314", moduli)
        with self.assertRaises(ValueError):
            modular_scan("314", [3], start=4)

    def test_roots_of_unity_identity(self):
        for p in (3, 7, 11, 17):
            for value in range(2 * p):
                expected = int(value % p == 0)
                self.assertAlmostEqual(root_of_unity_filter(value, p).real, expected, places=12)
                self.assertAlmostEqual(root_of_unity_filter(value, p).imag, 0, places=12)

    def test_gaussian_pairs_and_axis_exception(self):
        self.assertEqual(gaussian_pair(3, 13),
                         {"real": 8, "imag": 5, "norm": 89, "status": "prime"})
        self.assertEqual(gaussian_pair(13, 413),
                         {"real": 213, "imag": 200, "norm": 85369, "status": "prime"})
        self.assertEqual(gaussian_pair(3, 3)["status"], "prime")
        self.assertEqual(gaussian_pair(13, 13)["status"], "composite")
        with self.assertRaises(ValueError):
            gaussian_pair(3, 4)
        self.assertEqual(gaussian_adjacent("314", 2)[-1]["norm"], 85369)

    def test_gaussian_norms_congruent_nine_mod_twenty(self):
        values = list(reversed_prefixes("31415926535897932384"))
        for left in values:
            for right in values:
                self.assertEqual(gaussian_pair(left, right)["norm"] % 20, 9)

    def test_deterministic_whole_stream_controls(self):
        digits = "31415926535897932384"
        a, summary_a = compare_modular(digits, (3, 7, 11), 5, trials=10, seed=7)
        b, summary_b = compare_modular(digits, (3, 7, 11), 5, trials=10, seed=7)
        self.assertEqual((a, summary_a), (b, summary_b))
        self.assertEqual(a, modular_scan(digits, (3, 7, 11), 5))
        self.assertEqual(summary_a[7]["trials"], 10)
        self.assertEqual(summary_a["survivors"]["trials"], 10)


if __name__ == "__main__":
    unittest.main()