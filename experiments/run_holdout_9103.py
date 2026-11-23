"""Run the preregistered p=9103 holdout; audit full source prefix before scan.

Do not run until the protocol and native executable have been committed.
The first 1,000,000 digits' checksum is checked against original training data.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).parent
TRAIN_HASH = "387877db67fdddbde761c053c4376e0b411b10fd2b126fd8b1249963cb628877"


def run(digits_file, output, train_end=1_000_000, end=5_000_000, compiler="g++"):
    if train_end != 1_000_000 or end != 5_000_000:
        raise ValueError("Confirmatory window is frozen at 1,000,001..5,000,000")
    if shutil.which(compiler) is None:
        raise RuntimeError("C++17 compiler required")
    digits = "".join(c for c in Path(digits_file).read_text(encoding="ascii") if c.isdigit())
    if len(digits) != end or digits[:2] != "31":
        raise ValueError("Incorrect total digits or prefix")
    digest = hashlib.sha256(digits[:train_end].encode("ascii")).hexdigest()
    if digest != TRAIN_HASH:
        raise ValueError(f"TRAINING HASH MISMATCH: {digest}")
    full_digest = hashlib.sha256(digits.encode("ascii")).hexdigest()
    print(f"Training hash verified: {digest}; full hash: {full_digest}", flush=True)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    exe = output.parent / ("validate_9103.exe" if sys.platform == "win32" else "validate_9103")
    subprocess.run([compiler,"-O3","-std=c++17",str(ROOT/"validate_9103.cpp"),"-o",str(exe)],check=True)
    begin = time.perf_counter()
    result = subprocess.run([str(exe),str(digits_file),str(train_end),str(end)],capture_output=True,text=True,check=True)
    payload = json.loads(result.stdout)
    payload.update({"training_sha256":digest,"full_digits_sha256":full_digest,
                    "seconds":round(time.perf_counter()-begin,2),
                    "protocol":"research/HOLDOUT_9103_PREREGISTRATION.md"})
    output.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(payload,indent=2),flush=True)
    return payload


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--digits-file",type=Path,required=True)
    p.add_argument("--output",type=Path,default=Path("holdout-results/9103_validation.json"))
    p.add_argument("--compiler",default="g++")
    args=p.parse_args()
    run(args.digits_file,args.output,compiler=args.compiler)