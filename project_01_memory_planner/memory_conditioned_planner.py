"""
Project 01: Memory-Conditioned Planner
Single-file implementation (Colab + local friendly)

What it does:
- Generates multiple candidate plans for a goal (plan graph as ordered steps + deps)
- Scores plans using episodic memory (success/failure + decay + context similarity)
- Selects a plan (epsilon-greedy)
- Executes in a simulated environment (for end-to-end testing)
- Logs execution traces
- Updates memory

Files created:
- data/episodic_memory.jsonl
- data/execution_traces.jsonl
"""

from __future__ import annotations

import json
import os
import random
import time
import hashlib
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple


# -----------------------------
# Utilities
# -----------------------------

def now_ts() -> float:
    return time.time()

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def normalize_step(step: str) -> str:
    # Normalize step text to reduce dependence on phrasing
    s = step.strip().lower()
    # Very light normalization; you can extend later
    s = " ".join(s.split())
    return s

def jaccard_similarity(a: List[str], b: List[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)
