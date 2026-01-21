# ============================================
# Project 02: Explicit Reasoning Loop Agent
# Full end-to-end minimal implementation
# ============================================

import json
import os
import time
import hashlib
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import random

# ---------- Utilities ----------

def now_ts():
    return time.time()

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())

def jaccard(a: List[str], b: List[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

# ---------- Data Models ----------

@dataclass
class Observation:
    question: str
    context_tags: List[str]

@dataclass
class Hypothesis:
    hypothesis: str
    fingerprint: str

@dataclass
class Evidence:
    content: str
    tags: List[str]
    fingerprint: str

@dataclass
class ReasoningTrace:
    observation: Observation
    hypotheses: List[str]
    evidence_used: Dict[str, List[str]]
    conclusion: Optional[str]
    action: Optional[str]
    rejected_hypotheses: List[str]
    notes: str

# ---------- Evidence Store ----------

class EvidenceStore:
    def __init__(self):
        self.evidence = []

    def add(self, content: str, tags: List[str]):
        fp = stable_hash(normalize(content))
        self.evidence.append(Evidence(content, tags, fp))

    def retrieve(self, tags: List[str], top_k=3):
        scored = []
        for e in self.evidence:
            score = jaccard(tags, e.tags)
            if score > 0:
                scored.append((score, e))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [e for _, e in scored[:top_k]]

# ---------- Hypothesis Memory ----------

class HypothesisMemory:
    def __init__(self):
        self.rejected = {}

    def reject(self, hypothesis: str, reason: str):
        self.rejected[hypothesis] = reason

# ---------- Reasoning Agent ----------

class ExplicitReasoningAgent:
    def __init__(self, evidence_store, hypothesis_memory):
        self.evidence_store = evidence_store
        self.hypothesis_memory = hypothesis_memory

    def observe(self, question, context_tags):
        return Observation(question, context_tags)

    def generate_hypotheses(self, observation):
        q = observation.question.lower()
        if "api" in q:
            return [
                "The API is failing due to authentication issues",
                "The API is failing due to rate limiting",
                "The API is failing due to a server-side bug"
            ]
        return [
            "The issue is due to missing information",
            "The issue is due to incorrect assumptions"
        ]

    def reason(self, observation: Observation):
        hypotheses = self.generate_hypotheses(observation)
        evidence_used = {}
        rejected = []
        accepted = None

        for h in hypotheses:
            ev = self.evidence_store.retrieve(
                observation.context_tags + h.split()[:2]
            )

            if len(ev) < 1:
                self.hypothesis_memory.reject(h, "No supporting evidence")
                rejected.append(h)
                continue

            evidence_used[h] = [e.content for e in ev]
            accepted = h
            break

        action = None
        if accepted:
            action = f"Investigate: {accepted}"

        trace = ReasoningTrace(
            observation=observation,
            hypotheses=hypotheses,
            evidence_used=evidence_used,
            conclusion=accepted,
            action=action,
            rejected_hypotheses=rejected,
            notes="Accepted first hypothesis with sufficient evidence"
        )

        return trace
