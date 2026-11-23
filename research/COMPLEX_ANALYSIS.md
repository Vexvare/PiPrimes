# PiPrimes in the complex plane

This note distinguishes **proved statements about decimal prefixes** from **unproved assertions about prime occurrence**. These are mathematical proofs on paper, not machine-checked Lean certificates. Numerical experiments are evidence for or against particular statistical models, not proof of infinitude.

## Definitions and the actual rules

Let \(d_1d_2\ldots=314159\ldots\) be the ordinary decimal expansion of \(\pi\), with \(d_1=3\). The *Fundamental* reversed-prefix integer is

\[
 R_n=\sum_{k=1}^{n}d_k10^{k-1};\qquad R_1=3,\quad R_{n+1}=R_n+d_{n+1}10^n.
\]

The other game rules (Branch and Pruned) select subsets of positions in the reversed word; the statements below concern **Fundamental** integers unless specified otherwise. A zero newly prepended to the reversed word can leave the integer unchanged. Claims about infinitely many *distinct* primes must account for this.

## Theorem 1: generating functions and a natural boundary

Define

\[
D(z)=\sum_{k\geq1}d_kz^{k-1},\qquad H(z)=\sum_{n\geq1}R_nz^n.
\]

Then, for \(|z|<1/10\),

\[
\boxed{H(z)=\frac{z}{1-z}D(10z).}
\]

**Proof.** Absolute convergence permits changing the order of sums:

\[
\sum_{n\geq1}\sum_{k=1}^{n}d_k10^{k-1}z^n
 =\sum_{k\geq1}d_k10^{k-1}\frac{z^k}{1-z}
 =\frac{z}{1-z}D(10z).
\]

Both \(D\) and \(H\) have natural boundaries on \(|z|=1\) and \(|z|=1/10\), respectively.

**Proof.** The digits belong to a finite set and are not eventually zero, so \(D\) has radius of convergence 1. If its series were rational, its coefficients would satisfy an eventual constant-coefficient linear recurrence. A recurrence with a nonzero coefficient on its next term and only finitely many possible consecutive coefficient states forces the digit sequence to be eventually periodic. (Equivalently, a rational base-10 digit expansion is eventually periodic.) This contradicts the irrationality of \(\pi\). Thus \(D\) is not rational. The **Pólya–Carlson theorem** says that an integer-coefficient power series of radius 1 is rational or has the entire unit circle as a natural boundary. Therefore \(|z|=1\) is a natural boundary of \(D\). The displayed identity and the fact that \(z/(1-z)\) is analytic and nonzero near every point with \(|z|=1/10\) transfer this natural boundary to \(H\). \(\square\)

This does **not** imply that infinitely many \(R_n\) are prime. It is a general consequence of an irrational bounded-digit expansion, not a special distribution-of-primes theorem for \(\pi\).

## Theorem 2: exact complex-phase divisibility filter

For an integer modulus \(p\ge2\), let \(\omega_p=e^{2\pi i/p}\). For every integer \(R_n\),

\[
\boxed{\frac1p\sum_{j=0}^{p-1}\omega_p^{jR_n} = \mathbf1_{p\mid R_n}.}
\]

**Proof.** If \(p\mid R_n\), each summand is 1. Otherwise \(\omega_p^{R_n}\ne1\), and the numerator of the finite geometric sum is \(1-(\omega_p^{R_n})^p=0\). \(\square\)

An exact program should use the modular recurrence

\[
 r_{n+1}^{(p)}\equiv r_n^{(p)} + d_{n+1}10^n\pmod p,
\]

rather than evaluating near-canceling complex floats. The complex phase \(\omega_p^{r_n^{(p)}}\) is a *picture* of the exact integer residue. A discrete Fourier transform of the residue histogram measures non-uniformity, but a nonzero Fourier coefficient is **not** evidence of unusual π behavior without a matched null distribution. As \(R_n\) all end in 3, moduli 2 and 5 never divide \(R_n\); the CLI defaults to primes starting at 3.

## Theorem 3: normalize Gaussian-integer pairs

For two Fundamental values \(A=R_n\) and \(B=R_m\), define

\[
 Z=A+iB,\qquad W=\frac{Z}{1+i}
  =\frac{A+B}{2}+i\frac{B-A}{2}.
\]

