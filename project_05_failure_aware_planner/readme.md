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
