"""
web_server.py

This module provides a simple HTTP web server.

Requirement:
- GET /api/status returns current system status in JSON format.

The web server does not collect CPU/RAM data directly.
It uses get_system_status() from status.py.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.config import WEB_SERVER_HOST, WEB_SERVER_PORT
from app.status import get_system_status 

app = FastAPI(
    title="System Monitor API",
    description="Simple API for checking CPU and RAM usage",
    version="1.0.0",
)


@app.get("/")
def root() -> dict[str, str]:
    """
    Basic root endpoint.

    Useful for checking that the web server is running.
    """
    return {"message": "System Monitor API is running",
            "status_endpoint": "/api/status"
        }

@app.get("/api/status")
def api_status() -> JSONResponse:
    """
    Return current system status as JSON.

    Example response:
    {
        "timestamp": "2026-05-18T18:31:30+00:00",
        "cpu_percent": 12.5,
        "memory_total_bytes": 8589934592,
        "memory_available_bytes": 3000000000,
        "memory_used_bytes": 5589934592,
        "memory_usage_percent": 65.1
    }
    """
    status = get_system_status()
    return JSONResponse(content=status)


def run_web_server() -> None:
    """
    Start the web server.

    This function will be called from main.py.
    """
    uvicorn.run(app,
                host=WEB_SERVER_HOST,
                port=WEB_SERVER_PORT,
                log_level="info",
            )
    

if __name__ == "__main__":
    run_web_server()