"""Smoke tests for composite-modulus analysis and frozen 9103 holdout engine."""
import json
from math import gcd
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from experiments.composite_moduli import modular_counts
from modular_automaton import count_hits


class CompositeTests(unittest.TestCase):
    def test_composite_counts_match_reference(self):
        digits="314159265358979323846264338327950288419716939937510"
        mods=(9,21,49,77,91,121,143,20,50,100,125,175)
        rows=modular_counts(digits,mods,start=4)
        self.assertEqual([r["hits"] for r in rows],
                         [len(count_hits(digits,m,start=4)) if gcd(m,10)==1 else 0 for m in mods])
        for r in rows:
            if gcd(r["modulus"],10)>1:
                self.assertEqual(r["hits"],0)
                self.assertIsNone(r["iid_expected_approx"])

    def test_stabilized_mod_10powers(self):
        digits="3141592653589793238462643383279502884197"
        for L in range(1,5):
            suffix=int(digits[:L][::-1])
            for n in range(L,len(digits)+1):
                self.assertEqual(int(digits[:n][::-1])%10**L,suffix)

    @unittest.skipUnless(shutil.which("g++"),"requires C++ compiler")
    def test_holdout_native_synthetic(self):
        source=Path(__file__).parent/"experiments"/"validate_9103.cpp"
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)
            exe=path/"holdout"
            subprocess.run(["g++","-O2","-std=c++17",str(source),"-o",str(exe)],check=True)
            digits="3141592653589793238462643383279502884197169399375105820974944592"
            (path/"digits.txt").write_text(digits)
            command=[str(exe),str(path/"digits.txt"),"15",str(len(digits))]
            first=json.loads(subprocess.run(command,check=True,capture_output=True,text=True).stdout)
            second=json.loads(subprocess.run(command,check=True,capture_output=True,text=True).stdout)
            self.assertEqual(first,second)
            self.assertEqual(first["observed_hits"],len(count_hits(digits,9103,start=16)))
            self.assertEqual(first["control_trials"],9999)
            self.assertAlmostEqual(first["one_sided_p"],(first["controls_greater_equal"]+1)/10000)
            self.assertEqual(first["validation_start"],16)
            self.assertEqual(first["validation_end"],len(digits))

if __name__ == "__main__":
    unittest.main()