# PiPrimes

Landon Wells began this game on March 3, 2024 and completed the original implementation on March 5. Read π a digit at a time, including the initial 3. At each step reverse the prefix and look for primes. For example, the first three steps give these first discoveries.

| Length | Reversed word | Fundamental | Branch | Pruned |
| ---: | --- | --- | --- | --- |
| 1 | 3 | 3 | | |
| 2 | 13 | 13 | | |
| 3 | 413 | | 41 | 43 |

## Run

Use Python 3.9+ and install the dependencies. The default search covers 12 digits.

```sh
python -m pip install -r requirements.txt
python Fractal_Pi.py
python Fractal_Pi.py --mode fundamental --digits 100
python Fractal_Pi.py --mode fundamental --digits 7599 --at-end
python compare_density.py --digits 100 --trials 100 --seed 0
python -m unittest -v
```

Each result gives the source length, rule, primality status and integer value. Use `--at-end` to classify just one prefix, including values that might also occur earlier. Use `--constant e` or `--constant sqrt2` to change the source. Digits come from interval arithmetic with enough precision that both endpoints truncate to the same integer.

## Interactive prime atlas

Run `python visualize.py` after installing the requirements. It opens a self-contained HTML file in your browser. Move the π slider to 3 digits to see 13 (fundamental), 41 (branch), and 43 (pruned) light up in the two-digit block. Choose a fixed prime length to watch that block fill, or use Auto to follow the longest identified prime among the tracked lengths. Click a prime to highlight the positions that first produced it. Large blocks have a clickable overview of every prime and numbered cells below it.

The fractal tree tab shows keep/skip paths retaining the initial 3 through the first nine observed digits. Click a prime node and choose **Show in prime block** to compare that path with its first appearance under the full rules. The grid includes primes from all three rules across the entire selected prefix.

The default atlas covers primes of one through four digits across 100 source digits. For a larger export use `python visualize.py --digits 250 --max-length 5`. Use `--no-open` to generate the file without launching a browser and `--output PATH` to choose its location.

## Complex-plane research and visualizations

The atlas now has a **Complex plane** tab alongside Prime block and Fractal tree.
With the same digit-depth slider, explore a roots-of-unity wheel for a selectable
modulus and a small-prime divisibility heatmap. These are **exact modular tests**
displayed as phases; a surviving candidate is not necessarily prime.

```sh
python complex_analysis.py --digits 1000 --start 100 --max-prime 97 --trials 100 --seed 0 --pairs 20
python visualize.py --digits 250 --max-length 4
python -m unittest -v
```

The analyzer also compares full random-control digit streams starting with 31
and examines normalized Gaussian pairs `(R_n+i R_m)/(1+i)`. It labels large
norms as probable primes, not proven primes. See
[the complex-analysis research notes](research/COMPLEX_ANALYSIS.md)
for the generating-function natural-boundary theorem, exact Fourier divisibility
filter, Gaussian-prime criterion, proofs, assumptions, and open conjectures.

## Rules and counting

At step n, write the reversed word as Rₙ = dₙ…d₁. Keep zeros in the word while selecting positions. Interpret the selected digits as an integer when testing primality.

| Rule | Positions retained |
| --- | --- |
| Fundamental | The entire word |
| Branch | Any nonempty proper prefix |
| Pruned | The first and last positions of a chosen prefix, deleting at least one interior position. The chosen prefix can be the whole word. |

The last rule includes the original game's combination of branching and pruning. For example, 4173 can yield 47 by branching to 417 and dropping the 1. Every nonempty selection containing the first position fits one of the three rules. Multiple selections can give the same integer. The search reports a value once, at its earliest step, with ties resolved in table order. A rule witness describes how to obtain a prime even when an earlier step has already reported it.

An n-digit step has 2^(n−1) anchored position selections before pruning or deduplication. Exhaustive mode asks for `--force` above 18 digits. Fundamental mode uses the recurrence F₁ = d₁ and Fₙ₊₁ = Fₙ + dₙ₊₁ × 10ⁿ. It tests one candidate per step and supports a direct final-prefix test.

## Research statements

