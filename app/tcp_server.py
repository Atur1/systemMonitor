"""
tcp_server.py

This module provides a simple TCP server.

Requirement:
- A separate TCP server must run in parallel with the web server.
- When a client connects, the server automatically starts streaming
  system status data.
- The streamed data includes CPU usage and memory usage.
"""

import asyncio
import json
from app.config import (
    TCP_SERVER_HOST,
    TCP_SERVER_PORT,
    LOG_WRITE_INTERVAL_SECONDS
)
from app.status import get_system_status


async def handle_client(
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter) -> None:
    """
    Handle one connected TCP client.

    As soon as a client connects, this function starts sending system status
    data repeatedly until the client disconnects.
    """

    client_address = writer.get_extra_info('peername')
    print(f"TCPClient connected: {client_address}")

    try:
        while True:
            # Get system status data
            status_data = get_system_status()

            # Convert to JSON string
            message = json.dumps(status_data) + "\n"

            # Send to client
            writer.write(message.encode('utf-8'))
            await writer.drain()

            # Wait before sending the next update
            await asyncio.sleep(LOG_WRITE_INTERVAL_SECONDS)
    
    except ConnectionResetError:
        print(f"TCP Client disconnected unexpectedly: {client_address}")
    except BrokenPipeError:
        print(f"TCP Client connection broken: {client_address}")
    except asyncio.CancelledError:
        print(f"TCP Client task cancelled: {client_address}")
        raise
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"TCP Client disconnected: {client_address}")


async def start_tcp_server() -> None:
    """
    Start the TCP server.

    This function creates the TCP server and keeps it running forever.
    It will normally be called from main.py.
    """
    
    server = await asyncio.start_server(
        handle_client,
        TCP_SERVER_HOST,
        TCP_SERVER_PORT
    )
    addresses = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"TCP Server running on {addresses}")

    async with server:
        await server.serve_forever()


def run_tcp_server() -> None:
    """
    Run the TCP server directly.

    This is useful for testing tcp_server.py by itself.
    """
    try:
        asyncio.run(start_tcp_server())
    except KeyboardInterrupt:
        print("TCP Server stopped by user")


if __name__ == "__main__":
    run_tcp_server()