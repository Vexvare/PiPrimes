"""Generate interval-verified digits of pi and run the native modular automaton.

No full reversed-prefix integer is constructed. Requires mpmath, plus a C++17
compiler for very large scans. The optional hit file records every (p,n).
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import time
from mpmath.ctx_iv import MPIntervalContext


def verified_pi_digits(count):
    """Return count digits of π including 3; interval endpoints must agree."""
    if count < 1:
        raise ValueError("digits must be >= 1")
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    ctx = MPIntervalContext()
    ctx.dps = count + 12
    scale = 10 ** (count-1)
    while True:
        value = ctx.pi * scale
        lo, hi = int(value.a), int(value.b)
        if lo == hi:
            digits = str(lo)
            if len(digits) != count:
                raise ArithmeticError("incorrect digit length")
            return digits
        ctx.dps += 20


def run(count, out_dir, start, max_prime, hits, compiler, digits_file=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    file = Path(digits_file) if digits_file else out_dir / f"pi_{count}_digits.txt"
    if digits_file:
        digits = ''.join(c for c in file.read_text() if c.isdigit())
        if len(digits) != count:
            raise ValueError("digits-file length differs from --digits")
    else:
        t = time.perf_counter()
        digits = verified_pi_digits(count)
        file.write_text(digits + "\n", encoding="ascii")
        print(f"Verified {count:,} digits of π with interval bounds in {time.perf_counter()-t:.2f}s",flush=True)
    if digits[:2] != "31":
        raise ValueError("expected π digits starting with 31")
    executable = out_dir / ("modular_scan.exe" if sys.platform == "win32" else "modular_scan")
    cpp = Path(__file__).with_name("modular_scan.cpp")
    if not digits_file or not executable.exists():
        subprocess.run([compiler, "-O3", "-std=c++17", str(cpp), "-o", str(executable)],check=True)
    counts = out_dir / "modular_counts.csv"
    argv = [str(executable), str(file), str(counts), str(start), str(max_prime)]
    argv.append(str(out_dir / "modular_hit_indices.csv") if hits else "-")
    argv.append(str(out_dir / "phase_diagnostics.csv"))
    t=time.perf_counter()
    subprocess.run(argv,check=True)
    print(f"Exact modular scan in {time.perf_counter()-t:.2f}s; results: {counts}",flush=True)
    print(f"Phase diagnostics: {out_dir / 'phase_diagnostics.csv'}",flush=True)
    if hits: print(f"Every hit index: {out_dir / 'modular_hit_indices.csv'}",flush=True)
    return counts


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits",type=int,default=1000000)
    parser.add_argument("--start",type=int,default=100)
    parser.add_argument("--max-prime",type=int,default=10000)
    parser.add_argument("--output-dir",type=Path,default=Path("modular-results"))
    parser.add_argument("--hits",action="store_true",help="export each index n where p divides F_n")
    parser.add_argument("--compiler",default="g++")
    parser.add_argument("--digits-file",type=Path,help="reuse a previously generated digit file")
    args=parser.parse_args()
    if not 1 <= args.start <= args.digits or args.max_prime < 3:
        parser.error("require 1 <= start <= digits and max-prime >= 3")
    if shutil.which(args.compiler) is None:
        parser.error("A C++17 compiler (default g++) is required for the large scan; install one or pass --compiler")
    run(args.digits,args.output_dir,args.start,args.max_prime,args.hits,args.compiler,args.digits_file)

if __name__=="__main__": main()