"""HTTP client for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

import json
from typing import Any

from httpx import AsyncClient, Response


class ObservabilityClient:
    """Client for VictoriaLogs and VictoriaTraces HTTP APIs."""

    def __init__(self, victorialogs_url: str, victortraces_url: str) -> None:
        self.victorialogs_url = victorialogs_url.rstrip("/")
        self.victortraces_url = victortraces_url.rstrip("/")
        self._client: AsyncClient | None = None

    async def __aenter__(self) -> ObservabilityClient:
        self._client = AsyncClient()
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._client is not None:
            await self._client.aclose()

    async def logs_search(self, query: String, limit: int = 100, start: String | None = None, end: String | None = None) -> Response:
        """Search logs using LogsQL query.
        
        Args:
            query: LogsQL query string
            limit: Maximum number of log entries to return
            start: Start time filter (LogsQL format, e.g., "1h" or "2024-01-01T00:00:00Z")
            end: End time filter
        
        Returns:
            HTTP response with JSON logs
        """
        params = {"query": query, "limit": str(limit)}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        return await self._client.get(
            f"{self.victorialogs_url}/select/logsql/query",
            params=params,
        )

    async def logs_error_count(self, service: String | None = None, time_window: String = "1h") -> Response:
        """Count error-level logs per service over a time window.
        
        Args:
            service: Optional service name to filter (e.g., "Learning Management Service")
            time_window: Time window string like "1h", "10m", "24h"
        
        Returns:
            HTTP response with error count summary
        """
        query = f"{time_window} severity:ERROR"
        if service:
            query = f"{query} service.name:{service}"
        params = {"query": query, "limit": "1000"}  # Get enough to count
        return await self._client.get(
            f"{self.victorialogs_url}/select/logsql/query",
            params=params,
        )

    async def traces_list(self, service: String | None = None, limit: int = 100) -> Response:
        """List recent traces for a service.
        
        Args:
            service: Service name (e.g., "Learning Management Service")
            limit: Maximum number of traces to return
        
        Returns:
            HTTP response with trace data
        """
        params = {"service": service, "limit": str(limit)}
        return await self._client.get(
            f"{self.victortraces_url}/select/jaeger/api/traces",
            params=params,
        )

    async def traces_get(self, trace_id: String) -> Response:
        """Get a specific trace by ID.
        
        Args:
            trace_id: Trace identifier
        
        Returns:
            HTTP response with trace details
        """
        return await self._client.get(
            f"{self.victortraces_url}/select/jaeger/api/traces/{trace_id}",
        )