# System Monitor

A lightweight Python system monitoring application built with **FastAPI**, **asyncio**, **psutil**, **UV**, **PyArmor**, and **PyInstaller**.

The application runs three services in parallel:

1. **HTTP web server** — provides system status through `GET /api/status`.
2. **CSV logger** — writes CPU and RAM status to `logs/log.csv` in the background.
3. **TCP server** — automatically streams system status data when a TCP client connects.

The project is designed as a simple, scalable, cross-platform monitoring service for Windows, Linux, and macOS.

---

## Requirements Covered

This project satisfies the following requirements:

- Python 3 project managed with **UV**
- Simple HTTP web server
- `GET /api/status` endpoint returning system status in JSON format
- Background CSV logging independent of API requests
- Automatic log rotation when the CSV file exceeds the configured size
- Old log files compressed into `.gz`
- Configuration through `.env`
- Separate TCP server running in parallel
- TCP server automatically streams data after client connection
- CPU usage and RAM usage monitoring
- PyArmor-based binary build
- Designed to run on Windows, Linux, and macOS

---

## Project Structure

```text
systemMonitor/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── csv_logger.py
│   ├── status.py
│   ├── tcp_server.py
│   └── web_server.py
├── scripts/
│   └── build_binary.py
├── logs/
│   └── log.csv
├── main.py
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
└── README.md
```

### Main files

| File | Purpose |
|---|---|
| `main.py` | Starts the web server, CSV logger, and TCP server in parallel |
| `app/config.py` | Loads configuration from `.env` |
| `app/status.py` | Collects CPU and RAM status using `psutil` |
| `app/web_server.py` | Provides the FastAPI HTTP API |
| `app/tcp_server.py` | Provides the TCP streaming server |
| `app/csv_logger.py` | Writes system status to CSV and rotates/compresses logs |
| `scripts/build_binary.py` | Builds the protected binary using PyArmor and PyInstaller |

---

## Technologies Used

- **Python 3**
- **UV** — Python project and dependency manager
- **FastAPI** — web API framework
- **Uvicorn** — ASGI server for FastAPI
- **psutil** — CPU and RAM monitoring
- **python-dotenv** — loading `.env` configuration
- **asyncio** — concurrent TCP server and background logger
- **PyArmor** — source code protection/obfuscation
- **PyInstaller** — executable/binary generation

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd systemMonitor
```

### 2. Install UV

If UV is not installed, install it first.

macOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Check installation:

```bash
uv --version
```

### 3. Install project dependencies

```bash
uv sync
```

This creates a virtual environment and installs all dependencies from `pyproject.toml` and `uv.lock`.

---

## Configuration

Create a `.env` file in the project root.

You can copy the example file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Example `.env`:

```env
WEB_SERVER_HOST=127.0.0.1
WEB_SERVER_PORT=8000

TCP_SERVER_HOST=127.0.0.1
TCP_SERVER_PORT=9000

LOG_DIR=logs
LOG_FILE=log.csv
MAX_LOG_SIZE_MB=5
LOG_WRITE_INTERVAL_SECONDS=2.0
```

### Configuration values

| Variable | Description | Example |
|---|---|---|
| `WEB_SERVER_HOST` | HTTP server host | `127.0.0.1` |
| `WEB_SERVER_PORT` | HTTP server port | `8000` |
| `TCP_SERVER_HOST` | TCP server host | `127.0.0.1` |
| `TCP_SERVER_PORT` | TCP server port | `9000` |
| `LOG_DIR` | Directory where logs are stored | `logs` |
| `LOG_FILE` | Active CSV log filename | `log.csv` |
| `MAX_LOG_SIZE_MB` | Maximum CSV file size before rotation | `5` |
| `LOG_WRITE_INTERVAL_SECONDS` | Delay between log writes | `2.0` |

---

## Running the Application

From the project root, run:

```bash
uv run python main.py
```

Expected output:

```text
============================================================
System Monitor application starting...
Web server: http://127.0.0.1:8000
Status API: http://127.0.0.1:8000/api/status
TCP server: 127.0.0.1:9000
CSV log file: logs/log.csv
Logging interval: 2.0 seconds
============================================================
```

The program now runs:

- HTTP server on port `8000`
- TCP server on port `9000`
- CSV logger in the background

Stop the application with:

```bash
Ctrl + C
```

---

## HTTP API Usage

### Check root endpoint

```bash
curl http://127.0.0.1:8000/
```

Example response:

```json
{
  "message": "System Monitor API is running",
  "status_endpoint": "/api/status"
}
```

### Get system status

```bash
curl http://127.0.0.1:8000/api/status
```

Example response:

```json
{
  "timestamp": "2026-05-19T08:30:00.123456+00:00",
  "cpu_percent": 12.4,
  "memory_total_bytes": 8589934592,
  "memory_available_bytes": 4200000000,
  "memory_used_bytes": 4389934592,
  "memory_usage_percent": 51.1
}
```

The response includes:

| Field | Meaning |
|---|---|
| `timestamp` | Current UTC timestamp |
| `cpu_percent` | Current CPU usage percentage |
| `memory_total_bytes` | Total RAM in bytes |
| `memory_available_bytes` | Available RAM in bytes |
| `memory_used_bytes` | Used RAM in bytes |
| `memory_usage_percent` | RAM usage percentage |

---

## TCP Server Usage

The TCP server automatically starts streaming data when a client connects.

### macOS/Linux

```bash
nc 127.0.0.1 9000
```

### Windows PowerShell

If `telnet` is enabled:

```powershell
telnet 127.0.0.1 9000
```

Or use a simple Python TCP client:

```python
import socket

