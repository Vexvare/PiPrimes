# The reversed-prefix modular automaton: proofs and a million-digit test

**Scope.** For a decimal word `d_1 d_2 ...` beginning with `31`, define
\(F_n=\sum_{j=1}^n d_j10^{j-1}\). This note gives general theorems for **any**
digit stream and a conditional theorem about a **base-10 normal** stream.
None of these results proves that pi is normal or that infinitely many of its
reversed prefixes are prime. Proofs below are mathematical arguments, not Lean
formalizations. They should not be represented as novel publication-level results
without a search of the existing literature on finite automata and normality.

## Theorem 1: exact finite-state automaton and strong connectivity

Let \(p\) be a prime other than 2 or 5 and \(k=\operatorname{ord}_p(10)\).
After reading \(n\) digits, the state is \((r,n\bmod k)\), where
\(r\equiv F_n\pmod p\). A source digit \(d\in\{0,\ldots,9\}\) induces

\[
 T_d(r,a) = ((r+d10^a)\bmod p,\ (a+1)\bmod k).
\]

**Proof of strong connectivity.** Let \((r,a)\) and \((s,b)\) be any states.
Choose \(L\ge1\) with \(L\equiv b-a\pmod k\) and \(10^L\ge p\).
The next \(L\) source digits, read in the recurrence's little-endian order,
encode each integer \(x\in[0,10^L-1]\) exactly once. Their aggregate
increment is \(10^a x\pmod p\). In particular, \(x\) can be chosen to
satisfy \(x\equiv 10^{-a}(s-r)\pmod p\), as the interval contains a
representative of every residue class modulo \(p\). The resulting state is
\((s,b)\). This proves strong connectivity. **Ten outgoing edges alone would
not prove connectivity.** An executable constructive witness is provided by
`modular_automaton.universal_path`.

**Corollary.** With a fixed initial digit 3, no prime \(p\ne2,5\) is
unconditionally excluded as a possible future divisor across *all* choices of
subsequent digits. The residues modulo 2 and 5 never vanish because every
\(F_n\) ends in 3. This concerns *arbitrary* digit streams, not proof that a
particular stream (such as pi) reaches every zero state.

## Theorem 2: simple normality does not suffice

Take the digit sequence

`3 0123475968 0123475968 0123475968 ...`

All decimal digits occur with limiting frequency 1/10, so the infinite word
is simply normal (apart from its finite initial digit). Yet for modulus 11 the
full ten-digit block returns the state \((3,1)\) to itself, and none of the
intermediate states has zero residue. Consequently \(11\nmid F_n\) at every
\(n\ge1\). This is verified by `test_simple_normal_counterexample`.

Thus, the implication **"exclusion of p forces the digits not to be simply
normal" is false.** The stream is not *fully normal* (many length-two words
are missing).

## Theorem 3 (conditional): normal digits give frequency 1/p

**Claim.** If the entire source word is normal in base 10, then for each fixed
prime \(p\ne2,5\),

\[
 \lim_{N\to\infty}\frac1N\#\{1\le n\le N:p\mid F_n\}=\frac1p.
\]

**Proof.** Fix a starting automaton state \((r,a)\), and feed it \(L\) iid
uniform decimal digits. The integer encoded by the next \(j\) digits is
uniform on \([0,10^j-1]\). Since \(10^a\) is invertible modulo \(p\), the
probability \(q_j\) that the running residue after \(j\) digits is zero
satisfies \(|q_j-1/p|\le10^{-j}\), independently of the starting state.
For \(s<t\), conditional on a hit at \(s\), the probability of another hit
at \(t\) is exactly

\[
 u_{t-s}=\frac{\lceil 10^{t-s}/p\rceil}{10^{t-s}},
 \qquad |u_{t-s}-1/p|<10^{-(t-s)}.
\]

If \(K_L\) is the number of hit times in that length-\(L\) random block,
then \(|\mathbb E K_L-L/p|\le1/9\), and the covariance bound above gives
\(\operatorname{Var}(K_L)\le L/4+2L/9+2/81\). The constants are independent
of \((r,a)\). By Chebyshev's inequality, for any \(\varepsilon>0\), the
fraction of all decimal words of length \(L\) for which the number of hits
is farther than \(\varepsilon L\) from \(L/p\) is \(O(1/(L\varepsilon^2))\),
uniformly over *all* \(pk\) possible starting states (union bound).

A base-10 normal digit stream has each length-\(L\) word with asymptotic
frequency \(10^{-L}\) even when the stream is partitioned into aligned,
nonoverlapping length-\(L\) blocks. This is the standard equivalent
aligned-block characterization of normality (or simple normality in base
\(10^L\)). Thus, all but an arbitrarily small asymptotic fraction of blocks
have approximately \(L/p\) hits **regardless of the automaton state entering
the block**. Summing across blocks, then choosing \(L\) arbitrarily large,
proves the claimed density. QED.

The actual status of base-10 normality of pi is unknown. The conditional
claim is **not** an unconditional theorem about pi.

## Theorem 4: exact finite-prefix null probabilities, and dependence

Consider controls fixed at their first two digits `31`, followed by
independent uniform decimal digits. For \(n\ge2\), write

\[ F_n=13+100U_{n-2},\qquad U_t\sim\mathrm{Uniform}\{0,\ldots,10^t-1\}. \]

Let \(c_p\equiv -13\cdot100^{-1}\pmod p\), represented in \([0,p-1]\).
Then the **exact** null hit probability is

