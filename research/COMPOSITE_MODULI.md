# Universal base-10 obstructions and composite modular structure

For reversed prefixes of any source word with initial digit `3`, let
\(F_n = \sum_{j=1}^n d_j10^{j-1}\).

## Theorem: exact 10-adic stabilization

For each positive integer \(L\) and any \(n\ge L\),

\[
F_n\equiv F_L \pmod{10^L}.
\]

**Proof.** \(F_n-F_L=\sum_{j=L+1}^n d_j10^{j-1}\), and each summand is a
multiple of \(10^L\). QED.

In particular, every \(F_n\equiv3\pmod{10}\), hence
\(\gcd(F_n,10)=1\). Thus **every modulus sharing a prime factor 2 or 5
with 10 is universally excluded as an entire divisor** of \(F_n\): if
\(m\mid F_n\) and \(2\mid m\) or \(5\mid m\), we would have \(2\mid F_n\)
or \(5\mid F_n\), contradiction. In particular, \(m=20,50,100,125\)
have zero hits by theorem, not merely by an experiment.

For general \(m\), write \(m=m_{10}m_{\perp}\) with \(m_{10}=2^a5^b\) and
\(\gcd(m_{\perp},10)=1\). For \(10^L\) divisible by \(m_{10}\), the
\(m_{10}\)-component of \(F_n\) is frozen for \(n\ge L\), while the
\(m_{\perp}\)-component evolves through the additive digit automaton.

## Theorem: strong connectivity for general coprime moduli

For **any** \(m\ge2\) with \(\gcd(m,10)=1\), let \(k=\operatorname{ord}_m(10)\).
The automaton on \((F_n\bmod m,n\bmod k)\) is strongly connected.
The proof from the prime case applies verbatim: for any initial phase and
residue and requested target phase and residue, choose \(L\equiv b-a \pmod k\)
with \(10^L\ge m\), then select the base-10 integer \(x\in[0,10^L)\)
representing \(10^{-a}(s-r)\bmod m\). The increment is \(10^a x\bmod m\)
and the phase advances by \(L\).

Consequently, **no modulus coprime to 10 is universally excluded** across
unrestricted source digit sequences. This says nothing about a particular
source such as pi.

## Joint prime divisibility

For distinct primes \(p,q\notin\{2,5\}\), the Chinese remainder theorem
gives

\[
p\mid F_n\text{ and }q\mid F_n \quad\Longleftrightarrow\quad pq\mid F_n.
\]

The independent-random-digit null predicts a late-time marginal of
approximately \(1/(pq)\), not necessarily independence over different n.
Under full base-10 normality, the same block-concentration argument as in
`MODULAR_AUTOMATON.md` gives asymptotic frequency \(1/m\) for **every**
fixed \(m\) coprime to 10, including composites and prime powers.

A fixed finite length of block-normality, even one equal to
\(\operatorname{ord}_m(10)\), is **not sufficient by itself** to justify
independence of digits from automaton state. The conditional theorem requires
full normality (or equivalently uniform aligned blocks of arbitrarily long
fixed lengths). The normality of pi is unproved.

## Exact exploratory counts (existing 1M-digit sample)

For n=100..1,000,000 inclusive, and M=999,901, scanning the already verified
training source gives the following exact counts. \(M/m\) is a heuristic
baseline only for coprime \(m\).

| Modulus | Observed hits | M/m baseline if coprime |
|---:|---:|---:|
| 9 | 111219 | 111100.11 |
| 21 | 47337 | 47614.33 |
| 27 | 36835 | 37033.37 |
| 49 | 20076 | 20406.14 |
| 77 | 12936 | 12985.73 |
| 91 | 10961 | 10987.92 |
| 121 | 8059 | 8263.64 |
| 143 | 7025 | 6992.31 |
| 169 | 6013 | 5916.57 |
| 221 | 4640 | 4524.44 |
| 20 | 0 | Not applicable (universal obstruction) |
| 50 | 0 | Not applicable (universal obstruction) |
| 125 | 0 | Not applicable (universal obstruction) |

Reproduce with `python experiments/composite_moduli.py --digits-file
modular-results/pi_1000000_digits.txt --start 100`.