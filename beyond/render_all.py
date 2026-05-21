#!/usr/bin/env python3
# beyond/render_all.py
# ─────────────────────────────────────────────────────────────────
# Render toàn bộ scenes trong beyond/ rồi merge thành 1 video.
#
# Cách dùng (chạy từ thư mục gốc Lab01_3B1B/):
#
#   python beyond/render_all.py                    # 480p, render tất cả
#   python beyond/render_all.py -q qh              # 1080p60
#   python beyond/render_all.py -q qk              # 4K
#   python beyond/render_all.py --skip-existing    # bỏ qua scene đã có MP4
#   python beyond/render_all.py --parts intro p1   # chỉ render intro + part 1
#   python beyond/render_all.py --merge-only       # chỉ merge (không render lại)
#   python beyond/render_all.py --dry-run          # xem danh sách, không render
#   python beyond/render_all.py --open             # mở video sau khi xong
#
# Yêu cầu: manim, ffmpeg đều phải có trong PATH.
# ─────────────────────────────────────────────────────────────────

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

# Force UTF-8 output so Unicode symbols render correctly on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # Python 3.7+
    except AttributeError:
        pass

# ── Project root (thư mục chứa file này là beyond/, root là cha của nó) ────
SCRIPT_DIR  = Path(__file__).resolve().parent          # beyond/
PROJECT_ROOT = SCRIPT_DIR.parent                        # Lab01_3B1B/
MEDIA_ROOT   = PROJECT_ROOT / "media" / "videos"        # manim output

# Quality → resolution subfolder mapping
QUALITY_MAP = {
    "ql": "480p15",
    "qm": "720p30",
    "qh": "1080p60",
    "qk": "2160p60",
    "qp": "1080p60",   # production alias
}

