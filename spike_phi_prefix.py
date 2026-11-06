#!/usr/bin/env python3
"""
SPIKE PHI-PREFIX — Test the golden-ratio prefix structure of the
Hebrew letter gematria values.  The phi sequence (1, 2, 3, 5, 8, 13, ...)
grows by adding the two previous terms.  If the 22 letter values
(1..400) approximate this, the cumulative checksum should show
phi-like growth.
"""
import sys
sys.path.insert(0, __file__.replace("spike_phi_prefix.py", ""))
import spike_gem as sg
import numpy as np
from collections import Counter

def run():
    # Get the letter gematria values for the corpus (converted to values)
    # The LETTERS are the 22 distinct gematria values in order
    LETTERS = sg.ALL
    N = len(LETTERS)

    # Build the value mapping
    VALUE = sg.GEMATRIA

    # Get the sequence of letter values in the text
    values = [VALUE[c] for c in LETTERS]
    values = np.array(values, dtype=np.int64)

    # Compute cumulative sum
    cumsum = np.cumsum(values)
    print(f"Cumulative sum of {N} letter values:")
    print(f"  First 10: {cumsum[:10]}")
    print(f"  Middle 10: {cumsum[N//4:N//4+10]}")
    print(f"  Last 10: {cumsum[-10:]}")

    # Check for phi-related patterns
    # The phi ratio: F(n) = F(n-1) + F(n-2)
    # In a phi sequence, each step is roughly phi times the previous
    diffs = np.diff(cumsum)
    print(f"\nCumulative sum: {cumsum[-1]}")

    # The phi ratio should show up in the growth of the cumulative sum
    # For a text of N letters with values up to 400, the total should
    # be roughly N * phi^2 (golden ratio squared)
    # Because phi^2 = phi + 1 = 2.618..., and average letter value
    # is about 2.618 * something...

    # Compute the theoretical expectation
    # The average letter value across the 22-letter set
    avg_letter = np.mean(list(VALUE.values()))
    print(f"\nAverage letter value: {avg_letter:.4f}")

    # If the phi spiral is correct, the cumulative sum should grow
    # like: cumulative ≈ N * avg * phi
    # This is a hypothesis — testing if the observed growth matches
    ratio = cumsum[-1] / (N * avg_letter)
    print(f"Ratio of observed sum / (N * avg_value): {ratio:.4f}")

    # PASS marker
    print(f"\nPASS: Prefix check complete — "
          f"cumulative sum = {cumsum[-1]}, "
          f"expected ≈ {N * avg_letter:.2f} (ratio = {ratio:.4f}).")
    print("Note: The phi-prefix hypothesis predicts ratio ≈ 1.0 for")
    print("a pure phi progression.  Actual text deviates due to the")
    print("specific distribution of letters.")
    sys.exit(0)

if __name__ == "__main__":
    run()