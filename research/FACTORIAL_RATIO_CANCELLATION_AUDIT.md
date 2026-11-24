# Factorial-ratio Weyl cancellation: rigorous audit and stopping decision

**Status (2026-11-23): NO FIXED-FREQUENCY CANCELLATION ESTIMATE.**
We have rigorous additional denominator facts and explicit adversarial
counterexamples, but have not proved that `T_N(h)=o(N)` for even `h=1`.
The normality of pi remains open. This note records a completed search
for *elementary* leverage, not a theorem ruling out all future methods.

## 1. Definitions

Write `e(t)=exp(2*pi*i*t)` and

\[
w_j=\frac{2^j(j!)^2}{(2j+1)!}
    =\frac{2^j}{(2j+1)\binom{2j}{j}},\qquad
P_m=2\sum_{j=0}^{m-1}w_j+3w_m,
\]
\[
T_N(h)=\sum_{n=1}^N e(h\,10^nP_{4n}).
\]

Gibbons's spigot analysis yields `P_m <= pi <= P_m+w_m`,
`w_m<=2^{-m}` and `P_{m+1}>=P_m`. Thus

\[
0\le 10^n(\pi-P_{4n})\le (5/8)^n,\quad
\left|T_N(h)-\sum_{n=1}^N e(h10^n\pi)\right|
 \le \frac{10\pi}{3}|h|.
\]

**Consequence:** For every fixed nonzero integer h, the rational-sum
estimate `T_N(h)=o(N)` is *equivalent* to cancellation for the actual
decimal orbit `{10^n*pi}`. A proof for all h would prove base-10
normality. This equivalence by itself is valid for arbitrary reals
with suitably accurate rational approximants; it does not establish a
new statistical fact about pi.

## 2. Exact reduced denominators

Let `s_2(j)` be the number of 1-bits in the binary representation of j.
The 2-adic valuation of the central binomial coefficient is exactly
`v_2(C(2j,j))=s_2(j)`. Therefore the *reduced* denominator of w_j is

\[
\boxed{D_j=\frac{(2j+1)\binom{2j}{j}}{2^{s_2(j)}}.}
\]

It is odd, and Stirling's formula gives

\[
\boxed{\log D_j=j\log4+O(\log j).}
\]

Direct exact arithmetic:

| j | log10 D_j | digits in D_j |
|---:|---:|---:|
| 10 | 5.986757855 | 6 |
| 100 | 60.356987401 | 61 |
| 400 | 241.274798411 | 242 |

For every **odd** prime `p` with `j<p<=2j`, `v_p(D_j)=1`. Hence D_j
contains every prime in `(j,2j]`. These are *per-term* denominators;
cancellation may remove prime factors from the **sum** P_m.

## 3. Stronger, exact lcm theorem

**Theorem.** For all j>=0,

\[
\boxed{D_j\mid L_{2j+1},\quad
L_M=\operatorname{lcm}(1,2,\ldots,M).}
\]

**Proof.** For an odd prime p, Legendre's formula gives

\[
v_p(D_j)=\sum_{a\ge1}
\left(\left\lfloor\frac{2j+1}{p^a}\right\rfloor-
2\left\lfloor\frac{j}{p^a}\right\rfloor\right).
\]

Writing j=A*p^a+r, 0<=r<p^a, shows each summand is
`floor((2r+1)/p^a)`, either 0 or 1. It vanishes when
p^a>2j+1. Thus `v_p(D_j)<=floor(log_p(2j+1))=v_p(L_{2j+1})`.
At p=2 the reduced denominator has valuation zero. QED.

Since P_m is an integer linear combination of w_0,...,w_m,
its reduced denominator divides L_{2m+1}.

**Corollary.** Define the reduced fraction

\[
y_n=\{10^nP_{4n}\}=\frac{a_n}{q_n}.
\]

Then `q_n` is **coprime to 10**, and all its prime factors are at most
`8n+1`. More precisely,

\[
\boxed{q_n\mid \prod_{\substack{p\le8n+1\\p\notin\{2,5\}}}
p^{\lfloor\log_p(8n+1)\rfloor}.}
\]

Proof: P_(4n)'s denominator is odd and divides L_(8n+1).
Its 5-adic valuation is at most `floor(log_5(8n+1))<=n` for
all n>=1 (because 8n+1<5^(n+1)), so multiplication by 10^n
eliminates all factors of 5. QED.

Each e(h*y_n) is therefore an **exact root of unity** whose order
is coprime to 10 and whose prime factors are at most 8n+1.
Unlike BBP, however, the modulus *changes with n*.
Prime factor bounds and existence of multiplicative orders do
not provide a fixed-modulus orbit or cancellation over n.

