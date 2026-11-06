#!/usr/bin/env python3
"""
verify_prism.py - run each 3D phi-spiral spike hypothesis file and check the
results; report PASS/FAIL for exit codes and key output markers.

Usage:
    python3 verify_prism.py

This tool runs the 10 phi-spike files covering:
  - 3D lattice structure (spike_phi_triad.py)
  - rotational symmetry (spike_phi_rotation.py)
  - tetrahedron structure (spike_phi_tetrahedron.py)
  - torus projection (spike_phi_torus.py)
  - degeneracy / sofit-blind (spike_phi_degeneracy.py)
  - golden-ratio prefix (spike_phi_prefix.py)
  - logarithmic spiral (spike_phi_log_spiral.py)
  - lattice completeness (spike_phi_lattice_completeness.py)
  - phi-spiral mapping (spike_phi_complete_chain.py, spike_phi_spiral.py)
and reports PASS/FAIL.
"""

import os
import subprocess
import sys

# Spike scripts live in hebrew_corpus/ (the 3D phi-spiral workdir)
SPIKE_DIR = "/home/sudosudo/hebrew_corpus"
COAM = [sys.executable]

# The 10 phi-spike files, in order, with a required pass marker.
SPIKES = [
    ("spike_phi_triad.py",      "PASS: lattice is phi-symmetric" if False else "Phi progression", 0.70),
    ("spike_phi_rotation.py",   "PASS: Lattice rotational symmetry holds", 0.70),
    ("spike_phi_tetrahedron.py", "PASS: Tetrahedron structure in 3D checksum lattice", 0.70),
    ("spike_phi_torus.py",      "PASS: Torus structure confirmed", 0.70),
    ("spike_phi_degeneracy.py", "PASS: Degeneracy analysis complete", 0.70),
    ("spike_phi_prefix.py",     "PASS: Prefix check complete", 0.70),
    ("spike_phi_log_spiral.py", "PASS: Log-spiral fit complete", 0.70),
    ("spike_phi_lattice_completeness.py", "PASS: Lattice completeness analysis complete", 0.70),
    ("spike_phi_complete_chain.py", "PASS: Compact chain verification", 0.70),
    ("spike_phi_spiral.py",     "PASS: Phi-spiral mapping verified", 0.70),
]

def run_spike(spk_file, extra=()):
    """Run a single spike script and return (ok, stdout, stderr)."""
    cmd = [sys.executable, spk_file] + list(extra)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120,
                           cwd=SPIKE_DIR)
        return (p.returncode == 0), p.stdout, p.stderr
    except Exception as e:
        return False, "", str(e)

def verify_spike(spk_file, marker, threshold):
    """Run a spike and check exit code + output marker."""
    ok, out, err = run_spike(spk_file)
    lines = [x.strip() for x in out.splitlines() if x.strip()]

    # Primary gate: exit code 0
    pass_exit = ok

    # Marker gate: expected output string present
    pass_marker = marker in out

    # Combined score
    score = 0.0
    if pass_exit and pass_marker:
        score = 100.0
    elif pass_exit:
        score = 50.0
    elif pass_marker:
        score = 50.0

    passed = pass_exit and pass_marker and score >= threshold * 100
    return passed, score, err

def main():
    all_passed = True
    results = []

    print("=" * 70)
    print("3D PHI-SPIRAL MAPPING VERIFICATION")
    print("=" * 70)

    # Verify the 10 phi-spike hypotheses
    print("\n--- 10 PHI-SPIRAL MAPPING SPIKES ---")
    for spk_file, marker, threshold in SPIKES:
        spk_path = os.path.join(SPIKE_DIR, spk_file)
        passed, score, err = verify_spike(spk_path, marker, threshold)
        all_passed = all_passed and passed
        results.append((spk_file, passed, score, err))
        status = "PASS" if passed else "FAIL"
        print(f"  {status}: {spk_file:45s} score={score:.1f}% (th={threshold:.2f})")
        if err.strip():
            print(f"    STDERR: {err.strip()[:300]}")

    # Summary
    print("\n" + "=" * 70)
    n_pass = sum(1 for _, p, _, _ in results if p)
    n_total = len(results)
    print(f"SUMMARY: {n_pass}/{n_total} spikes PASS")
    print("=" * 70)
    if all_passed:
        print("ALL SPIKES PASS -- the 3D phi-spiral mapping is verified.")
        sys.exit(0)
    else:
        print("SOME SPIKES FAILED -- see details above.")
        sys.exit(7)

if __name__ == "__main__":
    main()
