#!/usr/bin/env python3
"""Render → extract QA frames → log manifest. Run scenes in narrative order.

Automated: render, ffmpeg frames at 35/60/85%, JSONL manifest.
Manual/agent: read frames + SOURCE_MANIM_REFERENCE_AUDIT.md → edit scene → re-run.

Usage:
  python scripts/scene_qa_loop.py --part 01
  python scripts/scene_qa_loop.py --from P01S03AModular
  python scripts/scene_qa_loop.py --only P01S07BEMMA
  python scripts/scene_qa_loop.py --list
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEOS = ROOT / "videos"
QA_DIR = ROOT / "studio" / "_qa_loop"
MANIFEST = QA_DIR / "manifest.jsonl"
AUDIT = ROOT / "SOURCE_MANIM_REFERENCE_AUDIT.md"
MANIM = Path(r"C:\Users\admin\miniconda3\Scripts\manimgl.exe")
FFMPEG = Path(r"C:\Users\admin\miniconda3\Library\bin\ffmpeg.exe")

FRAME_PCTS = (0.35, 0.60, 0.85)

# Same order as render_studio_all.ps1
SCENES: list[tuple[str, str]] = [
    ("studio/scenes/intro/i01_title_card.py", "I01TitleCard"),
    ("studio/scenes/intro/i02_the_hook.py", "I02TheHook"),
    ("studio/scenes/intro/i03_roadmap.py", "I03Roadmap"),
    ("studio/scenes/intro/i04_bridge_to_p1.py", "I04BridgeToP1"),
    ("studio/scenes/part01/p01_s01_title.py", "P01S01Title"),
    ("studio/scenes/part01/p01_s02a_genai_timeline.py", "P01S02AGenAITimeline"),
    ("studio/scenes/part01/p01_s02b_fm_definition.py", "P01S02BFMDefinition"),
    ("studio/scenes/part01/p01_s03a_modular.py", "P01S03AModular"),
    ("studio/scenes/part01/p01_s03b_e2e.py", "P01S03BE2E"),
    ("studio/scenes/part01/p01_s03c_hybrid.py", "P01S03CHybrid"),
    ("studio/scenes/part01/p01_s04a_longtail_problem.py", "P01S04ALongtailProblem"),
    ("studio/scenes/part01/p01_s04b_longtail_insight.py", "P01S04BLongtailInsight"),
    ("studio/scenes/part01/p01_s05_fm_empower.py", "P01S05FMEmpower"),
    ("studio/scenes/part01/p01_s06_vla_roadmap.py", "P01S06VLARoadmap"),
    ("studio/scenes/part01/p01_s07a_bevdriver.py", "P01S07ABEVDriver"),
    ("studio/scenes/part01/p01_s07b_emma.py", "P01S07BEMMA"),
    ("studio/scenes/part01/p01_s07c_drivevlm.py", "P01S07CDriveVLM"),
    ("studio/scenes/part01/p01_s08a_autovla_switch.py", "P01S08AAutoVLASwitch"),
    ("studio/scenes/part01/p01_s08b_autovla_results.py", "P01S08BAutoVLAResults"),
    ("studio/scenes/part01/p01_s09_takeaways.py", "P01S09Takeaways"),
    ("studio/scenes/part01/p01_s10_bridge_to_p2.py", "P01S10BridgeToP2"),
    ("studio/scenes/part02/p02_s01_title.py", "P02S01Title"),
    ("studio/scenes/part02/p02_s02a_119m.py", "P02S02A119M"),
    ("studio/scenes/part02/p02_s02b_waymo_reduce.py", "P02S02BWaymoReduce"),
    ("studio/scenes/part02/p02_s03_e2e_evolution.py", "P02S03E2EEvolution"),
    ("studio/scenes/part02/p02_s04a_occlusion_problem.py", "P02S04AOcclusionProblem"),
    ("studio/scenes/part02/p02_s05_radar_waves.py", "P02S05RadarWaves"),
    ("studio/scenes/part02/p02_s06_related_works.py", "P02S06RelatedWorks"),
    ("studio/scenes/part02/p02_s07_research_gaps.py", "P02S07ResearchGaps"),
    ("studio/scenes/part02/p02_s08_three_questions.py", "P02S08ThreeQuestions"),
    ("studio/scenes/part02/p02_s09_v2xpnp_arch.py", "P02S09V2XPnPArch"),
    ("studio/scenes/part02/p02_s10_v2xpnp_dataset.py", "P02S10V2XPnPDataset"),
    ("studio/scenes/part02/p02_s11a_turbotrain_problem.py", "P02S11ATurboTrainProblem"),
    ("studio/scenes/part02/p02_s11b_turbotrain_solution.py", "P02S11BTurboTrainSolution"),
    ("studio/scenes/part02/p02_s12_riskmap.py", "P02S12RiskMap"),
    ("studio/scenes/part02/p02_s13_summary.py", "P02S13Summary"),
    ("studio/scenes/part02/p02_s14_bridge_to_p3.py", "P02S14BridgeToP3"),
    ("studio/scenes/part03/p03_s01_title.py", "P03S01Title"),
    ("studio/scenes/part03/p03_s02_sim_real_gap.py", "P03S02SimRealGap"),
    ("studio/scenes/part03/p03_s03_smart_intersection.py", "P03S03SmartIntersection"),
    ("studio/scenes/part03/p03_s04a_time_calibration.py", "P03S04ATimeCalibration"),
    ("studio/scenes/part03/p03_s04b_space_calibration.py", "P03S04BSpaceCalibration"),
    ("studio/scenes/part03/p03_s05_data_collection.py", "P03S05DataCollection"),
    ("studio/scenes/part03/p03_s06_localization_role.py", "P03S06LocalizationRole"),
    ("studio/scenes/part03/p03_s07_kalman_filter.py", "P03S07KalmanFilter"),
    ("studio/scenes/part03/p03_s08_cooperfuse.py", "P03S08CooperFuse"),
    ("studio/scenes/part03/p03_s09_v2x_realo.py", "P03S09V2XReaLO"),
    ("studio/scenes/part03/p03_s10_opencda_ros.py", "P03S10OpenCDAROS"),
    ("studio/scenes/part03/p03_s11_simboost.py", "P03S11SimBoost"),
    ("studio/scenes/part03/p03_s12_digital_twin.py", "P03S12DigitalTwin"),
    ("studio/scenes/part03/p03_s13_infrax.py", "P03S13InfraX"),
    ("studio/scenes/part03/p03_s14_summary.py", "P03S14Summary"),
    ("studio/scenes/part03/p03_s15_bridge_to_p4.py", "P03S15BridgeToP4"),
    ("studio/scenes/part04/p04_s01_title.py", "P04S01Title"),
    ("studio/scenes/part04/p04_s02_v2x_overview.py", "P04S02V2XOverview"),
    ("studio/scenes/part04/p04_s03_annotation_cost.py", "P04S03AnnotationCost"),
    ("studio/scenes/part04/p04_s04_coopre_masked.py", "P04S04CooPReMasked"),
    ("studio/scenes/part04/p04_s05_turbotrain_landscape.py", "P04S05TurboTrainLandscape"),
    ("studio/scenes/part04/p04_s06_latency_chain.py", "P04S06LatencyChain"),
    ("studio/scenes/part04/p04_s07a_arithmetic_cost.py", "P04S07AArithmeticCost"),
    ("studio/scenes/part04/p04_s07b_memory_bound.py", "P04S07BMemoryBound"),
    ("studio/scenes/part04/p04_s08_quantv2x.py", "P04S08QuantV2X"),
    ("studio/scenes/part04/p04_s09_efficiency_summary.py", "P04S09EfficiencySummary"),
    ("studio/scenes/part04/p04_s10_bridge_to_p5.py", "P04S10BridgeToP5"),
    ("studio/scenes/part05/p05_s01_title.py", "P05S01Title"),
    ("studio/scenes/part05/p05_s02a_llm_vs_robot.py", "P05S02ALLMVsRobot"),
    ("studio/scenes/part05/p05_s02b_two_barriers.py", "P05S02BTwoBarriers"),
    ("studio/scenes/part05/p05_s03_micromobility.py", "P05S03Micromobility"),
    ("studio/scenes/part05/p05_s04a_compositional_quote.py", "P05S04ACompositionalQuote"),
    ("studio/scenes/part05/p05_s04b_metaurban.py", "P05S04BMetaUrban"),
    ("studio/scenes/part05/p05_s04c_metaurban_scaling.py", "P05S04CMetaUrbanScaling"),
    ("studio/scenes/part05/p05_s05a_urbansim_bottleneck.py", "P05S05AUrbanSimBottleneck"),
    ("studio/scenes/part05/p05_s05b_urbansim_results.py", "P05S05BUrbanSimResults"),
    ("studio/scenes/part05/p05_s06a_citywalker.py", "P05S06ACityWalker"),
    ("studio/scenes/part05/p05_s06b_pedgen.py", "P05S06BPedGen"),
    ("studio/scenes/part05/p05_s07_zombie_to_alive.py", "P05S07ZombieToAlive"),
    ("studio/scenes/part05/p05_s08_vid2sim.py", "P05S08Vid2Sim"),
    ("studio/scenes/part05/p05_s09_living_city.py", "P05S09LivingCity"),
    ("studio/scenes/part05/p05_s10_chain_of_solutions.py", "P05S10ChainOfSolutions"),
    ("studio/scenes/part05/p05_s11_final_frame.py", "P05S11FinalFrame"),
]


@dataclass
class SceneRecord:
    ts: str
    scene_file: str
    class_name: str
    render_ok: bool
    video_path: str | None
    frames: dict[str, str]
    audit_hints: list[str]
    error: str | None
    status: str  # rendered | failed | skipped


def load_audit_hints(scene_file: str) -> list[str]:
    """Pull audit table rows mentioning this scene path."""
    if not AUDIT.exists():
        return []
    text = AUDIT.read_text(encoding="utf-8")
    key = Path(scene_file).name.replace(".py", "")
    hints: list[str] = []
    for line in text.splitlines():
        if key in line or scene_file.replace("\\", "/") in line:
            if "|" in line and "Target Scene" not in line:
                hints.append(line.strip())
    # Scene rebuild targets section
    block = re.search(
        rf"`[^`]*{re.escape(key)}[^`]*`.*",
        text,
        re.IGNORECASE,
    )
    if block:
        hints.append(block.group(0)[:200])
    return hints[:8]


def probe_duration(video: Path) -> float:
    out = subprocess.run(
        [
            str(FFMPEG.parent / "ffprobe.exe"),
            "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(video),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(out.stdout.strip())


def extract_frames(video: Path, class_name: str) -> dict[str, str]:
    out_dir = QA_DIR / "frames" / class_name
    out_dir.mkdir(parents=True, exist_ok=True)
    duration = probe_duration(video)
    paths: dict[str, str] = {}
    for pct in FRAME_PCTS:
        t = max(0.0, min(duration * pct, duration - 0.05))
        label = f"{int(pct * 100):02d}pct"
        dest = out_dir / f"{class_name}_{label}.jpg"
        subprocess.run(
            [
                str(FFMPEG),
                "-y", "-ss", f"{t:.3f}", "-i", str(video),
                "-frames:v", "1", "-q:v", "2", str(dest),
            ],
            check=True,
            capture_output=True,
        )
        paths[label] = str(dest.relative_to(ROOT))
    return paths


def render_scene(scene_file: str, class_name: str) -> tuple[bool, str | None, str | None]:
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    path_env = (
        r"C:\Users\admin\miniconda3\Scripts;"
        r"C:\Users\admin\miniconda3\Library\bin;" + env.get("PATH", "")
    )
    env["PATH"] = path_env
    video = VIDEOS / f"{class_name}.mp4"
    temp = VIDEOS / f"{class_name}_temp.mp4"
    if temp.exists():
        try:
            temp.unlink()
        except OSError:
            pass
    cmd = [str(MANIM), "-w", "-l", scene_file, class_name]
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0 and video.exists():
        # WinError 32 on temp rename — video may still be valid
        err = (proc.stderr or proc.stdout or "")[-500:]
        if "WinError 32" in err:
            return True, str(video), None
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "")[-800:]
        return False, None, err
    if not video.exists() and temp.exists():
        try:
            temp.rename(video)
        except OSError:
            video = temp
    return True, str(video) if video.exists() else (str(temp) if temp.exists() else None), None


def append_manifest(rec: SceneRecord) -> None:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(rec), ensure_ascii=False) + "\n")


def filter_scenes(
    part: str | None,
    from_class: str | None,
    only: str | None,
) -> list[tuple[str, str]]:
    items = list(SCENES)
    if part:
        part = part.zfill(2)
        items = [s for s in items if f"/part{part}/" in s[0].replace("\\", "/")]
    if from_class:
        names = [c for _, c in items]
        if from_class in names:
            items = items[names.index(from_class):]
    if only:
        items = [s for s in items if s[1] == only]
    return items


def main() -> int:
    ap = argparse.ArgumentParser(description="Studio scene QA loop")
    ap.add_argument("--part", help="Only part number, e.g. 01")
    ap.add_argument("--from", dest="from_class", help="Start at class name")
    ap.add_argument("--only", help="Single class name")
    ap.add_argument("--list", action="store_true", help="List scenes and exit")
    ap.add_argument("--skip-render", action="store_true", help="Only extract frames from existing mp4")
    ap.add_argument("--render-only", action="store_true", help="Render without frames")
    args = ap.parse_args()

    if args.list:
        for f, c in SCENES:
            print(f"{c}\t{f}")
        return 0

    items = filter_scenes(args.part, args.from_class, args.only)
    if not items:
        print("No scenes matched.", file=sys.stderr)
        return 1

    print(f"QA loop: {len(items)} scene(s) -> {MANIFEST.relative_to(ROOT)}")
    for scene_file, class_name in items:
        ts = datetime.now(timezone.utc).isoformat()
        hints = load_audit_hints(scene_file)
        print(f"\n=== {class_name} ===")
        if hints:
            print("  Audit:", hints[0][:100], "...")

        video_path: str | None = None
        err: str | None = None
        ok = True

        if not args.skip_render:
            ok, video_path, err = render_scene(scene_file, class_name)
            print(f"  Render: {'OK' if ok else 'FAIL'}")

        if ok and (video_path or (VIDEOS / f"{class_name}.mp4").exists()):
            vp = Path(video_path or VIDEOS / f"{class_name}.mp4")
            if not args.render_only:
                try:
                    frames = extract_frames(vp, class_name)
                    print(f"  Frames: {', '.join(frames.values())}")
                except Exception as e:
                    frames = {}
                    err = str(e)
                    ok = False
                    print(f"  Frames: FAIL — {e}")
            else:
                frames = {}
        else:
            frames = {}

        rec = SceneRecord(
            ts=ts,
            scene_file=scene_file,
            class_name=class_name,
            render_ok=ok,
            video_path=video_path,
            frames=frames,
            audit_hints=hints,
            error=err,
            status="rendered" if ok else "failed",
        )
        append_manifest(rec)

        if ok and frames and not args.render_only:
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "vision_qa_check.py"), "--class", class_name],
                cwd=str(ROOT),
                check=False,
            )

    print(f"\nDone. Manifest: {MANIFEST}")
    print("Next: open frames in studio/_qa_loop/frames/<Class>/ — agent reads + audit + edits scene.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
