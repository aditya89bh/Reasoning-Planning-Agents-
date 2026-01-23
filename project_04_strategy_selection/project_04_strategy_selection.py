# ============================================
# Project 04: Strategy Selection Agent
# Full end-to-end minimal implementation
# ============================================

import time
import hashlib
import random
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
import json


# -----------------------------
# Utilities
# -----------------------------

def now_ts():
    return time.time()

def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())

def jaccard(a: List[str], b: List[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


# -----------------------------
# Data Models
# -----------------------------
