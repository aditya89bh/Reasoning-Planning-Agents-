# Project 05: Failure-Aware Planner

## Core Question
**How does an agent avoid repeating the same mistakes?**

---

## Problem

Most agents fail in a loop:

fail → retry → fail → retry → fail

They may reason correctly, plan well, and even choose the right strategy,
but once something goes wrong, they often:
- repeat the same failed actions
- retry blindly without adaptation
- lack an explicit memory of *why* something failed

Humans don’t work this way.

We say:
- “That failed because of X”
- “Don’t do that again”
- “Try a safer alternative”

This project gives agents that capability.

---

## What This Project Builds

A planner that can:

- detect execution failures
- classify *why* an action failed
- store failures as first-class memory
- mutate future plans to avoid known failures
- inject preventive constraints automatically

The agent learns not just *what worked*,  
but more importantly, *what should not be repeated*.

---

## Key Components

### 1. Failure Record
Each failure captures:
- the action that failed
- the cause of failure
- a timestamp

Failures are explicit data, not implicit signals.

---

### 2. Failure Memory
A persistent store that:
- tracks failed actions
- aggregates failure causes
- allows fast checks like “has this failed before?”

This enables experience-based avoidance.

---

### 3. Failure Taxonomy
Failures are categorized into meaningful causes such as:
- missing credentials
- environment mismatch
- incomplete testing
- unknown failure

This allows different recovery behaviors per failure type.

---

### 4. Plan Mutation Logic
When generating a new plan:
- actions that failed before are detected
- constraints like `avoid:<action>` are injected
- unsafe actions are replaced with safer alternatives

The agent does not retry blindly.
It **adapts the plan**.

---

### 5. Preventive Constraints
Constraints are added automatically to future plans, such as:
- avoiding specific actions
- forcing review steps
- preferring conservative variants

Constraints shape future behavior without hardcoding logic.

---

### 6. Execution Simulator
A simulated executor:
- introduces stochastic failures
- allows testing failure-handling logic
- validates that repeated failures are avoided

This keeps learning realistic.

---

## Why This Matters

This project introduces a critical property of intelligence:

> **An intelligent system does not fail the same way twice.**

With failure awareness:
- learning accelerates
- behavior stabilizes
- catastrophic loops are avoided
- trust in autonomy increases

This is essential for real-world agents.

---

## Relationship to Other Projects

- **Project 02:** Prevents bad reasoning
- **Project 03:** Prevents bad planning
- **Project 04:** Prevents bad strategy choice
- **Project 05:** Prevents repeated execution mistakes

Together, these form a robust decision-making stack.

---

## Mental Model

> A junior agent retries.  
> A senior agent adapts.

This project turns retrying into adapting.

---

## Success Criteria

The agent should:
- record execution failures explicitly
- attribute failures to meaningful causes
- mutate future plans to avoid known failures
- inject preventive constraints automatically

If this works, the agent demonstrates **experience-based learning**, not trial-and-error.

---

## Next Step

The next layer is **Project 06: Long-Horizon Planning**, where the agent:
- maintains goals across time
- detects drift
- replans intelligently over long sequences

Failure-aware planning is a prerequisite for long-horizon autonomy.
