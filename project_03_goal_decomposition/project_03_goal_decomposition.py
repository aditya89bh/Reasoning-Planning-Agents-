# ============================================
# Project 03: Goal Decomposition Planner
# Full end-to-end minimal implementation
# Colab + local friendly (single-cell runnable)
# ============================================

from __future__ import annotations

import json
import time
import hashlib
import random
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional, Tuple, Set


# -----------------------------
# Utilities
# -----------------------------

def now_ts() -> float:
    return time.time()

def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())

def fingerprint_goal(goal: str, constraints: Optional[Dict] = None) -> str:
    canonical = json.dumps(
        {"goal": normalize(goal), "constraints": constraints or {}},
        sort_keys=True
    )
    return stable_hash(canonical)

# -----------------------------
# Data Models
# -----------------------------

@dataclass
class GoalSpec:
    goal: str
    context_tags: List[str] = field(default_factory=list)
    constraints: Dict = field(default_factory=dict)  # e.g., {"time_budget_steps": 12, "resource_budget": 10}
    allow_refusal: bool = True

@dataclass
class DecompositionResult:
    goal_id: str
    goal: str
    subgoals: List[str]
    actions: Dict[str, List[str]]              # subgoal -> list of actions
    deps: List[Tuple[str, str]]                # (A -> B) means B depends on A (subgoals only)
    execution_order: List[str]                 # subgoals sorted by dependencies
    notes: str
    ts: float

@dataclass
class ExecutionState:
    goal_id: str
    subgoal_status: Dict[str, str]             # "pending"|"done"|"failed"|"skipped"
    action_status: Dict[str, List[Tuple[str, str]]]  # subgoal -> list of (action, status)
    rollback_log: List[str]
    ts: float

# -----------------------------
# Goal Decomposer
# -----------------------------

