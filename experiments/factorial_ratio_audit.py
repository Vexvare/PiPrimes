"""Exact rational arithmetic audit for Gibbons' pi approximants.

No fixed-frequency Weyl cancellation is established by this program.
"""
from bisect import bisect_right
from fractions import Fraction
from math import comb, cos, gcd, lcm, log10, sin, tau
import argparse


def w(j):
    if j < 0:
        raise ValueError("j must be >= 0")
    return Fraction(2**j, (2*j+1)*comb(2*j, j))


def denominator(j):
    if j < 0:
        raise ValueError("j must be >= 0")
    return ((2*j+1)*comb(2*j,j))//2**j.bit_count()


def approximant(m):
    """P_m = 2*sum(w_j,j<m) + 3*w_m."""
    if m < 0:
        raise ValueError("m must be >= 0")
    term = Fraction(1)
    p = 3*term
    for j in range(m):
        nxt = term*Fraction(j+1, 2*j+3)
        p += 3*nxt-term
        term = nxt
    return p


def phase_fraction(n):
    """Exact rational representative {10^n P_(4n)}."""
    if n < 1:
        raise ValueError("n must be positive")
    a = 10**n * approximant(4*n)
    return a - a.numerator//a.denominator


def lcm_upto(m):
    result = 1
    for j in range(2, m+1):
        result = lcm(result,j)
    return result


def sparse_orbit_mean(n,h=1):
    """Floating-point illustration for beta=sum 10^(-2^k), not a proof."""
    if n < 1:
        raise ValueError("n must be positive")
    powers = [2**k for k in range((n+32).bit_length()+2)]
    total = 0j
    for pos in range(1,n+1):
        start = bisect_right(powers,pos)
        x = sum(10.0**(pos-v) for v in powers[start:] if v-pos<18)
        theta = tau*h*x
        total += complex(cos(theta),sin(theta))
    return total/n


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--samples",type=int,nargs="+",default=[10,100,400])
    p.add_argument("--verify-through",type=int,default=40)
    p.add_argument("--sparse-n",type=int,nargs="+",default=[1000,10000,100000])
    a = p.parse_args()
    for j in a.samples:
        D = denominator(j)
        print(f"j={j:>4} log10(D_j)={log10(D):.6f} digits={len(str(D))}")
    for j in range(a.verify_through+1):
        assert denominator(j)==w(j).denominator
        assert lcm_upto(2*j+1)%denominator(j)==0
    for n in range(1,a.verify_through+1):
        assert gcd(phase_fraction(n).denominator,10)==1
        assert 10**n*w(4*n)<=Fraction(5,8)**n
    print("Exact arithmetic checks passed through",a.verify_through)
    for n in a.sparse_n:
        value=sparse_orbit_mean(n)
        print(f"sparse nonnormal beta: N={n:>7}, |mean|={abs(value):.9f}")


if __name__ == "__main__":
    main()