1. **Infinitely many fundamental primes.** The conjecture is that the set of distinct prime values among Fₙ is infinite. The original “there is always a larger one” claim is equivalent, since a bounded set of positive integers is finite.
2. **Infinitely many of each type.** For each rule separately, ask whether infinitely many distinct primes have a witness under that rule. First-discovery labels answer a different counting question. Fundamental infinitude alone would establish only the first case.
3. **Excess density.** Fix the truncation N before looking at results. Count distinct fundamental hits among the first N steps. Compare with independent random digit streams that start with 31 and use uniform independent digits thereafter. This preserves the shared suffix 13 from step two, dependence between successive prefixes, and the counting policy. Report the trial count, seed and fraction of controls matching or exceeding π. Large hits are probable primes. At N = 100, seed 0, π gives 7 hits versus a mean of 5.78 across 100 controls. 35 controls reach or exceed 7. This sample gives little evidence of an excess.
4. **Comparison with other constants.** A raw fundamental count already favors π over e. Every reversed prefix of e ends in 2, so its only fundamental prime is 2. Reversed prefixes of √2 end in 1. Compare each constant with streams sharing its initial digits before interpreting any difference as evidence about the remaining digits.
5. **Every prime is obtainable.** Under the combined rules above, this is equivalent to every decimal digit occurring infinitely often in π. The equivalence below leaves the digit recurrence question open. It also applies to other infinite decimal words.
6. **Fractal interpretation.** The rules give a recursive family of selections. A quantitative fractal claim still needs a specified object, metric and scaling law.

### Proof of the coverage equivalence

If each digit recurs infinitely, take any prime p and read its decimal digits backwards. Greedily find those digits at successively later positions of π. Reverse the prefix ending at the last chosen position. The selected digits now spell p and include the first position of the reversed word. The rule table covers this selection.

