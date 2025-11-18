"""
Utility to verify that importing the FastAPI app does not raise due to env parsing.

Usage:
    python run_import_check.py
Exit code 0 on success, 1 on failure.
"""
import subprocess
import sys


def main() -> int:
    # Delegate to the dedicated module to keep single source of truth.
    proc = subprocess.run(
        [sys.executable, "-m", "src.api._import_verify"],
        capture_output=True,
        text=True,
        check=False,
    )
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
