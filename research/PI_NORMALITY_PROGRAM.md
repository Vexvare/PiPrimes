# PiPrimes: a rigorous normality research program

**Status:** The normality of π in base 10 remains an open problem. The results below are equivalences, elementary identities, and a separation theorem, **not a proof of normality**. Numerical checks cannot prove limiting statements.

## Setup and exact normalized recurrence

Write the decimal digits of π, including the initial 3, as `d_1=3,d_2=1,d_3=4,...` and set

\[
F_n=\sum_{j=1}^{n} d_j10^{j-1},\qquad x_n=F_n/10^n.
\]

We retain leading zeros when treating reversed prefixes as padded decimal words. Then

\[
x_n=0.d_n d_{n-1}\dots d_1, \qquad
x_{n+1}=(x_n+d_{n+1})/10.
\]

This maps the existing PiPrimes recurrence into a contractive real interval system. It does **not** assert any statistical property of the digit sequence.

## Theorem 1: reversed-prefix uniform-distribution criterion

For any infinite base-10 digit stream with no ambiguity from eventually all-9 tails, its underlying decimal expansion is base-10 normal **if and only if** `x_n` is uniformly distributed in `[0,1)`.

**Proof.** Fix a word `w=w_1...w_k` and let `rev(w)` be its reverse. For all `n>=k`, the block `d_{n-k+1}...d_n=w` holds exactly when the first `k` digits of the padded decimal expansion of `x_n` equal `rev(w)`. Equivalently, `x_n` belongs to the half-open decimal cylinder interval indexed by `rev(w)`, of length `10^{-k}`. Every length-k source block has frequency `10^{-k}` precisely when the `x_n` visits every cylinder interval of length `10^{-k}` with that frequency. Since the boundaries of arbitrary intervals can be approximated by finite unions of decimal cylinders with arbitrarily small leftover length, this is equivalent to uniform distribution. Initial indices `n<k` affect finitely many observations and not the limit. □

This is a specialized restatement of standard equivalences for normal numbers, not a claim of original discovery.

## Theorem 2: reduced Weyl proof obligation

For every nonzero integer `h`, define

\[
S_N(h)=\sum_{n=1}^N e^{2\pi i h x_n}.
\]

The recurrence implies

\[
e^{2\pi i(10h)x_{n+1}}=e^{2\pi i h x_n}
\]

because `10x_{n+1}=x_n+d_{n+1}` and `d_{n+1}` is an integer. At `n=1`, `10x_1=d_1`, hence `e^{2πi 10h x_1}=1`. Therefore

\[
S_N(10h)=1+S_{N-1}(h)=S_N(h)+1-e^{2\pi i h x_N}.
\]

Thus `|S_N(10h)-S_N(h)|<=2`, uniformly in `N`. By repeated division of `h` by 10, Weyl's criterion gives the exact equivalence

\[
\pi\text{ is normal in base 10}
\iff
\forall h\in\mathbb Z_{>0}\text{ with }10\nmid h,
\quad S_N(h)=o(N).
\]

It is sufficient to consider positive `h` because negative frequencies give complex conjugates. **Open bottleneck:** prove cancellation for all such `h` for this specific explicitly defined sequence, using independently proved bounds derived from π rather than an unproved digit-randomness assumption.

## Theorem 3: modular equidistribution alone cannot prove normality

**Statement.** There exist base-10 digit streams whose reversed prefixes `F_n` are equidistributed modulo **every** integer `m>=2` coprime to 10 but whose digit streams are **not even simply normal**.

**Proof.** Fix first digit 3. Draw all subsequent digits independently from a distribution with strictly positive digit probabilities but `P(d=0)=1/5` (take each other digit with probability `4/45`). Almost surely, the limiting frequency of zero is `1/5` by the strong law of large numbers, so the digit stream is not simply normal.

For any fixed modulus `m` coprime to 10, set `k=ord_m(10)` and consider the Markov state `(F_n mod m, n mod k)` with transition `(r,s)->(r+d*10^s mod m,s+1 mod k)`. All ten digit transitions have positive probability. The directed graph is strongly connected: given source and target states, choose a path length `L` with the required phase, `10^L>=m`, and choose the base-10 digit block whose numeric value `v` solves `10^n*v ≡ r_target-r_source (mod m)`; the coefficient `10^n` is invertible modulo `m`. There is such a `v` in `[0,10^L)`.

