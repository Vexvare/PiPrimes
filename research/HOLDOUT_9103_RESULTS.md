# Results of the preregistered 9103 holdout

**Outcome: did not reject the null at the preregistered one-sided 1% threshold.**

## Audit trail

- **Preregistration commit, before viewing held-out digits:** [`7b0ad584addc081ce7297d5bbe4837cb99ec163a`](https://github.com/Vexvare/PiPrimes/commit/7b0ad584addc081ce7297d5bbe4837cb99ec163a).
- Frozen [protocol](HOLDOUT_9103_PREREGISTRATION.md): modulus 9103, held-out prefix lengths 1,000,001 through 5,000,000, one-sided excess, 9,999 matched digit continuations, seed 910320261123, threshold p <= 0.01.
- Pi digit source: 5,000,000 digits including initial 3, computed by GMP Chudnovsky binary splitting. The exact rational upper and lower bounds implied identical floors at the full five-million-digit scale; not a guessed floating-point conversion.
- Training-prefix SHA-256 (first 1,000,000 digits, no newline): `387877db67fdddbde761c053c4376e0b411b10fd2b126fd8b1249963cb628877`, identical to the original analysis.
- Full 5,000,000-digit SHA-256 (no newline): `8ceb06d34c73c67988ef22651a6436f859026e610f4d582995235b79226b0a06`.
- Frozen program and parameters were committed before validation. Raw pi digit files are omitted from Git because they are reproducibly generated from the stated source and checksums.

## Primary analysis

The first 1,000,000 source digits and therefore the modular state `(F_1000000 mod 9103, phase)` were fixed for observed data and all controls. The initial residue was **7181**, and the multiplicative period `ord_9103(10)` was **9102**.

| Statistic | Result |
|:---|---:|
| Holdout steps | 4,000,000 |
| Observed hit count, p=9103 | **486** |
| Marginal null reference, approximately M/9103 | **439.416** |
| Matched controls | 9,999 |
| Control mean | 439.433 |
| Control standard deviation | 22.983 |
| Control 2.5% / median / 97.5% quantiles | 395 / 439 / 485 |
| Controls with at least 486 hits | **231** |
| Primary one-sided Monte Carlo p-value | **(231+1)/10000 = 0.0232** |
| Preregistered significance threshold | **0.0100** |
| Primary decision | **Do not reject H0** |

The observed excess is 46.57 hits, around 2.03 empirical null SD. The count is just beyond the reported 97.5% empirical control quantile, but a **one-sided 1% threshold** was the locked decision rule and was not met. The empirical p-value has Monte Carlo uncertainty and should not be treated as mathematically exact under arbitrary distributions of pi digits; it is a calibrated simulation under the specific iid-uniform continuation null.

The original p=9103 training observation (164 versus about 109.84 expected) was **selected after screening 1,227 moduli**, so it must not be combined with this validation block as if both were prospective independent hypotheses. The validation has weaker but directionally similar excess. This does **not** establish an algebraic restriction, an infinite family of prime-producing prefixes, or a deviation from normality of pi.

## Independent recheck and reproducibility

An independent pure-Python modular pass over all 5,000,000 digits (separate from the C++ validation scanner) returned exactly `F_1000000 mod 9103 = 7181` and **486** held-out zero residues.

```sh
g++ -O3 -std=c++17 experiments/generate_pi_chudnovsky.cpp -lgmpxx -lgmp -o generate_pi
./generate_pi 5000000 pi_5000000_digits.txt
python experiments/run_holdout_9103.py --digits-file pi_5000000_digits.txt --output holdout-results/9103_validation.json
```

Detailed machine-readable output is checked in at [`records/holdout_9103_validation.json`](../records/holdout_9103_validation.json). The Monte Carlo engine uses unbiased rejection sampling from 64-bit outputs, not `rng() % 10` directly, to create iid uniform decimal digits. Each control starts at the same observed training state and uses a distinct random continuation. The sample is **not** a set of iid Bernoulli divisibility hits; correlations along the full automaton trajectory are preserved within every control.

**Next scientific step:** report this preregistered non-rejection openly. Do not reframe it as a successful 5% result, choose a different target/window after the fact, or run additional unregistered continuations to seek significance. Any new test would require a new independently preregistered sample.