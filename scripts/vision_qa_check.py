#!/usr/bin/env python3
"""Heuristic + manifest-driven frame QA. Writes review JSON for agent vision follow-up.

Run after scene_qa_loop.py. Agent should still Read() the JPG paths listed.

Usage:
  python scripts/vision_qa_check.py
  python scripts/vision_qa_check.py --class P01S03AModular
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    raise SystemExit("pip install pillow numpy")

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "studio" / "_qa_loop" / "manifest.jsonl"
REVIEWS = ROOT / "studio" / "_qa_loop" / "reviews"
BG_CREAM = np.array([255, 249, 230])  # #FFF9E6


def load_manifest() -> list[dict]:
    if not MANIFEST.exists():
        return []
    rows = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
  # latest per class_name
    by_class: dict[str, dict] = {}
    for r in rows:
        by_class[r["class_name"]] = r
    return list(by_class.values())


def analyze_frame(path: Path) -> dict:
    img = Image.open(path).convert("RGB")
    arr = np.asarray(img, dtype=np.float32)
    h, w = arr.shape[:2]

    # Background: sample corners
    corners = np.vstack([
        arr[0:40, 0:40].reshape(-1, 3),
        arr[0:40, -40:].reshape(-1, 3),
        arr[-40:, 0:40].reshape(-1, 3),
        arr[-40:, -40:].reshape(-1, 3),
    ])
    bg_mean = corners.mean(axis=0)
    cream_dist = np.linalg.norm(bg_mean - BG_CREAM)

    # Ink pixels (dark content)
    gray = arr.mean(axis=2)
    ink = gray < 200
    ys, xs = np.where(ink)
    if len(xs) == 0:
        bbox = None
        fill_ratio = 0.0
    else:
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        bbox = dict(x0=int(x0), x1=int(x1), y0=int(y0), y1=int(y1))
        content_area = (x1 - x0) * (y1 - y0)
        fill_ratio = content_area / (w * h)

    issues = []
    if cream_dist > 35:
        issues.append(f"background_not_cream: corner_rgb={bg_mean.astype(int).tolist()}")
    if bbox:
        margin_l = bbox["x0"] / w
        margin_r = (w - bbox["x1"]) / w
        if margin_l > 0.38 or margin_r > 0.38:
            issues.append(f"content_off_center: margins L={margin_l:.2f} R={margin_r:.2f}")
        if fill_ratio < 0.08:
            issues.append(f"content_too_small: fill={fill_ratio:.2%} (chart may be scaled down)")
        if bbox["y1"] > h * 0.92:
            issues.append("content_clipped_bottom")
    else:
        issues.append("no_visible_content")

    return dict(
        path=str(path.relative_to(ROOT)),
        size=[w, h],
        bg_rgb=bg_mean.astype(int).tolist(),
        bbox=bbox,
        fill_ratio=round(fill_ratio, 4) if bbox else 0,
        issues=issues,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--class", dest="class_name", default="")
    args = ap.parse_args()
    REVIEWS.mkdir(parents=True, exist_ok=True)

    entries = load_manifest()
    if args.class_name:
        entries = [e for e in entries if e["class_name"] == args.class_name]

    for entry in entries:
        cls = entry["class_name"]
        frames = entry.get("frames") or {}
        if not frames:
            continue
        frame_reports = {}
        all_issues: list[str] = []
        for label, rel in frames.items():
            p = ROOT / rel
            if p.exists():
                rep = analyze_frame(p)
                frame_reports[label] = rep
                for iss in rep["issues"]:
                    all_issues.append(f"{label}: {iss}")

        review = {
            "class_name": cls,
            "scene_file": entry["scene_file"],
            "render_ok": entry.get("render_ok"),
            "frames": frame_reports,
            "heuristic_issues": all_issues,
            "agent_action": (
                "Read all frame JPGs in vision; cross-check SOURCE_MANIM_REFERENCE_AUDIT.md; "
                "port reference code if scene still uses pipeline boxes; fix overlap/scale."
            ),
            "frame_paths_for_agent": [str(ROOT / p) for p in frames.values()],
        }
        out = REVIEWS / f"{cls}.json"
        out.write_text(json.dumps(review, indent=2), encoding="utf-8")
        status = "PASS" if not all_issues else "ISSUES"
        print(f"{cls}: {status} ({len(all_issues)} heuristic flags)")
        for iss in all_issues[:6]:
            print(f"  - {iss}")

    print(f"\nReviews -> {REVIEWS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
