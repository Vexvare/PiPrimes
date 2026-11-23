"""Independent checks for the exact automaton, analytic null, and C++ scanner."""
import csv
from itertools import product
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from modular_automaton import (count_hits, exact_null_mean, multiplicative_order_10,
                               random_tail_probability, scan_states, transition,
                               universal_path, rigorous_null_variance_upper)


class ModularAutomatonTests(unittest.TestCase):
    def test_orders(self):
        self.assertEqual({p: multiplicative_order_10(p) for p in (3,7,11,13,37,41,101)},
                         {3:1,7:6,11:2,13:6,37:3,41:5,101:4})
        for p in (2, 5, 10):
            with self.assertRaises(ValueError):
                multiplicative_order_10(p)

    def test_states_against_large_integer(self):
        for digits in ("3", "31", "314159265358979323846", "301000171"):
            expected = 0
            for n, state, phase in scan_states(digits, 7):
                if n:
                    expected += int(digits[n-1]) * 10**(n-1)
                self.assertEqual(state, expected % 7)
                self.assertEqual(phase, n % 6)
                if n < len(digits):
                    self.assertEqual(transition((state,phase), int(digits[n]), 7),
                                     ((expected+int(digits[n])*10**n)%7,(n+1)%6))

    def test_constructive_strong_connectivity(self):
        for p in (3,7,11,13):
            k = multiplicative_order_10(p)
            for a in range(k):
                for b in range(k):
                    for s in range(p):
                        for t in range(p):
                            word = universal_path(p, (s,a), (t,b))
                            self.assertTrue(word and word.isdecimal())
                            r,ph=s,a
                            for digit in word:
                                r,ph=transition((r,ph), int(digit), p)
                            self.assertEqual((r,ph),(t,b))

    def test_simple_normal_counterexample(self):
        block = "0123475968"   # each digit 0..9 occurs exactly once
        self.assertEqual(sorted(block), list("0123456789"))
        digits = "3" + block*24
        self.assertEqual(count_hits(digits,11),[])
        self.assertEqual(list(scan_states(digits[:11], 11))[-1],(11,3,1))

    def test_exact_null(self):
        for p in (3,7,11,13):
            for tail in range(4):
                numerator,denominator = random_tail_probability(p,tail)
                brute = sum((13 + 100*sum(int(d)*10**i for i,d in enumerate(word)))%p==0
                            for word in product("0123456789",repeat=tail))
                self.assertEqual((numerator,denominator),(brute,10**tail))
            n=5
            self.assertAlmostEqual(exact_null_mean(p,n,1),
                sum((1 if 3%p==0 else 0) + (1 if 13%p==0 else 0) +
                    sum(random_tail_probability(p,t)[0]/10**t for t in range(1,4))
                    for _ in range(1)))
            self.assertGreater(rigorous_null_variance_upper(100),0)

    @unittest.skipUnless(shutil.which("g++"), "requires g++")
    def test_native_matches_reference(self):
        root=Path(__file__).parent
        with tempfile.TemporaryDirectory() as tmp:
            tmp=Path(tmp)
            binary=tmp/"scan"
            subprocess.run(["g++","-O2","-std=c++17",str(root/"experiments/modular_scan.cpp"),"-o",str(binary)],check=True)
            digits="3141592653589793238462643383279502884197169399375105820974944592"
            (tmp/"digits.txt").write_text(digits)
            subprocess.run([str(binary),str(tmp/"digits.txt"),str(tmp/"counts.csv"),"2","101",str(tmp/"hits.csv"),str(tmp/"phase.csv")],check=True,capture_output=True)
            with (tmp/"counts.csv").open() as fh:
                rows=list(csv.DictReader(fh))
            self.assertEqual(len(rows),24)
            for row in rows:
                p=int(row["prime"])
                expected=count_hits(digits,p,2)
                self.assertEqual(int(row["hits"]),len(expected))
                self.assertEqual(int(row["order10"]),multiplicative_order_10(p))
            with (tmp/"hits.csv").open() as fh:
                hits=list(csv.DictReader(fh))
            self.assertEqual(len(hits),sum(int(row["hits"]) for row in rows))
            for hit in hits:
                p,n,phase=int(hit["prime"]),int(hit["n"]),int(hit["phase"])
                self.assertIn(n,count_hits(digits,p,2))
                self.assertEqual(phase,n%multiplicative_order_10(p))
            with (tmp/"phase.csv").open() as fh:
                phases=list(csv.DictReader(fh))
            for p in (3,7,11,13,37,41,101):
                rows_for_p=[row for row in phases if int(row["prime"])==p]
                self.assertEqual(sum(int(row["hits"]) for row in rows_for_p),len(count_hits(digits,p,2)))


if __name__ == "__main__": unittest.main()