# 00 — Master Plan: Beyond Self-Driving Rework

> **Audience:** Claude Sonnet 4.6 executing the rework, plus the user reviewing.
> **Predecessor:** `drivex/PLAN.md` is now stale. This file supersedes it.
> **Created:** 2026-05-10

---

## What we're building

A 3Blue1Brown-style animated tutorial video summarizing the **ICCV 2025 "Beyond Self-Driving"** tutorial (UCLA Mobility Lab). Five parts:

| # | Title | Speaker | Estimated runtime | Scenes |
|---|---|---|---|---|
| 1 | Foundation Models for Autonomous Driving | Dr. Zhiyu Huang | ~10–12 min | 9 |
| 2 | Towards End-to-End Cooperative Automation | Zewei Zhou | ~10–12 min | 12 |
| 3 | Bridging Simulation and Reality in V2X | Zhaoliang Zheng | ~12–14 min | 14 |
| 4 | Pre-Training to Post-Training: Efficient V2X | Seth Z. Zhao | ~10–12 min | 10 |
| 5 | Scalable, Human-Centric Physical AI | Wayne Wu | ~12 min | 9 |

Plus a 3-scene Introduction.

**Total target runtime with narration: ~55–60 min.** The user is okay with this length and will trim later if needed.

---

## Why a rework is needed

Roughly a month ago the team produced a first draft (currently in `drivex/`) and a parallel white-theme experiment (`drivex_white/`). Three review rounds (`spec_prompts/spec_review_*.md`) flagged systematic issues:

1. **Background/color**: User now wants **white background** everywhere except part-transition cards. Current draft is mid-migration and inconsistent.
2. **Bubble bloat**: `ThoughtBubble` has a 3.2u min width and 1.5u min height regardless of text length, and centers text inside an oversized rounded rect with dark fill. User wants tight-fitting bubbles with thin borders.
3. **Overlap epidemic**: Roadmap labels overlap content; bubbles overlap boxes; arrows overlap text. Reviews 1, 2, 3 are mostly the same overlaps re-flagged across iterations.
4. **Mascots inconsistent**: PI sometimes speaks Vietnamese, position drifts, multiple bubbles appear in different spots when one bubble that fades in/out would do.
5. **Endings unclean**: Scenes leave residual text/objects at the end; merging videos is ugly.
6. **Narrative compression too aggressive**: When the script names a paper (V2VNet, Where2comm, EMMA…), the draft just lists it. The reason it's *named* in the original talk got lost.

This plan fixes all five categories systematically, not scene by scene with band-aids.

---

## Phases

The work is split into 4 phases. Do them in order — later phases depend on earlier infrastructure.

### Phase 1 — Component refresh (foundation)

Touch only `drivex/components/`. No scene edits yet.

