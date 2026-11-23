"""Tests for the finite, exact portions of normality diagnostics."""
import cmath
import tempfile
import unittest
from pathlib import Path

from normality_weyl import analyze, digit_stream


class NormalityTests(unittest.TestCase):
    def test_reverse_prefix_recurrence(self):
        x = 0.0
        for digit, expected in zip([3, 1, 4, 1, 5], [.3, .13, .413, .1413, .51413]):
            x = (x + digit)/10
            self.assertAlmostEqual(x, expected, places=12)

    def test_exact_finite_block_counts(self):
        report = analyze([3, 1, 4, 1], harmonics=(1,), max_block=2)
        self.assertEqual(report['blocks']['2']['sample_size'], 3)
        self.assertEqual(report['blocks']['2']['max_word_count'], 1)
        self.assertEqual(report['blocks']['2']['min_word_count'], 0)

    def test_spectral_identity(self):
        xs = []
        x = 0
        for d in [3, 1, 4, 1, 5, 9, 2, 6, 5]:
            x = (x+d)/10
            xs.append(x)
        for h in [1, 2, 7, 19]:
            f = lambda y: cmath.exp(2j*cmath.pi*h*y)
            slow = sum(f(y) for y in xs)
            fast = sum(f(10*y) for y in xs)
            self.assertAlmostEqual(abs(fast - (slow + 1-f(xs[-1]))), 0, places=11)

    def test_digit_reading(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'digits.txt'
            path.write_text('314\n159 26\n', encoding='ascii')
            self.assertEqual(list(digit_stream(path, 6)), [3, 1, 4, 1, 5, 9])
            self.assertEqual(list(digit_stream(path)), [3, 1, 4, 1, 5, 9, 2, 6])
            path.write_text('31e4', encoding='ascii')
            with self.assertRaises(ValueError):
                list(digit_stream(path))

    def test_reject_empty_and_bad_harmonics(self):
        with self.assertRaises(ValueError):
            analyze([])
        with self.assertRaises(ValueError):
            analyze([3], harmonics=[0])


if __name__ == '__main__':
    unittest.main()
