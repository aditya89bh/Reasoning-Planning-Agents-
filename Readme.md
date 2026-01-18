# 🧠 Reasoning & Planning Agents  
_From Memory to Strategy_

This repository explores **reasoning and planning as first-class cognitive capabilities** in AI agents.

The focus is not on tool calling or prompt engineering, but on **how agents use past experience to decide what to do next**, how they break goals into executable steps, and how they avoid repeating mistakes over time.

These projects build directly on memory-agent foundations and move toward **deliberate, strategy-driven autonomy**.

---

## Why Reasoning & Planning Agents?

Most agents today:
- React to prompts
- Execute tasks in isolation
- Forget why something worked or failed
- Re-plan from scratch every time

Humans don’t work this way.

We:
- Reuse strategies
- Avoid known failures
- Break goals into manageable chunks
- Plan across time horizons
- Adjust behavior based on outcomes

This project set treats **reasoning and planning as cognitive systems**, not prompt patterns.

---

## Project Set Overview

### Project 1: Memory-Conditioned Planner  
**Core question**  
How should past outcomes shape future plans?

#### What this builds
- A planner that generates multiple candidate plans
- Each plan is scored using episodic memory
- Failures reduce future plan likelihood
- Success increases reuse probability

#### Key components
- Plan graph (steps and dependencies)
- Memory → plan score mapper
- Plan selection policy
- Execution trace logging

#### Why this matters
This is the first moment an agent **learns strategy**, not facts.

#### Non-toy upgrades
- Plan decay over time
- Confidence score per plan
- Plan fingerprints instead of raw text

---

### Project 2: Explicit Reasoning Loop Agent  
**Core question**  
Can an agent reason step-by-step without hallucinating forward?

#### What this builds
A structured reasoning loop:
1. Observe
2. Hypothesis generation
3. Evidence retrieval from memory
4. Reasoned conclusion
5. Action proposal

#### Key components
- Hypothesis memory
- Evidence linking
- Reasoning trace
- Contradiction detection

#### Why this matters
This is proto-thinking.  
Not chain-of-thought theater, but **controlled cognition**.

#### Non-toy upgrades
- Reject reasoning with weak evidence
- Force multiple competing hypotheses
- Store rejected conclusions

---

### Project 3: Goal Decomposition Planner  
**Core question**  
How does a long-term goal become executable steps?

#### What this builds
- High-level goal → subgoals → actions
- Dependency resolution
- Failure rollback
- Partial plan reuse

#### Key components
- Goal tree
- Subgoal memory
- Completion state tracker
- Retry logic

#### Why this matters
This is where agents stop being **task executors** and start being **operators**.

#### Non-toy upgrades
- Allow refusal of impossible goals
- Add time or resource constraints
- Store subgoal difficulty estimates

---

### Project 4: Strategy Selection Agent  
**Core question**  
Which strategy should I use in this situation?

#### What this builds
- Multiple strategy templates
- Context matching
- Strategy success scoring
- Strategy evolution over time

#### Key components
- Strategy memory
- Context embeddings
- Score updater
- Strategy retirement logic

#### Why this matters
Humans don’t plan from scratch.  
We reuse patterns. This agent does the same.

#### Non-toy upgrades
- Blend strategies
- Penalize overfitting
- Track strategy confidence

---

### Project 5: Failure-Aware Planner  
**Core question**  
How does an agent avoid repeating mistakes?

#### What this builds
- Failure taxonomy
- Failure → cause mapping
- Plan mutation based on failure type
- Preventive constraints

#### Key components
- Failure memory
- Causal tagging
- Constraint injector
- Retry policy

#### Why this matters
Most agents fail the same way forever.  
This one **learns from failure**.

#### Non-toy upgrades
- Separate execution failures vs reasoning failures
- Add recovery strategies
- Track near-misses

---

### Project 6: Long-Horizon Planning Agent  
**Core question**  
How does an agent think beyond the next step?

#### What this builds
- Multi-stage plans
- Intermediate checkpoints
- Drift detection
- Plan repair

#### Key components
- Plan horizon manager
- Checkpoint evaluator
- Drift detector
- Replanner

#### Why this matters
This is where **autonomy actually starts**.

#### Non-toy upgrades
- Allow agents to abandon goals
- Penalize excessive replanning
- Store horizon-length success statistics

---

## Design Philosophy

These projects emphasize:
- Explicit state and memory
- Traceable decisions
- Outcome-driven learning
- Separation of reasoning, planning, execution, and evaluation

No hidden magic.  
No agent frameworks doing the thinking for you.

---

## Intended Audience

This repository is for:
- Researchers exploring agent cognition
- Builders working on autonomous systems
- Designers thinking about AI behavior over time
- Anyone interested in **how intelligence compounds**

---

## Status

Work in progress.  
Each project is implemented incrementally and designed to stand alone while composing into a larger cognitive architecture.

---

## Big Picture

Memory answers: *What happened?*  
Reasoning answers: *Why did it happen?*  
Planning answers: *What should I do next?*

This repository is about **closing that loop**.