# ─────────────────────────────────────────────────────────────────
# SCENE ORDER — thứ tự chính xác theo kịch bản 5_PART_GUIDE.md
# Format: (scene_file_relative_to_beyond, ClassName, part_tag)
# ─────────────────────────────────────────────────────────────────
SCENES = [
    # ── INTRO ─────────────────────────────────────────────────────
    ("scenes/intro/i01_title_card.py",    "I01TitleCard",         "intro"),
    ("scenes/intro/i02_the_hook.py",      "I02Hook",              "intro"),
    ("scenes/intro/i03_roadmap.py",       "I03Roadmap",           "intro"),

    # ── PART 1 — Foundation Models ────────────────────────────────
    ("scenes/part01/p01_s01_title.py",        "P01S01Title",        "p1"),
    ("scenes/part01/p01_s02_genai_boom.py",   "P01S02GenAiBoom",    "p1"),
    ("scenes/part01/p01_s03_av_arch.py",      "P01S03AvArch",       "p1"),
    ("scenes/part01/p01_s04_longtail.py",     "P01S04LongTail",     "p1"),
    ("scenes/part01/p01_s05_fm_empower.py",   "P01S05FmEmpower",    "p1"),
    ("scenes/part01/p01_s06_vla_gallery.py",  "P01S06VlaGallery",   "p1"),
    ("scenes/part01/p01_s07_vla_arch.py",     "P01S07VlaArch",      "p1"),
    ("scenes/part01/p01_s08_autovla.py",      "P01S08AutoVLA",      "p1"),
    ("scenes/part01/p01_s09_takeaways.py",    "P01S09Takeaways",    "p1"),

    # ── PART 2 — Cooperative Perception ──────────────────────────
    ("scenes/part02/p02_s01_title.py",          "P02S01Title",        "p2"),
    ("scenes/part02/p02_s02_background.py",     "P02S02Background",   "p2"),
    ("scenes/part02/p02_s03_evolution.py",      "P02S03Evolution",    "p2"),
    ("scenes/part02/p02_s04_occlusion.py",      "P02S04Occlusion",    "p2"),
    ("scenes/part02/p02_s05_related_works.py",  "P02S05RelatedWorks", "p2"),
    ("scenes/part02/p02_s06_three_questions.py","P02S06ThreeQuestions","p2"),
    ("scenes/part02/p02_s07_v2xpnp.py",         "P02S07V2XPnP",       "p2"),
    ("scenes/part02/p02_s08_dataset.py",         "P02S08Dataset",      "p2"),
    ("scenes/part02/p02_s09_turbotrain.py",      "P02S09TurboTrain",   "p2"),
    ("scenes/part02/p02_s10_riskmap.py",         "P02S10RiskMap",      "p2"),
    ("scenes/part02/p02_s11_summary.py",         "P02S11Summary",      "p2"),
    ("scenes/part02/p02_s12_bridge.py",          "P02S12Bridge",       "p2"),

    # ── PART 3 — Sim to Reality ───────────────────────────────────
    ("scenes/part03/p03_s01_title.py",              "P03S01Title",           "p3"),
    ("scenes/part03/p03_s02_sim_gap.py",            "P03S02SimGap",          "p3"),
    ("scenes/part03/p03_s03_smart_intersection.py", "P03S03SmartIntersection","p3"),
    ("scenes/part03/p03_s04_calibration.py",        "P03S04Calibration",     "p3"),
    ("scenes/part03/p03_s05_kalman.py",             "P03S05Kalman",          "p3"),
    ("scenes/part03/p03_s06_cooperfuse.py",         "P03S06CooperFuse",      "p3"),
    ("scenes/part03/p03_s07_digital_twin.py",       "P03S07DigitalTwin",     "p3"),
    ("scenes/part03/p03_s08_localization.py",       "P03S08Localization",    "p3"),
    ("scenes/part03/p03_s10_v2x_realo.py",          "P03S10V2XReaLO",        "p3"),
    ("scenes/part03/p03_s11_opencda.py",            "P03S11OpenCDA",         "p3"),
    ("scenes/part03/p03_s12_simboost.py",           "P03S12SimBoost",        "p3"),
    ("scenes/part03/p03_s14_bridge.py",             "P03S14Bridge",          "p3"),

    # ── PART 4 — Efficiency ───────────────────────────────────────
    ("scenes/part04/p04_s01_title.py",              "P04S01Title",          "p4"),
    ("scenes/part04/p04_s02_annotation_cost.py",    "P04S02AnnotationCost", "p4"),
    ("scenes/part04/p04_s03_coopre.py",             "P04S03CooPre",         "p4"),
    ("scenes/part04/p04_s04_turbotrain_gradient.py","P04S04TurboTrainGrad", "p4"),
    ("scenes/part04/p04_s05_quantv2x.py",           "P04S05QuantV2X",       "p4"),
    ("scenes/part04/p04_s06_efficiency_summary.py", "P04S06EfficiencySummary","p4"),
    ("scenes/part04/p04_s07_latency_chain.py",      "P04S07LatencyChain",   "p4"),
    ("scenes/part04/p04_s09_bridge.py",             "P04S09Bridge",         "p4"),

    # ── PART 5 — Physical AI ─────────────────────────────────────
    ("scenes/part05/p05_s01_title.py",              "P05S01Title",       "p5"),
    ("scenes/part05/p05_s02_physical_ai_vision.py", "P05S02PhysicalAI",  "p5"),
    ("scenes/part05/p05_s03_metaurban.py",          "P05S03MetaUrban",   "p5"),
    ("scenes/part05/p05_s04_urbansim.py",           "P05S04UrbanSim",    "p5"),
    ("scenes/part05/p05_s05_citywalker_pedgen.py",  "P05S05CityWalker",  "p5"),
    ("scenes/part05/p05_s06_vid2sim.py",            "P05S06Vid2Sim",     "p5"),
    ("scenes/part05/p05_s07_living_city.py",        "P05S07LivingCity",  "p5"),
    ("scenes/part05/p05_s08_final_summary.py",      "P05S08FinalSummary","p5"),
]

