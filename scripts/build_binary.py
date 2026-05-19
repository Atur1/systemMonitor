"""
Build script for creating an obfuscated binary executable.

This script uses:
1. PyArmor to obfuscate the Python source code.
2. PyInstaller through PyArmor's --pack option to create a binary.

Run from the project root:

    uv run python scripts/build_binary.py

Output:
    dist/systemmonitor      Linux/macOS
    dist/systemmonitor.exe  Windows
"""

from __future__ import annotations

import platform
import shutil
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
PYARMOR_DIR = PROJECT_ROOT / ".pyarmor"

APP_NAME = "systemmonitor"


def run_command(command: list[str]) -> None:
    print(f"\nRunning: {' '.join(command)}\n")

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(command)}")


def clean_previous_builds() -> None:
    for path in [DIST_DIR, BUILD_DIR, PYARMOR_DIR]:
        if path.exists():
            print(f"Removing old build folder: {path}")
            shutil.rmtree(path)


def check_required_files() -> None:
    required_paths = [
        PROJECT_ROOT / "main.py",
        PROJECT_ROOT / "app",
        PROJECT_ROOT / "app" / "__init__.py",
        PROJECT_ROOT / "app" / "config.py",
        PROJECT_ROOT / "app" / "csv_logger.py",
        PROJECT_ROOT / "app" / "status.py",
        PROJECT_ROOT / "app" / "tcp_server.py",
        PROJECT_ROOT / "app" / "web_server.py",
    ]

    missing = [path for path in required_paths if not path.exists()]

    if missing:
        missing_list = "\n".join(str(path) for path in missing)
        raise FileNotFoundError(
            "Project structure is incorrect. Missing files:\n"
            f"{missing_list}"
        )


def configure_pyarmor_pack_options() -> None:
    """
    Configure extra PyInstaller options used by PyArmor.

    FastAPI/Uvicorn can require hidden imports because some modules are loaded
    dynamically.
    """

    pyinstaller_options = (
        f' --onefile'
        f' --name {APP_NAME}'
        f' --hidden-import uvicorn.logging'
        f' --hidden-import uvicorn.loops'
        f' --hidden-import uvicorn.loops.auto'
        f' --hidden-import uvicorn.protocols'
        f' --hidden-import uvicorn.protocols.http'
        f' --hidden-import uvicorn.protocols.http.auto'
        f' --hidden-import uvicorn.protocols.websockets'
        f' --hidden-import uvicorn.protocols.websockets.auto'
        f' --hidden-import uvicorn.lifespan'
        f' --hidden-import uvicorn.lifespan.on'
    )

    run_command(
        [
            "pyarmor",
            "cfg",
            "pack:pyi_options",
            pyinstaller_options,
        ]
    )


def build_binary() -> None:
    """
    Build the obfuscated one-file executable.

    PyArmor documentation uses:

        pyarmor gen --pack onefile foo.py

    For this project, main.py is the entry point and app/ contains the project
    modules.
    """

    run_command(
        [
            "pyarmor",
            "gen",
            "--pack",
            "onefile",
            "-r",
            "main.py",
            "app",
        ]
    )


def print_result() -> None:
    executable_name = f"{APP_NAME}.exe" if platform.system() == "Windows" else APP_NAME
    executable_path = DIST_DIR / executable_name

    print("\nBuild finished.")
    print(f"Expected executable: {executable_path}")

    if executable_path.exists():
        print("Binary created successfully.")
    else:
        print("Binary was not found at the expected path.")
        print("Check the PyArmor/PyInstaller output above.")


def main() -> None:
    check_required_files()
    clean_previous_builds()
    configure_pyarmor_pack_options()
    build_binary()
    print_result()


if __name__ == "__main__":
    main()