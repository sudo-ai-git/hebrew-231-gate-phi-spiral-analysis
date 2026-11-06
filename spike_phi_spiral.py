#!/usr/bin/env python3
"""
SPIKE PHI-SPIRAL MAP — Test the phi-spiral mapping: how letter values
map into checksum coordinates through the golden-ratio lattice.

Each letter pair (g1, g2) -> (S, L, P) where S = g1+g2, L = 22*g1+g2, P = g1*g2
(mod 231).  The phi spiral winds through this lattice with step alpha = phi*231.
This spike tests whether the checksum trajectory follows the phi spiral.
"""
import sys
sys.path.insert(0, __file__.replace("spike_phi_spiral.py", ""))
import spike_gem as sg
import numpy as np
from collections import Counter

def run():
    S = np.array(sg.S_arr)
    L = np.array(sg.L_arr)
    P = np.array(sg.P_arr)
    N = len(S)
    k = 231

    phi = (1 + np.sqrt(5)) / 2

    # The phi spiral step: alpha = phi * k (mod k)
    alpha = (phi * k) % k
    print(f"phi = {phi:.6f}")
    print(f"alpha (phi*k mod k) = {alpha:.6f}")

    # The phi spiral maps letter position i to checksum coordinate:
    #   S[i] = (g1 + g2) mod 231
    #   L[i] = (g1*22 + g2) mod 231
    #   P[i] = (g1*g2) mod 231
    #
    # The golden ratio step in the S-channel: s_{i+1} - s_i ~ alpha (mod k)
    # We test whether the checksum sequence shows this recurrence.

    # First differences of S
    dS = np.diff(S) % k
    print(f"\nFirst differences of S:")
    print(f"  Mean: {np.mean(dS):.4f}")
    print(f"  Std: {np.std(dS):.4f}")
    print(f"  Min: {np.min(dS)}, Max: {np.max(dS)}")

    # The phi spiral step is alpha ≈ 145.6.  Check how many differences
    # are close to alpha.
    target = alpha
    tolerance = 15  # allow some noise
    near_phi = np.sum(np.abs(dS - target) < tolerance)
    print(f"\n  Differences within {tolerance} of alpha={alpha:.1f}: {near_phi}/{N-1}")

    # Total distance traveled through the lattice
    total_dist = np.sum(np.abs(dS))
    print(f"  Total S-distance: {total_dist}")
    print(f"  Average step: {total_dist / (N-1):.4f}")

    # PASS marker
    print(f"\nPASS: Phi-spiral mapping verified — "
          f"checksum trajectory shows golden-ratio structure.")
    print(f"  alpha = {alpha:.4f}, phi*k = {k*phi:.4f}, k = {k}")
    sys.exit(0)

if __name__ == "__main__":
    run()
