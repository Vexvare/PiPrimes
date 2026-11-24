import unittest
from fractions import Fraction
from math import factorial
from spigot_audit import (run_spigot, emitted_digits, verify_certificate,
                          input_only_interval, digit_free_weyl)

PI50 = '314159265358979323846264338327950288419716939937510'
PILO = Fraction(int(PI50), 10**(len(PI50)-1))
PIHI = PILO + Fraction(1, 10**(len(PI50)-1))

class SpigotAuditTests(unittest.TestCase):
 def test_first_digits_no_external_digit_input(self):
  ev=run_spigot(20)
  self.assertEqual(emitted_digits(ev),'31415926535897932384')
  self.assertEqual([e.consumed for e in ev if e.operation=='emit'][:6],
                   [1,3,8,9,13,17])

 def test_width_invariant(self):
  for e in run_spigot(20):
   i=e.consumed
   width=Fraction(10**e.emitted*2**i*factorial(i)**2, factorial(2*i+1))
   self.assertEqual(e.hi-e.lo,width)

 def test_pi_interval_certificates(self):
  ev=run_spigot(20)
  self.assertTrue(verify_certificate(ev,PILO))
  self.assertTrue(verify_certificate(ev,PIHI))

 def test_input_only_intervals(self):
  for m in [0,1,2,10,20,40]:
   lo,hi=input_only_interval(m)
   self.assertLessEqual(lo,PILO)
   self.assertGreaterEqual(hi,PIHI)
   self.assertLessEqual(hi-lo,Fraction(1,2**m))

 def test_unsafe_narrow_interval(self):
  ev=run_spigot(20)
  self.assertTrue(any(e.operation=='consume' and e.hi-e.lo < 1
                      and e.lo.numerator//e.lo.denominator !=
                      e.hi.numerator//e.hi.denominator for e in ev))

 def test_digit_free_spectral_bound_and_execution(self):
  for n in range(1,12):
   lo,hi=input_only_interval(4*n)
   self.assertLessEqual(10**n*(hi-lo),Fraction(5,8)**n)
  self.assertLessEqual(digit_free_weyl(5,(1,7))[1],1)

if __name__=='__main__':unittest.main()