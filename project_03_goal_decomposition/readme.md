# Project 03: Goal Decomposition Planner

## Core Question
How does a high-level goal become executable steps?

---

## Problem

Most agents fail not because they cannot act,
but because they cannot **structure intent**.

They either:
- jump directly to actions
- generate shallow task lists
- fail to track dependencies
- restart from scratch after failure

What’s missing is a **goal decomposition layer**.

---

## What This Project Builds

A system that converts:

High-level goal  
→ structured subgoals  
→ executable actions  

with:
- dependency tracking
- partial reuse
- rollback on failure

---

## Key Components

- Goal node (intent)
- Subgoal tree
- Action nodes
- Dependency resolution
- Completion state tracking

---
