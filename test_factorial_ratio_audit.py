"""Tests for exact factorial-ratio arithmetic and nonnormal controls."""
from fractions import Fraction
from math import gcd
import unittest

from experiments.factorial_ratio_audit import (
    approximant, denominator, lcm_upto, phase_fraction, sparse_orbit_mean, w
)


class FactorialRatioTests(unittest.TestCase):
    def test_terms(self):
        self.assertEqual([w(j) for j in range(5)],
                         [Fraction(1), Fraction(1,3), Fraction(2,15),
                          Fraction(2,35), Fraction(8,315)])

    def test_reduced_denominator(self):
        for j in range(101):
            self.assertEqual(denominator(j),w(j).denominator)
            self.assertEqual(denominator(j)%2,1)

    def test_denominator_divides_lcm(self):
        for j in range(61):
            self.assertEqual(lcm_upto(2*j+1)%denominator(j),0)

    def test_phase_moduli_coprime_to_ten(self):
        for n in range(1,31):
            self.assertEqual(gcd(phase_fraction(n).denominator,10),1)

    def test_nested_pi_intervals(self):
        for m in range(1,41):
            self.assertLessEqual(approximant(m-1),approximant(m))
            self.assertLessEqual(approximant(m)+w(m),
                                 approximant(m-1)+w(m-1))

    def test_exponential_error(self):
        for n in range(1,41):
            self.assertLessEqual(10**n*w(4*n),Fraction(5,8)**n)

    def test_sparse_nonnormal_control(self):
        self.assertGreater(abs(sparse_orbit_mean(1000)),.99)
        self.assertGreater(abs(sparse_orbit_mean(10000)),
                           abs(sparse_orbit_mean(1000)))


if __name__=="__main__":
    unittest.main()