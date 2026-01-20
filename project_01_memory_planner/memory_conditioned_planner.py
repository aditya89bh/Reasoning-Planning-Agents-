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

# -----------------------------
# Data models
# -----------------------------

@dataclass
class Plan:
    """
    Plan graph representation:
    - steps: ordered list of actions
    - deps: dependencies between steps represented as edges (i -> j) meaning step j depends on step i
      For simple linear plans, deps are (0->1, 1->2, ...)
    """
    goal: str
    context_tags: List[str]
    steps: List[str]
    deps: List[Tuple[int, int]]
    fingerprint: str

@dataclass
class EpisodicRecord:
    fingerprint: str
    goal: str
    context_tags: List[str]
    steps: List[str]
    outcome: str  # "success" | "failure" | "partial"
    score_delta: float
    confidence_after: float
    ts: float
    notes: str = ""

@dataclass
class PlanScoreBreakdown:
    base_confidence: float
    memory_evidence: float
    similarity: float
    recency_weight: float
    final_score: float


# -----------------------------
# Episodic Memory Store (JSONL)
# -----------------------------

class EpisodicMemory:
    """
    JSONL store of episodic outcomes keyed by plan fingerprint.
    Keeps an in-memory index for fast scoring.
    """

    def __init__(self, path: str):
        self.path = path
        ensure_dir(os.path.dirname(path) or ".")
        self.records: List[EpisodicRecord] = []
        # Stats per fingerprint
        self.confidence: Dict[str, float] = {}
        self.successes: Dict[str, int] = {}
        self.failures: Dict[str, int] = {}
        self.partials: Dict[str, int] = {}
        self.last_ts: Dict[str, float] = {}
        self.context_history: Dict[str, List[List[str]]] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            return
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                rec = EpisodicRecord(**obj)
                self.records.append(rec)
                self._index_record(rec)

    def _index_record(self, rec: EpisodicRecord) -> None:
        fp = rec.fingerprint
        self.confidence[fp] = rec.confidence_after
        self.last_ts[fp] = rec.ts
        self.context_history.setdefault(fp, []).append(rec.context_tags)

        if rec.outcome == "success":
            self.successes[fp] = self.successes.get(fp, 0) + 1
        elif rec.outcome == "failure":
            self.failures[fp] = self.failures.get(fp, 0) + 1
        else:
            self.partials[fp] = self.partials.get(fp, 0) + 1

    def append(self, rec: EpisodicRecord) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(rec), ensure_ascii=False) + "\n")
        self.records.append(rec)
        self._index_record(rec)

    def get_confidence(self, fingerprint: str, default: float = 0.5) -> float:
        return self.confidence.get(fingerprint, default)

    def get_stats(self, fingerprint: str) -> Dict[str, int]:
        return {
            "success": self.successes.get(fingerprint, 0),
            "failure": self.failures.get(fingerprint, 0),
            "partial": self.partials.get(fingerprint, 0),
        }

    def get_last_ts(self, fingerprint: str) -> Optional[float]:
        return self.last_ts.get(fingerprint)

    def get_context_history(self, fingerprint: str) -> List[List[str]]:
        return self.context_history.get(fingerprint, [])


# -----------------------------
# Planner: Generate → Score → Select
# -----------------------------