Conversely, suppose digit d occurs only k times. Choose the suffix consisting of k+1 copies of d followed by 1, of length m = k+2. Its integer value a is coprime to 10^m. Dirichlet's theorem gives arbitrarily large primes congruent to a modulo 10^m. Take one larger than 10^m so that all m suffix positions exist, including any zeros. Its decimal expansion contains more than k copies of d. No selection from the source can produce it. This proves necessity. [Dirichlet's theorem, MIT lecture notes](https://math.mit.edu/classes/18.785/2021fa/LectureNotes18.pdf)

## First appearances and coverage

For a target prime p, scan the source for the digits of p in reverse order. Each greedy match is at or before the corresponding match in every other embedding, by induction. Hence the final match gives the earliest possible step, in O(N) time and constant auxiliary space per fixed target. Dropping any leading zeros from a reversed selection can only move its final source position earlier. For the label at the earliest endpoint, check whether the whole source prefix spells reversed(p), then whether it **ends** in reversed(p). A greedy witness can contain a gap even when a contiguous witness ties it. For example, both embeddings of 13 in source 331 finish at step 3, so the label is Branch.

Run the coverage experiment with the following command. The optional CSV records the first step and winning rule for each target. Empty fields denote targets unseen by the cutoff. The report counts all targets in the denominator and gives the empirical cumulative distribution at four checkpoints. Each control is one complete stream sharing the initial 31. Targets within one stream are dependent.

```sh
python compare_coverage.py --power 4 --digits 100 --trials 10000 --seed 0 --csv appearances.csv
```

| Source digits | π primes covered (of 1,229) | Exact null mean | Mean covered in controls | Controls at least as high |
| ---: | ---: | ---: | ---: | ---: |
| 25 | 491 | 425.21 | 426.14 | 2,795/10,000 |
| 50 | 1,110 | 1,002.19 | 1,003.06 | 2,341/10,000 |
| 75 | 1,229 | 1,186.97 | 1,187.16 | 914/10,000 |
| 100 | 1,229 | 1,222.79 | 1,222.84 | 5,443/10,000 |

The [per-prime results](records/first_appearances_10000.csv) give the endpoint and rule for each of the 1,229 targets. π reached full coverage at step 70. 443 of the 10,000 controls had reached full coverage by then. This is an exploratory comparison at one target bound.

For a fixed target there is also an exact null model. Consume the fixed initial 31 greedily. If r target digits remain, each subsequent independent uniform digit matches the next required digit with probability 1/10, regardless of the match history. For n ≥ 2 the probability of having found the target by step n equals P(Binomial(n−2, 0.1) ≥ r). Summing these probabilities gives the expected number of covered primes. Whole-stream simulation estimates the spread and completion-time distribution, which also depend on correlations between targets.

## Fundamental density at longer lengths

For large candidates the search sieves by primes through 10,000 using a GCD with their product, then applies gmpy2's strong BPSW test. The density CLI also reports the raw heuristic sum of 2.5/(n ln 10) over lengths 1 through N. The factor 2.5 accounts for a fixed final digit coprime to ten. For the matched **distinct** hit count, start at two known hits (3 and 13) and weight the terms from n = 3 onward by 0.9, the chance that a new digit is nonzero and changes the value. Both estimates use n ln 10 as a size approximation. The raw sum includes small lengths where the approximation is poor. Nested prefixes share digits, so these sums alone give no sampling variance.

```sh
python compare_density.py --digits 1000 --trials 32 --seed 0
python compare_density.py --digits 7599 --trials 4 --seed 0 --jobs 5
```

| Digits | π distinct hits | Raw heuristic | Adjusted heuristic | Control mean | Controls at least as high |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1,000 | 8 | 8.13 | 7.85 | 7.56 | 15/32 |
| 7,599 | 9 | 10.33 | 9.83 | 10.25 | 3/4 |

The complete π scan found hits at lengths 1, 2, 5, 6, 7, 11, 15, 712 and 7,599. The four full-length controls produced 12, 9, 14 and 6 hits in seed order. Four controls give a coarse empirical fraction. Choosing 7,599 after discovering a hit there makes that endpoint exploratory.

## Archived entries

Both original decimal strings are preserved and the tests regenerate them from π.

| Digits | Status and provenance |
| ---: | --- |
| [712](records/712.txt) | Proven prime. On January 7, 2018, Sean A. Irvine reported the proof. OEIS links his Primo certificate. Its synthesized b-file contains terms 1–7. [OEIS A007523](https://oeis.org/A007523) |
| [7,599](records/7599.txt) | The value passes strong BPSW. FactorDB lists the identical integer as PRP with creation date March 3, 2021, before the March 2024 PiPrimes project. The listing establishes prior database presence. Identifying who first found it or recognized the connection to π requires a dated attribution. [FactorDB entry](https://www.factordb.com/index.php?id=1100000002509421010) |

Generic CLI results report the guarantee of the test run. Independent certificates can establish stronger status for particular records. A new ECPP certificate, generated with software such as Primo and independently verified, would provide a proof for the 7,599-digit entry.

## Million-digit modular automaton and proofs

Explore the exact modular walk associated with Fundamental prefixes
\(F_{n+1}=F_n+d_{n+1}10^n\). For primes \(p\ne2,5\), the state
\((F_n\bmod p, n\bmod\operatorname{ord}_p(10))\) forms a strongly connected
directed automaton when digits 0–9 are unrestricted. The proof, a counterexample
showing simple normality is insufficient, an **if-normal-then-density-1/p**
theorem, and precise random-digit null formulas are in
[research/MODULAR_AUTOMATON.md](research/MODULAR_AUTOMATON.md).

For a large scan use Python 3.9+, `mpmath` (already required) and a C++17
compiler such as `g++`. On Windows, install a C++17-capable compiler and pass
its executable as `--compiler`; the script uses the GCC-compatible command
line `-O3 -std=c++17` so GCC/Clang are the easiest options.

```sh
python experiments/run_modular_scan.py --digits 1000000 --start 100 --max-prime 10000 --hits
python -m unittest -v test_modular_automaton
```

The script writes a verified source-digit file, exact [per-prime hit counts](records/modular_counts_1m.csv)
(example results), [small-order phase diagnostics](records/modular_phase_1m.csv),
and, with `--hits`, every observed `(prime,n,phase)` in a CSV.
The optional hit file can reach tens of megabytes and is not committed.
It does **not** run thousands of million-digit random controls: the expected
per-prime baseline is calculated analytically and the scan is deterministic.
These results **do not** prove that π is normal or that infinitely many
Fundamental Primes exist.

## Composite moduli and preregistered 9103 holdout

The [composite-modulus proof](research/COMPOSITE_MODULI.md) establishes the exact 10-adic stabilization `F_n = F_L (mod 10^L)` for `n >= L`. All multiples of 2 or 5 are excluded as *whole divisors*; all moduli coprime to 10 remain algebraically reachable with unrestricted digits. The [composite scanner](experiments/composite_moduli.py) reproduces the first-million-digit prime-power and joint-divisibility counts.

The [locked confirmation protocol](research/HOLDOUT_9103_PREREGISTRATION.md) tests the exploratory p=9103 observation on previously unused digit lengths 1,000,001–5,000,000, with 9,999 matched independent digit continuations, a fixed seed, and a single one-sided 1% threshold. The preregistration is committed ahead of the validation run. The C++17 [exact-rational-bounds Chudnovsky generator](experiments/generate_pi_chudnovsky.cpp) can efficiently produce five million digits without trusting floating-point rounding.

```sh
g++ -O3 -std=c++17 experiments/generate_pi_chudnovsky.cpp -lgmpxx -lgmp -o generate_pi
./generate_pi 5000000 pi_5000000_digits.txt
python experiments/run_holdout_9103.py --digits-file pi_5000000_digits.txt
python experiments/composite_moduli.py --digits-file modular-results/pi_1000000_digits.txt --start 100
python -m unittest -v test_composite_and_holdout
```

**Do not treat the exploratory 9103 z-score as a confirmatory p-value.** The validation runner uses the entire first million digits as a shared fixed prefix and applies the predetermined Monte Carlo decision rule only to the holdout continuation. The 5-million-digit generator requires GMP/GMPXX development headers and libraries; the separate original `mpmath` digit generator remains available.
