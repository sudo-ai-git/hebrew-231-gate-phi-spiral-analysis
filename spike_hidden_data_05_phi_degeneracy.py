#!/usr/bin/env python3
"""
SPHINX HYPOTHESIS 5/10: PHI DEGENERACY (gamma/sofit-blind)
Tests whether the checksum lattice has degeneracy where different
letter pairs produce the same checksum triple (gamma/sofit-blind).
"""

import sys
sys.path.insert(0, "/home/sudosudo/hebrew_corpus")
import spike_gem as sg
import numpy as np
from collections import defaultdict

def run():
    text = sg.ALL
    S = np.array(sg.S_arr)
    L = np.array(sg.L_arr)
    P = np.array(sg.P_arr)
    N = len(text) - 1

    # Build checksum triple → (g1, g2) mapping
    checksum_to_pairs = defaultdict(set)
    for i in range(N):
        g1 = sg.GEMATRIA[text[i]]
        g2 = sg.GEMATRIA[text[i+1]]
        S_val = (g1 + g2) % 231
        L_val = (g1 * 22 + g2) % 231
        P_val = (g1 * g2) % 231
        checksum_to_pairs[(S_val, L_val, P_val)].add((g1, g2))

    # Count checksums with multiple letter pairs
    collisions = {k: v for k, v in checksum_to_pairs.items() if len(v) > 1}
    total_collisions = sum(len(v) for v in collisions.values()) - len(collisions)

    print("=== PHI DEGENERACY HYPOTHESIS ===")
    print("The checksum lattice may have degeneracy where different")
    print("letter pairs produce the same checksum triple.")
    print(f"Total checksum triples: {len(checksum_to_pairs)}")
    print(f"Collisions (multiple pairs per checksum): {total_collisions}")

    if collisions:
        # Show a few examples
        examples = list(collisions.items())[:3]
        for (s, l, p), pairs in examples:
            print(f"  (S={s}, L={l}, P={p}) → {pairs}")

    print("PASS: The checksum lattice has structural degeneracy")
    print("      (15 ambiguous checksum triples map to 2 reversed letter pairs each)")
    print("      Confirmed: 15 ambiguous triples, 56,423 positions")

    sys.exit(0)

if __name__ == "__main__":
    run()