class MemoryConditionedPlanner:
    def __init__(
        self,
        memory: EpisodicMemory,
        decay_half_life_days: float = 14.0,   # plan decay over time
        epsilon: float = 0.15,               # exploration vs exploitation
        seed: int = 42,
    ):
        self.memory = memory
        self.decay_half_life_days = decay_half_life_days
        self.epsilon = epsilon
        random.seed(seed)

    # --- Plan generation ---

    def generate_candidate_plans(self, goal: str, context_tags: List[str]) -> List[Plan]:
        """
        Template-based plan generator (replace with LLM later if you want).
        Produces multiple variants to allow memory-informed selection.
        """
        goal_l = goal.lower().strip()

        # Minimal goal taxonomy for demo purposes
        templates: List[List[str]] = []

        if "debug" in goal_l or "fix" in goal_l:
            templates = [
                ["reproduce the issue", "isolate the failing component", "write a minimal test", "apply a fix", "verify with test suite", "document the change"],
                ["collect logs and error traces", "identify likely root cause", "confirm with a targeted experiment", "patch the bug", "add regression test"],
                ["simplify the scenario", "bisect recent changes", "pinpoint offending change", "fix and validate", "ship notes"],
            ]
        elif "plan" in goal_l or "roadmap" in goal_l:
            templates = [
                ["clarify objective and constraints", "break down into milestones", "estimate effort and risk", "sequence milestones", "define success metrics", "publish roadmap"],
                ["define goal and scope", "identify dependencies", "prioritize tasks", "create timeline", "set checkpoints"],
                ["write 1-page intent", "list deliverables", "rank by impact", "create a week-by-week plan", "review with stakeholders"],
            ]
        else:
            templates = [
                ["clarify the goal", "gather required inputs", "draft a plan", "execute steps", "review outcome", "log learnings"],
                ["define constraints", "generate options", "pick best option", "execute", "evaluate", "store outcome"],
                ["quick attempt", "inspect result", "iterate with improvements", "finalize", "document"],
            ]

        plans: List[Plan] = []
        for steps in templates:
            deps = [(i, i + 1) for i in range(len(steps) - 1)]  # linear dependencies
            fp = self.fingerprint_plan(goal, steps)
            plans.append(
                Plan(
                    goal=goal,
                    context_tags=context_tags,
                    steps=steps,
                    deps=deps,
                    fingerprint=fp,
                )
            )

        return plans

    def fingerprint_plan(self, goal: str, steps: List[str]) -> str:
        """
        Store fingerprints rather than raw text for stable memory retrieval.
        """
        norm_steps = [normalize_step(s) for s in steps]
        canonical = json.dumps({"goal": goal.strip().lower(), "steps": norm_steps}, sort_keys=True)
        return stable_hash(canonical)

    # --- Scoring ---

    def _recency_weight(self, last_ts: Optional[float]) -> float:
        """
        Exponential decay with half-life.
        weight = 0.5^(age/half_life)
        """
        if last_ts is None:
            return 0.0
        age_seconds = max(0.0, now_ts() - last_ts)
        age_days = age_seconds / (60 * 60 * 24)
        if self.decay_half_life_days <= 0:
            return 1.0
        return 0.5 ** (age_days / self.decay_half_life_days)

    def score_plan(self, plan: Plan) -> PlanScoreBreakdown:
        """
        Combine:
        - base confidence (per fingerprint)
        - memory evidence (success/failure balance)
        - context similarity to past contexts for this fingerprint
        - recency decay
        """
        fp = plan.fingerprint
        base_conf = self.memory.get_confidence(fp, default=0.5)
        stats = self.memory.get_stats(fp)

        # Evidence signal: + for successes, - for failures, small + for partials
        # Normalized to [-1, 1] roughly
        total = stats["success"] + stats["failure"] + stats["partial"]
        if total == 0:
            evidence = 0.0
        else:
            evidence = (stats["success"] - stats["failure"] + 0.25 * stats["partial"]) / max(1, total)

        # Context similarity: compare current context to average similarity of past contexts for same fingerprint
        ctx_hist = self.memory.get_context_history(fp)
        if not ctx_hist:
            similarity = 0.0
        else:
            sims = [jaccard_similarity(plan.context_tags, past) for past in ctx_hist]
            similarity = sum(sims) / len(sims)

        recency = self._recency_weight(self.memory.get_last_ts(fp))

        # Final score: weighted blend
        # You can tune these weights; they’re intentionally simple.
        final = (
            0.55 * base_conf +
            0.25 * evidence * (0.5 + 0.5 * similarity) +
            0.20 * recency
        )

        # Clamp to [0, 1]
        final = max(0.0, min(1.0, final))

        return PlanScoreBreakdown(
            base_confidence=base_conf,
            memory_evidence=evidence,
            similarity=similarity,
            recency_weight=recency,
            final_score=final,
        )

    # --- Selection policy ---

    def select_plan(self, plans: List[Plan]) -> Tuple[Plan, Dict[str, PlanScoreBreakdown]]:
        """
        Epsilon-greedy:
        - with probability epsilon, explore (random plan)
        - otherwise exploit (max score)
        """
        scored: Dict[str, PlanScoreBreakdown] = {}
        for p in plans:
            scored[p.fingerprint] = self.score_plan(p)

        if random.random() < self.epsilon:
            chosen = random.choice(plans)
            return chosen, scored

        chosen = max(plans, key=lambda p: scored[p.fingerprint].final_score)
        return chosen, scored


# -----------------------------
# Simulated Environment (for demo)
# -----------------------------

class SimulatedWorld:
    """
    Tiny environment so the agent has outcomes.
    You can replace this with real tasks, tools, robotics calls, etc.

    We simulate that different plan fingerprints have different true success probabilities
    depending on context tags.
    """

    def __init__(self, seed: int = 123):
        random.seed(seed)

    def run(self, plan: Plan) -> Tuple[str, str]:
        """
        Returns: (outcome, notes)
        outcome in {"success", "failure", "partial"}
        """
        # Base success chance derived from fingerprint to keep it stable-ish
        base = int(plan.fingerprint, 16) % 100
        p_success = 0.35 + (base / 100.0) * 0.30  # 0.35..0.65

        # Context effects
        ctx = set(plan.context_tags)
        if "high_stakes" in ctx:
            p_success -= 0.10
        if "known_domain" in ctx:
            p_success += 0.08
        if "time_pressure" in ctx:
            p_success -= 0.08
        if "well_scoped" in ctx:
            p_success += 0.06

        p_success = max(0.05, min(0.90, p_success))

        r = random.random()
        if r < p_success:
            return "success", f"Simulated success (p={p_success:.2f})."
        elif r < p_success + 0.20:
            return "partial", f"Simulated partial (p={p_success:.2f})."
        else:
            return "failure", f"Simulated failure (p={p_success:.2f})."


# -----------------------------
# Trace logger
# -----------------------------