class GoalDecomposer:
    """
    Converts high-level goals into subgoals + action lists + dependencies.
    Includes:
    - refusal for impossible goals (rule-based)
    - time/resource constraints (lightweight)
    - partial plan reuse (cache by fingerprint)
    """

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.cache: Dict[str, DecompositionResult] = {}  # goal_id -> decomposition

    def decompose(self, spec: GoalSpec) -> DecompositionResult:
        goal_id = fingerprint_goal(spec.goal, spec.constraints)

        # Partial plan reuse
        if goal_id in self.cache:
            cached = self.cache[goal_id]
            return DecompositionResult(
                goal_id=cached.goal_id,
                goal=cached.goal,
                subgoals=cached.subgoals,
                actions=cached.actions,
                deps=cached.deps,
                execution_order=cached.execution_order,
                notes=cached.notes + " | reused_from_cache=true",
                ts=now_ts()
            )

        # Refusal logic (simple but useful)
        impossible_reason = self._detect_impossible_goal(spec.goal, spec.constraints)
        if impossible_reason and spec.allow_refusal:
            raise ValueError(f"Goal refused: {impossible_reason}")

        # Create subgoals + actions
        subgoals, actions, deps, notes = self._rule_based_decomposition(spec)

        # Apply constraints (lightweight)
        subgoals, actions, deps, notes = self._apply_constraints(
            spec, subgoals, actions, deps, notes
        )

        # Dependency resolution
        order = self._toposort_subgoals(subgoals, deps)

        result = DecompositionResult(
            goal_id=goal_id,
            goal=spec.goal,
            subgoals=subgoals,
            actions=actions,
            deps=deps,
            execution_order=order,
            notes=notes,
            ts=now_ts()
        )

        self.cache[goal_id] = result
        return result

    def _detect_impossible_goal(self, goal: str, constraints: Dict) -> Optional[str]:
        g = normalize(goal)
        # Very simple refusal rules; upgrade later.
        if "teleport" in g or "time travel" in g:
            return "Contains physically impossible requirement."
        if "guarantee" in g and "zero risk" in g:
            return "Cannot guarantee zero risk."
        # If hard constraints are impossibly tight
        if "time_budget_steps" in constraints and constraints["time_budget_steps"] <= 1:
            return "Time budget too small to decompose into executable steps."
        return None

    def _rule_based_decomposition(self, spec: GoalSpec):
        g = normalize(spec.goal)
        tags = set(spec.context_tags)

        # Default skeleton
        subgoals: List[str] = []
        actions: Dict[str, List[str]] = {}
        deps: List[Tuple[str, str]] = []
        notes = "rule_based=true"

        if any(k in g for k in ["demo", "pitch", "investor"]):
            subgoals = [
                "clarify_goal_and_success_metrics",
                "create_storyline",
                "build_demo_flow",
                "prepare_assets",
                "rehearse_and_iterate"
            ]
            actions = {
                "clarify_goal_and_success_metrics": [
                    "write one-sentence demo objective",
                    "define what success looks like",
                    "list constraints and assumptions"
                ],
                "create_storyline": [
                    "draft narrative arc (problem → insight → solution)",
                    "write 3 key takeaways",
                    "prepare 30-second opener"
                ],
                "build_demo_flow": [
                    "outline demo steps end-to-end",
                    "identify risky steps and add fallbacks",
                    "create a timed run sheet"
                ],
                "prepare_assets": [
                    "prepare slides or visuals",
                    "prepare backup screenshots/video",
                    "set up environment and dependencies"
                ],
                "rehearse_and_iterate": [
                    "run 2 full rehearsals",
                    "capture issues and fix top 3",
                    "final timed rehearsal"
                ],
            }
            deps = [
                ("clarify_goal_and_success_metrics", "create_storyline"),
                ("create_storyline", "build_demo_flow"),
                ("build_demo_flow", "prepare_assets"),
                ("prepare_assets", "rehearse_and_iterate"),
            ]
        elif any(k in g for k in ["blog", "article", "post", "write"]):
            subgoals = [
                "choose_topic_and_angle",
                "gather_evidence",
                "outline_structure",
                "draft_content",
                "edit_and_publish"
            ]
            actions = {
                "choose_topic_and_angle": [
                    "pick core insight",
                    "define target reader",
                    "write hook idea"
                ],
                "gather_evidence": [
                    "pull notes/examples",
                    "list 3 supporting points",
                    "collect 1 counterpoint"
                ],
                "outline_structure": [
                    "create headings",
                    "map examples to headings",
                    "write conclusion bullet points"
                ],
                "draft_content": [
                    "write first draft quickly",
                    "insert examples",
                    "add transitions"
                ],
                "edit_and_publish": [
                    "tighten and remove fluff",
                    "add final CTA",
                    "publish and share"
                ],
            }
            deps = [
                ("choose_topic_and_angle", "gather_evidence"),
                ("gather_evidence", "outline_structure"),
                ("outline_structure", "draft_content"),
                ("draft_content", "edit_and_publish"),
            ]
        else:
            # Generic decomposition
            subgoals = [
                "clarify_intent",
                "break_into_subtasks",
                "sequence_and_dependencies",
                "execute",
                "review_and_log"
            ]
            actions = {
                "clarify_intent": [
                    "write goal in one sentence",
                    "list constraints",
                    "define completion criteria"
                ],
                "break_into_subtasks": [
                    "list 5-10 subtasks",
                    "identify unknowns",
                    "estimate difficulty"
                ],
                "sequence_and_dependencies": [
                    "order subtasks",
                    "identify prerequisites",
                    "create fallback options"
                ],
                "execute": [
                    "start with highest-leverage task",
                    "track progress",
                    "handle blockers"
                ],
                "review_and_log": [
                    "summarize outcome",
                    "note what worked/failed",
                    "store reusable template"
                ],
            }
            deps = [
                ("clarify_intent", "break_into_subtasks"),
                ("break_into_subtasks", "sequence_and_dependencies"),
                ("sequence_and_dependencies", "execute"),
                ("execute", "review_and_log"),
            ]

        # Context-based tweaks (simple)
        if "time_pressure" in tags:
            notes += " | time_pressure=true"
            # Add faster actions or reduce depth
            if "rehearse_and_iterate" in actions:
                actions["rehearse_and_iterate"] = [
                    "run 1 rehearsal",
                    "fix top 2 issues",
                    "final timed run"
                ]
        if "high_stakes" in tags:
            notes += " | high_stakes=true"
            # Encourage backups / fallbacks
            if "prepare_assets" in actions:
                actions["prepare_assets"].append("prepare failure fallback plan")

        return subgoals, actions, deps, notes

    def _apply_constraints(self, spec: GoalSpec, subgoals, actions, deps, notes):
        # time_budget_steps: maximum number of total actions allowed
        tb = spec.constraints.get("time_budget_steps")
        if tb is not None:
            all_actions = [(sg, a) for sg in subgoals for a in actions.get(sg, [])]
            if len(all_actions) > tb:
                notes += f" | time_budget_steps={tb} applied"
                # Trim actions from the end (simple)
                keep = all_actions[:tb]
                new_actions = {sg: [] for sg in subgoals}
                for sg, a in keep:
                    new_actions[sg].append(a)
                actions = new_actions

        # resource_budget: pretend each subgoal costs 1, and each action costs 1
        rb = spec.constraints.get("resource_budget")
        if rb is not None:
            cost = len(subgoals) + sum(len(actions.get(sg, [])) for sg in subgoals)
            if cost > rb:
                notes += f" | resource_budget={rb} applied"
                # Drop the last subgoal(s) until within budget (simple)
                while subgoals and (len(subgoals) + sum(len(actions.get(sg, [])) for sg in subgoals)) > rb:
                    removed = subgoals.pop()
                    actions.pop(removed, None)
                    deps = [(a, b) for (a, b) in deps if a != removed and b != removed]

        return subgoals, actions, deps, notes

    def _toposort_subgoals(self, subgoals: List[str], deps: List[Tuple[str, str]]) -> List[str]:
        # Kahn’s algorithm
        indeg = {s: 0 for s in subgoals}
        adj = {s: [] for s in subgoals}

        for a, b in deps:
            if a in adj and b in indeg:
                adj[a].append(b)
                indeg[b] += 1

        q = [s for s in subgoals if indeg[s] == 0]
        order = []

        while q:
            n = q.pop(0)
            order.append(n)
            for nxt in adj.get(n, []):
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    q.append(nxt)

        # If cycle (shouldn't happen here), fallback to input order
        if len(order) != len(subgoals):
            return subgoals
        return order


