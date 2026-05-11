# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Q: What is the agentic loop?**

```
The agentic loop is the recurring cycle that lets an autonomous software agent
(or AI system) perceive, think, act, and learn from its own actions. It can be
broken down into four steps:

 1 Perception / Observation – Gather information from the environment (e.g.,
   read files, call APIs, receive user input, read sensors).
 2 Reasoning / Planning – Process the observations, update internal state, and
   decide on the next action (via prompting, symbolic reasoning, planning
   algorithms, policies, etc.).
 3 Action / Execution – Carry out the chosen operation that changes the
   environment (write files, send commands, make HTTP requests, schedule jobs,
   invoke tools, etc.).
 4 Feedback / Evaluation – Observe the outcome of the action, check success or
   error signals, and assess progress toward the goal.

After the feedback step the loop starts again with a new perception step, using
the updated knowledge to refine future decisions.

Why it's important
 • Autonomy: Repeating this cycle lets an agent operate with little human
   supervision.
 • Adaptivity: Feedback lets the agent correct mistakes and adjust to changing
   conditions.
 • Goal-directed behavior: Planning ensures actions are purposeful rather than
   random.

Variants
 • Reactive loops: Skip explicit planning and act directly on observations
   (simple rule-based bots).
 • Hierarchical loops: Higher-level loops set sub-goals for lower-level loops
   (common in robotics).
 • Learning loops: Incorporate model updates (e.g., reinforcement learning)
   during the feedback stage.
```

## Task 1B — Agent with LMS tools

**Q: What labs are available?**

```
Available labs

 #  Title
 ──────────────────────────────────────────────────────────
 1  Lab 01 – Products, Architecture & Roles
 2  Lab 02 — Run, Fix, and Deploy a Backend Service
 3  Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4  Lab 04 — Testing, Front‑end, and AI Agents
 5  Lab 05 — Data Pipeline and Analytics Dashboard
 6  Lab 06 — Build Your Own Agent
 7  Lab 07 — Build a Client with an AI Coding Agent
 8  lab‑08

Let me know if you’d like details about any specific lab!
```

**Q: Is the LMS backend healthy?**

```
The LMS backend is healthy, and it currently holds **56 items**.
```

## Task 1C — Skill prompt

**Q: Show me the scores** (without specifying a lab)

```
I can pull the scores for a specific lab, but I need to know which one you'd
like to see. Here are the available labs:

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 — Run, Fix, and Deploy a Backend Service
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4 Lab 04 — Testing, Front‑end, and AI Agents
 5 Lab 05 — Data Pipeline and Analytics Dashboard
 6 Lab 06 — Build Your Own Agent
 7 Lab 07 — Build a Client with an AI Coding Agent
 8 lab‑08

Which lab's scores would you like to view?
```

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
