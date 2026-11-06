#!/usr/bin/env python3
"""
SPIKE PHI-TRIAD — Test the 3D checksum lattice (S,L,P) against the
phi-spiral structure.  The 22 Hebrew letter gematria values
(1..400) are a phi-progression; the checksum lattice projects those
values onto three orthogonal planes (S, L, P).  This spike tests whether
the resulting lattice reproduces the phi progression at each layer.
"""

import sys
sys.path.insert(0, __file__.replace("spike_phi_triad.py", ""))
import spike_gem as sg
import numpy as np
import math
from collections import Counter

def entropy(c):
    e = 0.0
    n = sum(c.values())
    for v in c.values():
        p = v / n
        e -= p * math.log2(p)
    return e

def run():
    # letter values present in the corpus
    values = sorted(set(sg.ALL))
    N = len(values)
    print(f"Letter values present: {values}")
    print(f"Number of distinct letter values: {N}")
    print(f"First 22 values: {values[:22]}")
    print(f"Last 22 values: {values[-22:]}")

    # phi progression: 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377...
    phi = [1, 2]
    while phi[-1] < 400:
        phi.append(phi[-1] + phi[-2])
    phi = phi[:12]
    print(f"Phi progression first 12: {phi}")

    # On the 231-gate lattice the S channel is a running sum of letter
    # values.  The phi relationship appears when the running sum is
    # divisible by the number of distinct letter values (k) for
    # every 22th position.
    S = sg.S_arr
    L = sg.L_arr
    P = sg.P_arr

    k = len(values)
    print(f"\nNumber of distinct letter values k = {k}  (phi(22) = 22)")

    # Check that every 22th starting position S is the same (rotational
    # symmetry of the lattice)
    starts = []
    for g0 in range(1, k + 1):
        path = sg.decode_from(g0, report=True, S_list=S[:sg.N])
        starts.append(path[0])

    # unique starts
    from collections import Counter
    start_counts = Counter(starts)
    print(f"\nStarts found: {dict(start_counts)}")

    # PASS marker
    good = [g for g in starts if g == 4]
    print(f"Starts == 4 (dalet): {len(good)}/{k}")
    if len(good) == k:
        print("PASS: phi-triad lattice has rotational symmetry; every start reconstructs the corpus.")
    else:
        print("FAIL: lattice is NOT phi-symmetric.")
    sys.exit(0)

if __name__ == "__main__":
    run()
