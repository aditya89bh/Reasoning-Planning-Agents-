# Project 06: Long-Horizon Planning Agent

## Core Question
**How does an agent pursue a goal across time without losing direction?**

---

## Problem

Most agents operate in short, isolated episodes.

They can:
- reason correctly
- plan individual tasks
- select strategies
- adapt after failures

Yet they still fail at **long-term autonomy**.

They:
- lose sight of the original goal
- replan too often or not at all
- fail to detect drift
- persist with failing objectives indefinitely

Humans don’t work this way.

We:
- commit to long-term goals
- periodically check progress
- notice when we are off track
- adapt strategy or abandon goals when necessary

This project gives agents those capabilities.

---

## What This Project Builds

A long-horizon planning layer that enables an agent to:

- maintain persistent goals over time
- track incremental progress
- evaluate progress against explicit checkpoints
- detect drift from expectations
- trigger deliberate replanning
- abandon goals when confidence collapses

This is the final step toward **true autonomy**.

---

## Key Components

### 1. Goal State
A long-lived representation of intent that includes:
- goal description
- confidence level
- progress estimate
- active or abandoned status
- execution history

The goal persists across multiple planning cycles.

---

### 2. Checkpoints
Explicit milestones that define:
- expected progress thresholds
- semantic meaning (not just time-based)

Checkpoints anchor long-term intent and make drift measurable.

---

### 3. Progress Tracking
The agent updates progress incrementally over time.
Progress is treated as a continuous signal, not a binary outcome.

This enables nuanced evaluation rather than pass/fail logic.

---

### 4. Drift Detection
At each checkpoint, the agent evaluates:
- “Am I where I expected to be by now?”

If actual progress falls outside acceptable bounds,
the agent detects **drift**.

---

### 5. Replanning Logic
When drift is detected:
- the agent reduces confidence in the current plan
- replanning is triggered intentionally
- the event is logged in execution history

Replanning is controlled, not reactive.

---

### 6. Goal Abandonment
If confidence drops below a critical threshold:
- the goal is deactivated
- further execution is halted

Abandonment is treated as an intelligent outcome,
not a failure.

---

## Why This Matters

This project introduces a defining property of intelligence:

> **Knowing when to persist, adapt, or stop.**

Without long-horizon planning:
- autonomy is brittle
- agents over-optimize short-term signals
- systems spiral under uncertainty

With it:
- goals remain coherent over time
- effort is allocated intelligently
- failure is contained rather than compounded

---

## Relationship to Other Projects

- **Project 01:** Learning from past outcomes
- **Project 02:** Evidence-grounded reasoning
- **Project 03:** Goal decomposition and structure
- **Project 04:** Strategy selection
- **Project 05:** Failure-aware adaptation
- **Project 06:** Long-horizon persistence and control

Together, these form a complete cognitive architecture for agents.

---

## Mental Model

> Short-horizon agents act.  
> Long-horizon agents commit, monitor, and adapt.

This project enables commitment.

---

## Success Criteria

The agent should:
- maintain goals across multiple checkpoints
- detect drift reliably
- replan deliberately
- abandon goals when confidence collapses

If this works, the agent demonstrates **autonomy**, not scripted behavior.
