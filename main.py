#!/usr/bin/env python3
"""Entry for make.fun news-image-20261119.

Writes the one-image front page of 19 November 2026 world news to
/output/entry.png. Standard library only: the image (entry.png, drawn by
tools/draw_image.py in this repository) is copied byte for byte, so two
runs produce identical bytes.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    # The grader sets MAKEFUN_OUTPUT_DIR; /output is the harness default.
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
