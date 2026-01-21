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
