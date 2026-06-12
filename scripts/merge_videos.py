#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

video_dir = Path(r"C:\Users\admin\Downloads\ML\Lab01_3B1B\drivex\media\videos")
output_dir = video_dir / "FINAL"
output_dir.mkdir(exist_ok=True)

scenes = ["i01_title_card", "i02_hook", "p01_s01_opening", "p01_s02_genai_boom"]
resolution = "480p15"  # Actual resolution manim rendered to

print(f"Checking videos at {resolution}...")
videos = []
for scene in scenes:
    video_path = video_dir / scene / resolution
    mp4_files = list(video_path.glob("*.mp4"))
    if mp4_files:
        videos.append(mp4_files[0])
        size_mb = mp4_files[0].stat().st_size / (1024 * 1024)
        print(f"✓ {scene}: {size_mb:.1f} MB")
    else:
        print(f"⚠ {scene}: NOT FOUND at {video_path}")

if len(videos) == 0:
    print("\n✗ No videos found")
    exit(1)

# Create concat file
concat_file = output_dir / "concat_list.txt"
with open(concat_file, "w") as f:
    for video in videos:
        f.write(f"file '{video}'\n")

print(f"\n✓ Merging {len(videos)} videos...")

# Merge with ffmpeg
output_video = output_dir / "WhiteTheme_Final.mp4"
cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", "-y", str(output_video)]

result = subprocess.run(cmd, capture_output=True, text=True)

if output_video.exists():
    size_mb = output_video.stat().st_size / (1024 * 1024)
    print(f"\n✓✓✓ MERGE COMPLETE ✓✓✓")
    print(f"Output: {output_video}")
    print(f"Size: {size_mb:.1f} MB")
    print("\nOpening video...")
    os.startfile(str(output_video))
else:
    print(f"\n✗ Error:")
    print(result.stderr)
