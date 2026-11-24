"""Exact rational-interval audit of Gibbons's decimal pi spigot.

No decimal digits are inputs: the stream is generated from A_k(x)=
(k*x+4*k+2)/(2*k+1) and an interval floor test.
The audit demonstrates the exact coupling between emissions and digits;
it does not establish any digit-frequency theorem.
"""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Event:
    operation: str
    consumed: int
    emitted: int
    digit: int | None
    lo: Fraction
    hi: Fraction
    # C_e is the prefix as a rational, and e is number of digits emitted,
    # including initial integer digit 3.
    prefix: Fraction


def run_spigot(n_digits=20, max_operations=100000):
    if n_digits < 1 or max_operations < 1:
        raise ValueError("need positive n_digits and max_operations")
    q, r, s, t = 1, 0, 0, 1
    k = 1
    e = 0
    prefix = Fraction(0)
    events = []
    for _ in range(max_operations):
        lo = Fraction(3*q+r, 3*s+t)
        hi = Fraction(4*q+r, 4*s+t)
        if lo > hi:
            raise AssertionError("monotone increasing invariant broken")
        y = lo.numerator // lo.denominator
        if y == hi.numerator // hi.denominator:
            # z -> 10(z-y); this is digit emission, not an independent series step.
            prefix += Fraction(y, 10**e) if e else y
            e += 1
            q, r, s, t = 10*(q-y*s), 10*(r-y*t), s, t
            # Include post-transition bounds to expose the output orbit.
            events.append(Event("emit", k-1, e, y,
                                Fraction(3*q+r, 3*s+t),
                                Fraction(4*q+r, 4*s+t), prefix))
            if e == n_digits:
                return events
        else:
            # z -> z o A_k; input transform explicit and digit independent.
            q, r, s, t = q*k, q*(4*k+2)+r*(2*k+1), s*k, s*(4*k+2)+t*(2*k+1)
            k += 1
            events.append(Event("consume", k-1, e, None,
                                Fraction(3*q+r, 3*s+t),
                                Fraction(4*q+r, 4*s+t), prefix))
    raise RuntimeError("max_operations exceeded")


def emitted_digits(events):
    return ''.join(str(e.digit) for e in events if e.operation == 'emit')


def verify_certificate(events, rational_value, epsilon=0):
    """For exact input value π (or a certified rational interval), checks
    10^e*(π-C_e) is enclosed after every consume/emit event.
    This is an audit of the output transformation invariant; passing
    requires high precision for a long prefix (not a normality argument).
    """
    for event in events:
        rem = 10**event.emitted * (rational_value - event.prefix)
        if not event.lo - epsilon <= rem <= event.hi + epsilon:
            return False
    return True




def input_only_interval(terms):
    """Certified rational interval for pi from input LFTs only, no output digits."""
    if terms < 0:
        raise ValueError('terms must be nonnegative')
    width = Fraction(1)
    offset = Fraction(0)
    for k in range(1, terms+1):
        offset += 2*width
        width *= Fraction(k, 2*k+1)
    return offset+3*width, offset+4*width


def digit_free_weyl(length, harmonics=(1, 7)):
    """Compute T_N(h)=sum_{n=1}^N exp(2*pi*i*h*10^n*P_{4n}).

    Since |pi-P_{4n}|<=16**(-n), the difference between this sum
    and the standard pi orbit Weyl sum is bounded independently of N.
    Numerics are exploratory, and these sums are not proved to cancel.
    """
    import math
    if length < 1:
        raise ValueError('length must be positive')
    hs = tuple(harmonics)
    if not hs or any(not isinstance(h, int) or h == 0 for h in hs):
        raise ValueError('harmonics must be nonzero integers')
    sums = [0j]*len(hs)
    width = Fraction(1)
    offset = Fraction(0)
    scale = 1
    k = 0
    for n in range(1, length+1):
        while k < 4*n:
            k += 1
            offset += 2*width
            width *= Fraction(k, 2*k+1)
        lower = offset + 3*width
        scale *= 10
        # Use exact rational reduction before floating-point trigonometry.
        numerator = (scale * lower.numerator) % lower.denominator
        phase = numerator / lower.denominator
        for j, h in enumerate(hs):
            theta = (2*math.pi*h)*phase
            sums[j] += complex(math.cos(theta),math.sin(theta))
    return {h: abs(v)/length for h,v in zip(hs,sums)}

if __name__ == '__main__':
    from argparse import ArgumentParser
    p=ArgumentParser(description=__doc__)
    p.add_argument('--digits', type=int, default=20)
    args=p.parse_args()
    events=run_spigot(args.digits)
    print('digits:', emitted_digits(events))
    print('emitted\tterms-consumed\tpost-emit-certified-width')
    for e in events:
        if e.operation=='emit':
            print(e.emitted,e.consumed,float(e.hi-e.lo),sep='\t')