# ── Colour helpers (Windows cmd-safe ANSI) ────────────────────────
def _c(text, code): return f"\033[{code}m{text}\033[0m"
def green(t):  return _c(t, "92")
def red(t):    return _c(t, "91")
def yellow(t): return _c(t, "93")
def cyan(t):   return _c(t, "96")
def bold(t):   return _c(t, "1")
def dim(t):    return _c(t, "2")


# ── Helpers ───────────────────────────────────────────────────────

def mp4_path(scene_rel: str, class_name: str, resolution: str) -> Path:
    """Return expected MP4 path for a rendered scene."""
    stem = Path(scene_rel).stem           # e.g. "i01_title_card"
    return MEDIA_ROOT / stem / resolution / f"{class_name}.mp4"


def scene_label(scene_rel: str, class_name: str) -> str:
    return f"{Path(scene_rel).stem}  →  {class_name}"


def check_ffmpeg() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"],
                       capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def render_scene(scene_rel: str, class_name: str,
                 quality: str, dry_run: bool) -> bool:
    """
    Render one scene. Returns True on success.
    scene_rel is relative to SCRIPT_DIR (beyond/).
    """
    scene_abs = SCRIPT_DIR / scene_rel
    cmd = ["manim", f"-{quality}", str(scene_abs), class_name]

    if dry_run:
        print(f"  {dim('[dry-run]')} manim -{quality} {scene_rel} {class_name}")
        return True

    result = subprocess.run(
        cmd,
        cwd=str(PROJECT_ROOT),
        capture_output=False,     # let manim output stream to terminal
    )
    return result.returncode == 0


def merge_videos(video_paths: list[Path], output_path: Path) -> bool:
    """ffmpeg concat demuxer merge — lossless, instant."""
    concat_file = output_path.parent / "_concat_list.txt"
    concat_file.write_text(
        "\n".join(f"file '{p}'" for p in video_paths),
        encoding="utf-8"
    )
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(output_path),
    ]
    print(f"\n{cyan('ffmpeg concat →')} {output_path.name}")
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    concat_file.unlink(missing_ok=True)
    return result.returncode == 0


