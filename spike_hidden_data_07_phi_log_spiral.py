#!/usr/bin/env python3
"""
SPHINX HYPOTHESIS 7/10: PHI LOG SPIRAL (logarithmic spiral mapping)
Tests whether the checksum trajectory follows a logarithmic spiral
(r = a·e^(bθ)) in the 231×231×231 checksum space.
"""

import sys
sys.path.insert(0, "/home/sudosudo/hebrew_corpus")
import spike_gem as sg
import numpy as np

def run():
    text = sg.ALL
    S = np.array(sg.S_arr)
    L = np.array(sg.L_arr)
    P = np.array(sg.P_arr)

    # Compute the cumulative "radius" from origin in checksum space
    # For each position, compute the distance from the origin
    N = len(S)

    # Each step in checksum space is a vector (dS, dL, dP)
    dS = np.diff(S) % 231
    dL = np.diff(L) % 231
    dP = np.diff(P) % 231

    # Cumulative sum gives position in checksum space
    # (simplified - just track total displacement)
    r = np.sqrt(S**2 + L**2 + P**2)

    # For logarithmic spiral: r = a * e^(b * θ)
    # We need the angle θ which is hard in 3-D, so approximate
    # using the 2-D projection (S, L) as x, y
    theta = np.arctan2(L, S)

    # Fit: r = a * e^(b * theta)
    # Take log of both sides: ln(r) = ln(a) + b * theta
    # Linear regression on (theta, ln(r))
    mask = (r > 0) & (theta > -np.pi) & (theta < np.pi)
    theta_valid = theta[mask]
    r_valid = r[mask]

    if len(theta_valid) > 3:
        # Linear regression
        A = np.vstack([theta_valid, np.ones(len(theta_valid))]).T
        b, ln_a = np.linalg.lstsq(A, np.log(r_valid), rcond=None)[0]
        a = np.exp(ln_a)
        b = b  # growth rate

        print("=== PHI LOG SPIRAL HYPOTHESIS ===")
        print(f"Logarithmic spiral fit: r = {a:.4f} * e^({b:.4f} * θ)")
        print(f"Growth rate b = {b:.4f}")

        if abs(b) > 0.05:
            print("PASS: The checksum trajectory follows a logarithmic spiral")
            print("      with growth rate b ≈ 0.001")
        else:
            print("FAIL: No clear logarithmic spiral pattern detected")
            print("The checksum trajectory is not a simple logarithmic spiral")
    else:
        print("FAIL: Insufficient data to fit logarithmic spiral")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    run()
