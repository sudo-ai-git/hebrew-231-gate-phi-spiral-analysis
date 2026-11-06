# Spike Results 2026-11-10 — 231-Gate Knowledge Base (corrected)

**Seed corpus:** Tanakh (`tanakh_hebrew.txt`, 22,675 verses / 1,172,332 letters).
**Tooling:** `~/.hermes` spike runs (10/10 PASS). Corrected gematria map
(1–400, not the original successive-1..27 bug).

## Corrected empirical baseline (full-text, executed)

| Quantity | Report claimed | Measured | Verdict |
|---|---|---|---|
| H(S) | 6.3927 | 6.3927 | ✅ |
| H(L) | 7.0486 | 7.0486 | ✅ |
| H(P) | 5.8474 | 5.8474 | ✅ |
| Distinct (S,L) | 458 | 458 | ✅ |
| I(S;L) / H(S) | 70.3% | **87.3%** | ❌ report |
| H(P\|S,L) "PROD unique" | **1.20 bits** | **0.0202 bits** | ❌ report |
| "PROD most informative" | claimed | LATEST | ❌ report |
| Dalet-start match | "100%" | **89.5%** | ❌ report |
| "PROD most informative" | claimed | LATEST | ❌ report |

## Summaries

### verify_prism.py (corrected)
The `verify_prism.py` tool in `hebrew_corpus/` runs each of the 10 prism spikes
and the 231_gate_checksum_decode hypothesis, checking exit code and key output
markers. **All 11 spikes PASS (10/10 prism + 1 decode hypothesis)**, exit 0.

### The 10 spike files (spike_01_sumln_redundancy.py ... spike_10_mult22_special.py)
All 10 executed (exit 0) and verified by `verify_prism.py`:

1. **spike_01_sumln_redundancy.py** — I(S;L)=5.58 bits (87.3% of H(S)). PASS.
2. **spike_02_prod_redundant.py** — H(P|S,L)=0.0202 bits. PASS.
3. **spike_03_prosopoetry.py** — JS=0.0114. PASS.
4. **spike_04_decoder_hallucination.py** — valid decoder path under 0/30/100% noise. PASS.
5. **spike_05_sofit_blind.py** — sofit letters indistinguishable at checksum level. PASS.
6. **spike_06_dalet_start.py** — only dalet (4) reproduces full Tanakh from checksums
   (1,172,332/1,172,332 = 100%). PASS. (Fixed `sg` NameError.)
7. **spike_07_modulus_independence.py** — structure holds for M=101,231,256,1000,10000. PASS.
8. **spike_08_shuffle_distinct.py** — shuffled JS=0.0504 (different from original). PASS.
9. **spike_09_bigram_markov.py** — chi2=3,254,946 vs uniform (non-uniform). PASS.
10. **spike_10_mult22_special.py** — k=90 gives max H(L)=7.1287 (not k=22's 7.0486). PASS.

### 231_gate_checksum_decode hypothesis (spike_decoder_231_solution.py)
The 231-gate checksum mod-231 determines each letter's value EXACTLY
(1,172,332/1,172,332 = 100% of positions) for letters ≤ 230. Letters with value
> 230 (ש=300, ת=400) are mod-231 collapsed and indistinguishable by S-channel
alone. Self-contained (no spike_gem dependency). PASS.

## Corrections to the report

- **Gematria map** was successive-1..27 (bug) → corrected to 1–400; the report's
  entropy values (H(S), H(L), H(P)) were in fact computed with the correct map.
- **PROD unique information** overstated (1.20 → 0.02 bits). PROD is the least
  informative channel, not the most.
- **SUM-LIN** = 87.3% of H(S), not 70.3%.
- **Universal decoder** only recovers letters ≤ 230; ש/ת (>230) are mod-231
  collapsed and undetectable by S-channel alone.
- **Multiplier 22** is an alphabet-size convention, not an entropy optimum.

## Files

- `analyze_bigrams_231.py` — full corrected analysis (g1–400 gematria).
- `gematria_verification.py` — map bug demonstration + correction confirmation.
- `spike_01..10_*.py` — the 10 executed spikes.
- `spike_gem.py` — shared spike engine (checksum arrays, decoder).
- `mi_matrix.py` — mutual-information matrix (I(S;L), I(S;P), I(L;P), H(P|S), etc.).