## 4. Dynamics is only a vanishing perturbation

Set `y_n={10^n P_(4n)}`. Then

\[
y_{n+1}=\{10y_n+\varepsilon_n\},\quad
\varepsilon_n=10^{n+1}(P_{4n+4}-P_{4n}).
\]
Since P_m increases to pi,

\[
\boxed{0\le\varepsilon_n\le10^{n+1}w_{4n}
\le10(5/8)^n.}
\]

In circular distance `dist(y_n,{10^n pi})<=(5/8)^n`.
The tail forcing is summable, and the rational orbit shadows
the original pi orbit. Small forcing does not imply mixing or
equidistribution; the exact map `{10y}` itself has fixed and
periodic orbits.

## 5. Additional beta-integral structure does not give cancellation

The factorial ratios have the exact representation

\[
w_j=\int_0^1[2t(1-t)]^j\,dt,
\]
and
\[
2\sum_{j\ge0}w_j=
2\int_0^1\frac{dt}{1-2t(1-t)}=\pi.
\]

This is genuine pi-specific structure. But the phase
`e(h*10^n*integral f(t)dt)` is NOT equal to
`integral e(h*10^n*f(t))dt`. The integral representation does
not yield a stationary-phase argument for T_N(h) without a new
identity or a nontrivial estimate.

## 6. Adversarial test: optimal irrationality exponent still fails

Let

\[
\beta=\sum_{k\ge0}10^{-2^k}
=0.1101000100000001\ldots.
\]

It is an explicit nonnormal Mahler number. Its irrationality
exponent is known to equal 2 (see the references below). Only
O(log N) digits among the first N are nonzero.

Fix an integer h and a block length K. Of the first N positions,
at most `K*(1+floor(log_2(N+K)))` have a digit 1 among their
next K digits. At every other position
`{10^n beta}<10^{-K}`. Therefore

\[
\left|\frac1N\sum_{n=1}^N e(h10^n\beta)-1\right|
\le2\pi|h|10^{-K}+
\frac{2K(1+\lfloor\log_2(N+K)\rfloor)}N.
\]

First take N to infinity, then K to infinity. We obtain

\[
\boxed{\frac1N\sum_{n=1}^N e(h10^n\beta)\longrightarrow1}
\]
for **every fixed integer h**, not zero.

So even `mu=2` plus irrationality, computability, very accurate
rational approximants, and explicit arithmetic recurrences cannot
by themselves imply Weyl cancellation.

Numerical values in the executable audit are *illustrations*;
the displayed block-count inequality is the proof.

## 7. Go/no-go evaluation

| Candidate technique | Result |
|---|---|
| Approximation error `|pi-P_m|` | Gives O_h(1) comparison, no cancellation |
| Smooth/odd reduced denominators | Exact restriction, but modulus varies with n |
| Multiplicative orders of 10 | Defined for each q_n, no controlled phase correlation |
| Summable forcing in ×10 dynamics | Shadowing of unsolved original orbit |
| Beta-integral / positivity | Identity for pi, no valid phase-integral interchange |
| Irrationality exponent, even mu=2 | Explicit nonnormal beta disproves sufficiency |

**Decision:** Stop pursuing elementary cancellation from these ingredients.
A restart would require a new *pi-specific* theorem giving correlations
among the **reduced numerators a_n as n varies**, or a genuine
oscillatory/integral estimate for these varying rational phases that
does not simply assume equidistribution.

In particular we have not proved `T_N(1)=o(N)`, nor a positive power
saving, nor even a uniform positive-proportion saving from the
factorial-ratio structure. This is a limitation of our current
arguments, *not a theorem of impossibility*.

## References

- Jeremy Gibbons, *Unbounded Spigot Algorithms for the Digits of Pi*:
  https://www.cs.ox.ac.uk/jeremy.gibbons/publications/spigot.pdf
- Irrationality-exponent background for lacunary Mahler numbers, e.g.
  J. Bell, Y. Bugeaud, M. Coons, *Diophantine approximation of Mahler
  numbers*: https://arxiv.org/abs/1307.4123
- Discussion of `mu(sum_{k>=0} b^(-2^k))=2`:
  https://mathoverflow.net/questions/145484/on-the-irrationality-measure-of-sum-n-1-infty-a-bn
- See also `research/SPIGOT_CIRCULARITY_AUDIT.md` and
  `research/PI_NORMALITY_PROGRAM.md`.