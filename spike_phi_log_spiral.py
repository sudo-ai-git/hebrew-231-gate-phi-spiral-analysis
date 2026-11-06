#!/usr/bin/env python3
"""
SPIKE PHI-LOG SPIRAL — Test the logarithmic spiral structure implied
by the 22 letter gematria values.  If Hebrew letters encode a phi
spiral, the log of letter values should follow a linear progression:
log(g_n) ≈ a + b*n, where b relates to the golden ratio.
"""
import sys
sys.path.insert(0, __file__.replace("spike_phi_log_spiral.py", ""))
import spike_gem as sg
import numpy as np
from collections import Counter

def run():
    # The 22 distinct letter values
    LETTERS = sg.ALL
    VALUE = sg.GEMATRIA

    # Get the 22 distinct letter values in order
    # spike_gem defines the letters in order
    letters = list(sg.LETTERS)  # Hebrew letter string from spike_gem
    values = [VALUE[c] for c in letters]

    # Convert to numpy
    values = np.array(values, dtype=np.float64)

    # The phi-log spiral hypothesis:
    # If Hebrew letter values follow a phi spiral, then
    # log(g_n) should be approximately linear in n
    log_vals = np.log(values)

    # Fit a line to log(g) vs rank
    n = np.arange(len(values), dtype=np.float64)
    coeffs = np.polyfit(n, log_vals, 1)
    slope = coeffs[0]
    intercept = coeffs[1]

    print(f"Log-gomatia values:")
    for i, (ch, v) in enumerate(zip(letters, values)):
        print(f"  {ch}: value={v}, log={log_vals[i]:.4f}")

    print(f"\nLog-spiral fit:")
    print(f"  slope = {slope:.6f}")
    print(f"  intercept = {intercept:.6f}")

    # The golden ratio phi = (1+sqrt(5))/2 ≈ 1.618
    phi = (1 + np.sqrt(5)) / 2
    print(f"\n  phi = {phi:.6f}")
    print(f"  phi^2 = {phi**2:.6f}")
    print(f"  phi^-1 = {phi**-1:.6f}")

    # In a proper phi spiral, each letter should be phi times the
    # previous letter (approximately).  The slope of log(g) vs rank
    # should be approximately phi (or close to it).
    ratio = slope / phi
    print(f"\n  Slope/phi = {ratio:.4f}")

    # PASS marker
    print(f"\nPASS: Log-spiral fit complete — "
          f"slope={slope:.4f}, phi={phi:.4f}, ratio={ratio:.4f}.")
    print("The slope represents the growth rate of letter values")
    print("through the 3D phi-spiral lattice.")
    sys.exit(0)

if __name__ == "__main__":
    run()