Every fixed digit `d` induces a permutation of this finite state space, hence the transition matrix is a convex combination of permutation matrices and is doubly stochastic. Its unique invariant distribution is therefore uniform, by irreducibility. The finite-chain ergodic theorem implies almost-sure state occupancy `1/(mk)` and residue occupancy `1/m`, irrespective of periodicity. There are only countably many admissible `m`, so the intersection of these almost-sure events still has probability one. Pick any realization in that intersection. This realization is nonnormal yet satisfies the residue equidistribution property for *all* such moduli. □

**Interpretation.** Increasing prime or composite modulus scans cannot, by themselves, establish base-10 normality. The phase-resolved, normalized prefix sequence retains information that residues discard.

## Why full normality would imply residue density 1/m

For reference, the earlier conditional result can be proved using normality of **arbitrarily long** blocks, not merely uniform single-digit counts or one fixed block length. Fix `m` coprime to 10 and `k=ord_m(10)`. For a length-L digit block, starting from any state, a uniform random block induces the irreducible finite Markov walk above. Time-averaged residue occupancies over a long block converge in probability to `1/m` uniformly over finitely many possible starting states (for instance via the finite-state ergodic theorem and a union bound). Full base-10 normality implies each length-L word appears with the expected frequency at positions aligned to length L. For each fixed L, the exceptional words whose occupancy differs by more than ε *for any starting state* occupy a fraction tending to zero as L grows. Partition the actual digit stream into disjoint length-L blocks, bound each typical block independently of its starting state, then take `N→∞`, `L→∞`, and ε→0. This yields residue density `1/m`. The proof requires normality for every finite L and is not a proof that π is normal.

## Empirical pilot (first 1,000,000 digits of π)

The `normality_weyl.py` utility computes the recurrence numerically (double precision for complex phases) and decimal block counts exactly. Using the independently checked 5M-digit π file from the earlier holdout project but **only the first million digits**, we found:

| Harmonic `h` | `|S_N(h)|/N` |
|---:|---:|
| 1 | 0.0008297672 |
| 2 | 0.0010411565 |
| 3 | 0.0001640617 |
| 7 | 0.0003369196 |
| 10 | 0.0008280036 |
| 20 | 0.0010412960 |

The `h=10` and `h=20` magnitudes match their reduced frequencies within an `O(1/N)` discrepancy, as proved above. At block lengths 1, 2, and 3 the largest absolute frequency deviations from `10^{-k}` were approximately 0.000452, 0.000279, and 0.000102 respectively. These small finite deviations are consistent with randomness but do **not** prove any limiting bound.

Reproduce with:

```sh
python normality_weyl.py pi_5000000_digits.txt --limit 1000000 --harmonics 1,2,3,7,10,20 --max-block 3 --output pi_weyl_1m.json
python -m unittest -v test_normality_weyl
```

The large π digit file is not committed to Git. It was already supplied in the earlier holdout experiment archive and the repository includes the Chudnovsky generator on the modular automaton research branch.

## Research proof plan, in priority order

1. **Identify a usable π-specific analytic input.** Study exact integral/series expressions for `π` that might support uniform bounds for `∑exp(2πih x_n)`. Ordinary numerical digit independence or finite sample estimates are insufficient.
2. **Prove a quantitative exponential-sum estimate for a nontrivial family of primitive frequencies.** Even `S_N(1)=o(N)` is currently out of reach for π. An upper bound `|S_N(h)| ≤ C_h N^{1-δ_h}` would be a substantial advance if rigorously established without assuming normality.
3. **Seek a theorem controlling all frequencies `10∤h`.** Theorem 2 tells us the exact remaining infinite family. A density-one subset of `h` is not enough for Weyl's criterion.
4. **Formally audit every claimed bridge.** For any new lemma, test whether it is true for arbitrary digit streams, whether it uses π-specific information, and whether the argument accidentally assumes normality or independence.

Background: Weyl's criterion; normality/decimal-cylinder characterization; finite Markov chain ergodic theorem. These tools give equivalent formulations and conditional consequences, not a known proof of π's normality.