---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to LMS MCP tools that query the Learning Management System backend.

## Available tools

- `lms_health` — check backend health and get item count
- `lms_labs` — list all available labs with their IDs and titles
- `lms_learners` — list learner submissions for a specific lab
- `lms_pass_rates` — get pass rates per lab (requires lab_id)
- `lms_timeline` — submission timeline data for a lab (requires lab_id)
- `lms_groups` — group performance data for a lab (requires lab_id)
- `lms_top_learners` — top learners for a lab (requires lab_id, optional limit)
- `lms_completion_rate` — completion rate for a lab (requires lab_id)
- `lms_sync_pipeline` — trigger data sync from autochecker

## Strategy

- If the user asks for scores, pass rates, completion, groups, timeline, or top learners without naming a lab, call `lms_labs` first to discover available labs.
- If multiple labs are available, ask the user to choose one before proceeding.
- Use each lab's title as the user-facing label.
- When a lab_id parameter is required and not provided, ask the user which lab.
- Format numeric results nicely: percentages as "XX.X%", counts as whole numbers.
- For health checks, call `lms_health` and report the item count and backend status.
- Keep responses concise and structured.

## Limits

You can only answer questions about data that exists in the LMS backend. If no data exists yet, suggest running `lms_sync_pipeline` to trigger a sync first.