"""
status.py

This module collects current system status information:
- CPU usage
- RAM usage
- timestamp

It is used by:
- web_server.py for GET /api/status
- csv_logger.py for writing log.csv file
- tcp_server.py for streaming status data
"""

from datetime import datetime, timezone
from typing import Any

import psutil


def get_system_status() -> dict[str, Any]:
    """
    Get current system status.

    Returns:
        A dictionary containing CPU and memory usage information.
        The dictionary is JSON-compatible, so it can be returned by the web API.
    """

    memory = psutil.virtual_memory()

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_total_bytes": memory.total,
        "memory_available_bytes": memory.available,
        "memory_used_bytes": memory.used,
        "memory_usage_percent": memory.percent,
    }


def get_status_csv_headers() -> list[str]:
    """
    Get CSV headers for the system status.

    Returns:
        A list of strings representing the CSV headers.
    """
    return [
        "timestamp",
        "cpu_percent",
        "memory_total_bytes",
        "memory_available_bytes",
        "memory_used_bytes",
        "memory_usage_percent",
    ]

def get_status_csv_row() -> list[Any]:
    """
    Return system status as a list.

    This is useful for writing one row into log.csv.
    """
    status = get_system_status()

    return [
        status["timestamp"],
        status["cpu_percent"],
        status["memory_total_bytes"],
        status["memory_available_bytes"],
        status["memory_used_bytes"],
        status["memory_usage_percent"],
    ]