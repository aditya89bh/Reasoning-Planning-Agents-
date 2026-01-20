# Project 01: Memory-Conditioned Planner

## Core Question
How should past outcomes shape future plans?

---

## Problem

Most agents generate plans in isolation.

They:
- ignore what worked before
- repeat known failures
- treat every task as a fresh problem

As a result, they **do not develop strategy**.  
They only execute.

---

## What This Project Builds

A planner that:
- generates multiple candidate plans
- scores each plan using episodic memory
- prefers plans that worked in similar contexts
- avoids plans associated with past failures

This introduces **experience-driven decision making**.

---
