#!/usr/bin/env python3
"""Master entrypoint: regenerate all 28 SVG diagrams and render high-DPI PNGs."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent


def main() -> None:
    for script in ["gen_viz_a.py", "gen_viz_b.py", "gen_viz_c.py"]:
        path = SCRIPTS / script
        print(f"Running {path.name}...")
        subprocess.run([sys.executable, str(path)], check=True)
    print("All 28 SVG and PNG diagrams regenerated cleanly.")


if __name__ == "__main__":
    main()
