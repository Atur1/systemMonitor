"""
csv_logger.py

This module logs system status to a CSV file in the background.

Requirements:
- Log CPU and RAM status into log.csv
- Logging must happen independently of web requests
- When the CSV file becomes larger than the configured size,
  compress the old file into .gz and create a new log.csv
"""

import csv
import gzip
import asyncio
import shutil
from datetime import datetime
from pathlib import Path
from app.config import (
    LOG_FILE_PATH,
    LOG_MAX_BYTES,
    LOG_WRITE_INTERVAL_SECONDS,
    ensure_log_dir_exists,
)
from app.status import get_status_csv_headers, get_status_csv_row


def csv_file_exists_and_has_content(file_path: Path) -> bool:
    """
    Check if the CSV log file exists and has content.
    This is used to determine whether to write the header row.
    """
    return file_path.exists() and file_path.stat().st_size > 0


def write_csv_header_if_needed() -> None:
    """
    Write the CSV header row if the file does not exist or is empty.
    """
    if not csv_file_exists_and_has_content(LOG_FILE_PATH):
        with LOG_FILE_PATH.open(mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(get_status_csv_headers())


def write_status_row() -> None:
    """
    Write a single row of system status data to the CSV file.
    """
    write_csv_header_if_needed()

    with LOG_FILE_PATH.open(mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(get_status_csv_row())


def should_rotate_log() -> bool:
    """
    Check if the current log file exceeds the maximum allowed size.
    If it does, we need to rotate (compress and start a new file).
    """
    if not LOG_FILE_PATH.exists():
        return False
    
    return LOG_FILE_PATH.stat().st_size >= LOG_MAX_BYTES


def build_rotated_log_path() -> Path:
    """
    Create a unique filename for the compressed rotated log file.

    Example:
    logs/log_20260518_185644.csv.gz
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_stem = LOG_FILE_PATH.stem  # e.g. "log"
    original_suffix = LOG_FILE_PATH.suffix  # e.g. ".csv"

    rotated_filename = f"{original_stem}_{timestamp}{original_suffix}.gz"

    return LOG_FILE_PATH.parent / rotated_filename


def rotate_log_file() -> None:
    """
    Compress the current log.csv into a .gz file and remove the old log.csv.
    A new log.csv will be created automatically on the next write.
    """
    if not LOG_FILE_PATH.exists():
        return
    
    rotated_log_path = build_rotated_log_path()

    # Compress the log file
    with LOG_FILE_PATH.open('rb') as source_file:
        with gzip.open(rotated_log_path, 'wb') as compressed_file:
            shutil.copyfileobj(source_file, compressed_file)

    # Remove the original log file
    LOG_FILE_PATH.unlink()

    print(f"Rotated log file: {rotated_log_path}")


async def start_csv_logger() -> None:
    """
    Start the CSV logger in an infinite loop.

    This function will run in the background and periodically write system status
    data to the CSV file. It also checks if log rotation is needed before each write.
    """
    ensure_log_dir_exists()
    write_csv_header_if_needed()

    print(f"CSV logger started: {LOG_FILE_PATH}")

    while True:
        if should_rotate_log():
            rotate_log_file()
            write_csv_header_if_needed()
        
        write_status_row()

        await asyncio.sleep(LOG_WRITE_INTERVAL_SECONDS)


def run_csv_logger() -> None:
    """
    Run the CSV logger directly.

    This is useful for testing csv_logger.py by itself.
    """
    try:
        asyncio.run(start_csv_logger())
    except KeyboardInterrupt:
        print("CSV Logger stopped by user")


if __name__ == "__main__":
    run_csv_logger()