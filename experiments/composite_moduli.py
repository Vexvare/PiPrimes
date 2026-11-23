"""Exact modular divisibility checks for composite moduli on an existing digit prefix.

For m coprime to 10, random independent tail digits predict about (N-start+1)/m
hits, but observations at adjacent n are dependent. For m with a factor 2 or 5,
F_n is never divisible by m, since F_n ends in 3 for every n>=1.
"""
import argparse
import csv
from math import gcd
from pathlib import Path

DEFAULT_MODULI = (9, 21, 27, 49, 77, 91, 121, 143, 169, 221, 1001,
                  20, 50, 100, 125, 175, 200, 625)


def modular_counts(digits, moduli=DEFAULT_MODULI, start=100):
    if not digits or not digits.isascii() or not digits.isdecimal() or digits[0] != '3':
        raise ValueError("expected decimal digits starting in 3")
    if not 1 <= start <= len(digits):
        raise ValueError("start must be in 1..N")
    rows=[]
    for m in moduli:
        if m < 2:
            raise ValueError("moduli must be >= 2")
        rem=0
        weight=1
        hits=0
        for n,ch in enumerate(digits,1):
            rem=(rem+int(ch)*weight)%m
            weight=weight*10%m
            if n >= start and rem==0: hits+=1
        coprime=gcd(m,10)==1
        rows.append({"modulus":m,"coprime_to_10":coprime,"hits":hits,
                     "tested":len(digits)-start+1,
                     "iid_expected_approx":(len(digits)-start+1)/m if coprime else None})
    return rows


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--digits-file",type=Path,required=True)
    p.add_argument("--start",type=int,default=100)
    p.add_argument("--moduli",type=int,nargs="*",default=DEFAULT_MODULI)
    p.add_argument("--csv",type=Path,default=Path("modular-results/composite_counts.csv"))
    a=p.parse_args()
    digits="".join(c for c in a.digits_file.read_text() if c.isdigit())
    rows=modular_counts(digits,a.moduli,a.start)
    a.csv.parent.mkdir(parents=True,exist_ok=True)
    with a.csv.open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys())
        writer.writeheader();writer.writerows(rows)
    for row in rows:
        print(row)


if __name__=="__main__":main()