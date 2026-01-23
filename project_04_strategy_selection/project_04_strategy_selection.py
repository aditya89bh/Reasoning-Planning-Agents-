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

class StrategyMemory:
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}

    def add_strategy(self, strategy: Strategy):
        self.strategies[strategy.fingerprint] = strategy

    def all(self) -> List[Strategy]:
        return list(self.strategies.values())

    def update_confidence(self, fp: str, delta: float):
        s = self.strategies[fp]
        s.confidence = max(0.05, min(0.95, s.confidence + delta))
        s.usage_count += 1
        s.last_used_ts = now_ts()


# -----------------------------
# Strategy Selector
# -----------------------------

class StrategySelector:
    def __init__(self, memory: StrategyMemory, exploration_rate: float = 0.15):
        self.memory = memory
        self.exploration_rate = exploration_rate

    def score_strategy(self, strategy: Strategy, context_tags: List[str]) -> float:
        similarity = jaccard(strategy.context_tags, context_tags)
        score = (
            0.6 * strategy.confidence +
            0.4 * similarity
        )
        return score

    def select(self, context_tags: List[str]) -> StrategyDecision:
        scores = {}
        strategies = self.memory.all()

        for s in strategies:
            scores[s.name] = self.score_strategy(s, context_tags)

        # Exploration
        if random.random() < self.exploration_rate:
            chosen = random.choice(strategies)
            note = "exploration"
        else:
            chosen = max(strategies, key=lambda s: scores[s.name])
            note = "exploitation"

        self.memory.update_confidence(
            chosen.fingerprint,
            delta=0.05 if note == "exploitation" else 0.01
        )

        return StrategyDecision(
            context_tags=context_tags,
            considered=scores,
            chosen_strategy=chosen.name,
            ts=now_ts(),
            notes=note
        )


# -----------------------------
# Demo Setup
# -----------------------------

@dataclass
class Strategy:
    name: str
    description: str
    context_tags: List[str]
    confidence: float = 0.5
    usage_count: int = 0
    last_used_ts: Optional[float] = None
    fingerprint: str = field(init=False)

    def __post_init__(self):
        self.fingerprint = stable_hash(self.name)


@dataclass
class StrategyDecision:
    context_tags: List[str]
    considered: Dict[str, float]
    chosen_strategy: str
    ts: float
    notes: str


# -----------------------------
# Strategy Memory
# -----------------------------
