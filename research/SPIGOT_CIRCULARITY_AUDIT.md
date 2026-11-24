# Audit: Does Gibbons's spigot provide an independent route to normality?

**Verdict:** Gibbons's unbounded decimal spigot supplies *digit-independent input arithmetic* but its **consume/emit switching** is coupled to the value of the next output digit. The algorithm is not logically circular: it computes digits correctly from an independently specified series. However, a claim that the emitted-state distribution is uniform is essentially a claim about the ordinary decimal orbit of pi, not a consequence of the spigot's existence. We identify an exact digit-free rational Weyl target below, but obtaining cancellation for it remains open.

**Primary reference:** Jeremy Gibbons, *Unbounded Spigot Algorithms for the Digits of Pi*, American Mathematical Monthly 113 (2006), 318–328; author copy: https://www.cs.ox.ac.uk/jeremy.gibbons/publications/spigot.pdf . We audit the **Section 5** LFT construction; the paper also describes Lambert/Gosper versions with different input matrices and interval bounds. Do not confuse an implementation optimization or the paper's explicitly *conjectural* always-safe Gosper variant with a proved replacement for the branch test.

## A. Exact state machine

Let an integer 2x2 matrix `(q,r;s,t)` represent the homography `z(x)=(qx+r)/(sx+t)`. In the Section 5 construction the digit-free input sequence is

\[
A_k(x)=\frac{kx+4k+2}{2k+1}=2+\frac{k}{2k+1}x,\qquad k\ge1.
\]

The tail of the infinite composition is known to lie in `[3,4]`. Starting with `z(x)=x`, `k=1`, the steps are:

- Candidate `y=floor(z(3))`.
- If `floor(z(3)) = floor(z(4))`, **emit** `y` and update `z <- E_y o z`, with `E_y(x)=10(x-y)`. Keep the same next input index `k`.
- Otherwise **consume** `A_k` by updating `z <- z o A_k`, and increment `k`.

For the Section 5 construction all maps are increasing affine functions (the lower-left matrix element stays zero); floor checks and state updates therefore use **exact integer arithmetic**. The input transformations are explicit functions of `k`. But previous emissions enter subsequent states through `E_y`, and the switch between `emit` and `consume` depends on the current interval's location relative to decimal integer boundaries.

For example, after six input terms and two emitted digits, the certified interval for the next digit is about `[3.74847,4.28127]`: its width is *less than 1*, but it straddles an integer, so a further input term is necessary. Contraction alone cannot determine when a digit is safe.

## B. The exact coupling to the usual decimal shift

Let `e` digits, **including the integer digit 3**, have been emitted. Define their decimal prefix

\[
C_e=d_1+\frac{d_2}{10}+\cdots+\frac{d_e}{10^{e-1}},\quad e\ge1,
\]

and let `B_i=A_1 o ... o A_i`. The current LFT after `i` input terms and `e` emitted digits satisfies the exact functional identity

\[
\boxed{z_{i,e}(x)=10^e\bigl(B_i(x)-C_e\bigr).}
\]

For the true, unknown tail `t_i in [3,4]` of the input composition, `B_i(t_i)=pi`. Hence the certified interval `z_{i,e}([3,4])` contains

\[
10^e(\pi-C_e)=10\{10^{e-1}\pi\}\quad(e\ge1).
\]

This is exactly the ordinary base-10 shift orbit, scaled to `[0,10)`. **Any result asserting that these true residuals are uniformly distributed is already a normality theorem.** A mere representation of the residuals by matrices does not establish their statistical distribution. This is the key sense in which the apparent proof strategy risks circularity; the *algorithm itself is not circular*.

## C. A digit-independent width invariant

Put

\[
w_i=\prod_{j=1}^i\frac{j}{2j+1}
 =\frac{2^i(i!)^2}{(2i+1)!},\qquad w_0=1.
\]

Every consumed input multiplies interval width by `j/(2j+1)`; every emitted digit multiplies it by 10. Thus, after `i` consumes and `e` emissions, the certified interval has **exact width**

\[
\boxed{W_{i,e}=10^e w_i,\qquad w_i<2^{-i}\quad(i\ge1).}
\]

This part is completely independent of the emitted digits. It bounds the rate of *certification*, not the values of the digits. Even small width is insufficient for a safe output if the interval happens to straddle an integer.

