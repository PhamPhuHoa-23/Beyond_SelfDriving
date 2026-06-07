#!/usr/bin/env python3
"""Extract a single frame from a rendered studio video for visual QA.

Usage:
  python scripts/extract_frame.py videos/P01S02BFMDefinition.mp4 0.55 out.jpg
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 4:
        print("Usage: extract_frame.py <video.mp4> <fraction_0_to_1> <output.jpg>")
        sys.exit(1)
    video = Path(sys.argv[1])
    frac = float(sys.argv[2])
    out = Path(sys.argv[3])
    if not video.is_file():
        print(f"Missing video: {video}")
        sys.exit(1)
    probe = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(video),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    duration = float(probe.stdout.strip())
    t = max(0.0, min(duration * frac, duration - 0.05))
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", str(video),
            "-frames:v", "1", "-q:v", "2", str(out),
        ],
        check=True,
    )
    print(f"Wrote {out} @ t={t:.2f}s ({frac * 100:.0f}%)")


if __name__ == "__main__":
    main()
