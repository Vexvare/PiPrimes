# PiPrimes: preregistered holdout protocol for modulus 9103

**Status at registration: NOT YET RUN.** This file must be committed in a timestamped GitHub commit **before** any digits past the 1,000,000-digit training boundary are examined by the validation program. Once registered, do not revise the decision rule in response to validation results. Any change requires a new independent holdout.

## Exploratory selection and scientific question

The prime 9103 was selected after scanning 1,227 primes in the first 1,000,000 decimal digits of pi (including the initial 3). Its 164 zero residues in lengths 100..1,000,000, against an approximate mean 109.84, is **exploratory** and subject to multiple-testing bias. The confirmatory question is whether a *higher than null* incidence occurs in entirely unseen lengths 1,000,001..5,000,000 inclusive (M = 4,000,000).

## Locked primary design

- Single confirmatory target: prime **p = 9103** (no other moduli will enter the primary decision).
- Source: correctly ordered decimal digits of pi including the initial `3` as digit 1, with the same reversed-prefix recurrence `F_{n+1} = F_n + d_{n+1} 10^n`.
- **Training ends at n = 1,000,000.** Validation begins at **n = 1,000,001** and ends at **n = 5,000,000**, both inclusive. The value F_1,000,000 mod 9103 and phase are fixed and shared by observed and all control continuations.
- Null H0: conditional on those fixed first 1,000,000 source digits, the following 4,000,000 digits are independent discrete uniforms on {0,...,9}. No assumption that the real digits of pi are independent is made.
- Primary statistic H: number of n in the holdout with F_n = 0 mod 9103.
- Direction: **one-sided excess**, H1: more hits than expected under H0.
- Monte Carlo null: **9,999** independently simulated uniform-digit continuations of length 4,000,000, each started from the exact common training automaton state. This is equivalent to preserving the entire observed prefix (and therefore the initial `31`) in each control.
- PRNG: C++ `std::mt19937_64`, fixed 64-bit seed **910320261123**; to produce unbiased decimal digits, rejection sample 64-bit outputs below 18*10^18 and expand uniformly distributed integers in [0, 10^18) into 18 base-10 digits (least significant first). The random generator's state is never reset between trials.
- Primary p estimate: `(1 + number of controls whose hit count >= observed H) / 10000` (conservative randomized rank test, with a tie counted against rejection).
- Significance threshold: **p <= 0.01**, one-sided, with no optional stopping, reselection, or alternate windows. Since there is *one* selected confirmatory test on new data, the original 1,227-way exploration need not be Bonferroni-corrected again; the original discovery does not itself qualify as confirmation.
- Also report the exact observed H, control mean/SD, empirical 2.5%, 50%, and 97.5% quantiles, mean M/p, and the minimum/maximum across controls. These are descriptive and do not change the decision.

**Interpretation:** A rejection indicates an excess relative to the specified iid-digit null on this holdout. It is not evidence of a proved algebraic restriction and does not establish anything about the normality or primality of the digits of pi. A non-rejection is not proof that the observed stream is random or normal. Random controls are a Monte Carlo approximation; reproducibility is ensured by the seed and fixed implementation.

## Verification / audit requirements

- The first 1,000,000 digits of the 5,000,000-digit input must SHA-256 match the preexisting exploratory training prefix: `387877db67fdddbde761c053c4376e0b411b10fd2b126fd8b1249963cb628877` (with no newline).
- Independently generate pi by interval arithmetic to disambiguate the final digit if digits are not supplied; verify full digit length and prefix checksum *before* running the scanner.
- Output JSON with the frozen parameters, validation SHA-256, seed, control count, observed hits, exceedance count and primary p estimate; never alter the preregistration to fit the result.
- The protocol and executable source must be committed **before** validation, and their commit SHA recorded in the results. Any further exploratory tests must be labeled exploratory.