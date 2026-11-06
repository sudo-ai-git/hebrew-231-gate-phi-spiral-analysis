#!/usr/bin/env python3
"""Shared spike harness for 231-gate hypothesis testing.

Loads the Tanakh corpus once, exposes checksum channels and a decoder, so each
spike is a thin, focused experiment. All spikes use the CORRECT 1-400 gematria
(or verify the alternative convention where the spike calls for it).
"""
import re
from collections import Counter

CORPUS = "/home/sudosudo/hebrew_corpus/tanakh_hebrew.txt"
LETTERS = "אבגדהוזחטיכךלמםנןסעףפצץקרשת"
GEMATRIA = {c: v for c, v in [
    ("א",1),("ב",2),("ג",3),("ד",4),("ה",5),("ו",6),("ז",7),("ח",8),("ט",9),("י",10),
    ("כ",20),("ך",20),("ל",30),("מ",40),("ם",40),("נ",50),("ן",50),("ס",60),
    ("ע",70),("ף",80),("פ",80),("צ",90),("ץ",90),("ק",100),("ר",200),("ש",300),("ת",400),
]}

HEB = re.compile(r"[^\u05D0-\u05EA]")
def only_heb(s):
    return HEB.sub("", s)

def load_corpus():
    rec = []
    with open(CORPUS, encoding="utf-8") as f:
        for line in f:
            if "\t" not in line:
                continue
            _, t = line.split("\t", 1)
            rec.append(only_heb(t))
    return "".join(rec)

ALL = load_corpus()
N = len(ALL)

# Precomputed checksum arrays (S, L, P) for the whole corpus (mod 231).
S_arr = [0] * (N - 1)
L_arr = [0] * (N - 1)
P_arr = [0] * (N - 1)

def build_checksums():
    for i in range(N - 1):
        g1 = GEMATRIA[ALL[i]]
        g2 = GEMATRIA[ALL[i + 1]]
        S_arr[i] = (g1 + g2) % 231
        L_arr[i] = (g1 * 22 + g2) % 231
        P_arr[i] = (g1 * g2) % 231

build_checksums()

def channels(g1, g2):
    return ((g1 + g2) % 231, (g1 * 22 + g2) % 231, (g1 * g2) % 231)

def decode_from(g0, S_range=None, L_range=None, report=False, S_list=None, L_list=None):
    """Reconstruct the letter-value path from first letter g0 and checksums.

    Deterministic decoder: g_{i+1} = (S_i - g_i) mod 231. If S_list/L_list are
    given they are used (e.g. for corruption testing) instead of the module
    arrays. Always succeeds (over-determined) -- that is the hallucination
    property under test.
    """
    path = [g0]
    g = g0
    if S_list is not None:
        S_iter = S_list
        L_iter = L_list
    else:
        S_iter = S_arr[S_range[0]:S_range[1]] if S_range else S_arr
        L_iter = L_arr[L_range[0]:L_range[1]] if L_range else L_arr
    for s in S_iter:
        g = (s - g) % 231
        path.append(g)
    return path

def letter_to_value(ch):
    return GEMATRIA[ch]

def value_to_let(v):
    for c, val in GEMATRIA.items():
        if val == v:
            return c
    return None

# ---- 231-solution decoder: valid-letter lookup ----

VALID_SET = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400}

def candidates(r):
    """Letter-values v (<=400) with v ≡ r (mod 231)."""
    out = []
    if 1 <= r <= 400 and r in VALID_SET:
        out.append(r)
    r2 = r + 231
    if r2 <= 400 and r2 in VALID_SET:
        out.append(r2)
    return out

def reconstruct_from(g0):
    """Walk the checksum chain using valid-letter lookup; returns (mod_path,
    alternatives).

    mod_path[j] = valid letter VALUE at position j (exact, 100% of positions);
    alternatives[j-1] = candidate letter values for position j, the first of
    which is the mod-231 value if it is itself a valid letter, otherwise the
    +231 variant that is the only valid letter for that mod-231 class.
    """
    mod_path = [g0]
    alternatives = []
    g = g0
    for i in range(N - 1):
        r = (S_arr[i] - g) % 231
        cands = candidates(r)
        alternatives.append(cands)
        g = cands[0]          # valid letter value (exact)
        mod_path.append(g)
    return mod_path, alternatives

if __name__ == "__main__":
    print(f"Corpus: {N} letters, {len(S_arr)} checksum pairs (S,L,P)")
    print(f"Distinct S={len(set(S_arr))}, L={len(set(L_arr))}")
