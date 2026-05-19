"""
main.py

Main entry point of the System Monitor application.

This file starts all required parts of the program:

1. Web server:
   - GET /api/status returns CPU and RAM status as JSON

2. CSV logger:
   - Writes system status to log.csv in the background
   - Works even when nobody sends web requests
   - Rotates and compresses log file when it becomes too large

3. TCP server:
   - Starts a separate TCP server
   - When a client connects, it automatically streams system status data

The important requirement is that all services run in parallel.
"""

import asyncio

from app.config import (
    WEB_SERVER_HOST,
    WEB_SERVER_PORT,
    TCP_SERVER_HOST,
    TCP_SERVER_PORT,
    LOG_FILE_PATH,
    LOG_WRITE_INTERVAL_SECONDS,
    ensure_log_dir_exists,
)
from app.csv_logger import start_csv_logger
from app.tcp_server import start_tcp_server
from app.web_server import run_web_server


async def main() -> None:
    """
    Start the full application.

    The web server is started in a separate thread because uvicorn.run()
    is blocking.

    The CSV logger and TCP server are started as asyncio background tasks.
    """

    ensure_log_dir_exists()

    print("=" * 60)
    print("System Monitor application starting...")
    print(f"Web server: http://{WEB_SERVER_HOST}:{WEB_SERVER_PORT}")
    print(f"Status API: http://{WEB_SERVER_HOST}:{WEB_SERVER_PORT}/api/status")
    print(f"TCP server: {TCP_SERVER_HOST}:{TCP_SERVER_PORT}")
    print(f"CSV log file: {LOG_FILE_PATH}")
    print(f"Logging interval: {LOG_WRITE_INTERVAL_SECONDS} seconds")
    print("=" * 60)

    # Start FastAPI/Uvicorn web server in a separate thread.
    # This is needed because uvicorn.run() blocks the current thread.
    web_server_task = asyncio.create_task(
        asyncio.to_thread(run_web_server)
    )

    # Start CSV logger in the background.
    csv_logger_task = asyncio.create_task(start_csv_logger())

    # Start TCP server in the background.
    tcp_server_task = asyncio.create_task(start_tcp_server())

    try:
        await asyncio.gather(
            web_server_task,
            csv_logger_task,
            tcp_server_task,
        )

    except asyncio.CancelledError:
        print("Application cancelled.")
        raise

    except KeyboardInterrupt:
        print("Application stopped by user.")

    finally:
        print("System Monitor application stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Application stopped by user.")