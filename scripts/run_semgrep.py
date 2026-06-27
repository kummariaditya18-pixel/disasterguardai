"""Run Semgrep when its native engine is available."""

from __future__ import annotations

import shutil
import subprocess
import sys


def main() -> int:
    semgrep = shutil.which("semgrep")
    semgrep_core = shutil.which("semgrep-core") or shutil.which("semgrep-core.exe")

    if semgrep is None or semgrep_core is None:
        print("Semgrep engine not available; skipping Semgrep hook.")
        return 0

    result = subprocess.run([semgrep, "--config=auto", *sys.argv[1:]], check=False)

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
