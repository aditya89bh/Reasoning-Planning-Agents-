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
