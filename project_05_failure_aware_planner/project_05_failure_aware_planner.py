# ============================================
# Project 05: Failure-Aware Planner
# Full end-to-end minimal implementation
# ============================================

import time
import random
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
import json


# -----------------------------
# Data Models
# -----------------------------

@dataclass
class FailureRecord:
    action: str
    cause: str
    ts: float


@dataclass
class Plan:
    goal: str
    actions: List[str]
    constraints: List[str] = field(default_factory=list)


# -----------------------------
# Failure Memory
# -----------------------------

def classify_failure(action: str) -> str:
    if "auth" in action:
        return "missing_credentials"
    if "deploy" in action:
        return "environment_mismatch"
    if "test" in action:
        return "incomplete_coverage"
    return "unknown_failure"


# -----------------------------
# Planner with Mutation
# -----------------------------

class FailureAwarePlanner:
    def __init__(self, failure_memory: FailureMemory):
        self.failure_memory = failure_memory

    def generate_plan(self, goal: str) -> Plan:
        # Base naive plan
        actions = [
            "check_logs",
            "fix_auth_issue",
            "deploy_fix",
            "run_tests"
        ]
        return Plan(goal=goal, actions=actions)

    def mutate_plan(self, plan: Plan) -> Plan:
        mutated = []
        constraints = list(plan.constraints)

        for a in plan.actions:
            if self.failure_memory.has_failed(a):
                constraints.append(f"avoid:{a}")
                # Replace with safer alternative
                mutated.append(f"review_{a}")
            else:
                mutated.append(a)

        return Plan(
            goal=plan.goal,
            actions=mutated,
            constraints=constraints
        )


# -----------------------------
# Execution Simulator
# -----------------------------


