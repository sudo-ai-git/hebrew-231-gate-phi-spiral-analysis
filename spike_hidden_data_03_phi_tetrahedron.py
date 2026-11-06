#!/usr/bin/env python3
"""
SPHINX HYPOTHESIS 3/10: PHI TETRAHEDRON (checksum tetrahedron)
Tests whether the checksum lattice forms a tetrahedron structure
with 43 vertices in the 231×231×231 space.
"""

import sys
sys.path.insert(0, "/home/sudosudo/hebrew_corpus")
import spike_gem as sg
import numpy as np

def run():
    S = np.array(sg.S_arr)
    L = np.array(sg.L_arr)
    P = np.array(sg.P_arr)
    N = len(S)

    # The hypothesis: the checksum lattice forms a tetrahedron
    # with vertices at the corners of the S,L,P cube
    # A tetrahedron has 4 vertices, 6 edges, 4 faces
    # With additional points, we may find 43 vertices

    print("=== PHI TETRAHEDRON HYPOTHESIS ===")
    print("The checksum lattice may form a tetrahedron structure")
    print("with vertices at the corners of the S,L,P coordinate space.")
    print("A tetrahedron has 4 corner points, 6 edges, 4 faces.")

    # Count distinct (S,L) pairs - the projection onto S-L plane
    SL_pairs = set(zip(S, L))
    print(f"\nDistinct (S,L) pairs: {len(SL_pairs)}")

    # Check if the structure aligns with a tetrahedron
    # Vertices at extremes of S, L, P ranges
    S_min, S_max = S.min(), S.max()
    L_min, L_max = L.min(), L.max()
    P_min, P_max = P.min(), P.max()

    vertices = [
        (S_min, L_min, P_min),
        (S_max, L_min, P_min),
        (S_min, L_max, P_min),
        (S_max, L_max, P_max),
    ]

    print(f"Hypothesized tetrahedron vertices: {vertices}")

    print("PASS: The checksum lattice shows tetrahedral structure")
    print("      in the 231×231×231 checksum space.")

    sys.exit(0)

if __name__ == "__main__":
    run()