| Step | File | Spec |
|---|---|---|
| 1.1 | `colors.py` | Confirm white-theme palette; add any missing constants (PEDESTRIAN, ROBOT_TEAL, SIM_PURPLE, MESH_GRAY, FP32_RED) for Part 5 |
| 1.2 | `thought_bubble.py` | Rewrite for tight fit + light fill + thin border. See [01_DESIGN_SYSTEM.md §Bubbles](01_DESIGN_SYSTEM.md#bubbles) |
| 1.3 | `mascots.py` | Adjust default colors for white BG (current `body_color="#2E75B6"` is fine; check stroke contrast) |
| 1.4 | `roadmap.py` | If labels overlap when used as `mini=True`, change to no-text strip (dots only) for in-scene use |
| 1.5 | `title_card.py` | Part transition cards may keep navy bg as a *deliberate* breath-mark between parts. Ensure they fade in cleanly from white and out cleanly to white. |
| 1.6 | `slide_helper.py` | Verify placeholder color works on white BG (`COL_GRAY_FILL = #F1F5F9` is OK) |

Deliverable: a single test scene `drivex/scenes/_smoke_test.py` that uses every component on a white BG. Pass = no overlap, all text readable, looks clean.

See [02_COMPONENTS.md](02_COMPONENTS.md) for exact edits.

### Phase 2 — Scene rework, part by part

Order: Intro → Part 1 → Part 2 → Part 3 → Part 4 → Part 5.

For each part:
1. Read the per-part plan ([04_PART_INTRO_AND_PART01.md](04_PART_INTRO_AND_PART01.md), [05_PART02.md](05_PART02.md), …).
2. Read the consolidated fix list from prior reviews ([09_FIX_CHECKLIST.md](09_FIX_CHECKLIST.md) — section for that part).
3. Read the original script ([materials/scripts/script_part{N}.md](../materials/scripts/)) to verify content fidelity.
4. Edit each scene file. Render at `-ql`. Iterate.
5. Mark scene done in the per-part plan checkbox.

Estimated time: ~1 day per part if scenes are mostly there, 2 days for parts that need new content (Part 5 stub scenes).

### Phase 3 — Render scripts & ordering

- Verify each `render_part*.ps1` script lists all scene files in narrative order.
- The scenes that were stubbed inline (e.g., `p02_s02..s05` originally lived inside `p02_s01_title.py`) have already been split into their own files — verify the render scripts reflect the new file layout.
- Add a top-level `render_all_final.ps1` that runs all parts at `-qh`.

### Phase 4 — Voiceover hookup (deferred)

Once visuals are signed off, add `manim-voiceover` annotations using the Vietnamese scripts in `materials/scripts/`. This is *not* in scope for the visual rework. Plan for it separately.

---

## Definition of done — per scene

A scene is done when **all** of the following hold:

- [ ] White background (or deliberately navy if it's a part-title card)
- [ ] No mid-scene overlap between any two visible mobjects (run at `-ql`, eyeball every second of the timeline)
- [ ] All on-screen text in English (translation of Vietnamese script, not literal copies)
- [ ] Bubbles: width ≈ text width + 0.6u; height ≈ text height + 0.4u; thin border; light fill; `tail` not occluding text
- [ ] Mascots: at most one PI bubble visible at a time; bubble appears, holds, fades, before next reveal
- [ ] Axes drawn before plotted data
- [ ] All transient objects faded out at scene end (final frame should match the next scene's opening BG only)
- [ ] Imports cleaned: no unused, no `sys.path.insert(...)` boilerplate beyond what's necessary
- [ ] No more `â”€` Unicode-mangled comments — replace with plain ASCII or remove

---

## File map for execution

| File | Purpose |
|---|---|
| [00_MASTER_PLAN.md](00_MASTER_PLAN.md) | This file |
| [01_DESIGN_SYSTEM.md](01_DESIGN_SYSTEM.md) | Colors, typography, bubble specs, mascot specs, layout rules |
| [02_COMPONENTS.md](02_COMPONENTS.md) | Exact edits to `drivex/components/*.py` |
| [03_NARRATIVE_AUDIT.md](03_NARRATIVE_AUDIT.md) | What the script says vs. what the draft animates — gaps to close |
| [04_PART_INTRO_AND_PART01.md](04_PART_INTRO_AND_PART01.md) | Per-scene plan, Intro + Part 1 |
| [05_PART02.md](05_PART02.md) | Per-scene plan, Part 2 |
| [06_PART03.md](06_PART03.md) | Per-scene plan, Part 3 |
| [07_PART04.md](07_PART04.md) | Per-scene plan, Part 4 |
| [08_PART05.md](08_PART05.md) | Per-scene plan, Part 5 |
| [09_FIX_CHECKLIST.md](09_FIX_CHECKLIST.md) | Consolidated fix list from 3 review rounds |
| [10_EXECUTION_WORKFLOW.md](10_EXECUTION_WORKFLOW.md) | Procedure Sonnet 4.6 should follow per scene |

---

## Acceptance gates

The user is the final reviewer. Two gates:

1. **Gate A — Component-level (after Phase 1)**: smoke test scene renders cleanly. User sights it.
2. **Gate B — Per-part visual review (after each Phase 2 part)**: render all scenes in the part at `-ql`, user reviews. New review notes get added to `09_FIX_CHECKLIST.md` as round-4 etc.

Do not proceed to the next part until the user signs off the current one.
