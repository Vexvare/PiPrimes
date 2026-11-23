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

## Archived probable primes

The original 712- and 7,599-digit entries are stored verbatim in [records/712.txt](records/712.txt) and [records/7599.txt](records/7599.txt). The tests regenerate the reversed π prefix at each length and compare every digit. To rerun the primality check for either value, use the fundamental command above with its length and `--at-end`. The fundamental sequence also appears in [OEIS A007523](https://oeis.org/A007523), which mentions the 712-digit probable prime. Priority for the 7,599-digit entry is unverified.

The output labels passing values below 2⁶⁴ as prime and larger passing values as probable primes. A primality certificate would establish a proof for an archived value. [SymPy primality testing](https://docs.sympy.org/latest/modules/ntheory.html#sympy.ntheory.primetest.isprime)
