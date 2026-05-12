"""Typed response models for the observability MCP server."""

from pydantic import BaseModel


class LogEntry(BaseModel):
    timestamp: str = ""
    level: str = ""
    service: str = ""
    event: str = ""
    message: str = ""
    trace_id: str = ""


class ErrorCount(BaseModel):
    service: str
    error_count: int
    window: str


class TraceSpan(BaseModel):
    span_id: str = ""
    operation: str = ""
    service: str = ""
    duration_ms: float = 0.0
    status: str = ""
    error: str = ""


class TraceSummary(BaseModel):
    trace_id: str
    service: str = ""
    operation: str = ""
    span_count: int = 0
    error_count: int = 0
    duration_ms: float = 0.0


class TraceDetail(BaseModel):
    trace_id: str
    spans: list[TraceSpan] = []
