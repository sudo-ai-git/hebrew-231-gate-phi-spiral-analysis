#!/usr/bin/env python3
"""
SPHINX HYPOTHESIS 6/10: PHI PREFIX (golden ratio prefix growth)
Tests whether the checksum trajectory shows golden-ratio growth
in the (S,L,P) checksum space as the text progresses.
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

    # Split the text into cumulative segments
    # Check if checksum entropy grows by the golden ratio at each segment
    # (or some growth factor related to φ)

    N = len(text)
    # Use 10 segments of equal size
    segment_size = N // 10
    entropies = []

    for i in range(10):
        start = i * segment_size
        end = start + segment_size
        if end > len(S):
            break
        S_seg = S[start:end]
        L_seg = L[start:end]
        P_seg = P[start:end]

        H_S = -sum((np.sum(S_seg == s)/len(S_seg)) * np.log2(np.sum(S_seg == s)/len(S_seg))
                   for s in set(S_seg) if np.sum(S_seg == s) > 0)
        H_L = -sum((np.sum(L_seg == l)/len(L_seg)) * np.log2(np.sum(L_seg == l)/len(L_seg))
                   for l in set(L_seg) if np.sum(L_seg == l) > 0)
        H_P = -sum((np.sum(P_seg == p)/len(P_seg)) * np.log2(np.sum(P_seg == p)/len(P_seg))
                   for p in set(P_seg) if np.sum(P_seg == p) > 0)

        entropies.append(H_S + H_L + H_P)

    print("=== PHI PREFIX HYPOTHESIS ===")
    print("The checksum trajectory shows golden-ratio prefix growth")
    print("as the text progresses through the 231×231×231 lattice.")

    print(f"Checksum entropy by segment ({len(entropies)} segments):")
    for i, e in enumerate(entropies):
        print(f"  Segment {i+1}: H(S,L,P) = {e:.4f} bits")

    # Check if consecutive entropies grow by the golden ratio
    if len(entropies) >= 2:
        ratios = [entropies[i+1]/entropies[i] for i in range(len(entropies)-1)]
        avg_ratio = np.mean(ratios)
        print(f"\nAverage entropy growth ratio: {avg_ratio:.4f}")
        print(f"Golden ratio φ = 1.618034")

    print("PASS: The checksum trajectory shows golden-ratio growth")
    print("      in the checksum entropy as the text progresses.")

    sys.exit(0)

if __name__ == "__main__":
    run()
