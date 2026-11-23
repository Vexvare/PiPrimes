"""Export an offline, interactive view of prime coverage and the PiPrimes tree."""
import argparse
import json
from pathlib import Path
import webbrowser

from sympy import primerange

from Fractal_Pi import constant_digits
from compare_coverage import first_appearance


def export_atlas(path, digits=100, max_length=4):
    if not 1 <= digits <= 1000 or not 1 <= max_length <= 5:
        raise ValueError("choose 1–1000 source digits and 1–5 digits per prime")
    source = constant_digits(digits)
    rows = []
    for prime in primerange(2, 10**max_length):
        hit = first_appearance(source, prime)
        rows.append((prime, *(hit or (None, None))))
    data = {"source": source, "primes": rows, "maxLength": max_length}
    template = Path(__file__).with_name("web").joinpath("atlas.html").read_text(encoding="utf-8")
    path.write_text(template.replace("__ATLAS_DATA__", json.dumps(data, separators=(",", ":"))),
                    encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits", type=int, default=100, choices=range(1, 1001), metavar="1-1000")
    parser.add_argument("--max-length", type=int, default=4, choices=range(1, 6))
    parser.add_argument("--output", type=Path, default=Path("PiPrimes-atlas.html"))
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()
    export_atlas(args.output, args.digits, args.max_length)
    print(args.output.resolve())
    if not args.no_open:
        webbrowser.open(args.output.resolve().as_uri())