### Consequence of a finite irrationality exponent

Suppose the irrationality exponent of π is finite, `mu(pi) < v`. Then for some `c_v>0`, every sufficiently large integer `e` satisfies

\[
\operatorname{dist}(10^e\pi,\mathbb Z) \ge c_v 10^{-(v-1)e}.
\]

After `e` digits have been emitted, consuming sufficiently many terms to make `W_{i,e} < dist(10^e pi, Z)` guarantees that the certified interval cannot cross an integer boundary. As `W_{i,e}<=10^e 2^{-i}`, it suffices that

\[
i> v\,e\log_2(10)+O_v(1).
\]

Consequently the simple Gibbons Section 5 spigot consumes at most `O(e)` input transformations before emitting the first `e` decimal digits (with an asymptotic coefficient no larger than any `v log_2 10` for `v>mu(pi)`). The known unconditional irrationality-measure bounds imply such a linear worst-case upper bound, though with an enormous and ineffective intercept. This is a quantitative link between Diophantine approximation and spigot *runtime*, not a normality proof. The conditional reported 2026 exponent-two claim would improve the coefficient if validated, but is not needed.

## D. An explicit digit-FREE Weyl target

There is one particularly useful way to remove the digit-emission schedule altogether.

The truncated input composition `B_m` itself gives rational bounds

\[
P_m=B_m(3)=2\sum_{j=0}^{m-1}w_j+3w_m,\qquad
Q_m=B_m(4)=P_m+w_m.
\]

Since `pi in [P_m,Q_m]`, and `w_m <= 2^{-m}`, choose `m=4n` to obtain

\[
\boxed{\left|10^n\pi-10^nP_{4n}\right|\le(5/8)^n.}
\]

Let `e(t)=exp(2 pi i t)` and form an explicit arithmetic exponential sum

\[
T_N(h)=\sum_{n=1}^N e\!\left(h\,10^nP_{4n}\right).
\]

Term by term, `|e(a)-e(b)|<=2 pi |a-b|`. Summing the geometric error bound yields

\[
\boxed{\left|T_N(h)-\sum_{n=1}^N e(h\,10^n\pi)\right|
\le\frac{10\pi}{3}|h|.}
\]

The right-hand side is **independent of N**. By Weyl's criterion this gives a rigorous equivalence

\[
\boxed{\pi\text{ is base-10 normal}\ \Longleftrightarrow\
T_N(h)=o(N)\quad\text{for every nonzero integer }h.}
\]

All terms in `T_N(h)` are **explicit rationals defined from factorial ratios**, without unknown decimal digits, digit-floor or emission decisions. This does pass the syntactic independence test. But it is a re-expression of the ordinary `10^n pi` Weyl problem using exponentially accurate rational approximations. No cancellation estimate has been obtained for `T_N(h)`, so this is **not substantive progress toward proving normality** by itself. It would require a new analytic theorem exploiting the specific arithmetic of `P_{4n}`.

## E. Research gate / falsification checks

1. **Proved:** Input `A_k` is prescribed independently of the output digit sequence. The Section 5 branch predicate is not.
2. **Proved:** The emitted residual equals `10 {10^{e-1} pi}`. A state-mixing claim about this residual would be normality in disguise.
3. **Proved:** The exact width invariant controls resolution and a finite irrationality exponent gives weak, linear consumption bounds. Neither gives output frequencies.
4. **Proved:** The digit-free sums `T_N(h)` differ by `O_h(1)` from standard π-orbit sums. This is a bona fide pi-specific formula but an *equivalent difficult problem*.
5. **Still needed:** A nontrivial *unconditional* bound for `T_N(h)` that uses the factorial-ratio terms; proving just `T_N(h)=o(N)` for `h=1` would already be valuable, but does not prove full normality alone.
6. **Counterexample gate:** Every proposed new lemma should be checked against periodic or de Bruijn-cycle digit streams and biased digit streams. Generic properties of the emission/safety mechanism are not enough: they also apply to digit extractors for nonnormal numbers.

## Reproduction

```sh
python experiments/spigot_audit.py --digits 20
python -m unittest -v test_spigot_audit
```

The test suite verifies the first emitted digits, exact rational enclosure of a known decimal interval for π, the width formula at every transition, a narrow-but-unsafe interval, and the digit-free Weyl approximation error. The finite numerical implementation does not claim any asymptotic result.