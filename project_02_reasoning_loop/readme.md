# Project 02: Explicit Reasoning Loop Agent

## Core Question
Can an agent reason step-by-step without hallucinating forward?

---

## Problem

Most “reasoning agents” today either:
- produce an answer immediately (uncontrolled)
- generate verbose chain-of-thought (hard to trust and hard to audit)
- hallucinate evidence because nothing forces grounding

What’s missing is a **controlled reasoning loop** where each step must be backed by evidence.

---

## What This Project Builds

A structured reasoning loop that enforces:

1. **Observe**
2. **Generate hypotheses**
3. **Retrieve evidence from memory**
4. **Reason to a conclusion**
5. **Propose an action**
6. **Trace everything**
7. **Detect contradictions**
8. **Store rejected hypotheses**

This creates proto-thinking that is:
- explicit
- auditable
- evidence-linked
- self-correcting (to a point)

---

## Key Components

### 1. Observation
A structured input describing:
- goal / question
- context tags
- constraints
- known facts (if any)

### 2. Hypothesis Memory
A store of:
- hypotheses generated for similar situations
- which ones were accepted or rejected
- confidence and timestamps

### 3. Evidence Store
A store of “evidence snippets” from:
- past episodes
- curated facts
- tool outputs (later)
- human notes (later)

### 4. Evidence Linking
Each reasoning step must link to:
- at least 1 evidence item
- a similarity score or match rationale

### 5. Reasoning Trace
A complete trace of:
- hypotheses considered
- evidence retrieved
- reasoning steps
- rejection reasons
- contradiction flags
- final conclusion + action proposal

### 6. Contradiction Detection
Detects when:
- the conclusion conflicts with known facts
- the reasoning contains a direct negation conflict

---

