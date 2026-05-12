---
name: observability
description: Use observability MCP tools for logs and traces
always: true
---

# Observability Skill

You have access to observability MCP tools that query VictoriaLogs and VictoriaTraces.

## Available tools

- `mcp_obs_logs_search` — search logs using LogsQL queries
- `mcp_obs_logs_error_count` — count error-level logs per service over a time window
- `mcp_obs_traces_list` — list recent traces for a service
- `mcp_obs_traces_get` — get a specific trace by ID

## Strategy

- If the user asks about errors, system health, or failures, use `mcp_obs_logs_error_count` first to check for recent errors.
- If errors are found, use `mcp_obs_logs_search` to get detailed log entries and look for trace IDs.
- If a trace ID is found in the logs, use `mcp_obs_traces_get` to fetch the full trace and analyze the failure point.
- If the user asks for recent activity or traces without a specific ID, use `mcp_obs_traces_list` to show recent traces.
- When summarizing trace data, describe the span hierarchy and timing in plain language.
- Keep responses concise: summarize findings and only include relevant log/trace excerpts.

## Limits

You can only access logs and traces from the last 7 days (retention period). Use time-window filters to keep queries efficient.