# -----------------------------
# Execution Simulator (Rollback)
# -----------------------------

class Executor:
    """
    Simulates executing actions.
    Supports:
    - completion tracking
    - failure rollback at subgoal level
    """

    def __init__(self, seed: int = 7, fail_rate: float = 0.12):
        random.seed(seed)
        self.fail_rate = fail_rate

    def execute(self, plan: DecompositionResult) -> ExecutionState:
        subgoal_status = {sg: "pending" for sg in plan.execution_order}
        action_status = {sg: [] for sg in plan.execution_order}
        rollback_log: List[str] = []

        for sg in plan.execution_order:
            # execute all actions for this subgoal
            failed = False
            for action in plan.actions.get(sg, []):
                if random.random() < self.fail_rate:
                    action_status[sg].append((action, "failed"))
                    failed = True
                    break
                else:
                    action_status[sg].append((action, "done"))

            if failed:
                subgoal_status[sg] = "failed"
                # rollback: mark remaining subgoals as skipped
                rollback_log.append(f"rollback_triggered_at={sg}")
                for rest in plan.execution_order[plan.execution_order.index(sg)+1:]:
                    subgoal_status[rest] = "skipped"
                break
            else:
                subgoal_status[sg] = "done"

        return ExecutionState(
            goal_id=plan.goal_id,
            subgoal_status=subgoal_status,
            action_status=action_status,
            rollback_log=rollback_log,
            ts=now_ts()
        )

# -----------------------------
# Pretty Printing
# -----------------------------

def print_plan(plan: DecompositionResult):
    print("\n" + "="*90)
    print("PROJECT 03: GOAL DECOMPOSITION PLANNER")
    print("-"*90)
    print(f"GOAL: {plan.goal}")
    print(f"GOAL_ID: {plan.goal_id}")
    print(f"NOTES: {plan.notes}")
    print(f"TIMESTAMP: {plan.ts}")
    print("-"*90)

    print("SUBGOALS:")
    for i, sg in enumerate(plan.subgoals, 1):
        print(f"  {i}. {sg}")

    print("\nDEPENDENCIES (A -> B means B depends on A):")
    if not plan.deps:
        print("  (none)")
    else:
        for a, b in plan.deps:
            print(f"  {a} -> {b}")

    print("\nEXECUTION ORDER:")
    for i, sg in enumerate(plan.execution_order, 1):
        print(f"  {i}. {sg}")

    print("\nACTIONS PER SUBGOAL:")
    for sg in plan.execution_order:
        acts = plan.actions.get(sg, [])
        print(f"  - {sg}:")
        if not acts:
            print("      (no actions - trimmed by constraints)")
        for j, a in enumerate(acts, 1):
            print(f"      {j}. {a}")

    print("="*90 + "\n")


def print_execution(state: ExecutionState):
    print("\n" + "-"*90)
    print("EXECUTION RESULT")
    print("-"*90)
    for sg, st in state.subgoal_status.items():
        print(f"{sg}: {st}")
        for action, ast in state.action_status.get(sg, []):
            print(f"   - {ast}: {action}")
    if state.rollback_log:
        print("\nROLLBACK LOG:")
        for x in state.rollback_log:
            print(" ", x)
    print("-"*90 + "\n")


# -----------------------------
# Demo Runner
# -----------------------------

if __name__ == "__main__":
    decomposer = GoalDecomposer(seed=42)
    executor = Executor(seed=7, fail_rate=0.15)

    # Choose a goal example; edit freely
    spec = GoalSpec(
        goal="Prepare an investor demo for a robotics product",
        context_tags=["high_stakes", "time_pressure"],
        constraints={"time_budget_steps": 12, "resource_budget": 18},
        allow_refusal=True
    )

    try:
        plan = decomposer.decompose(spec)
        print_plan(plan)

        # Run execution simulation (for rollback + tracking)
        state = executor.execute(plan)
        print_execution(state)

        # Demonstrate partial reuse: run decomposition again (should reuse from cache)
        plan2 = decomposer.decompose(spec)
        print("Re-run decomposition (cache reuse):", plan2.notes)

    except ValueError as e:
        print("REFUSED:", str(e))





