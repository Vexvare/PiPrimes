"""Finite-state modular automaton for reversed-prefix decimal numbers.

Pure-Python reference implementation and rigorously specified null calculations.
For a million-digit scan use experiments/modular_scan.cpp, which computes the
same exact recurrence with bounded native integer arithmetic.
"""
from math import gcd


def digits_checked(digits):
    if not isinstance(digits, str) or not digits or not digits.isascii() or not digits.isdecimal():
        raise ValueError("expected a nonempty ASCII decimal digit string")
    return digits


def multiplicative_order_10(p):
    """Return ord_p(10), or raise if 10 is not invertible modulo p."""
    if not isinstance(p, int) or p < 2 or gcd(p, 10) != 1:
        raise ValueError("modulus must be an integer >= 2 coprime to 10")
    k, weight = 0, 1
    while True:
        k += 1
        weight = weight * 10 % p
        if weight == 1:
            return k


def transition(state, digit, p):
    """From (F_n mod p, n mod k), consume the next source digit."""
    residue, phase = state
    k = multiplicative_order_10(p)
    if not isinstance(digit, int) or not 0 <= digit <= 9:
        raise ValueError("digit must be 0..9")
    if not 0 <= residue < p or not 0 <= phase < k:
        raise ValueError("invalid modular state")
    return ((residue + digit * pow(10, phase, p)) % p, (phase + 1) % k)


def scan_states(digits, p):
    """Yield (n, residue, phase) including n=0 before the source starts."""
    digits_checked(digits)
    residue, phase = 0, 0
    yield (0, residue, phase)
    k = multiplicative_order_10(p)
    powers = [pow(10, j, p) for j in range(k)]
    for n, digit in enumerate(digits, 1):
        residue = (residue + int(digit) * powers[phase]) % p
        phase = (phase + 1) % k
        yield (n, residue, phase)


def count_hits(digits, p, start=1):
    """Return observed hit indices, exact for any source digit string."""
    if not 1 <= start <= len(digits_checked(digits)):
        raise ValueError("start must lie within the source")
    return [n for n, residue, _ in scan_states(digits, p) if n >= start and residue == 0]


def random_tail_probability(p, tail_length, initial_value=13, place=2):
    """Exact P(F_{place+tail_length} = 0 mod p) given initial digits.

    Independent uniform source digits give an integer U uniform on
    [0,10**tail_length), with F = initial_value + 10**place * U.
    """
    if gcd(10, p) != 1 or tail_length < 0:
        raise ValueError("require p coprime to 10 and tail_length >= 0")
    size = 10 ** tail_length
    target = (-initial_value * pow(pow(10, place, p), -1, p)) % p
    number = size // p + (target < size % p)
    return number, size


def exact_null_mean(p, count, start=1, fixed_prefix="31"):
    """Expected hits for iid uniform subsequent digits, as a floating sum.

    The exact expression is a sum of rational numbers from
    random_tail_probability. For large n the 1/p correction is bounded by
    10**(-(n-len(fixed_prefix))) and is safely negligible.
    """
    if not 1 <= start <= count:
        raise ValueError("bad source window")
    digits_checked(fixed_prefix)
    if gcd(10, p) != 1:
        raise ValueError("p must be coprime to 10")
    fixed_length = len(fixed_prefix)
    if count < fixed_length:
        raise ValueError("count must include the fixed prefix")
    base = sum(int(d) * 10 ** j for j, d in enumerate(fixed_prefix))
    initial_hits = sum(1 for n, r, _ in scan_states(fixed_prefix, p)
                       if start <= n <= fixed_length and r == 0)
    suffix_start = max(start, fixed_length + 1)
    if suffix_start > count:
        return float(initial_hits)
    total = initial_hits + (count - suffix_start + 1) / p
    # Corrections decay exponentially. For tail >= 18, error < 1e-18.
    for n in range(suffix_start, min(count, fixed_length + 18) + 1):
        numerator, denominator = random_tail_probability(p, n - fixed_length, base, fixed_length)
        total += numerator / denominator - 1 / p
    return total


def universal_path(p, start_state, target_state):
    """Construct a sequence of digits connecting two automaton states.

    Since gcd(10,p)=1, all residues appear in any range of p consecutive
    possible digit-block integers. The requested end phase determines L mod k.
    """
    k = multiplicative_order_10(p)
    s, a = start_state
    t, b = target_state
    if not 0 <= s < p or not 0 <= t < p or not 0 <= a < k or not 0 <= b < k:
        raise ValueError("invalid states")
    L = (b - a) % k
    while 10 ** L < p:
        L += k
    if L == 0:
        L = k
    x = (t - s) * pow(pow(10, a, p), -1, p) % p
    return str(x).zfill(L)[::-1]  # little-endian source digits


def rigorous_null_variance_upper(count):
    """Safe elementary variance bound for counts of F_n=0 over a full stream.

    With a fixed 31 prefix and iid uniform tail, the pairwise covariance
    differs from its independent value by exponentially small terms in the
    digit separation. This intentionally loose bound holds for any p coprime
    to 10; it provides a conservative Chebyshev band, NOT a binomial test.
    """
    # q_n(1-q_n) <= 1/4. For n<m, the covariance is bounded by
    # 10**(-(m-n)) + 10**(-(m-2)), with a 1/p correction.
    # Sum 10^(-h) over lags h >= 1 is 1/9. For the second term,
    # sum_{m>=3} (m-1)10**(-(m-2)) = 19/81.
    return count / 4 + 2 * count / 9 + 2 * (19 / 81)