Every Fundamental value ends in the units digit 3, hence \(A,B\) are odd. Therefore \(Z\) is divisible by the nonunit Gaussian integer \(1+i\), and **\(Z\) is not Gaussian prime** (since \(A,B\) are positive and \(Z/(1+i)\) is not a unit).

The normalized number \(W\) has Gaussian norm

\[
\boxed{N(W)=\frac{A^2+B^2}{2}\equiv 9\pmod{20}.}
\]

**Proof.** Since \(A\equiv B\equiv3\pmod{10}\), their squares are each 9 modulo 40: \((10t+3)^2=20t(5t+3)+9\), and \(t(5t+3)\) is even for every integer \(t\). Thus \(A^2+B^2\equiv18\pmod{40}\), giving \(N(W)\equiv9\pmod{20}\). \(\square\)

**Gaussian primality criterion.** If \(A\ne B\), both real and imaginary parts of \(W\) are nonzero; then \(W\) is Gaussian prime **if and only if** its ordinary integer norm \(N(W)\) is prime. If \(A=B\), then \(W=A\) lies on the real axis; it is Gaussian prime exactly when \(A\) is an ordinary prime congruent to 3 modulo 4. This axis exception matters because \(R_n\) can repeat when the newly included source digit is zero.

Examples:

* \(A=3,B=13\): \(W=8+5i\), norm \(89\), a Gaussian prime.
* \(A=13,B=413\): \(W=213+200i\), norm \(85,369\), a Gaussian prime even though 413 is composite.
* \(A=B=3\): \(W=3\), a Gaussian prime despite its norm being the composite \(9\).
* \(A=B=13\): \(W=13\), not Gaussian prime, since \(13\equiv1\pmod4\).

For large norms, the existing repository's BPSW-based computation tests *probable* primality; that is not a certificate for a Gaussian prime. The congruence and the algebraic equivalence are rigorously proved independently of this computational limitation.

## Prime-indicator generating function: a conditional research target

Put \(a_n=\mathbf1_{R_n\text{ is prime}}\) and \(P(z)=\sum_{n\ge1}a_nz^n\), \(|z|<1\). This power series has nonnegative coefficients and

\[
 \#\{n:R_n\text{ is prime}\}=\infty \quad\Longleftrightarrow\quad
 \lim_{r\uparrow1}P(r)=+\infty.
\]

That equivalence is elementary by monotone convergence. Distinct-value infinitude follows if infinitely many **different** \(R_n\) are prime; each fixed integer can occur only finitely many times in the π prefix sequence because π has infinitely many nonzero digits.

**Heuristic, NOT theorem.** Since every candidate ends in 3, a rough prime probability is \(2.5/(n\log 10)\) for large \(n\). If one could establish an actual average asymptotic \(\sum_{n\le N}a_n\sim C\log N\) with \(C>0\), then Abelian summation would yield \(P(r)\sim C\log[1/(1-r)]\) as \(r\uparrow1\). None of that prime-count asymptotic has been proved for π. The natural-boundary theorem above does not give it, and even an RH/GRH result for ordinary primes does not automatically control this extremely sparse digit-defined sequence.

## Reproducible experiment

```sh
python complex_analysis.py --digits 1000 --start 100 --max-prime 97 --trials 100 --seed 0 --pairs 20
python complex_analysis.py --digits 7599 --start 100 --max-prime 97 --trials 400 --seed 0 --pairs 20 --csv modular_7599.csv
python -m unittest -v
python visualize.py --digits 250 --max-length 4
```

Counts are exact modular calculations over the selected prefix lengths. Matched controls keep the first **two** π digits (31) and draw the remaining digits independently and uniformly from 0–9, *once per whole stream*. The resulting between-stream distribution is the right unit for empirical comparisons; successive prefix observations **are not independent**. Report the parameters and do not select endpoints after observing an interesting event without marking the analysis exploratory. The offline atlas includes a complex-phase wheel and divisibility heatmap driven by the same π slider as the prime tree.

## External mathematical references

* [Pólya–Carlson theorem overview (Wolfram MathWorld)](https://mathworld.wolfram.com/PowerSeries.html)
* [Gaussian-prime classification (FLINT documentation)](https://fredrikj.net/fdoc/html/algorithms/number-theory/gaussian-integers.html)
* [Lean/Mathlib joint statement on the November 2026 RH proof](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) — important historical context, **not** a proof that PiPrimes has infinitely many primes.