with socket.create_connection(("127.0.0.1", 9000)) as sock:
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(data.decode("utf-8"), end="")
```

Example TCP output:

```json
{"timestamp": "2026-05-19T08:30:00.123456+00:00", "cpu_percent": 10.5, "memory_total_bytes": 8589934592, "memory_available_bytes": 4200000000, "memory_used_bytes": 4389934592, "memory_usage_percent": 51.1}
{"timestamp": "2026-05-19T08:30:02.123456+00:00", "cpu_percent": 11.2, "memory_total_bytes": 8589934592, "memory_available_bytes": 4190000000, "memory_used_bytes": 4399934592, "memory_usage_percent": 51.3}
```

---

## CSV Logging

The logger writes system status to:

```text
logs/log.csv
```

Example CSV content:

```csv
timestamp,cpu_percent,memory_total_bytes,memory_available_bytes,memory_used_bytes,memory_usage_percent
2026-05-19T08:30:00.123456+00:00,12.4,8589934592,4200000000,4389934592,51.1
2026-05-19T08:30:02.123456+00:00,10.7,8589934592,4210000000,4379934592,51.0
```

Logging happens continuously in the background, even when no HTTP requests are sent.

---

## Log Rotation

When `logs/log.csv` becomes larger than `MAX_LOG_SIZE_MB`, the program:

1. Compresses the old log file into `.gz`
2. Removes the old `log.csv`
3. Creates a new `log.csv`
4. Continues logging

Example rotated file:

```text
logs/log_20260519_083000.csv.gz
```

To test rotation quickly, temporarily set a very small size in `.env`:

```env
MAX_LOG_SIZE_MB=1
LOG_WRITE_INTERVAL_SECONDS=0.5
```

Then run the application and wait until the file rotates.

---

## Building the Binary with PyArmor

The project includes a build script:

```text
scripts/build_binary.py
```

It uses:

- **PyArmor** to obfuscate/protect the source code
- **PyInstaller** through PyArmor's `--pack onefile` option to create an executable file

### 1. Make sure build dependencies are installed

```bash
uv sync
```

Check that PyArmor and PyInstaller are available:

```bash
uv run pyarmor --version
uv run pyinstaller --version
```

If they are missing, add them:

```bash
uv add --dev pyarmor pyinstaller
```

### 2. Build the binary

Run from the project root:

```bash
uv run python scripts/build_binary.py
```

### 3. Output location

On macOS/Linux:

```text
dist/systemmonitor
```

On Windows:

```text
dist/systemmonitor.exe
```

### 4. Run the binary

macOS/Linux:

```bash
./dist/systemmonitor
```

Windows PowerShell:

```powershell
.\dist\systemmonitor.exe
```

---

## Important Cross-Platform Note

PyInstaller is not a cross-compiler.

That means:

| Target binary | Build on |
|---|---|
| Windows `.exe` | Windows |
| Linux binary | Linux |
| macOS binary | macOS |

For example, if you build on macOS, the result is a macOS binary.  
To create a Windows `.exe`, run the build script on Windows.

---

## Development Commands

Run the app:

```bash
uv run python main.py
```

Run the binary build:

```bash
uv run python scripts/build_binary.py
```

Test HTTP API:

```bash
curl http://127.0.0.1:8000/api/status
```

Test TCP stream:

```bash
nc 127.0.0.1 9000
```

Check logs:

```bash
cat logs/log.csv
```

Remove generated files:

```bash
rm -rf build dist .pyarmor logs app/__pycache__
```

---

## GitHub Submission Checklist

Before sending the GitHub repository link, make sure the repository contains:

```text
app/
scripts/build_binary.py
main.py
pyproject.toml
uv.lock
README.md
.env.example
.gitignore
```

Do not commit:

```text
.venv/
.env
__pycache__/
logs/
build/
.pyarmor/
```

Normally, `dist/` is not committed.  
However, if the reviewer specifically expects to see the binary file in the repository, you can include it manually:

macOS/Linux:

```bash
git add -f dist/systemmonitor
```

Windows:

```bash
git add -f dist/systemmonitor.exe
```

Then commit:

```bash
git commit -m "Add PyArmor binary build"
git push
```

Alternative recommended approach: upload the binary as a **GitHub Release artifact**.

---

## Troubleshooting

### `No module named pyarmor.__main__`

Do not run:

```bash
python -m pyarmor
```

Use:

```bash
uv run pyarmor --version
```

or:

```bash
uv run python scripts/build_binary.py
```

### Port already in use

If port `8000` or `9000` is already used, change the ports in `.env`:

```env
WEB_SERVER_PORT=8080
TCP_SERVER_PORT=9001
```

### `.env` changes do not apply

Restart the application after editing `.env`.

### TCP command not found

If `nc` is not installed, use the Python TCP client shown in the TCP section.