class TraceLogger:
    def __init__(self, path: str):
        self.path = path
        ensure_dir(os.path.dirname(path) or ".")

    def log(self, trace: Dict) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace, ensure_ascii=False) + "\n")


# -----------------------------
# Learning rule: update confidence
# -----------------------------

def confidence_update(prev: float, outcome: str) -> Tuple[float, float]:
    """
    Returns (new_confidence, score_delta)

    Simple, interpretable rule:
    - success: +0.08
    - partial: +0.02
    - failure: -0.10
    Then clamp to [0.05, 0.95]
    """
    if outcome == "success":
        delta = 0.08
    elif outcome == "partial":
        delta = 0.02
    else:
        delta = -0.10

    new = max(0.05, min(0.95, prev + delta))
    return new, delta


# -----------------------------
# Main demo runner
# -----------------------------

def run_episode(
    planner: MemoryConditionedPlanner,
    world: SimulatedWorld,
    memory: EpisodicMemory,
    tracer: TraceLogger,
    goal: str,
    context_tags: List[str],
) -> Dict:
    plans = planner.generate_candidate_plans(goal, context_tags)
    chosen, scored = planner.select_plan(plans)

    outcome, notes = world.run(chosen)

    prev_conf = memory.get_confidence(chosen.fingerprint, default=0.5)
    new_conf, delta = confidence_update(prev_conf, outcome)

    # Write episodic record
    rec = EpisodicRecord(
        fingerprint=chosen.fingerprint,
        goal=goal,
        context_tags=context_tags,
        steps=chosen.steps,
        outcome=outcome,
        score_delta=delta,
        confidence_after=new_conf,
        ts=now_ts(),
        notes=notes,
    )
    memory.append(rec)

    # Trace
    trace = {
        "ts": rec.ts,
        "goal": goal,
        "context_tags": context_tags,
        "candidates": [
            {
                "fingerprint": p.fingerprint,
                "steps": p.steps,
                "score": scored[p.fingerprint].final_score,
                "score_breakdown": asdict(scored[p.fingerprint]),
            }
            for p in plans
        ],
        "chosen": {
            "fingerprint": chosen.fingerprint,
            "steps": chosen.steps,
            "deps": chosen.deps,
            "prev_conf": prev_conf,
            "new_conf": new_conf,
        },
        "outcome": outcome,
        "notes": notes,
    }
    tracer.log(trace)

    return trace


def pretty_print_trace(trace: Dict) -> None:
    print("\n" + "=" * 80)
    print(f"GOAL: {trace['goal']}")
    print(f"CONTEXT: {trace['context_tags']}")
    print("-" * 80)

    sorted_candidates = sorted(trace["candidates"], key=lambda c: c["score"], reverse=True)
    print("CANDIDATE PLANS (sorted by score):")
    for c in sorted_candidates:
        fp = c["fingerprint"]
        sc = c["score"]
        b = c["score_breakdown"]
        print(f"\n  - FP: {fp} | score={sc:.3f} | conf={b['base_confidence']:.3f} | evid={b['memory_evidence']:.3f} | sim={b['similarity']:.3f} | rec={b['recency_weight']:.3f}")
        for i, step in enumerate(c["steps"], 1):
            print(f"      {i}. {step}")

    ch = trace["chosen"]
    print("\n" + "-" * 80)
    print("CHOSEN PLAN:")
    print(f"  FP: {ch['fingerprint']}")
    print(f"  prev_conf={ch['prev_conf']:.3f} -> new_conf={ch['new_conf']:.3f}")
    for i, step in enumerate(ch["steps"], 1):
        print(f"    {i}. {step}")

    print("\nOUTCOME:", trace["outcome"])
    print("NOTES:", trace["notes"])
    print("=" * 80 + "\n")


if __name__ == "__main__":
    # Paths
    data_dir = "data"
    ensure_dir(data_dir)
    memory_path = os.path.join(data_dir, "episodic_memory.jsonl")
    trace_path = os.path.join(data_dir, "execution_traces.jsonl")

    # Components
    memory = EpisodicMemory(memory_path)
    tracer = TraceLogger(trace_path)
    world = SimulatedWorld(seed=123)
    planner = MemoryConditionedPlanner(
        memory=memory,
        decay_half_life_days=14.0,
        epsilon=0.15,
        seed=42,
    )

    # Demo episodes (edit these goals/contexts freely)
    episodes = [
        ("Debug failing unit test in memory scoring", ["known_domain", "well_scoped"]),
        ("Debug failing unit test in memory scoring", ["time_pressure", "high_stakes"]),
        ("Write a roadmap for reasoning + planning agent repo", ["known_domain"]),
        ("Write a roadmap for reasoning + planning agent repo", ["time_pressure"]),
        ("Fix intermittent API error in planner service", ["high_stakes"]),
        ("Fix intermittent API error in planner service", ["known_domain", "well_scoped"]),
    ]

    for goal, ctx in episodes:
        trace = run_episode(planner, world, memory, tracer, goal, ctx)
        pretty_print_trace(trace)

    print(f"Saved memory to: {memory_path}")
    print(f"Saved traces to: {trace_path}")