# ── Main ──────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Render all beyond/ scenes then merge into one video."
    )
    ap.add_argument("-q", "--quality", default="ql",
                    choices=list(QUALITY_MAP.keys()),
                    help="Manim quality flag (default: ql = 480p15)")
    ap.add_argument("--parts", nargs="*",
                    choices=["intro", "p1", "p2", "p3", "p4", "p5"],
                    help="Render only these parts (default: all)")
    ap.add_argument("--skip-existing", action="store_true",
                    help="Skip scenes whose MP4 already exists")
    ap.add_argument("--merge-only", action="store_true",
                    help="Skip rendering — just merge existing MP4s")
    ap.add_argument("--no-merge", action="store_true",
                    help="Render but do NOT merge at the end")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print commands without executing")
    ap.add_argument("--open", action="store_true",
                    help="Open the merged video when done (Windows)")
    ap.add_argument("--output", default=None,
                    help="Output video filename (default: BeyondSelfDriving_<quality>.mp4)")
    args = ap.parse_args()

    # Enable ANSI on Windows
    os.system("")

    resolution = QUALITY_MAP[args.quality]
    output_name = args.output or f"BeyondSelfDriving_{args.quality}.mp4"
    output_dir  = PROJECT_ROOT / "media" / "videos" / "_FINAL"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_name

    # Filter by parts
    active_parts = set(args.parts) if args.parts else None
    scenes = [
        (f, c, p) for f, c, p in SCENES
        if active_parts is None or p in active_parts
    ]

    print(bold(f"\n{'='*60}"))
    print(bold(f"  Beyond Self-Driving — Render Pipeline"))
    print(bold(f"{'='*60}"))
    print(f"  Quality   : {yellow(args.quality)}  ({resolution})")
    print(f"  Scenes    : {len(scenes)}")
    print(f"  Skip exist: {args.skip_existing}")
    print(f"  Output    : {output_path}")
    print(bold(f"{'='*60}\n"))

    if not check_ffmpeg() and not args.no_merge:
        print(red("⚠  ffmpeg not found — merging will be skipped."))
        print(red("   Install ffmpeg and add to PATH to enable merge.\n"))
        args.no_merge = True

    # ── RENDER PHASE ────────────────────────────────────────────
    ok_videos:   list[Path] = []
    failed:      list[str]  = []
    skipped:     int        = 0
    total_start              = time.time()

    for idx, (scene_rel, class_name, part) in enumerate(scenes, 1):
        mp4 = mp4_path(scene_rel, class_name, resolution)
        label = f"[{idx:02d}/{len(scenes):02d}]  {class_name}"

        if args.merge_only:
            if mp4.exists():
                ok_videos.append(mp4)
                print(f"  {green('✓')} {label}  {dim(str(round(mp4.stat().st_size/1024/1024, 1)) + ' MB')}")
            else:
                print(f"  {red('✗')} {label}  {red('NOT FOUND')}")
                failed.append(class_name)
            continue

        if args.skip_existing and mp4.exists():
            size_mb = mp4.stat().st_size / 1024 / 1024
            print(f"  {dim('↩')} {label}  {dim(f'{size_mb:.1f} MB — skipped')}")
            ok_videos.append(mp4)
            skipped += 1
            continue

        print(f"\n{cyan('▶')} {label}")
        t0 = time.time()

        success = render_scene(scene_rel, class_name, args.quality, args.dry_run)
        elapsed = time.time() - t0

        if success and (args.dry_run or mp4.exists()):
            size_str = ""
            if mp4.exists():
                size_str = f"  {dim(str(round(mp4.stat().st_size/1024/1024, 1)) + ' MB')}"
            print(f"  {green('✓')} Done  {dim(f'{elapsed:.1f}s')}{size_str}")
            if not args.dry_run:
                ok_videos.append(mp4)
        else:
            print(f"  {red('✗ FAILED')}  {dim(f'{elapsed:.1f}s')}")
            failed.append(class_name)

    # ── SUMMARY ─────────────────────────────────────────────────
    total_elapsed = time.time() - total_start
    print(bold(f"\n{'='*60}"))
    print(f"  Rendered  : {green(str(len(ok_videos)))} / {len(scenes)}")
    if skipped:
        print(f"  Skipped   : {dim(str(skipped))}  (already existed)")
    if failed:
        print(f"  Failed    : {red(str(len(failed)))}")
        for f in failed:
            print(f"    {red('✗')} {f}")
    total_size_mb = sum(
        p.stat().st_size for p in ok_videos if p.exists()
    ) / 1024 / 1024
    print(f"  Total size: {total_size_mb:.1f} MB")
    print(f"  Time      : {int(total_elapsed // 60)}m {int(total_elapsed % 60)}s")
    print(bold(f"{'='*60}"))

    if args.no_merge or args.dry_run:
        print(dim("\n  Merge skipped."))
        return

    if len(ok_videos) == 0:
        print(red("\n  No videos to merge."))
        sys.exit(1)

    # ── MERGE PHASE ─────────────────────────────────────────────
    print(f"\n{bold('MERGE')}  {len(ok_videos)} clips → {yellow(output_path.name)}")

    success = merge_videos(ok_videos, output_path)

    if success and output_path.exists():
        size_mb = output_path.stat().st_size / 1024 / 1024
        print(green(f"\n✓✓✓  MERGE COMPLETE"))
        print(f"     {output_path}")
        print(f"     {size_mb:.1f} MB  ·  {len(ok_videos)} scenes")

        if args.open:
            print(f"\n  Opening video...")
            os.startfile(str(output_path))   # Windows only
    else:
        print(red("\n✗  Merge failed — check ffmpeg output above."))
        sys.exit(1)


if __name__ == "__main__":
    main()