\[
 q_n=\Pr(p\mid F_n)=\frac{\lfloor10^{n-2}/p\rfloor+
  \mathbf{1}\{c_p<(10^{n-2}\bmod p)\}}{10^{n-2}}.
\]

In particular, \(|q_n-1/p|<10^{-(n-2)}\), while \(F_1=3\) is fixed.
For \(m>n\ge2\), the joint probability is

\[
 \Pr(p\mid F_n,\ p\mid F_m)=q_n\,u_{m-n},
 \quad u_h=\lceil10^h/p\rceil/10^h.
\]

The indicators are **not independent Bernoulli variables**. Increments
\(d_{n+1}10^n\bmod p\) are not zero-mean real martingale differences, so
applying elementary Azuma-Hoeffding directly to the modular count would be
incorrect. The displayed joint law gives the variance exactly through its
pairwise-covariance sum. For a fixed prime and a long late window of length
\(M\), the asymptotic variance per observation is

\[
 \sigma_p^2=\frac1p\left(1-\frac1p\right)+
 \frac2p\sum_{h=1}^\infty\left(\frac{\lceil10^h/p\rceil}{10^h}-\frac1p\right).
\]

This series converges exponentially and is used for **descriptive** standard
deviations below (not exact finite-sample Gaussian p-values). A universal
but conservative rigorous variance bound for any fixed-initial-`31` window
of \(M\) tested lengths is
\(\operatorname{Var}(H)\le17M/36+38/81\), from the exponentially decreasing
covariances. Chebyshev thus provides a nonasymptotic tail guarantee, although
it is much looser than a calibrated finite-state tail calculation.

## Reproducible empirical result: first 1,000,000 digits of pi

Commands:

```sh
python experiments/run_modular_scan.py --digits 1000000 --start 100 --max-prime 10000 --hits
# Or compile/run the engine independently on a verified source file:
g++ -O3 -std=c++17 experiments/modular_scan.cpp -o modular_scan
./modular_scan modular-results/pi_1000000_digits.txt \
  modular-results/modular_counts.csv 100 10000 \
  modular-results/modular_hit_indices.csv modular-results/phase_diagnostics.csv
```

`run_modular_scan.py` uses `mpmath` interval arithmetic: it accepts the
truncated digit expansion only if the lower and upper interval endpoints
produce the same million-digit integer. It then runs a C++17 bounded-
integer exact residue scan; no million-digit reversed integer is built.
The data include the first `3` in their million digits. The count window is
**n=100 through n=1,000,000 inclusive**, with \(M=999,901\).

- All **1,227** primes between 3 and 10,000 other than 5 had **at least one**
  zero residue in the tested window.
- There were **1,781,466** prime-prefix incidences, summing over all the
  moduli. The sum of the naive null expectations \(M/p\) was 1,782,883.42.
- The smallest observed hit count across tested primes was **77**.
- Representative observations and approximate expected counts:

| p | ord_p(10) | observed hits | M/p | descriptive z (correlation-adjusted) |
|--:|--:|--:|--:|--:|
| 3 | 1 | 333,471 | 333,300.33 | +0.33 |
| 7 | 6 | 142,192 | 142,843.00 | -1.73 |
| 11 | 2 | 91,207 | 90,900.09 | +1.05 |
| 13 | 6 | 77,313 | 76,915.46 | +1.45 |
| 37 | 3 | 26,966 | 27,024.35 | -0.33 |
| 41 | 5 | 24,073 | 24,387.83 | -1.89 |
| 101 | 4 | 9,977 | 9,900.01 | +0.72 |
| 9,103 | 9,102 | 164 | 109.84 | +4.68 |

**Multiple comparisons caution:** 9,103 was the most extreme *exploratory*
standardized deviation among 1,227 moduli. This was discovered after looking
at the same million digits, and the normal z is only an approximation;
there is no defensible claim of a statistically established pi anomaly yet.
The timestamped [preregistered holdout protocol](HOLDOUT_9103_PREREGISTRATION.md)
uses n=1,000,001 through 5,000,000 for p=9,103, 9,999 matched continuations,
and an independently fixed one-sided 1% threshold. The earlier proposed
1M-to-2M window is superseded before any continuation was inspected.

Source-digit SHA-256 (without newline):
`387877db67fdddbde761c053c4376e0b411b10fd2b126fd8b1249963cb628877`.
The checked-in summary CSVs contain all per-prime counts and tracked small-
order phase diagnostics. Raw individual `(prime,n)` hit indices are intentionally
not committed as a very large source file; run with `--hits` to reproduce them.

## Interpretation and limits

1. A million sampled positions without a zero-hit modulus is **not** a proof
   that any specific prime divides infinitely many reversed pi prefixes.
2. A prime `p` with zero empirical hits could be a finite-sample fluctuation,
   not a universal modular obstruction. A proposed obstruction must involve
   an actual proved property of pi's digits.
3. The strong-connectivity theorem is elementary and holds for arbitrary
   digit words. No special structure of pi has been identified by it.
4. A full-base-normality assumption produces the exact conditional density
   1/p; *simple normality alone is insufficient*.
5. The first million digits were already examined in constructing this
   report; a claim based on the 9,103 observation requires a distinct holdout.

## Literature background

- [Normal numbers and computer science (Carton)](https://www.irif.fr/~carton/Enseignement/MPRI/Dynam-symbol/Documents/chapter.pdf), for equivalent block/aligned-block normality definitions.
- [Pólya–Carlson and normality background](https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/descriptive-complexity-in-cantor-series/19EAD3B2B426D3826A6DA9405DFB7D81), noting Wall's theorem on normality and normality in power bases.