"""Finite diagnostics for the reversed-prefix Weyl criterion for base-10 normality.

These observations are not a proof of pi's normality. Input is a digit stream,
including its integer digit (e.g. '314159...'). Leading zeros in reversed
prefixes are represented by x_n=F_n/10**n, not discarded.

Example:
    python normality_weyl.py pi_5000000_digits.txt --limit 1000000 \
        --harmonics 1,2,3,7,10,20 --max-block 3
"""
import argparse
import json
import math
from pathlib import Path


def digit_stream(path, limit=None):
    """Read ASCII decimal digits in chunks; optionally stop at `limit` digits."""
    if limit is not None and limit < 1:
        raise ValueError("limit must be positive")
    emitted = 0
    with Path(path).open("r", encoding="ascii") as handle:
        while True:
            chunk = handle.read(1 << 20)
            if not chunk:
                return
            for ch in chunk:
                if ch in "\r\n \t":
                    continue
                if ch < "0" or ch > "9":
                    raise ValueError("input must contain only ASCII digits and whitespace")
                yield ord(ch) - ord("0")
                emitted += 1
                if limit is not None and emitted == limit:
                    return


def analyze(digits, harmonics=(1, 2, 3, 7, 10, 20), max_block=3):
    """Return finite Weyl and digit-block statistics for an iterable of digits.

    x_n satisfies x_{n+1}=(x_n+d_{n+1})/10; floating point is only used
    for phase visualization. Rolling decimal block counts are integer-exact.
    """
    harmonics = tuple(dict.fromkeys(int(h) for h in harmonics))
    if not harmonics or any(h == 0 for h in harmonics):
        raise ValueError("supply at least one nonzero harmonic")
    if max_block < 1 or max_block > 5:
        raise ValueError("max_block must be between 1 and 5")
    counts = [[0] * 10**k for k in range(1, max_block+1)]
    mods = [10**k for k in range(1, max_block+1)]
    rolling = [0] * max_block
    real = [0.0] * len(harmonics)
    imag = [0.0] * len(harmonics)
    x = 0.0
    n = 0
    for d in digits:
        if not isinstance(d, int) or isinstance(d, bool) or not 0 <= d <= 9:
            raise ValueError("digits must be integers in 0..9")
        n += 1
        x = (x + d) / 10.0
        for j, h in enumerate(harmonics):
            phase = (2 * math.pi * h) * x
            real[j] += math.cos(phase)
            imag[j] += math.sin(phase)
        for j, modulus in enumerate(mods):
            rolling[j] = (10 * rolling[j] + d) % modulus
            if n >= j + 1:
                counts[j][rolling[j]] += 1
    if n == 0:
        raise ValueError("empty digit input")
    blocks = {}
    for k, row in enumerate(counts, 1):
        total = n - k + 1
        if total <= 0:
            continue
        expected = total / (10**k)
        worst = max(abs(v - expected) for v in row)
        blocks[str(k)] = {
            "sample_size": total,
            "expected_per_word": expected,
            "max_abs_count_deviation": worst,
            "max_abs_frequency_deviation": worst / total,
            "min_word_count": min(row),
            "max_word_count": max(row),
        }
    return {
        "n": n,
        "x_last": x,
        "harmonics": {str(h): {
            "mean_real": real[j]/n,
            "mean_imag": imag[j]/n,
            "mean_magnitude": math.hypot(real[j], imag[j])/n,
        } for j, h in enumerate(harmonics)},
        "blocks": blocks,
        "caveat": "Finite-sample diagnostics only; normality requires limits for all block lengths / harmonics.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("digits_file", type=Path, help="ASCII file of digits, starting at the initial 3")
    parser.add_argument("--limit", type=int, default=1000000)
    parser.add_argument("--harmonics", type=str, default="1,2,3,7,10,20")
    parser.add_argument("--max-block", type=int, default=3)
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    args = parser.parse_args(argv)
    try:
        harmonics = [int(s.strip()) for s in args.harmonics.split(",")]
        report = analyze(digit_stream(args.digits_file, args.limit), harmonics, args.max_block)
    except (OSError, ValueError) as e:
        parser.error(str(e))
    encoded = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
