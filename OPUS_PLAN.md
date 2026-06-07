Compiled 2026-05-22 · Opus 4.7 Plan Mode
0. EXECUTIVE SUMMARY
This plan rebuilds the entire Manim production for ICCV 2025 "Beyond Self-Driving" as a new package, studio/, built from zero. The old beyond/ package (dark theme, 56 scenes, often slide-like) stays untouched as reference. The new package is light/pastel, uses CMU Serif with multi-color MarkupText, separates each concept into its own visual-first scene, and reuses idioms from Source_manim_reference/ as a mandatory rule.

The story arc remains the through-line from 5_PART_GUIDE.md: single-agent limits → cooperation → grounding in reality → efficiency → physical AI for everyone. The total scene count grows from 56 → 73 scenes (Intro 4, P1 14, P2 15, P3 16, P4 12, P5 12) because crowded scenes (P01-S03 three architectures, P01-S07 three VLAs, P03-S04 time+space calibration, P05-S05 stats+transform) are each split. Each scene is one question with one visual answer; each ends with a FadeOut so nothing leaks into the next.

Tooling stays the same (manim CE 0.20.1, base conda, Windows 11, PowerShell renders). The seven-session implementation roadmap (components → intro+P1 → P2 → P3 → P4 → P5+finale → render-fix-QA) keeps each session under ~14 scenes of code so a fresh Claude session can finish it from this plan alone.

1. DESIGN SYSTEM
1.1 Color Palette

# Backgrounds
BG_PAPER     = "#FAFAF8"   # Warm white — default body background
BG_CARD      = "#F0EEE8"   # Slightly darker — info panels, cards
BG_SECTION   = "#F5F3EF"   # Section divider panels
BG_TITLECARD = "#0F1419"   # Deep ink — ONLY part transition cards (I01, P0xS01)

# Pastel fills (panels, zones, soft fills)
PASTEL_BLUE   = "#C8DCFA"   # P1 Foundation
PASTEL_TEAL   = "#B0E8DA"   # P2 Cooperation
PASTEL_GREEN  = "#C8EDD0"   # P3 Sim-to-Real
PASTEL_AMBER  = "#FAE3B0"   # P4 Efficiency
PASTEL_PINK   = "#F9C8D8"   # P5 Physical AI

# Vivid accents (borders, key data, focal arrows)
ACCENT_BLUE   = "#2563EB"   # P1
ACCENT_TEAL   = "#0891B2"   # P2
ACCENT_GREEN  = "#16A34A"   # P3
ACCENT_AMBER  = "#D97706"   # P4
ACCENT_PINK   = "#DB2777"   # P5

# Ink (text)
INK_DARK   = "#1E293B"   # primary text — slate, never pure black
INK_MID    = "#475569"   # secondary text
INK_LIGHT  = "#94A3B8"   # caption, footnote

# Functional semantic
GOLD_RICH    = "#D97706"   # key numbers, insight emphasis
RED_ERROR    = "#DC2626"   # failure, bottleneck, before-fix
GREEN_FIX    = "#16A34A"   # success, after-fix, gain
PURPLE_MODEL = "#7C3AED"   # neural net, model internals
ORANGE_INFRA = "#EA580C"   # RSU, infrastructure
CYAN_RADAR   = "#06B6D4"   # radar, V2X waves
GOLD_KEY     = "#EAB308"   # gallery highlight (AutoVLA), part-finale gold

# Lines / structure
LINE_GRID  = "#E2E8F0"   # background grid
LINE_SEP   = "#CBD5E1"   # divider
LINE_ARROW = "#475569"   # default arrow stroke
1.2 Typography

FONT_PRIMARY = "CMU Serif"          # detected at runtime; fallback below
FONT_FALLBACK = "Latin Modern Roman" # used if CMU Serif not found
FONT_MONO    = "CMU Typewriter Text" # fallback "Courier New"

# Decision logic, executed at config load:
#   if "CMU Serif" in available_fonts: FONT_PRIMARY = "CMU Serif"
#   elif "Latin Modern Roman" in available_fonts: FONT_PRIMARY = "Latin Modern Roman"
#   else: raise RuntimeError("Install CMU Serif or LMR — Times New Roman is forbidden.")

# Sizes (px-equivalent, Manim font_size units)
SIZE_HERO   = 96   # title-card hero text
SIZE_TITLE  = 56   # scene titles
SIZE_H1     = 40   # section headers within scene
SIZE_BODY   = 28   # body text
SIZE_LABEL  = 22   # diagram labels
SIZE_CAPS   = 18   # captions, footnotes
SIZE_MICRO  = 14   # MINIMUM — never go below
1.3 MarkupText Patterns
Use Pango markup; reach for this whenever a single text run mixes two semantic concepts. Five canonical patterns:


# Pattern A — Value-vs-cost contrast
MarkupText(
    'Just <span foreground="#DC2626">1%</span> of scenarios '
    'cause <span foreground="#D97706">100%</span> of fatal accidents.',
    font="CMU Serif", font_size=28, color=INK_DARK,
)

# Pattern B — Flow with semantic color per stage
MarkupText(
    '<span foreground="#0891B2">Cameras</span> → '
    '<span foreground="#7C3AED">LLM reasoning</span> → '
    '<span foreground="#D97706">action</span>',
    font="CMU Serif", font_size=32, color=INK_DARK,
)

# Pattern C — Before/after compression
MarkupText(
    '<span foreground="#DC2626">100 MB · FP32</span>  →  '
    '<span foreground="#16A34A">0.33 MB · INT8</span>',
    font="CMU Serif", font_size=36, color=INK_DARK,
)

# Pattern D — Italic quote with gold key word
MarkupText(
    '<i>Cooperation is a <span foreground="#D97706">physics</span> solution,</i>\n'
    '<i>not an algorithm one.</i>',
    font="CMU Serif", font_size=40, color=INK_DARK,
)

# Pattern E — Inline icon-color cue (replaces unicode ✓)
MarkupText(
    '<span foreground="#16A34A">[OK]</span> No error accumulation\n'
    '<span foreground="#DC2626">[NO]</span> Black box — hard to debug',
    font="CMU Serif", font_size=24, color=INK_DARK,
)
Rules: Do NOT use MarkupText for equations (use MathTex). Do NOT mix MarkupText and MathTex inline in the same VGroup row. Do NOT use MarkupText for single-color text (use Text).

1.4 Layout Zones

Canvas: 14.22u wide × 8.00u tall (Manim CE default)

+--------------------------------------------------------------+ y= +4.0
|                          SAFE MARGIN                          |
|    +----------------------------------------------------+    |
|    |  TITLE ZONE        (y >  +2.8)                     |    |
|    |  Scene title + thin LINE_SEP divider               |    |
|    +----------------------------------------------------+    |  y= +2.8
|    |                                                    |    |
|    |  CONTENT ZONE      ( -3.2 < y < +2.7 )             |    |
|    |                                                    |    |
|    |    LEFT          CENTER          RIGHT             |    |
|    |  (x < -1.5)  (-1.5..+1.5)    (x > +1.5)            |    |
|    |                                                    |    |
|    |                                                    |    |
|    +----------------------------------------------------+    |  y= -3.2
|    |  FOOTER ZONE       (y < -3.2)                       |    |
|    |  small footnotes, key-number callouts               |    |
|    +----------------------------------------------------+    |
|                          SAFE MARGIN                          |
+--------------------------------------------------------------+ y= -4.0
   x = -7.11   ...   -6.5 (text edge limit)   ...   +6.5   ...   +7.11
Hard rules: text bounding box never crosses x = ±6.5 or y = ±3.7. Always use _open() / _close() from StudioScene so every scene fades clean.

1.5 Scene Type Taxonomy
Code	Name	Visual signature	Closing beat
TYPE_TITLE_CINEMATIC	Cinematic title	Particle/forge assembly of headline	Hold 1.5–2s, fade to BG_PAPER
TYPE_PROBLEM_FIRST	Problem-first	Show failure/bottleneck → reveal solution	Solution lingers 1s
TYPE_BEFORE_AFTER	Before/after	Two columns + transform arrow at center	Right column glow, left dim
TYPE_PIPELINE_FLOW	Pipeline w/ packets	Block diagram, moving data packets	Packets clear, blocks dim
TYPE_TIMELINE	Timeline evolution	Spine + beads dropping in sequence	Last bead pulse, others dim
TYPE_CHART_REVEAL	Chart reveal	Axes first, then data, then annotation	Annotation hold 1.5s
TYPE_AGENT_SIM	Agent simulation	City/intersection + moving agents + signals	Camera settle, agents continue
TYPE_GALLERY_CARDS	Gallery cards	Method cards with mini mechanism inside each	Cards arrange, hero card glows
TYPE_BRIDGE_RECAP	Bridge	3 recap bullets + 1 forward question	Forward question gold, hold 1.5s
TYPE_MATH_REVEAL	Math/matrix reveal	Equation/matrix animates into geometry	Equation collapses into result
TYPE_UNCERTAINTY_CLOUD	Probability field	Gaussian clouds, density overlays	Clouds converge to single point
TYPE_3D_OPENGL	3D scene	OpenGL renderer, RSU/radar shells, agents	Camera return, full fade
2. COMPONENT ARCHITECTURE
2.1 File Structure

studio/
├── __init__.py
├── config.py                 # BG_PAPER, FONT_PRIMARY decision, quality presets
├── DESIGN_SYSTEM.md          # this section, persisted as docs
├── components/
│   ├── __init__.py           # re-exports for `from studio.components import *`
│   ├── colors.py             # palette constants (Section 1.1)
│   ├── typography.py         # FONT_PRIMARY decision, size constants, MarkupText builders
│   ├── base_scene.py         # StudioScene + Studio3DScene base classes
│   ├── pipeline.py           # pipeline_block, pipeline_row, pipeline_flow
│   ├── charts.py             # axes_deploy, bar_reveal, curve_trace, scatter_rain
│   ├── agents.py             # vehicle_icon, pedestrian_icon, rsu_icon, drone_icon
│   ├── signals.py            # radar_shells, sensor_cone, v2x_link, ambient_glow
│   ├── annotations.py        # callout, thought_bubble, contribution_badge, key_number
│   ├── animations.py         # scene_open, scene_close, particle_assemble, forge_text
│   └── layout.py             # zone helpers (place_title, place_left, place_right, footer)
└── scenes/
    ├── intro/                # I01..I04
    ├── part01/               # P01-S01..P01-S14
    ├── part02/               # P02-S01..P02-S15
    ├── part03/               # P03-S01..P03-S16
    ├── part04/               # P04-S01..P04-S12
    └── part05/               # P05-S01..P05-S12
2.2 API Spec Per Component
2.2.1 studio/components/colors.py
Plain module of Final[str] hex constants matching Section 1.1. Exports PART_PALETTES: dict[int, dict] with keys pastel, accent, ink per part. No functions.

2.2.2 studio/components/typography.py

def detect_primary_font() -> str:
    """Return 'CMU Serif' if available, else 'Latin Modern Roman', else raise."""

FONT_PRIMARY: str = detect_primary_font()
FONT_MONO: str = "CMU Typewriter Text"   # falls back to Courier New if missing

SIZE_HERO, SIZE_TITLE, SIZE_H1, SIZE_BODY, SIZE_LABEL, SIZE_CAPS, SIZE_MICRO = (
    96, 56, 40, 28, 22, 18, 14,
)

def text(s: str, size: int = SIZE_BODY, color: str = INK_DARK, **kw) -> Text:
    """Studio Text default — uses FONT_PRIMARY, INK_DARK, weight=NORMAL."""

def markup(s: str, size: int = SIZE_BODY, **kw) -> MarkupText:
    """Studio MarkupText default — same font, accepts <span foreground=...> tags."""

def math(s: str, size: int = SIZE_BODY, color: str = INK_DARK) -> MathTex:
    """Studio MathTex default — uses tex_template that loads lmodern."""

def gold_key_number(s: str, size: int = SIZE_HERO) -> Text:
    """Big GOLD_RICH key number for footer-zone callouts."""
2.2.3 studio/components/base_scene.py

class StudioScene(Scene):
    PART_NUM: int = 0           # 0 = intro/finale; 1..5 = parts
    PART_COLOR: str = ACCENT_BLUE
    PART_PASTEL: str = PASTEL_BLUE
    SCENE_TITLE: str = ""       # short title shown in TITLE ZONE

    def setup(self):
        self.camera.background_color = BG_PAPER

    def _open(self, title: str | None = None) -> VGroup:
        """Create title (top), separator line under title, and a small part-color dot.
        Returns VGroup so subclass can FadeOut later. Title text always uses Text(SIZE_TITLE).
        """

    def _close(self, *extra: Mobject, fade_lag: float = 0.04) -> None:
        """LaggedStart FadeOut everything still on screen plus `extra`. Always last call."""

    def _roadmap_strip(self) -> VGroup:
        """Optional 5-dot strip at footer for part title cards. Active dot = PART_COLOR."""


class Studio3DScene(ThreeDScene):
    """Same defaults but inherits ThreeDScene; sets opening camera phi=70, theta=-30."""
2.2.4 studio/components/pipeline.py

def pipeline_block(
    label: str,
    *,
    width: float = 2.4,
    height: float = 1.0,
    fill: str = PASTEL_BLUE,
    stroke: str = ACCENT_BLUE,
) -> VGroup:
    """Rounded rect + centered label. Returns VGroup(rect, label)."""

def pipeline_row(blocks: list[VGroup], *, gap: float = 0.6) -> VGroup:
    """Arrange blocks horizontally with arrows between them."""

def pipeline_arrow(start: Mobject, end: Mobject, *, color: str = LINE_ARROW) -> Arrow:
    """Studio default arrow: stroke 2.5, tip_length 0.18."""

def pipeline_flow(
    blocks: list[VGroup], *, packet_color: str = CYAN_RADAR, n_packets: int = 4,
) -> Animation:
    """LaggedStart of packets traveling through arrows between blocks.
    Adapted from network_flow.py:55 `get_block` depth motif."""
2.2.5 studio/components/charts.py

def axes_deploy(
    x_range: tuple, y_range: tuple,
    *, x_label: str = "", y_label: str = "",
) -> tuple[Axes, Animation]:
    """Returns (axes, deploy_animation). Animation = Create(x_line) then Create(y_line)
    then FadeIn(labels). Always call this BEFORE plotting data."""

def bar_reveal(axes: Axes, values: list[float], *, colors: list[str]) -> AnimationGroup:
    """LaggedStart bars growing from y=0. One color per bar."""

def curve_trace(axes: Axes, fn: Callable, *, color: str = ACCENT_BLUE) -> Animation:
    """Trace a function curve with a glowing leading dot.
    Pattern adapted from: generalization/p46_56.py — power-law curve reveal."""

def scatter_rain(axes: Axes, points: list[tuple], *, color: str) -> Animation:
    """Points fall in from y_max position to their final coord. Used for failure scatter."""
2.2.6 studio/components/agents.py

def vehicle_icon(*, color: str = ACCENT_BLUE, scale: float = 1.0) -> VGroup:
    """Simple top-down car: rounded rect body + two small wheels + heading triangle."""

def pedestrian_icon(*, color: str = GOLD_KEY) -> VGroup:
    """Stick figure: head circle + body line + 4 limbs. Used for human-aware scenes."""

def rsu_icon(*, color: str = ORANGE_INFRA) -> VGroup:
    """2D top-down RSU: square base + triangle antenna + small dot."""

def rsu_tower_3d(*, color: str = ORANGE_INFRA, height: float = 2.0) -> VGroup:
    """3D lattice tower with 4 legs + cross struts.
    Pattern adapted from: 3b1b_videos/_2026/hairy_ball/model3d.py:68 RadioTower."""

def drone_icon(*, color: str = INK_LIGHT) -> VGroup:
    """Top-down drone: center circle + 4 rotor circles."""

def agent_trail(mob: Mobject, *, color: str, max_length: float = 2.0) -> TracedPath:
    """Fading trail behind a moving agent. Adapted from random_puzzles.py:18 DotHistory."""
2.2.7 studio/components/signals.py

def radar_shells_2d(
    center: np.ndarray, *, color: str = CYAN_RADAR,
    n_shells: int = 4, max_radius: float = 3.0,
) -> tuple[VGroup, Animation]:
    """2D version: concentric circles expanding outward with opacity falloff."""

def radar_shells_3d(
    center: np.ndarray, *, color: str = CYAN_RADAR,
    n_shells: int = 5, max_radius: float = 3.5,
) -> tuple[VGroup, Animation]:
    """3D expanding spherical shells via ValueTracker.
    Pattern adapted from: hairy_ball/model3d.py:260 RadioBroadcast.update_shells."""

def sensor_cone(
    source: np.ndarray, angle: float, *, color: str = ACCENT_AMBER,
    spread: float = PI/4, length: float = 3.5,
) -> AnnularSector:
    """Sensor frustum / camera FOV cone.
    Pattern adapted from: welchlabs/once_useful_constructs/light.py:95 Spotlight."""

def v2x_link(
    a: Mobject, b: Mobject, *, color: str = ACCENT_TEAL,
) -> tuple[Line, Animation]:
    """Thin line between two agents with a moving packet pulse."""

def ambient_glow(center: Mobject, *, color: str, radius: float = 0.8) -> VGroup:
    """Concentric annuli with radial opacity falloff.
    Pattern adapted from: light.py:65 AmbientLight."""

def interference_pattern(sources: list[np.ndarray], *, color: str) -> VGroup:
    """Three-source wave interference visualization for P02-S05 hero moment."""
2.2.8 studio/components/annotations.py

def callout(text: str, target: Mobject, *, side: str = "right") -> VGroup:
    """Tight-fit speech callout (text + thin border + leader line).
    Bubble width = text_width + 0.4. Slim 1.5pt border."""

def thought_bubble(text: str, target: Mobject) -> VGroup:
    """Pi-style thought bubble — three small circles + main bubble. Used sparingly."""

def contribution_badge(label: str, *, color: str = GOLD_KEY) -> VGroup:
    """Gold rounded badge for paper credits: '[IROS 2025 Best Paper · UCLA]'."""

def key_number(value: str, label: str, *, color: str = GOLD_RICH) -> VGroup:
    """SIZE_HERO value + SIZE_LABEL caption underneath. For footer zone."""

def failure_icon(*, kind: str) -> VGroup:
    """One of: 'phone_pedestrian', 'inverted_lights', 'snow_lane'.
    Simple line-art illustration, not photo."""
2.2.9 studio/components/animations.py

def forge_text(s: str, *, size: int = SIZE_HERO, color: str = GOLD_RICH) -> Animation:
    """Glyph-by-glyph reveal: each char appears white-hot, settles to color.
    Used for title cards. Variable lag per char for hand-drawn feel."""

def particle_assemble(target: VMobject, *, n_particles: int = 200) -> Animation:
    """Explode from origin, then converge into target shape.
    Pattern adapted from: 3b1b_videos/custom/logo.py:192 LogoGenerationFlurry."""

def fivefold_assemble(target: VGroup) -> Animation:
    """Radial 5-fold assembly for the 5-part roadmap.
    Pattern adapted from: 3b1b_videos/custom/logo.py:216 LogoGenerationFivefold."""

def scan_reveal(target: VMobject, *, direction: str = "down") -> Animation:
    """Holographic scan-line sweep that reveals target left-to-right or top-down."""

def dust_dissolve(*targets: Mobject) -> Animation:
    """Particles drift upward as objects fade. Inverse of particle_assemble."""

def write_chiseled(t: Text, *, run_time: float = 3.0) -> Animation:
    """Slow Write — used for the project's three quote moments (I02, P02-S05, finale)."""
2.2.10 studio/components/layout.py

TITLE_Y: float = 3.2     # title baseline
SEP_Y: float = 2.85      # separator line
CONTENT_TOP: float = 2.7
CONTENT_BOTTOM: float = -3.2
FOOTER_Y: float = -3.5
LEFT_X: float = -4.0
RIGHT_X: float = 4.0
CENTER_X: float = 0.0
MAX_TEXT_X: float = 6.5

def place_title(t: Mobject) -> Mobject: ...
def place_left(t: Mobject, *, y: float = 0.0) -> Mobject: ...
def place_right(t: Mobject, *, y: float = 0.0) -> Mobject: ...
def place_footer(t: Mobject) -> Mobject: ...

def two_column(left: VGroup, right: VGroup, *, gap: float = 1.0) -> VGroup: ...
def three_column(left: VGroup, mid: VGroup, right: VGroup) -> VGroup: ...
def grid_4(items: list[VGroup]) -> VGroup: ...
3. FULL SCENE INVENTORY
Scene ID	New file name	Type	Slide ref	Script ref	Visual core	Reference source	MarkupText use	Dur
I-01	i01_title_card.py	TITLE_CINEMATIC	—	5_PART_GUIDE I-01	200-particle burst → forge "BEYOND SELF-DRIVING" wordmark in GOLD_RICH	logo.py:192 LogoGenerationFlurry	speaker line italic gold	25s
I-02	i02_the_hook.py	3D_OPENGL	—	5_PART_GUIDE I-02	3D intersection, radar shells distorted by building, blind zone red → 3 cars cooperate, zone green, pedestrian reveal	model3d.py:260 RadioBroadcast + light.py:95 Spotlight + optics/adding_waves.py	"smart agent / blind to occlusion" + Pattern D quote	75s
I-03	i03_roadmap.py	TITLE_CINEMATIC	—	5_PART_GUIDE I-03	Center star pulsing, 5 orbital nodes appear with part colors, lightning trace 1→5	logo.py:216 LogoGenerationFivefold	each part label in its pastel	30s
I-04	i04_bridge_to_p1.py	BRIDGE_RECAP	—	implicit	3 setup bullets + "Why can FM solve this?" forward question	—	forward Q in gold italic	18s
P01-S01	p01_s01_title.py	TITLE_CINEMATIC	Part1 slide 1	script_p1 Slide 1	Forge "Foundation Models / for Autonomous Driving" + Zhiyu Huang + opening quote	logo.py:103 LogoGenerationTemplate	quote italic gold	25s
P01-S02a	p01_s02a_genai_timeline.py	TIMELINE	Part1 slide 3	script_p1 Slide 3	2020→2025 spine, GPT-3/CLIP/ChatGPT/GPT-4 beads with bloom on ChatGPT and GPT-4	covid.py:770 ShowLogisticCurve	year labels in INK_MID	35s
P01-S02b	p01_s02b_fm_definition.py	CHART_REVEAL	Part1 slide 3-4	script_p1 Slide 3-4	Hub diagram: data sources left → FM hub center → downstream tasks right	network_flow.py:73 show_initial_text_embedding	"<span>self-supervised</span> learning" key tag	35s
P01-S03a	p01_s03a_modular.py	PROBLEM_FIRST	Part1 slide 5	script_p1 Slide 5	5-block modular pipeline builds clean → noise particle in Perception cascades, arrows flash red, car drifts	network_flow.py:227 mention_repetitions (motif)	3 failure badges via Pattern E	35s
P01-S03b	p01_s03b_e2e.py	PROBLEM_FIRST	Part1 slide 5	script_p1 Slide 5	Single big box with neurons pulsing inside; sensors in, action out; black-box badge	network_flow.py:174 progress_through_mlp_block	"[OK] joint opt / [WARN] black box" Pattern E	30s
P01-S03c	p01_s03c_hybrid.py	PROBLEM_FIRST	Part1 slide 5	script_p1 Slide 5	Hybrid combines ML perception+planning with classical control; ends "but all 3 share a flaw"	—	"All three: <red>long tail</red>"	28s
P01-S04a	p01_s04a_longtail_problem.py	PROBLEM_FIRST	Part1 slide 6	script_p1 Slide 6	3 failure-icon cards (phone-pedestrian, inverted-lights, snow-lane), then power-law curve traces, red tail	generalization/p8_15.py + decision_boundary_utils.py	"1% scenarios → <red>100%</red> accidents" Pattern A	40s
P01-S04b	p01_s04b_longtail_insight.py	PROBLEM_FIRST	Part1 slide 6	script_p1 Slide 6	Dim overlay, single quote: "We need generalist experience to handle the long tail." Gold, hold 2.5s	logo.py:211 WrittenLogo write-chiseled idiom	quote in gold italic + Pattern D	25s
P01-S05	p01_s05_fm_empower.py	PIPELINE_FLOW	Part1 slide 7	script_p1 Slide 7	Hub-and-spoke: VFM/VGM/LLM/MLLM left → hexagonal "Foundation Models" hub → AV needs right; hex-packet flow	network_flow.py:73 + custom packet idiom	source labels each in their accent color	45s
P01-S06	p01_s06_vla_roadmap.py	TIMELINE	Part1 slide 9-11	script_p1 Slide 9-11	2023→2025 VLA timeline beads; quote about language interface; DriveLM/CoVLA dataset chips drop	network_flow.py:73	quote attribution caption	35s
P01-S07a	p01_s07a_bevdriver.py	GALLERY_CARDS	Part1 slide 12-14	script_p1 Slide 12-14	LiDAR point cloud → BEV grid press-down → LLM box; teal card with mini mechanism	vla/p31_61_1.py:214 make_embedding_row	"3D → <teal>BEV</teal> → LLM" Pattern B	40s
P01-S07b	p01_s07b_emma.py	GALLERY_CARDS	Part1 slide 14-15	script_p1 Slide 14-15	Camera → Gemini box → chain-of-thought typed lines → simultaneous outputs (trajectory, bbox, road graph)	vla/p31_61_1.py:149 P52_61	chain-of-thought lines colored by output type	45s
P01-S07c	p01_s07c_drivevlm.py	BEFORE_AFTER	Part1 slide 16	script_p1 Slide 16	Two parallel tracks: Fast (gray, narrow, fast) above; Slow (color, wide, deep) below; merge to one output	network_flow.py:161 play_simple_attention_animation	"Fast for <gray>routine</gray>. Slow for <gold>complex</gold>."	35s
P01-S08a	p01_s08a_autovla_switch.py	GALLERY_CARDS	Part1 slide 17-18	script_p1 Slide 17-18	Gold AutoVLA card; central switch; simple scene → fast mode; complex scene → reasoning mode	vla/p31_61_1.py:671 P34_Pickup	chain-of-thought lines in gold italic	45s
P01-S08b	p01_s08b_autovla_results.py	CHART_REVEAL	Part1 slide 18-20	script_p1 Slide 18-20	nuPlan/nuScenes bar comparison + counter "+10.6% planning, -66.8% runtime"; IROS badge	covid.py:770 ShowLogisticCurve + p31_61_1.py:654 row transform	gold key numbers	35s
P01-S09	p01_s09_takeaways.py	BRIDGE_RECAP	Part1 slide 22	script_p1 Slide 22	4 takeaway bullets, each with a tiny icon; honest-limits italic note	—	bullet keywords colored	30s
P01-S10	p01_s10_bridge_to_p2.py	BRIDGE_RECAP	Part1 slide 24	script_p1 Slide 24	Recap "AutoVLA handles long tail" + forward "But it still only sees what's in front of it."	—	forward Q gold italic	18s
P02-S01	p02_s01_title.py	TITLE_CINEMATIC	Part2 slide 1	script_p2 Slide 1	Teal wave forge of "Towards End-to-End Cooperative Automation" + Zhou + roadmap (P2 lit)	logo.py:163 SortingLogoGeneration	quote italic	25s
P02-S02a	p02_s02a_119m.py	CHART_REVEAL	Part2 slide 2	script_p2 Slide 2-3	Counter rolls 0 → 1,190,000 in red, then "people die / yr" caption	covid.py:205 ViralSpreadModel	"1.19M / 94% / 80%" Pattern A	30s
P02-S02b	p02_s02b_waymo_reduce.py	CHART_REVEAL	Part2 slide 2	script_p2 Slide 2-3	10×10 icon grid; 94 red icons; brace shows 80% reduction Waymo	covid.py:723 ViralSpreadModelWithClusters	"Waymo: <green>-80%</green> injuries"	25s
P02-S03	p02_s03_e2e_evolution.py	TIMELINE	Part2 slide 4	script_p2 Slide 4	PnPNet→GameFormer→UniAD→DiffusionDrive bead drop on slight upward spine	network_flow.py:227	each method label in distinct hue	40s
P02-S04a	p02_s04a_occlusion_problem.py	PROBLEM_FIRST	Part2 slide 5	script_p2 Slide 5	Single car, LiDAR scan blocked by truck, blind zone pulses red; "Chưa." (Not yet) hold	light.py:95 Spotlight	"blind to <red>occlusion</red>"	30s
P02-S05	p02_s05_radar_waves.py	3D_OPENGL	Part2 slide 5	script_p2 Slide 5 + 5_PART_GUIDE P2-04	THE hero scene — full radar gravitational waves cinematic. Building drop, distortion, 3-car cooperation, interference pattern, pedestrian reveal, "Cooperation is a physics solution" quote	model3d.py:260 RadioBroadcast + adding_waves.py + light.py:95	quote Pattern D with gold "physics"	75s
P02-S06	p02_s06_related_works.py	TIMELINE	Part2 slide 6-8	script_p2 Slide 6-8	V2VNet→V2X-ViT→Where2comm→CodeFilling chain, each "addresses prior bottleneck" tag, gap at end	network_flow.py:227 mention_repetitions	"bottleneck" labels in red	50s
P02-S07	p02_s07_research_gaps.py	BEFORE_AFTER	Part2 slide 9	script_p2 Slide 9	Top row single-frame fusion → bottom row multi-frame multi-task fusion; 3 trajectories show why temporal matters	network_flow.py:174 progress_through_mlp_block	"single-frame" vs "<gold>multi-frame multi-task</gold>"	35s
P02-S08	p02_s08_three_questions.py	GALLERY_CARDS	Part2 slide 10	script_p2 Slide 10	What/When/How three cards, each with mini-animation; converge to "V2XPnP answers all three"	—	"<teal>What?</teal> <amber>When?</amber> <purple>How?</purple>"	35s
P02-S09	p02_s09_v2xpnp_arch.py	PIPELINE_FLOW	Part2 slide 10-15	script_p2 Slide 10-15	3-tier framework: agents → one-step transmit (burst) → temporal+spatial attention → 3 task outputs	network_flow.py:161 play_simple_attention_animation + p31_61_1.py:149 P52_61	attention head labels each colored	60s
P02-S10	p02_s10_v2xpnp_dataset.py	CHART_REVEAL	Part2 slide 13-14	script_p2 Slide 12-15	V2XPnP-Seq stats counters: 2 cars, 2 infra, 40K LiDAR, 208K cam, HD maps	covid.py:770	gold key numbers	30s
P02-S11a	p02_s11a_turbotrain_problem.py	CHART_REVEAL	Part2 slide 16	script_p2 Slide 16-22	AP×EPA chart: orange dots rain (one-time fails), blue dots stage by stage (manual 4-stage)	backprop_3/geometry_while_learning_2.py	"120 epochs, manual" caption	35s
P02-S11b	p02_s11b_turbotrain_solution.py	BEFORE_AFTER	Part2 slide 18-22	script_p2 Slide 18-22	Gradient conflict (3 arrows tug), then TurboTrain 2-stage smooth spiral; counter 120→45 epochs	backprop_3/geometry_while_learning_2.py	"120→<green>45</green> epochs" Pattern C	50s
P02-S12	p02_s12_riskmap.py	AGENT_SIM	Part2 slide 23-25	script_p2 Slide 23-25	Top-down road; heatmap risk field; other car swerves → red zone blooms; ego trajectory curves around	region.py:50 plane_partition + e_field.py	"Risk is a <gold>language</gold>, not a bounding box."	50s
P02-S13	p02_s13_summary.py	BRIDGE_RECAP	Part2 slide 26-28	script_p2 Slide 26-28	V2XPnP / TurboTrain / RiskMap recap as 3 stacked panels	—	each method gold-bordered card	25s
P02-S14	p02_s14_bridge_to_p3.py	BRIDGE_RECAP	Part2 cầu nối	script_p2 cầu nối	Forward: "But all of this needs real data from real sensors on real roads."	—	forward Q gold italic	18s
P03-S01	p03_s01_title.py	TITLE_CINEMATIC	Part3 slide 1	script_p3 Slide 1	Green forge of "Bridging Simulation and Reality" + Zheng + "Theory without deployment is just fiction"	logo.py:103	quote italic	25s
P03-S02	p03_s02_sim_real_gap.py	BEFORE_AFTER	Part3 slide 5	script_p3 Slide 3-5	Screen split by lightning crack; left teal sim-world clean; right amber real-world messy; "Sim-to-Real Gap" red label	optics/objects.py	"<teal>Sim</teal>	<amber>Real</amber>" Pattern B
P03-S03	p03_s03_smart_intersection.py	AGENT_SIM	Part3 slide 6-11	script_p3 Slide 6-11	UCLA campus overhead map, 2 infrastructure nodes pulse, hardware specs deploy as blueprint, all sensors activate simultaneously	model3d.py:68 RadioTower + light.py:95 Spotlight	sensor labels colored by modality	50s
P03-S04a	p03_s04a_time_calibration.py	PROBLEM_FIRST	Part3 slide 12-13	script_p3 Slide 12-17	Car 60km/h; infra observation lags 50ms → 83cm position error; GPS+hardware trigger sync animation	optics/wave_machine.py	"<red>50 ms</red> → <amber>83 cm</amber> error" Pattern A	35s
P03-S04b	p03_s04b_space_calibration.py	MATH_REVEAL	Part3 slide 14-17	script_p3 Slide 12-17	Two point clouds in own frames; transform matrix flies in, fuse into one; bad calib → ghost object red flash	vector_space_scene.py:204 LinearTransformationScene + linear_algebra.py:32	matrix elements highlighted	40s
P03-S05	p03_s05_data_collection.py	TIMELINE	Part3 slide 18-22	script_p3 Slide 18-22	Basic routes (R turn / L turn / straight) → combined routes; times of day grid; V2X-Real + V2XPnP-Seq dataset cards	—	dataset name in gold badges	35s
P03-S06	p03_s06_localization_role.py	PROBLEM_FIRST	Part3 slide 23-28	script_p3 Slide 23-32	Two views of same object; without precise localization, fused point cloud is wrong (worse than single); with precise localization, clean fuse	region.py:50 + vector_space_scene.py	"no loc → <red>worse than single</red>"	40s
P03-S07	p03_s07_kalman_filter.py	UNCERTAINTY_CLOUD	Part3 slide 28-32	script_p3 Slide 23-32	Three rivers: GNSS (5 Hz, blocked by buildings) + IMU (100 Hz, drifts) + LiDAR-map (1 Hz, accurate); confluence at Kalman node; output 100 Hz smooth stream	_2018/uncertainty.py + random_puzzles.py:363	"<blue>5 Hz</blue> + <amber>100 Hz</amber> + <green>1 Hz</green> → <gold>100 Hz lane-level</gold>"	50s
P03-S08	p03_s08_cooperfuse.py	UNCERTAINTY_CLOUD	Part3 slide 33-43	script_p3 Slide 33-43	Two bounding boxes from V & I, two Gaussian ellipses, NMS (left, throws info away) vs CooperFuse (right, multiplies Gaussians → tighter result)	region.py + uncertainty.py	"NMS: <red>discard</red>" vs "CooperFuse: <green>fuse</green>"	50s
P03-S09	p03_s09_v2x_realo.py	PIPELINE_FLOW	Part3 slide 44-49	script_p3 Slide 44-49	BEV feature large → compress 32× → 0.5 MB per message → real-time over V2X	network_flow.py:55 get_block	"<red>16 MB</red> → <green>0.5 MB</green> · 32× compress" Pattern C	45s
P03-S10	p03_s10_opencda_ros.py	PIPELINE_FLOW	Part3 slide 50-54	script_p3 Slide 50-59	Real-world ROS bag → OpenCDA-ROS bridge → CARLA simulation; arrows both directions	network_flow.py:55 + graph_theory.py:56	bidirectional arrow labels	40s
P03-S11	p03_s11_simboost.py	PIPELINE_FLOW	Part3 slide 55-58	script_p3 Slide 50-59	CDA-SimBoost loop: real data → digital twin → challenging scenarios → train → deploy back	covid.py:723 + ShowLogisticCurve	"challenging <amber>scenarios</amber>" inline	40s
P03-S12	p03_s12_digital_twin.py	AGENT_SIM	Part3 slide 50-54	script_p3 Slide 50-54	Scan line sweeps L→R, real-side dissolves into digital-twin side; both sides live-sync agents	optics/objects.py	"OpenCDA → real-time <gold>digital twin</gold>"	45s
P03-S13	p03_s13_infrax.py	GALLERY_CARDS	Part3 slide 58-59	script_p3 Slide 58-59	OpenCDA-InfraX: 4 mini-cards (sensor config / multi-modality / weather / vector maps)	—	4 feature tags in pastel	30s
P03-S14	p03_s14_summary.py	BRIDGE_RECAP	Part3 summary	implicit	4 contributions recap (intersection, calibration, fusion, twin)	—	each as gold badge	25s
P03-S15	p03_s15_bridge_to_p4.py	BRIDGE_RECAP	Part3 cầu nối	script_p3 cầu nối	"Now it works — but is it efficient enough to deploy?" 3 bottlenecks tease	—	forward Q gold italic	18s
P04-S01	p04_s01_title.py	TITLE_CINEMATIC	Part4 slide 1	script_p4 Slide 1	Amber forge "From Pre-Training to Post-Training" + Zhao + "A system that can't run real-time is a demo"	logo.py:163	quote italic	25s
P04-S02	p04_s02_v2x_overview.py	TIMELINE	Part4 slide 2-7	script_p4 Slide 2-7	Quick V2X recap timeline + USDOT smart-intersection mention; 3 bottlenecks teaser	network_flow.py:227	3 bottleneck tags in red	30s
P04-S03	p04_s03_annotation_cost.py	CHART_REVEAL	Part4 slide 8-9	script_p4 Slide 9-14	3-bar chart V2V4Real / DAIR-V2X / V2X-Real; counter 240K/460K/1.2M; "5× in 2 years" brace	ShowLogisticCurve	"<gold>5×</gold> in 2 years" key	40s
P04-S04	p04_s04_coopre_masked.py	AGENT_SIM	Part4 slide 9-14	script_p4 Slide 9-14	BEV grid; 40% voxels mask; Agent B particles stream into masked voxels reconstructing; results bars; IROS badge	spheres_talk/volumes.py:53 VolumeGrid + p31_61_1.py:332 diffusion frames	"50% data → <green>same perf</green> / 100% data → <gold>+4% AP</gold>"	75s
P04-S05	p04_s05_turbotrain_landscape.py	UNCERTAINTY_CLOUD	Part4 slide 15-22	script_p4 Slide 15-22	Loss-landscape surface; 3 task gradient arrows tug; without TurboTrain zigzag chaos; with: smooth spiral to optimum	backprop_3/geometry_while_learning_2.py + decision_boundary_utils.py	"<red>conflict</red> → <green>smooth</green>"	60s
P04-S06	p04_s06_latency_chain.py	PIPELINE_FLOW	Part4 slide 22-23	script_p4 Slide 22-31	Local inference → comm → fusion inference, each block has time budget; bottleneck glows red	optics/wave_machine.py	"<red>FP32</red> too slow"	40s
P04-S07	p04_s07_arithmetic_cost.py	MATH_REVEAL	Part4 slide 24-26	script_p4 Slide 22-31	FP32 multiplication vs INT8 add; memory access 640 pJ vs 5 pJ visualized as energy droplets	network_flow.py:55	"<red>640 pJ</red> vs <green>5 pJ</green>" Pattern A	35s
P04-S08	p04_s08_quantv2x.py	PIPELINE_FLOW	Part4 slide 27-31	script_p4 Slide 27-31	3-stage QuantV2X: pretrain → codebook → PTQ; BEV blob squeeze from FP32 100MB to INT8 0.33MB, channel opens	network_flow.py block stack + custom compression motif	"<red>100 MB · FP32</red> → <green>0.33 MB · INT8</green> · <gold>300×</gold>" Pattern C	65s
P04-S09	p04_s09_efficiency_summary.py	BRIDGE_RECAP	Part4 recap	implicit	Data / training / inference 3-card recap with key numbers	—	each card gold-bordered	25s
P04-S10	p04_s10_bridge_to_p5.py	BRIDGE_RECAP	Part4 cầu nối	script_p4 cầu nối	"But Parts 2-4 are all about cars. The physical world has people, robots, scooters..."	—	forward Q in pink	18s
P05-S01	p05_s01_title.py	TITLE_CINEMATIC	Part5 slide 1	script_p5 Slide 1	Pink wave forge "Scalable, Human-Centric Physical AI" + Wayne Wu + "Beyond cars — to any agent, any space"; 5 roadmap nodes all light up simultaneously for the first time	logo.py:216 LogoGenerationFivefold	quote italic gold	30s
P05-S02a	p05_s02a_llm_vs_robot.py	BEFORE_AFTER	Part5 slide 2-4	script_p5 Slide 2-8	Internet → LLM flood vs Robot → trickle; data volume disparity	covid.py:205 + ShowLogisticCurve	"<gold>Trillions</gold> tokens vs <red>10 hrs / robot</red>"	35s
P05-S02b	p05_s02b_two_barriers.py	PROBLEM_FIRST	Part5 slide 5-8	script_p5 Slide 2-8	Barrier 1 (no web-scale robot data) + tiny "zombie city" preview; Barrier 2 (no human model)	covid.py:723	"Barrier 1 / Barrier 2" each red header	35s
P05-S03	p05_s03_micromobility.py	GALLERY_CARDS	Part5 slide 9-12	script_p5 Slide 9-12	60% < 5 mi stat; 4 vehicle cards (delivery robot, e-wheelchair, scooter, humanoid); COCO partnership badge	—	"<gold>60%</gold> trips < 5 mi"	30s
P05-S04a	p05_s04a_compositional_quote.py	TITLE_CINEMATIC	Part5 slide 13-15	script_p5 Slide 13-24	Dark gold quote scene: "The world is compositional, or there is a god." — Stuart Geman; hold 3s	logo.py:8 OpeningQuote	quote italic gold	20s
P05-S04b	p05_s04b_metaurban.py	PIPELINE_FLOW	Part5 slide 14-22	script_p5 Slide 13-24	Description script terminal → procedural generator gear spins → scene1 morph scene2 morph scene3 (∞)	logo.py:216 + generalization/p46_56.py	"<gold>Diversity</gold> > Quantity"	50s
P05-S04c	p05_s04c_metaurban_scaling.py	CHART_REVEAL	Part5 slide 22-24	script_p5 Slide 13-24	Power-law scaling curve: unique layouts vs performance; "100 diverse > 1000 repeated" callout	generalization/p46_56.py	power-law label in gold	30s
P05-S05a	p05_s05a_urbansim_bottleneck.py	PROBLEM_FIRST	Part5 slide 25-30	script_p5 Slide 25-38	Traditional CPU↔GPU transfer pipeline; arrows flash red bottleneck; 180 GPU-days bar runs off screen	network_flow.py:55	"<red>180 GPU-days</red>"	35s
P05-S05b	p05_s05b_urbansim_results.py	CHART_REVEAL	Part5 slide 30-38	script_p5 Slide 25-38	UrbanSim all-GPU flow; 256 parallel envs tile grid; counter 180d → 3h, 2620 FPS burst	covid.py:723 + ShowLogisticCurve	"<red>180 days</red> → <green>3 hours</green> · <gold>2620 FPS</gold>" Pattern C	45s
P05-S06a	p05_s06a_citywalker.py	CHART_REVEAL	Part5 slide 39-43	script_p5 Slide 39-47	World map of 227 cities; pink dots LaggedStart; stats counters; 4 stick-figure diversity micro-loops	random_puzzles.py:18 DotHistory	gold counters	35s
P05-S06b	p05_s06b_pedgen.py	PIPELINE_FLOW	Part5 slide 44-47	script_p5 Slide 39-47	3 inputs (scene voxel, SMPL body, goal) → diffusion noise → clean walking skeleton emerges	p31_61_1.py:332 diffusion frames + p31_61_1.py:654 row transform	"noise → <pink>human</pink>"	50s
P05-S07	p05_s07_zombie_to_alive.py	BEFORE_AFTER	Part5 slide 47	script_p5 Slide 39-47 + 5_PART_GUIDE P5-05	Zombie city (gray squares, straight lines) → freeze → each pedestrian transforms to stick figure, pink, organic path with avoidance	covid.py:723 ViralSpreadModelWithClusters	"Zombie City" → "<green>Human-Centric Physical AI</green>"	45s
P05-S08	p05_s08_vid2sim.py	PIPELINE_FLOW	Part5 slide 50-54	script_p5 Slide 50-54	Real video → 3D Gaussian splat dissolution → mesh wireframe trace → interactive sim with robot path	p31_61_1.py:43 P61a (image patches) + spheres_talk/volumes.py:365	"video → <gold>playground</gold>"	45s
P05-S09	p05_s09_living_city.py	3D_OPENGL	—	5_PART_GUIDE P5-07 Phase 1-2	The hero finale 3D scene. City night, agents fade in by type (cars, robots, chairs, peds, RSU, drones), web of V2X links lights up, radar wave interference everywhere, camera slowly orbits	model3d.py:260 + light.py:216 LightSource + covid.py:723 + DotHistory trails	per-agent type labels in their colors	50s
P05-S10	p05_s10_chain_of_solutions.py	GALLERY_CARDS	—	5_PART_GUIDE P5-07 Phase 3	5 vignette panels drop in, each mini-replays its part's iconic animation, then fade	—	each card titled by part color	35s
P05-S11	p05_s11_final_summary.py	TITLE_CINEMATIC	—	5_PART_GUIDE Final Frame	City continues; gold text "Beyond Self-Driving." / "Not just smarter cars." / "A safer world."; roadmap all gold; UCLA logo; converge to single dot	logo.py:192 LogoGenerationFlurry inverse	each line gold italic, write-chiseled	45s
Total: 73 scenes (4 intro + 14 P1 + 15 P2 + 16 P3 + 12 P4 + 12 P5).

4. SCENE DETAIL BLOCKS
Format per Section 8 of the prompt. Each block names what the viewer sees, the source pattern, the MarkupText runs, the gold key number, the components needed, the English voiceover-ready script, and inter-scene dependencies.

INTRO
I-01 — Title Card
Type: TITLE_CINEMATIC · Duration: ~25s · Slide: — · Script: 5_PART_GUIDE I-01

Visual Core

Beat 1 (0–3s): BG_TITLECARD ink-dark canvas. Centered point of light, single shimmer.
Beat 2 (3–8s): point bursts → 200 particles fly out trailing afterglow (cyan / gold / blue).
Beat 3 (8–15s): before particles dissipate, the wordmark "BEYOND SELF-DRIVING" forges glyph-by-glyph in GOLD_RICH (each glyph appears white-hot, cools to gold).
Beat 4 (15–20s): under wordmark — small line "ICCV 2025 Tutorial · UCLA Mobility Lab"; thin gold rule draws L→R; five speaker names fade in.
Beat 5 (20–25s): everything dust-dissolves upward.
Reference Reuse

3b1b_videos/custom/logo.py:192 LogoGenerationFlurry — particle burst → assemble
3b1b_videos/custom/logo.py:211 WrittenLogo — slow write timing for wordmark
MarkupText Usage — italic gold speaker-names line.

Key Number — none; this is mood.

Components Needed — animations.particle_assemble, animations.forge_text, animations.dust_dissolve.

Script (EN) — no narration; ambient sound only. Optional voiceover: "Beyond Self-Driving. An ICCV 2025 tutorial from UCLA Mobility Lab."

Dependencies — first scene. Output: leads into I-02.

I-02 — The Hook
Type: 3D_OPENGL · Duration: ~75s · Slide: — · Script: 5_PART_GUIDE I-02

Visual Core

Beat 1 (0–12s, Act A): Studio3DScene phi=70, theta=-30. Dark intersection grid glowing faintly. Hero car drives in from left, stops at center. Three small floating hexagons (foundation-model icons) anchor above it, connected by pulsing thin lines. Then radar shells expand from antenna — ellipsoidal 3D rings, uneven spacing, cyan with afterglow.
Beat 2 (12–22s, Act B — collision): Building DROPS from above with squish + digital dust. Radar wave bends around corner; red translucent zone forms behind building (blind spot). FM hex icons fade out.
Beat 3 (22–30s): MarkupText overlay top-right "Even the smartest single agent / cannot see around corners." Hold 2s.
Beat 4 (30–48s, Act C — cooperation): All FM icons fully gone. Two more cars enter from other directions. Three shell systems pulse simultaneously. Interference pattern crystallizes. Red zone fades to green. Pedestrian silhouette materializes inside formerly-blind region.
Beat 5 (48–60s): Quote write-chiseled, gold italic centered: "So we taught them to cooperate." Hold 3s.
Beat 6 (60–75s): fade to dark.
Reference Reuse

hairy_ball/model3d.py:260 RadioBroadcast.update_shells — expanding 3D shells
welchlabs/once_useful_constructs/light.py:95 Spotlight — sensor cone idiom
3b1b_videos/_2023/optics_puzzles/adding_waves.py — interference pattern
MarkupText Usage — Pattern A on first overlay; Pattern D on chiseled quote.

Key Number — none; this is the project's emotional thesis.

Components Needed — signals.radar_shells_3d, signals.interference_pattern, agents.vehicle_icon, agents.pedestrian_icon, animations.write_chiseled.

Script (EN, voiceover ready)

"Even the smartest single agent cannot see around corners.
So we taught them to cooperate.
Cooperation, it turns out, is a physics solution — not an algorithm one."

Dependencies — Requires I-01 complete. Output: thesis established → leads to I-03.

I-03 — Orbital Roadmap
Type: TITLE_CINEMATIC · Duration: ~30s · Script: 5_PART_GUIDE I-03

Visual Core

Beat 1 (0–5s): pulsing gold star centers screen.
Beat 2 (5–18s): five orbital nodes appear LaggedStart at different ellipse radii — P1 indigo top-left, P2 teal lower-left, P3 green bottom, P4 amber lower-right, P5 pink upper-right.
Beat 3 (18–25s): a lightning trace P1→P2→P3→P4→P5 runs along the orbit, leaving fading violet afterglow.
Beat 4 (25–30s): node P1 brightens to GOLD_RICH, camera zoom-in to P1.
Reference Reuse — logo.py:216 LogoGenerationFivefold — radial 5-fold assembly.

MarkupText Usage — each node label uses its part pastel/accent split (e.g., <span color="#2563EB">Foundation Models</span>).

Components Needed — animations.fivefold_assemble, layout.three_column (for label placement).

Script (EN) — "Five parts. One road."

Dependencies — bridges I-02 → P01-S01.

I-04 — Bridge to Part 1
Type: BRIDGE_RECAP · Duration: ~18s

Visual Core — three small recap chips ("smart agent → blind", "physics not algorithm", "five-part journey"), then large forward question gold italic: "But before we cooperate, what is the agent's mind?"

MarkupText — forward Q italic gold.

Components Needed — annotations.callout, typography.markup.

Script (EN) — "Before we make many agents cooperate — what's actually inside one agent's mind?"

PART 1 — FOUNDATION MODELS
P01-S01 — Title Card
Type: TITLE_CINEMATIC · Duration: ~25s · Slide: Part 1 slide 1

Visual Core — BG_TITLECARD. "Part 01" tiny top-right. Title forge: "Foundation Models / for Autonomous Driving" white-hot → indigo settle. Underneath "Dr. Zhiyu Huang · UCLA". Roadmap strip bottom: P1 lit gold, others dim. Quote italic gold: "Why, in 2025, can AI write code, draw art, answer anything — yet self-driving cars still can't go everywhere?"

Reference — logo.py:103 LogoGenerationTemplate.

MarkupText — quote italic gold; part number indigo.

Components — animations.forge_text, base_scene._roadmap_strip.

Script (EN) — "Part 1: Foundation Models for Autonomous Driving — with Dr. Zhiyu Huang."

P01-S02a — GenAI Boom Timeline
Type: TIMELINE · Duration: ~35s · Slide: Part 1 slide 3 · Script: script_part1 Slide 3

Visual Core

Beat 1 (0–6s): horizontal time axis 2020→2025 traces L→R like a laser.
Beat 2 (6–18s): beads drop: GPT-3 small/dim, CLIP brighter, ChatGPT FLASH yellow bloom, GPT-4 LARGEST burst (history inflection point), then dense cluster 2024-25.
Beat 3 (18–28s): under-curve gradient fill purple appears, casting light up onto curve.
Beat 4 (28–35s): pull-quote at footer: "GPT-4 writes code, draws art, answers anything — why not driving?" fades, leaving the timeline alone.
Reference — covid.py:770 ShowLogisticCurve.

MarkupText — year-label color codes; "GPT-4" highlight gold.

Key Number — visual emphasis on GPT-4 bead.

Components — charts.axes_deploy, charts.curve_trace, annotations.key_number.

Script (EN)

"Since 2023, generative AI has done what felt impossible — write code, reason across documents, generate video from a sentence. So a natural question: why not driving?"

Dependencies — feeds P01-S02b (FM definition).

P01-S02b — Foundation Model Definition
Type: CHART_REVEAL · Duration: ~35s · Slide: Part 1 slide 3-4

Visual Core — left column: data sources (text/image/speech/3D) as small tiles; center: large hexagonal "Foundation Model" hub pulsing; right: downstream tasks (auto-labeling, object recognition, image captioning, QA) tiles. Arrows L→C→R, packets travel.

Reference — network_flow.py:73 show_initial_text_embedding.

MarkupText — "Train on <span color='#D97706'>diverse, large-scale data</span> via <span color='#7C3AED'>self-supervised learning</span>".

Components — pipeline.pipeline_block, pipeline.pipeline_flow, annotations.callout.

Script (EN) — "A foundation model is any model trained on diverse, large-scale data — usually through self-supervised learning — and adapted to many downstream tasks."

P01-S03a — Modular Architecture
Type: PROBLEM_FIRST · Duration: ~35s · Slide: Part 1 slide 5

Visual Core — 5 blocks stack vertically (Perception → Localization → Prediction → Planning → Control). Each builds cleanly. Then a tiny noise particle in Perception block. As packets travel down, the noise AMPLIFIES at each step — by Planning the particle is huge, arrows flash red one-by-one (cascade), tiny car at output drifts off lane.

Reference — network_flow.py:227 mention_repetitions motif for stack visual.

MarkupText — Pattern E: [NO] Error accumulation / [NO] No joint optimization / [NO] Cannot learn continuously.

Components — pipeline.pipeline_block, pipeline.pipeline_flow, agents.vehicle_icon.

Script (EN) — "Modular systems are commercially dominant — but errors accumulate. A small mistake in perception becomes a big one by the time the car steers."

P01-S03b — End-to-End Architecture
Type: PROBLEM_FIRST · Duration: ~30s · Slide: Part 1 slide 5

Visual Core — single large rounded box; inside, neural network nodes pulse and edges glow synapse-like. Sensors → arrow → box → arrow → action.

Reference — network_flow.py:174 progress_through_mlp_block — neuron cloud inside block.

MarkupText — Pattern E: [OK] No error accumulation / [OK] Joint optimization / [WARN] Black box — hard to debug.

Components — pipeline.pipeline_block, custom neuron-cloud helper inside.

Script (EN) — "End-to-end replaces the whole pipeline with one neural network. Optimal — but a black box."

P01-S03c — Hybrid Architecture
Type: PROBLEM_FIRST · Duration: ~28s · Slide: Part 1 slide 5

Visual Core — modular skeleton with two stages highlighted (Perception, Planning) tinted PURPLE_MODEL = ML; Control tinted INK_DARK = classical. Then dim everything except the bottom line.

MarkupText — "All three share <span color='#DC2626'>one weakness</span>: the long tail."

Components — pipeline.pipeline_block, pipeline.pipeline_row.

Script (EN) — "Hybrid systems split the difference — ML where it helps, classical control where it must. But all three approaches share one weakness."

Dependencies — sets up the long-tail reveal in P01-S04a.

P01-S04a — Long-Tail Problem
Type: PROBLEM_FIRST · Duration: ~40s · Slide: Part 1 slide 6 · Script: script_part1 Slide 6

Visual Core

Beat 1 (0–10s): three corner cards — phone-pedestrian (red ? flashing), inverted-traffic-lights truck (AI scan lines confused), snow-covered lane (detector outputs nonsense paths).
Beat 2 (10–22s): power-law curve traces center; head left = "99% of driving" tinted PASTEL_BLUE; tail right = "1%" tinted PASTEL_PINK flashing red.
Beat 3 (22–32s): three weird icons crawl from corners onto the long tail — they look like parasitic bugs.
Beat 4 (32–40s): question float-up: "Why can humans handle this?"
Reference — welchlabs/_2025/generalization/p8_15.py for curve idiom + decision_boundary_utils.py for failure region overlay.

MarkupText — Pattern A: "Just <span color='#DC2626'>1%</span> of scenarios cause <span color='#D97706'>100%</span> of fatal accidents."

Key Number — "1% scenarios = 100% of fatal accidents" SIZE_H1 gold at footer.

Components — annotations.failure_icon, charts.curve_trace, charts.axes_deploy.

Script (EN)

"Self-driving fails most where it's seen least. Just one percent of scenarios cause virtually all fatal accidents. And rare doesn't mean safe."

Dependencies — sets up insight in P01-S04b.

P01-S04b — Long-Tail Insight
Type: PROBLEM_FIRST · Duration: ~25s · Slide: Part 1 slide 6

Visual Core — dim overlay 60% on the curve. Centered chiseled-write text appears line by line:


Contextual reasoning.
Common sense.
A lifetime of experience.
Then KEY INSIGHT below in gold large: "We need generalist experience to handle the long tail." Hold 2.5s.

Reference — logo.py:211 WrittenLogo — chiseled-write lag idiom.

MarkupText — full key insight italic gold.

Components — animations.write_chiseled, annotations.key_number.

Script (EN) — "Why do humans handle these? Contextual reasoning, common sense, a lifetime of experience. That's what we need to teach the long tail."

P01-S05 — FM Empowers AV
Type: PIPELINE_FLOW · Duration: ~45s · Slide: Part 1 slide 7 · Script: script_part1 Slide 7

Visual Core — central pulsing hexagon "Foundation Models" indigo. Left fan: 4 source chips (VFM SAM/DINO/CLIP, VGM Wan/Cosmos, LLM, MLLM Gemma3/Qwen3-VL). Right fan: 5 AV needs chips, "E2E Driving Stack" largest and brightest. Hex packets flow from each source to corresponding AV need through the hub. At footer: "Long-tail Generalization & Generalist Experience."

Reference — network_flow.py:73.

MarkupText — each chip labeled with its accent.

Components — pipeline.pipeline_flow, signals.ambient_glow on hub.

Script (EN) — "Foundation models don't replace the AV stack — they empower it: better labels, better scenarios, better reasoning. All pointing one direction: long-tail generalization."

P01-S06 — VLA Roadmap
Type: TIMELINE · Duration: ~35s · Slide: Part 1 slide 9-11 · Script: script_part1 Slide 9-11

Visual Core — 2023→2025 timeline beads for four research directions: text actions, numerical actions, explicit guidance, implicit transfer. Below: dataset chips (DriveLM, CoVLA, Impromptu VLA) drop in. Quote slides up: "Language is not only input — it's an interface for reasoning."

Reference — network_flow.py:73.

MarkupText — quote italic; four directions colored ACCENT_TEAL/BLUE/AMBER/PINK.

Components — charts.curve_trace, pipeline.pipeline_block.

Script (EN) — "Since 2023, four directions: language as output, language as motion, language as guidance, language as transfer. Each forces the model to explain — and explanation is generalization."

P01-S07a — BEVDriver
Type: GALLERY_CARDS · Duration: ~40s · Slide: Part 1 slide 12-14

Visual Core — Teal card. LiDAR point-cloud 3D mess → big down-arrow → presses flat into BEV grid → fed into "LLM" box → outputs waypoints.

Reference — vla/p31_61_1.py:214 make_embedding_row — token row idiom.

MarkupText — Pattern B "3D → <teal>BEV</teal> → LLM".

Components — pipeline.pipeline_block, pipeline.pipeline_flow.

Script (EN) — "BEVDriver flattens the 3D world into a bird's-eye-view grid, then projects it into a language model that predicts waypoints."

P01-S07b — EMMA
Type: GALLERY_CARDS · Duration: ~45s · Slide: Part 1 slide 14-15

Visual Core — Blue-electric card. Camera input → "Gemini" box → chain-of-thought lines typewriter ("There is a pedestrian crossing..." / "Light is red..." → "Brake. Yield.") → simultaneous outputs: trajectory polyline (gold), bounding boxes (cyan), road graph (purple).

Reference — vla/p31_61_1.py:149 P52_61 — VLA full architecture.

MarkupText — each chain-of-thought line in INK_MID, final action line GOLD_RICH.

Components — pipeline.pipeline_block, annotations.thought_bubble, animations.write_chiseled for thought lines.

Script (EN) — "EMMA from Waymo runs everything through language. The car thinks out loud — and then acts."

P01-S07c — DriveVLM
Type: BEFORE_AFTER · Duration: ~35s · Slide: Part 1 slide 16

Visual Core — two parallel rails: top "Fast" — gray, narrow, fast packets; bottom "Slow" — colored, wider, slower; they merge to single action output.

Reference — network_flow.py:161 attention arc idiom.

MarkupText — "<span color='#94A3B8'>Fast</span> for routine. <span color='#D97706'>Slow</span> for complex."

Components — pipeline.pipeline_flow × 2 stacked.

Script (EN) — "DriveVLM splits the brain — a fast traditional pipeline for routine, a slow visual-language model for the hard cases."

P01-S08a — AutoVLA Switch
Type: GALLERY_CARDS · Duration: ~45s · Slide: Part 1 slide 17-18 · Script: script_part1 Slide 17-18

Visual Core — GOLD card brighter than the others. Central switch icon. Left input: simple-scene image; right input: complex-scene (night/rain) image. Switch toggles. For simple → arrow to Fast-mode → quick action output. For complex → arrow to Reasoning-mode → typewriter chain-of-thought: "There is a person waving — flagging the vehicle — safe action: slow down, assess..." Gold badge: [IROS 2025 Best Paper · UCLA].

Reference — vla/p31_61_1.py:671 P34_Pickup + p31_61_1.py:654 row transform for the reasoning → action morph.

MarkupText — chain-of-thought italic gold; switch labels in pastel.

Components — annotations.contribution_badge, pipeline.pipeline_flow, animations.write_chiseled.

Script (EN) — "AutoVLA, from UCLA, learns when to think. Easy scene? Act fast. Ambiguous? Slow down and reason — like a human driver."

P01-S08b — AutoVLA Results
Type: CHART_REVEAL · Duration: ~35s · Slide: Part 1 slide 18-20

Visual Core — bar chart nuPlan vs nuScenes, AutoVLA bar tallest. Counter rolls: +10.6% planning score / −66.8% runtime. Gold burst when numbers settle.

Reference — covid.py:770 ShowLogisticCurve + p31_61_1.py:654.

MarkupText — Pattern C: "<span color='#16A34A'>+10.6%</span> planning · <span color='#16A34A'>−66.8%</span> runtime".

Key Number — "+10.6% / −66.8%" gold large.

Components — charts.bar_reveal, annotations.key_number.

Script (EN) — "Reasoning beats action-only training on every metric — even ones that don't involve language. Plus RFT cuts runtime by two-thirds."

P01-S09 — Part 1 Takeaways
Type: BRIDGE_RECAP · Duration: ~30s · Slide: Part 1 slide 22

Visual Core — 4 bullet recap, each with a small icon: long-tail handled, MLLMs scalable, architectures diverse, honest limits (safety, latency, data).

MarkupText — each bullet key word colored by topic.

Components — annotations.callout, layout.grid_4.

Script (EN) — "Four takeaways: foundation models open the long tail; multi-modal LLMs are the leading architecture; there's no dominant paradigm yet; and safety, latency, data — still hard."

P01-S10 — Bridge to Part 2
Type: BRIDGE_RECAP · Duration: ~18s · Slide: Part 1 slide 24

Visual Core — recap chip "AutoVLA handles the long tail." Forward gold italic: "But even the smartest agent sees only what's in front of it." P2 roadmap node brightens.

Components — annotations.callout, base_scene._roadmap_strip.

Script (EN) — "AutoVLA handles the long tail. But even the smartest agent only sees what's in front of it."

PART 2 — COOPERATIVE PERCEPTION
P02-S01 — Title Card
Type: TITLE_CINEMATIC · Duration: ~25s · Slide: Part 2 slide 1

Visual Core — Teal wave bloom from center. "Part 02 / Towards End-to-End / Cooperative Automation" forge. Zewei Zhou · UCLA. Quote: "A single agent, no matter how smart, is limited by its own line of sight." Roadmap: P2 teal lit.

Reference — logo.py:163 SortingLogoGeneration.

Components — animations.forge_text, base_scene._roadmap_strip.

Script (EN) — "Part 2: Towards End-to-End Cooperative Automation — with Zewei Zhou."

P02-S02a — 1.19 Million
Type: CHART_REVEAL · Duration: ~30s · Slide: Part 2 slide 2-3

Visual Core — counter rolls 0 → 1,190,000 in red, accelerating. Locks in with a red pulse. Caption underneath: "people die in traffic each year."

Reference — covid.py:205 ViralSpreadModel counter idiom.

MarkupText — final number <span color='#DC2626'>1,190,000</span> then label.

Key Number — 1,190,000.

Components — annotations.key_number, custom counter helper.

Script (EN) — "Every year, 1.19 million people die in traffic. Ninety-four percent because of human error."

P02-S02b — 94% / 80% Reduction
Type: CHART_REVEAL · Duration: ~25s · Slide: Part 2 slide 2-3

Visual Core — 10×10 person-icon grid. 94 icons flash red LaggedStart. The 94 red ones shrink by 80% with a brace label "Waymo: −80% injury crashes."

Reference — covid.py:723 ViralSpreadModelWithClusters.

MarkupText — "<span color='#DC2626'>94%</span> human error → Waymo: <span color='#16A34A'>−80%</span> injury".

Components — layout.grid_4 (extend to 10×10), annotations.callout.

Script (EN) — "94% of those crashes are human error — and AVs are starting to show real gains. Waymo: 80% fewer injury crashes."

P02-S03 — Single-Agent Evolution
Type: TIMELINE · Duration: ~40s · Slide: Part 2 slide 4

Visual Core — slight uphill spine. Bead drops: PnPNet (2021, CNN+LSTM) → GameFormer (2022, interactive prediction) → UniAD (2023, query-based E2E) → DiffusionDrive (2024, diffusion trajectory). Under each: one-line reason next bead was needed.

Reference — network_flow.py:227 mention_repetitions.

MarkupText — method names colored distinctly.

Components — pipeline.pipeline_flow, annotations.callout.

Script (EN) — "From PnPNet to DiffusionDrive — the single-agent stack has come a long way. Each step solved the previous bottleneck."

P02-S04a — Occlusion Problem
Type: PROBLEM_FIRST · Duration: ~30s · Slide: Part 2 slide 5

Visual Core — top-down single car. Big truck appears in front. LiDAR scan from the car hits the truck and stops. Blind region behind truck pulses red. Text "Chưa" → "Not yet." giant red center, hold 2s.

Reference — light.py:95 Spotlight for blocked-cone idiom.

MarkupText — "single agent → <span color='#DC2626'>blind to occlusion</span>".

Components — signals.sensor_cone, agents.vehicle_icon, signals.ambient_glow.

Script (EN) — "Has end-to-end solved everything? Not yet."

P02-S05 — Radar Gravitational Waves (HERO)
Type: 3D_OPENGL · Duration: ~75s · Slide: Part 2 slide 5 · Script: script_part2 Slide 5 + 5_PART_GUIDE P2-04

Visual Core — full 3D set piece per 5_PART_GUIDE P2-04 (already detailed in source). Camera phi=70 → tilt to 65; theta rotates +15° during cooperation reveal. Three colored radar systems interfere; blind zone red → green; pedestrian silhouette materializes; quote "Cooperation is a physics solution, not an algorithm one." gold italic write-chiseled hold 2.5s.

Reference — model3d.py:260 RadioBroadcast (shells) + adding_waves.py (interference) + light.py:95 (cones).

MarkupText — Pattern D on closing quote with gold "physics".

Key Number — none — emotional climax.

Components — signals.radar_shells_3d × 3, signals.interference_pattern, agents.pedestrian_icon, animations.write_chiseled.

Script (EN) — "Three cars. Three radar systems. Where their waves meet — interference, and the blind zone vanishes. Cooperation is a physics solution, not an algorithm one."

P02-S06 — Related Works Chain
Type: TIMELINE · Duration: ~50s · Slide: Part 2 slide 6-8

Visual Core — uphill rail spine. Beads V2VNet (2020, teal) → V2X-ViT (2022, blue, GAP) → Where2comm (2022, indigo, VOLUME) → CodeFilling (2024, gold). Each bead labeled with what it addresses and what its bottleneck is. After CodeFilling: empty stretch with "???". PI bubble (or similar small mascot label): "But all 4 miss multi-frame multi-task fusion." New gold bead V2XPnP flies in.

Reference — network_flow.py:227 mention_repetitions.

MarkupText — bottleneck: <span color='#DC2626'>...</span> per bead.

Components — pipeline.pipeline_block, annotations.callout, annotations.contribution_badge.

Script (EN) — "The field has matured through V2VNet, V2X-ViT, Where2comm, CodeFilling. Each solved the previous bottleneck — but none of them are multi-frame, multi-task. That's the gap V2XPnP fills."

P02-S07 — Research Gaps
Type: BEFORE_AFTER · Duration: ~35s · Slide: Part 2 slide 9

Visual Core — top half: single-frame cooperative perception flow. Bottom half: cooperative temporal perception + prediction flow. Three trajectories shown bottom (turning, straight, stopped) to motivate why temporal matters.

Reference — network_flow.py:174 progress_through_mlp_block.

MarkupText — "single-frame" vs "<span color='#D97706'>multi-frame multi-task</span>".

Components — pipeline.pipeline_flow, agents.vehicle_icon.

Script (EN) — "Three trajectories — turning, straight, stopped. Without history, you can't tell which is which. Temporal is not optional."

P02-S08 — Three Questions
Type: GALLERY_CARDS · Duration: ~35s · Slide: Part 2 slide 10

Visual Core — three cards: WHAT (3 mini-icons raw/bbox/BEV), WHEN (two cars approaching, comm window opens green then closes), HOW (two streams temporal+spatial merging). Cards pulse together, converge into single line "V2XPnP answers all three."

MarkupText — Pattern B with three accent colors.

Components — layout.three_column, annotations.callout, signals.v2x_link.

Script (EN) — "Three questions: what to transmit, when to transmit, how to fuse. V2XPnP answers all three."

P02-S09 — V2XPnP Architecture
Type: PIPELINE_FLOW · Duration: ~60s · Slide: Part 2 slide 10-15

Visual Core — 3 tiers built up. Tier 1: 4 agents (2 cars, 2 infra) appear. Tier 2: one-step communication burst (visual: huge packet swarm collapses through narrow neck and re-expands) → temporal attention block + spatial attention block. Tier 3: 3 outputs (detection cyan, prediction gold, planning purple) fan out. Benchmark stamps "SOTA detection / SOTA prediction".

Reference — network_flow.py:161 play_simple_attention_animation + p31_61_1.py:149 P52_61.

MarkupText — task names colored.

Components — pipeline.pipeline_flow, signals.v2x_link, pipeline.pipeline_block.

Script (EN) — "V2XPnP transmits everything in one shot, fuses across time and space, and supports three tasks at once: detect, predict, plan."

P02-S10 — V2XPnP-Seq Dataset
Type: CHART_REVEAL · Duration: ~30s · Slide: Part 2 slide 13-14

Visual Core — counter cards: 2 vehicles · 2 infra · 40 K LiDAR frames · 208 K camera frames · HD maps · trajectories.

MarkupText — gold key numbers.

Components — annotations.key_number, layout.grid_4.

Script (EN) — "The first real-world dataset that covers every V2X mode — V2V, V2I, V2X, I2I — with sequential frames and HD maps."

P02-S11a — TurboTrain Problem
Type: CHART_REVEAL · Duration: ~35s · Slide: Part 2 slide 16

Visual Core — AP vs EPA chart, axes deploy. Orange dots rain into low region (one-time training fails). Blue dots appear stage by stage rising (manual 4-stage). Broken line divides them.

Reference — backprop_3/geometry_while_learning_2.py.

MarkupText — "<span color='#EA580C'>one-time: fail</span> / <span color='#2563EB'>manual 4-stage: 120 epochs</span>".

Components — charts.axes_deploy, charts.scatter_rain.

Script (EN) — "Training a multi-agent, multi-frame, multi-task model is unstable — and gradient conflict makes it worse. Manual four-stage training works, but it costs 120 epochs of human-guided pipeline."

P02-S11b — TurboTrain Solution
Type: BEFORE_AFTER · Duration: ~50s · Slide: Part 2 slide 18-22

Visual Core — left: 3 task gradient arrows tug different directions, conflict region red. Without TurboTrain: zigzag path on weight surface. With TurboTrain: pretraining nudges start point closer to optimum, then 2-stage hybrid (free / conflict-suppressing) traces smooth spiral to gold-star optimum. Counter 120 → 45 epochs, 4 stages → 2.

Reference — backprop_3/geometry_while_learning_2.py + decision boundary utils.

MarkupText — Pattern C: "<span color='#DC2626'>120 epochs</span> → <span color='#16A34A'>45 epochs</span>".

Components — charts.curve_trace, custom landscape surface helper.

Script (EN) — "TurboTrain pretrains a task-agnostic 4D representation, then balances gradients during fine-tuning. 120 epochs becomes 45 — and no human expertise needed to decide when to switch stages."

P02-S12 — RiskMap
Type: AGENT_SIM · Duration: ~50s · Slide: Part 2 slide 23-25

Visual Core — top-down road, ego car moving. Risk heatmap overlay: hot red near other cars, transparent green in safe lanes, amber in unknown corners. A car swerves suddenly → red zone blooms. Ego trajectory snakes around hot zones like a river around rocks.

Reference — region.py:50 plane_partition + e_field.py.

MarkupText — "Risk is a <span color='#D97706'>language</span>, not a bounding box."

Components — signals.ambient_glow, custom heatmap helper, agents.vehicle_icon, agents.agent_trail.

Script (EN) — "Risk isn't a bounding box. It's a field — continuous, predictive. The planner doesn't pick objects to avoid; it picks paths through low-risk regions."

P02-S13 — Part 2 Summary
Type: BRIDGE_RECAP · Duration: ~25s

Visual Core — 3 stacked gold-bordered cards: V2XPnP / TurboTrain / RiskMap, each with a one-line takeaway.

Components — annotations.contribution_badge, layout.grid_4.

Script (EN) — "Three contributions, one stack: V2XPnP for fusion, TurboTrain for training, RiskMap for interpretable planning."

P02-S14 — Bridge to Part 3
Type: BRIDGE_RECAP · Duration: ~18s

Visual Core — "All of this needs real data from real sensors on real roads." gold italic forward question.

Script (EN) — "But all of this is theory until you put real sensors on real roads. That's Part 3."

PART 3 — SIM-TO-REAL
P03-S01 — Title Card
Type: TITLE_CINEMATIC · Duration: ~25s · Slide: Part 3 slide 1

Visual Core — Green wave bloom. Title forge "Bridging Simulation and Reality / in Cooperative V2X Systems" + Zhaoliang Zheng. Quote: "Theory without deployment is just fiction." Roadmap: P3 green lit.

Reference — logo.py:103.

Script (EN) — "Part 3: Bridging Simulation and Reality — with Zhaoliang Zheng."

P03-S02 — Sim-to-Real Gap
Type: BEFORE_AFTER · Duration: ~40s · Slide: Part 3 slide 3-5

Visual Core — Screen split by zigzag lightning crack (draws top-down). Left: clean digital sim (geometric, uniform). Right: messy real (cracked pavement, shadows, rain artifacts). Broken arrow attempting L→R bounces back. Red label "Sim-to-Real Gap". Later in part, the crack heals.

Reference — optics_puzzles/objects.py.

MarkupText — Pattern B: "<span color='#0891B2'>Sim</span> | <span color='#D97706'>Real</span>".

Components — custom crack-draw helper, layout.two_column, agents.vehicle_icon.

Script (EN) — "Two worlds. Clean simulation on the left, messy reality on the right. The gap between them is where careers get stuck."

P03-S03 — UCLA Smart Intersection
Type: AGENT_SIM · Duration: ~50s · Slide: Part 3 slide 6-11

Visual Core — UCLA campus overhead schematic. NW + SE nodes pulse red. Each node "deploys" hardware spec card (LiDAR 128, cameras, radar, C-V2X). 2 CAV cards too. Then ALL sensors activate simultaneously: camera amber FOV cones, LiDAR cyan rings, radar cyan wave, V2X hex packets. Web of signals — circuit-board feel.

Reference — model3d.py:68 RadioTower (for RSU icon) + light.py:95 Spotlight (sensor cones).

MarkupText — sensor labels colored by modality.

Components — agents.rsu_icon, signals.sensor_cone, signals.radar_shells_2d, signals.v2x_link, pipeline.pipeline_block.

Script (EN) — "This is not simulation. This is a working intersection at UCLA — two infrastructure nodes, two connected vehicles, and every sensor type lit up at once."

P03-S04a — Time Calibration
Type: PROBLEM_FIRST · Duration: ~35s · Slide: Part 3 slide 12-13

Visual Core — top: car icon labeled "60 km/h". Timeline. Infrastructure observation tagged "−50 ms ago" sits behind real car position. Distance label "83 cm error" in red. Then GPS reference + hardware trigger animation: all sensor timestamps snap to common clock (like a clock-sync visual).

Reference — optics/wave_machine.py.

MarkupText — Pattern A: "<span color='#DC2626'>50 ms</span> delay → <span color='#D97706'>83 cm</span> error".

Key Number — "83 cm error" red.

Components — agents.vehicle_icon, custom clock-sync helper.

Script (EN) — "A 50-millisecond delay at 60 km/h is 83 centimeters of position error. GPS reference plus hardware triggers fix it — software triggers have jitter."

P03-S04b — Space Calibration
Type: MATH_REVEAL · Duration: ~40s · Slide: Part 3 slide 14-17

Visual Core — two point clouds of the same pedestrian, different frames. Transform matrix 4×4 (with rotation R and translation t labeled) flies in. Applied to point clouds → they rotate and merge into one figure. Then a counter-example: bad calibration → ghost object appears, red flash, label "Ghost — does not exist."

Reference — vector_space_scene.py:204 LinearTransformationScene + linear_algebra.py:32 vector_coordinate_label.

MarkupText — matrix elements R/t colored.

Components — custom point-cloud helper, pipeline.pipeline_block.

Script (EN) — "Space calibration is the transform from one sensor's frame into a common one. Get it wrong and you fuse two views into a ghost — an object that doesn't exist."

P03-S05 — Data Collection
Type: TIMELINE · Duration: ~35s · Slide: Part 3 slide 18-22

Visual Core — basic routes drawn (R-turn, L-turn, straight). Then combined routes overlay. Times-of-day grid (morning, noon, evening, night). Final cards: V2X-Real (ECCV 2024) and V2XPnP-Seq dataset badges.

Components — agents.vehicle_icon, annotations.contribution_badge, layout.grid_4.

Script (EN) — "Data isn't collected randomly — it's collected systematically: basic routes, combined routes, every time of day. Then it becomes V2X-Real and V2XPnP-Seq."

P03-S06 — Localization Role
Type: PROBLEM_FIRST · Duration: ~40s · Slide: Part 3 slide 23-28

Visual Core — same object from two viewpoints. Without precise localization: fused point cloud is offset, looks worse than single. Label red: "worse than single-agent." With precise localization: clean overlay, one crisp object.

Reference — region.py:50 + vector_space_scene.py.

MarkupText — "no loc → <span color='#DC2626'>worse than single</span>".

Components — custom point-cloud helper, pipeline.pipeline_block.

Script (EN) — "With cooperative perception, localization matters even more. Get the position wrong and you make things worse — fusion amplifies errors."

P03-S07 — Kalman Filter (Three Rivers)
Type: UNCERTAINTY_CLOUD · Duration: ~50s · Slide: Part 3 slide 28-32

Visual Core — three rivers converging metaphor. GNSS (blue, wide, slow, blocked by building icons periodically). IMU+wheel (amber, medium, drifts visibly). LiDAR-map (green, narrow, intermittent but accurate). They flow into a pulsing Kalman node. Output: single smooth 100 Hz green river.

Reference — _2018/uncertainty.py + random_puzzles.py:363 Random3DVectors.

MarkupText — three sources colored, output gold: "<span color='#2563EB'>5 Hz</span> + <span color='#D97706'>100 Hz</span> + <span color='#16A34A'>1 Hz</span> → <span color='#EAB308'>100 Hz lane-level</span>".

Components — custom river/stream helper, pipeline.pipeline_block, signals.ambient_glow on Kalman node.

Script (EN) — "Three sources, three weaknesses. GNSS is absolute but slow and blocked. IMU is fast but drifts. LiDAR map-matching is exact but heavy. The Kalman filter fuses all three into a single, lane-level stream at a hundred hertz."

P03-S08 — CooperFuse
Type: UNCERTAINTY_CLOUD · Duration: ~50s · Slide: Part 3 slide 33-43

Visual Core — two bounding boxes (V and I) for one object, slightly offset. Two Gaussian ellipses around each. Left side NMS: pick higher-confidence, discard other with red X. Right side CooperFuse: Gaussians multiply → smaller, tighter result box crystallizes. Math-style beauty.

Reference — region.py + _2018/uncertainty.py.

MarkupText — "NMS: <span color='#DC2626'>discard</span> vs CooperFuse: <span color='#16A34A'>fuse</span>".

Components — custom Gaussian-ellipse helper, pipeline.pipeline_block.

Script (EN) — "NMS throws information away. CooperFuse fuses by temporal bounding-box features — and the result is more precise than either source alone."

P03-S09 — V2X-ReaLO
Type: PIPELINE_FLOW · Duration: ~45s · Slide: Part 3 slide 44-49

Visual Core — BEV feature blob big, then 32× compression squeeze, then 0.5 MB packet transmits over V2X link, real-time.

Reference — network_flow.py:55 get_block.

MarkupText — Pattern C: "<span color='#DC2626'>16 MB</span> → <span color='#16A34A'>0.5 MB</span> · <span color='#EAB308'>32×</span> compress".

Components — pipeline.pipeline_flow, signals.v2x_link.

Script (EN) — "Intermediate fusion shares rich BEV features — but you have to compress 32× to fit V2X bandwidth. V2X-ReaLO hits the sweet spot at 0.5 megabytes per message."

P03-S10 — OpenCDA-ROS
Type: PIPELINE_FLOW · Duration: ~40s · Slide: Part 3 slide 50-54

Visual Core — real-world ROS bag (left card) → OpenCDA-ROS bridge (center) → CARLA simulation (right card). Arrows both directions show code portability.

Reference — network_flow.py:55 + graph_theory.py:56 DiscreteGraphScene.

MarkupText — bridge label gold.

Components — pipeline.pipeline_block, pipeline.pipeline_flow.

Script (EN) — "OpenCDA-ROS bridges robotics middleware to simulation. Code that runs on a real car also runs in CARLA — no rewrite."

P03-S11 — CDA-SimBoost
Type: PIPELINE_FLOW · Duration: ~40s · Slide: Part 3 slide 55-58

Visual Core — closed loop: real data → digital twin → challenging scenarios → train → deploy back to real. Each step is a card; loop animates packets going around.

Reference — covid.py:723 + ShowLogisticCurve.

MarkupText — "challenging <span color='#D97706'>scenarios</span>".

Components — pipeline.pipeline_flow (loop variant).

Script (EN) — "Real data builds a digital twin. The twin generates challenging scenarios — rain, sensor failure, sudden pedestrian — that you couldn't safely produce on the street."

P03-S12 — Digital Twin
Type: AGENT_SIM · Duration: ~45s · Slide: Part 3 slide 50-54

Visual Core — split scene. Left: real intersection (icon style). A horizontal scan line sweeps L→R. As it passes, the right side morphs each element into its digital twin (street → teal grid, car → cyan wireframe box, RSU → circuit-board icon, tree → mesh). Both sides then live-sync as agents move.

Reference — optics/objects.py.

MarkupText — "OpenCDA → real-time <span color='#EAB308'>digital twin</span>".

Components — animations.scan_reveal, agents.vehicle_icon, agents.rsu_icon.

Script (EN) — "Scan a real intersection, build its digital twin. Now the twin moves when reality moves — with 100 milliseconds of lag."

P03-S13 — InfraX
Type: GALLERY_CARDS · Duration: ~30s · Slide: Part 3 slide 58-59

Visual Core — 4 feature cards: sensor configuration / multi-modality / weather variation / vector maps. Each card a small mechanism.

Components — layout.grid_4, annotations.callout.

Script (EN) — "OpenCDA-InfraX is the data-generation platform: configurable sensors, modalities, weather, and maps — all in one."

P03-S14 — Part 3 Summary
Type: BRIDGE_RECAP · Duration: ~25s

Visual Core — 4 contribution badges: Smart Intersection / Calibration / Real-time Fusion / Digital Twin.

Components — annotations.contribution_badge.

Script (EN) — "Four contributions: a real smart intersection, calibration that works, fusion that runs real-time, and a digital twin that closes the loop."

P03-S15 — Bridge to Part 4
Type: BRIDGE_RECAP · Duration: ~18s

Visual Core — "Now it works. But is it efficient enough to deploy?" three bottleneck tags (data / training / inference) blink.

Script (EN) — "Now it works. But efficient enough to deploy? Three bottlenecks — data, training, inference — are next."

PART 4 — EFFICIENCY
P04-S01 — Title Card
Type: TITLE_CINEMATIC · Duration: ~25s · Slide: Part 4 slide 1

Visual Core — amber electric bloom. Title forge: "From Pre-Training / to Post-Training" + Seth Z. Zhao. Quote: "A system that can't run real-time is a demo." Roadmap: P4 amber lit.

Reference — logo.py:163.

Script (EN) — "Part 4: From Pre-Training to Post-Training — with Seth Zhao."

P04-S02 — V2X Overview & 3 Bottlenecks
Type: TIMELINE · Duration: ~30s · Slide: Part 4 slide 2-7

Visual Core — quick V2X recap timeline. USDOT smart-intersection mention chip. Then 3 red bottleneck tags drop in: Data · Training · Inference.

Reference — network_flow.py:227.

MarkupText — each bottleneck red.

Components — pipeline.pipeline_block, annotations.callout.

Script (EN) — "V2X is no longer just research — USDOT is funding smart intersections. But three bottlenecks block real deployment: data, training, and inference."

P04-S03 — Annotation Cost Explosion
Type: CHART_REVEAL · Duration: ~40s · Slide: Part 4 slide 8-9

Visual Core — bar chart, 3 bars: V2V4Real (240 K, blue), DAIR-V2X (460 K, amber), V2X-Real (1.2 M, green). Counter rolls each. Brace "5× in 2 years." Annotation right side: human cost lines.

Reference — ShowLogisticCurve.

MarkupText — Pattern A: "<span color='#EAB308'>5×</span> in 2 years".

Key Number — 1.2 M / 5×.

Components — charts.bar_reveal, annotations.key_number.

Script (EN) — "Datasets have grown five times in two years — but annotation cost grew with them. We can't scale this way."

P04-S04 — CooPre Masked Puzzle
Type: AGENT_SIM · Duration: ~75s · Slide: Part 4 slide 9-14 · Script: script_part4 Slide 9-14

Visual Core

Beat 1 (0–10s): BEV grid + 2 agents shooting LiDAR beams.
Beat 2 (10–25s): 40% voxels mask LaggedStart (irregular pattern); caption "Can you fill in what you can't see?" floats.
Beat 3 (25–55s): Agent B particles stream along curved trajectories into masked voxels; each voxel restores with bloom LaggedStart.
Beat 4 (55–70s): result bars — 50% data CooPre matches 100% baseline; 100% data CooPre +4% AP. Counter stamps with checkmarks.
Beat 5 (70–75s): IROS 2025 + CVPR 2025 DriveX badge.
Reference — spheres_talk/volumes.py:53 VolumeGrid + vla/p31_61_1.py:332 (diffusion frame motif).

MarkupText — "50% data → <span color='#16A34A'>same perf</span> / 100% data → <span color='#EAB308'>+4% AP</span>".

Key Number — +4% AP gold.

Components — signals.v2x_link, pipeline.pipeline_block, annotations.contribution_badge, custom voxel-grid helper.

Script (EN) — "CooPre masks 40 percent of voxels and asks the model to fill them in — using what other agents see. The model learns exactly what cooperative perception needs: when I can't see, I ask. Half the labels, same performance."

Dependencies — feeds into P04-S05 (training efficiency motivation).

P04-S05 — TurboTrain Landscape
Type: UNCERTAINTY_CLOUD · Duration: ~60s · Slide: Part 4 slide 15-22

Visual Core — 2D loss-landscape surface (contour lines). Three task gradient arrows (det / pred / plan) tug from origin in different directions. Without TurboTrain: zigzag chaotic path, fails to converge. With TurboTrain: pretraining places start near optimum; 2-stage hybrid traces smooth spiral to gold-star optimum. Counter 120 → 45 epochs.

Reference — backprop_3/geometry_while_learning_2.py + decision_boundary_utils.py.

MarkupText — Pattern A: "<span color='#DC2626'>conflict</span> → <span color='#16A34A'>smooth</span>".

Components — charts.curve_trace, custom landscape helper.

Script (EN) — "In weight space, three task gradients pull three directions. Without help the model thrashes. With pretraining plus gradient balancing, it spirals smoothly into a good basin."

P04-S06 — Latency Chain
Type: PIPELINE_FLOW · Duration: ~40s · Slide: Part 4 slide 22-23

Visual Core — chain of blocks: local inference → communication → fusion inference, each with a "time budget" tag and packet pulses. One block glows red — bottleneck.

Reference — optics/wave_machine.py.

MarkupText — "<span color='#DC2626'>FP32: too slow</span>".

Components — pipeline.pipeline_flow, signals.v2x_link.

Script (EN) — "Every V2X frame has a latency budget. Each stage eats into it. FP32 inference doesn't fit."

P04-S07 — Arithmetic Cost
Type: MATH_REVEAL · Duration: ~35s · Slide: Part 4 slide 24-26

Visual Core — FP32 multiplication animation (big, expensive, energy droplets fly out) vs INT8 addition (small, cheap). Memory access: 640 pJ DRAM droplet visual vs 5 pJ SRAM. Same scene.

Reference — network_flow.py:55 get_block.

MarkupText — Pattern A: "<span color='#DC2626'>640 pJ DRAM</span> vs <span color='#16A34A'>5 pJ SRAM</span>".

Components — pipeline.pipeline_block, custom energy-droplet helper.

Script (EN) — "Floating-point multiplication is expensive. Memory access is more expensive. INT8 turns multiplies into adds and shrinks the memory footprint — and edge hardware speaks INT8 natively."

P04-S08 — QuantV2X
Type: PIPELINE_FLOW · Duration: ~65s · Slide: Part 4 slide 27-31

Visual Core

Beat 1 (0–10s): big red FP32 BEV blob, channel ahead of it clogged red.
Beat 2 (10–25s): Stage 1 box "Full-Precision Pretraining" builds.
Beat 3 (25–40s): Stage 2 box "Codebook Learning" — dictionary array, blob replaced by indices.
Beat 4 (40–55s): Stage 3 box "Post-Training Quantization" — calibration animation.
Beat 5 (55–65s): big squeeze reveal — blob shrinks to 1% size, color flips to green INT8. Channel opens, packets flow freely. Counter 100 MB → 0.33 MB, "300× smaller".
Reference — network_flow.py:55 get_block + custom compression motif.

MarkupText — Pattern C: "<span color='#DC2626'>100 MB · FP32</span> → <span color='#16A34A'>0.33 MB · INT8</span> · <span color='#EAB308'>300×</span>".

Key Number — 300×.

Components — pipeline.pipeline_flow, pipeline.pipeline_block, custom squeeze-animation helper.

Script (EN) — "QuantV2X quantizes both the model and the communication. From 100 megabytes to 330 kilobytes — three hundred times smaller. The channel finally opens."

P04-S09 — Efficiency Summary
Type: BRIDGE_RECAP · Duration: ~25s

Visual Core — 3 gold-bordered cards: Data (CooPre · 50% labels) / Training (TurboTrain · 45 epochs) / Inference (QuantV2X · 300×). Each with its key number.

Components — annotations.contribution_badge, annotations.key_number.

Script (EN) — "Three efficiency contributions, three key numbers: 50% labels, 45 epochs, 300×."

P04-S10 — Bridge to Part 5
Type: BRIDGE_RECAP · Duration: ~18s

Visual Core — "All of this — for cars. But the world has robots, scooters, and people." forward question pink italic.

Script (EN) — "Everything so far has been about cars. But the world has delivery robots, wheelchairs, scooters — and the most unpredictable agent of all: humans."

PART 5 — PHYSICAL AI
P05-S01 — Title Card
Type: TITLE_CINEMATIC · Duration: ~30s · Slide: Part 5 slide 1

Visual Core — Pink bloom. Title forge "Scalable, / Human-Centric / Physical AI" + Wayne Wu. Quote: "Beyond cars — to any agent, any space." Then roadmap strip — for the first and only time, all 5 nodes light up sequentially, each in its part color, then all flip to GOLD with a gold line connecting them. Hold 2s.

Reference — logo.py:216 LogoGenerationFivefold for the sequential bloom.

MarkupText — quote italic gold.

Components — animations.fivefold_assemble, base_scene._roadmap_strip (gold-flip variant).

Script (EN) — "Part 5: Scalable, Human-Centric Physical AI — with Wayne Wu. Beyond cars — to any agent, any space."

P05-S02a — LLM vs Robot Data
Type: BEFORE_AFTER · Duration: ~35s · Slide: Part 5 slide 2-4

Visual Core — left: Internet sources flood (books / Wikipedia / GitHub / Reddit) → LLM → "trillions of tokens." Right: 3 robots collecting → 10 hours each → trickle.

Reference — covid.py:205 ViralSpreadModel + ShowLogisticCurve.

MarkupText — "<span color='#EAB308'>Trillions</span> of tokens vs <span color='#DC2626'>10 hours</span> per robot".

Components — pipeline.pipeline_flow with thick vs thin streams.

Script (EN) — "LLMs work because of web-scale data. Physical AI doesn't have that. Every behavior datapoint is collected by a robot, in the real world, one task at a time."

P05-S02b — Two Barriers
Type: PROBLEM_FIRST · Duration: ~35s · Slide: Part 5 slide 5-8

Visual Core — Barrier 1 red banner: "No web-scale robot data." Small zombie-city preview (gray squares walking straight through each other). Barrier 2 banner: "No human model in the loop."

Reference — covid.py:723 ViralSpreadModelWithClusters.

MarkupText — barrier labels red.

Components — annotations.callout, custom zombie-pedestrian helper.

Script (EN) — "Two barriers. No data at internet scale. And no model of human behavior — so simulations look like zombie cities."

P05-S03 — Micro-Mobility Testbed
Type: GALLERY_CARDS · Duration: ~30s · Slide: Part 5 slide 9-12

Visual Core — big stat "60% of US trips < 5 miles". 4 cards: delivery robot, e-wheelchair, intelligent scooter, humanoid. COCO Robotics partnership badge.

MarkupText — "<span color='#EAB308'>60%</span> of US trips < 5 mi".

Components — layout.grid_4, annotations.contribution_badge.

Script (EN) — "Sixty percent of US trips are under five miles. That's the domain of micro-mobility: delivery robots, wheelchairs, scooters, humanoids. The everyday cases."

P05-S04a — Compositional Quote
Type: TITLE_CINEMATIC · Duration: ~20s · Slide: Part 5 slide 13-15

Visual Core — dark scene (BG_TITLECARD), then individual letters appear at random positions and fly into place forming Stuart Geman's quote: "The world is compositional, or there is a god." Gold italic. Hold 3s.

Reference — 3b1b_videos/custom/opening_quote.py:8 OpeningQuote framing.

MarkupText — quote italic gold.

Components — animations.write_chiseled (variant), animations.particle_assemble.

Script (EN) — "The world is compositional, or there is a god — Stuart Geman."

P05-S04b — MetaUrban Generator
Type: PIPELINE_FLOW · Duration: ~50s · Slide: Part 5 slide 14-22

Visual Core — terminal-style code box showing generate_scene(...) parameters. Big gear icon center spins cyan. Output scenes flicker scene1 → morph → scene2 → morph → scene3 → ... ∞ symbol. Each scene distinct.

Reference — logo.py:216 + generalization/p46_56.py.

MarkupText — "<span color='#EAB308'>Diversity</span> > Quantity".

Components — pipeline.pipeline_block, custom procedural-scene-tile helper.

Script (EN) — "MetaUrban generates urban scenes from a script: block layout, intersections, sidewalks, objects. No two scenes alike — and diversity, not quantity, drives generalization."

P05-S04c — MetaUrban Scaling
Type: CHART_REVEAL · Duration: ~30s · Slide: Part 5 slide 22-24

Visual Core — power-law curve "Number of unique layouts" × "performance on unseen environments." Compare with linear baseline (dimmer). Callout: "100 diverse scenes > 1000 repeated."

Reference — generalization/p46_56.py.

MarkupText — power-law label gold.

Components — charts.axes_deploy, charts.curve_trace.

Script (EN) — "The scaling is power-law. A hundred diverse scenes beat a thousand near-duplicates."

P05-S05a — UrbanSim Bottleneck
Type: PROBLEM_FIRST · Duration: ~35s · Slide: Part 5 slide 25-30

Visual Core — traditional pipeline: CPU → transfer → GPU → transfer → CPU. Transfer arrows flash red, bottleneck visible. Bar "180 GPU-days" stretches off screen, camera pans to reveal length.

Reference — network_flow.py:55.

MarkupText — "<span color='#DC2626'>180 GPU-days</span>".

Components — pipeline.pipeline_flow, charts.bar_reveal.

Script (EN) — "Training a simple RL agent used to take 180 GPU-days — because every step bounced between CPU and GPU."

P05-S05b — UrbanSim Results
Type: CHART_REVEAL · Duration: ~45s · Slide: Part 5 slide 30-38

Visual Core — UrbanSim all-GPU pipeline (green smooth arrows). 256 parallel environments tile as a grid. Counter 180 d → 3 h. Burst: "2,620 FPS · 256 envs · 11.2 GB VRAM."

Reference — covid.py:723 for parallel-env tiling + ShowLogisticCurve for the timing curve.

MarkupText — Pattern C: "<span color='#DC2626'>180 days</span> → <span color='#16A34A'>3 hours</span> · <span color='#EAB308'>2620 FPS</span>".

Key Number — 2620 FPS.

Components — layout.grid_4 (extended), annotations.key_number.

Script (EN) — "UrbanSim keeps everything on the GPU, samples scenes asynchronously, and pushes 256 environments in parallel. Three hours instead of 180 days."

P05-S06a — CityWalker Dataset
Type: CHART_REVEAL · Duration: ~35s · Slide: Part 5 slide 39-43

Visual Core — world map outline, pink dots LaggedStart over 227 cities. Stats counters: 30.8 hours / 120 K pedestrians / 16 K scenes / 227 cities. Around the map, four tiny stick-figure micro-loops: stroller, suitcase-pull, wall-talker, sitting-and-scratching.

Reference — random_puzzles.py:18 DotHistory.

MarkupText — gold counters.

Components — agents.pedestrian_icon (animated loops), annotations.key_number, custom world-map helper.

Script (EN) — "CityWalker captures pedestrian behavior in context — 30 hours of video, 120 thousand pedestrians, across 227 cities."

P05-S06b — PedGen
Type: PIPELINE_FLOW · Duration: ~50s · Slide: Part 5 slide 44-47

Visual Core — 3 inputs (scene voxel block, SMPL skeleton, goal pin) → big diffusion box. Noise particles inside resolve step by step into a clean walking SMPL skeleton. Output: pink walking figure animation.

Reference — p31_61_1.py:332 (diffusion frames) + p31_61_1.py:654 (row transform).

MarkupText — "noise → <span color='#DB2777'>human</span>".

Components — pipeline.pipeline_flow, agents.pedestrian_icon, custom diffusion helper.

Script (EN) — "PedGen is a diffusion model conditioned on scene, body, and goal. Three inputs, one walker — anatomically realistic, contextually coherent."

P05-S07 — Zombie to Alive Transform
Type: BEFORE_AFTER · Duration: ~45s · Slide: Part 5 slide 47 · Script: 5_PART_GUIDE P5-05

Visual Core

Beat 1 (0–8s): zombie city — gray squares walking straight lines, passing through each other.
Beat 2 (8–14s): all freeze. Dim overlay.
Beat 3 (14–35s): each square transforms — square → stick figure, gray → PINK, straight path → organic curved path with collision avoidance.
Beat 4 (35–45s): label "Zombie City" fades. New label appears: "Human-Centric Physical AI" in green. Hold 2s.
Reference — covid.py:723 ViralSpreadModelWithClusters for the agent dynamics.

MarkupText — "<span color='#94A3B8'>Zombie City</span>" → "<span color='#16A34A'>Human-Centric Physical AI</span>".

Components — agents.pedestrian_icon, agents.agent_trail, custom transform-step helper.

Script (EN) — "Without human modeling, the simulation is a zombie city — bodies that walk through each other. PedGen and CityWalker make it alive — human-centric, finally."

P05-S08 — Vid2Sim
Type: PIPELINE_FLOW · Duration: ~45s · Slide: Part 5 slide 50-54

Visual Core — real city-tour video frame (left). Frame dissolves into thousands of colored Gaussian splats — beautiful galaxy. Mesh wireframe traces over the splats. Right: interactive sim with robot path on top of reconstructed environment.

Reference — vla/p31_61_1.py:43 P61a (image-patch grid) + spheres_talk/volumes.py:365 BuildCircleWithCombinedAnnulusses for the splat composition.

MarkupText — "video → <span color='#EAB308'>playground</span>".

Components — pipeline.pipeline_flow, custom Gaussian-splat helper.

Script (EN) — "Vid2Sim turns a city-tour video into a simulator: gaussians for visuals, a mesh for physics. Train in it, deploy in the real world."

P05-S09 — The Living City (HERO)
Type: 3D_OPENGL · Duration: ~50s · Slide: — · Script: 5_PART_GUIDE P5-07 Phase 1-2

Visual Core — full 3D finale per 5_PART_GUIDE P5-07. Camera isometric 60°. Streets glow grid-line. Agents fade in by type at scheduled times (cars blue, robots green, wheelchairs pink, pedestrians gold, RSU orange, drones white). Then V2X web lights up LaggedStart hundreds of links. All agents emit radar shells, interference pattern blooms across the city. Camera slowly orbits theta +30°.

Reference — model3d.py:260 RadioBroadcast + light.py:216 LightSource + covid.py:723 + random_puzzles.py:18 DotHistory for trails.

MarkupText — none (visual showpiece).

Components — signals.radar_shells_3d, signals.v2x_link, agents.vehicle_icon, agents.pedestrian_icon, agents.rsu_tower_3d, agents.drone_icon, agents.agent_trail, signals.ambient_glow.

Script (EN) — "Every agent. Every signal. A city that breathes by electromagnetic radiation."

P05-S10 — Chain of Solutions Montage
Type: GALLERY_CARDS · Duration: ~35s · Slide: — · Script: 5_PART_GUIDE P5-07 Phase 3

Visual Core — camera pulls back. 5 vignette panels drop in. Each plays a 3-second mini-replay of its part's iconic animation, then settles to a still. After all 5 settle they fade out, city full-screen returns.

Components — layout.grid_4 (extended to 5), annotations.contribution_badge.

Script (EN) — "Five parts. Five solutions. One story."

P05-S11 — Final Frame
Type: TITLE_CINEMATIC · Duration: ~45s · Slide: — · Script: 5_PART_GUIDE Final Frame

Visual Core — city continues moving. Then gold write-chiseled centered:


Beyond Self-Driving.
Not just smarter cars.
A safer world.
Hold 2s after last line. Roadmap strip: all 5 nodes GOLD, gold pulsing connector. UCLA logo fades in below. Everything dust-converges (inverse of I-01 explosion) into a single dot, pulses, fades. [FIN]

Reference — logo.py:192 LogoGenerationFlurry inverse for the converge.

MarkupText — each line italic gold.

Components — animations.write_chiseled, animations.dust_dissolve (inverse / converge variant), base_scene._roadmap_strip (all-gold variant).

Script (EN) — "Beyond Self-Driving. Not just smarter cars. A safer world."

5. SCRIPT UPDATE NOTES PER PART
Part 1
Drift fix: existing scenes reduce VLA methods to bare names. Re-incorporate the why per script_part1 slide 12-14: BEVDriver = BEV before LLM; EMMA = language as universal interface; DriveVLM = dual-system fast/slow.
Missing numbers to surface: AutoVLA's "+10.6% planning score" and "−66.8% runtime" must appear as gold key numbers (P01-S08b).
English voiceover format: 2-3 sentences per scene, declarative, no Vietnamese phrasing in scene files. Save each line as SCRIPT = """...""" docstring at top of scene for future TTS.
Part 2
Drift fix: original P02-S04 mixes occlusion problem and radar-wave cooperation in one scene; the rebuild splits it (P02-S04a problem, P02-S05 hero cooperation). The hero scene budget = 75s — do not crowd with extra annotations.
Missing: "1.19 million deaths" and "94% human error" need to be visualized as concrete counters (P02-S02a, P02-S02b) — the old scene treated them as text only.
Missing: 3-question framing (What/When/How) per script_part2 slide 9 was implicit in old version; promote it to its own scene (P02-S08).
Part 3
Drift fix: time and space calibration combined in old p03_s04_calibration.py. Split into S04a (time, with 50ms→83cm number) and S04b (space, with transform matrix + ghost object).
Missing: localization role per script_part3 slide 23-28 deserves its own scene (P03-S06) — "no localization → worse than single agent" is a strong inverted result not previously emphasized.
Missing: CooperFuse's Gaussian-multiplication mechanic (slide 33-43) was simplified; restore the math beauty (P03-S08).
Part 4
Drift fix: old TurboTrain was repeated across P2 and P4; here P02-S11b shows the gradient-conflict idea, P04-S05 deepens it as a true loss-landscape scene.
Missing: arithmetic-cost numbers (640 pJ DRAM vs 5 pJ SRAM) per script_part4 slide 22-23 — promote to MATH_REVEAL scene (P04-S07).
Missing: explicit "[OK] Both model + communication quantized" framing — make it the climax of P04-S08.
Part 5
Drift fix: original p05_s05_citywalker_pedgen.py packed stats + architecture + zombie transform in one scene; split into S06a (stats), S06b (architecture), S07 (zombie → alive transform).
Missing: Stuart Geman quote per script_part5 slide 13-15 deserves its own quote scene (P05-S04a) — currently absorbed into MetaUrban scene.
Missing: "2,620 FPS · 256 envs · 11.2 GB VRAM" stat trio per script_part5 slide 30-38 — promote to gold key number burst in P05-S05b.
Voiceover format
Top of each scene file:


SCRIPT = """
(EN voiceover, 2–3 sentences, declarative.)
"""
This becomes the seed for manim-voiceover once TTS is integrated.

6. REFERENCE REUSE MAP
Source path:line	Adapted into	Adaptation notes
3b1b_videos/custom/logo.py:192 LogoGenerationFlurry	I-01, P05-S11	Particle burst + assembly. Strip 3B1B logo geometry; use studio wordmark glyphs as the target shape.
3b1b_videos/custom/logo.py:211 WrittenLogo	I-01, P01-S01, all title cards	Variable per-glyph lag for the "forge" feel. Port the timing curve only.
3b1b_videos/custom/logo.py:216 LogoGenerationFivefold	I-03, P05-S01	5-fold radial assembly for 5-part roadmap. Replace logo spikes with part-color dots.
3b1b_videos/custom/opening_quote.py:8 OpeningQuote	P05-S04a, all part quotes	Quote-framing pacing — hold 3s, italic, centered.
3b1b_videos/_2024/transformers/network_flow.py:55 get_block	All pipeline scenes	Depth-aware pipeline block via CE Prism/Cube. Skip text-heavy labels.
3b1b_videos/_2024/transformers/network_flow.py:73 show_initial_text_embedding	P01-S02b, P01-S05	Token-tile → embedding-row idiom for source/target chips.
3b1b_videos/_2024/transformers/network_flow.py:161 play_simple_attention_animation	P01-S07c, P02-S09	Attention arcs as ShowPassingFlash on ArcBetweenPoints.
3b1b_videos/_2024/transformers/network_flow.py:174 progress_through_mlp_block	P01-S03b, P02-S07	Neuron-cloud inside a block. Use sparse dot+line, not full graph.
3b1b_videos/_2024/transformers/network_flow.py:227 mention_repetitions	P01-S03a, P02-S03, P02-S06, P04-S02	Brace + thin-block stack for "many similar steps".
3b1b_videos/_2026/hairy_ball/model3d.py:68 RadioTower	P03-S03, P05-S09	Lattice 4-leg + cross-strut tower built with Line3D. Color ORANGE_INFRA.
3b1b_videos/_2026/hairy_ball/model3d.py:260 RadioBroadcast + :275 update_shells	I-02, P02-S05, P05-S09	Expanding spherical shells driven by ValueTracker. Wrap as signals.radar_shells_3d.
welchlabs/once_useful_constructs/light.py:65 AmbientLight	I-02, P02-S12, P05-S09, every glow	Annulus stack with radial opacity falloff. Wrap as signals.ambient_glow.
welchlabs/once_useful_constructs/light.py:95 Spotlight	I-02, P02-S04a, P03-S03, P05-S09	Sector frustum from source. Wrap as signals.sensor_cone.
welchlabs/_2026/vla/p31_61_1.py:43 P61a	P01-S07a, P05-S08	Multi-camera patch-grid layout. Use generated colored squares (no asset paths).
welchlabs/_2026/vla/p31_61_1.py:149 P52_61	P01-S07b, P02-S09	Full VLA architecture skeleton — image encoders → embeddings → LLM → action expert. Adapt structure only.
welchlabs/_2026/vla/p31_61_1.py:214 make_embedding_row	P01-S07a, P02-S09	Compact embedding-bar row. Port as studio.components.charts.feature_rows.
welchlabs/_2026/vla/p31_61_1.py:332 (diffusion frames)	P04-S04, P05-S06b	Noise → clean signal frame sequence.
welchlabs/_2026/vla/p31_61_1.py:654 (ReplacementTransform rows)	P01-S08a, P05-S06b	Transform language-color rows into action-color rows.
welchlabs/_2026/vla/p31_61_1.py:671 P34_Pickup	P01-S08a	Prompt + multi-view + action expert composition.
welchlabs/once_useful_constructs/vector_space_scene.py:204 LinearTransformationScene	P03-S04b, P03-S06	Coordinate-frame alignment for calibration.
welchlabs/once_useful_constructs/region.py:50 plane_partition	P02-S12, P03-S08	Occlusion / risk-field polygon partitioning.
welchlabs/_2025/generalization/p8_15.py	P01-S04a, P05-S04c	Long-tail / power-law curve idiom.
welchlabs/_2025/generalization/p46_56.py	P05-S04c	Scaling-curve reveal pattern.
welchlabs/_2025/backprop_3/geometry_while_learning_2.py	P02-S11b, P04-S05	Optimization trajectory over loss landscape.
welchlabs/_2025/backprop_3/decision_boundary_utils.py	P01-S04a, P04-S05	Decision-region overlays for failure / generalization.
3b1b_videos/_2018/uncertainty.py	P03-S07, P03-S08	Gaussian / uncertainty cloud idioms.
3b1b_videos/_2026/spheres_talk/volumes.py:53 VolumeGrid	P04-S04	Voxel grid + cell highlights.
3b1b_videos/_2026/spheres_talk/volumes.py:365 BuildCircleWithCombinedAnnulusses	P05-S08	Splat composition motif.
3b1b_videos/_2026/spheres_talk/random_puzzles.py:18 DotHistory	P05-S06a, P05-S09	Fading-trail for moving agents. Wrap as agents.agent_trail.
3b1b_videos/_2020/covid.py:205 ViralSpreadModel	P02-S02a, P05-S02a	Counter-driven population motion.
3b1b_videos/_2020/covid.py:723 ViralSpreadModelWithClusters	P02-S02b, P05-S02b, P05-S07, P05-S09	Clustered agent dynamics → district behavior, zombie city.
3b1b_videos/_2020/covid.py:770 ShowLogisticCurve	P01-S02a, P01-S08b, P03-S11, P04-S03, P05-S05b	Curve-reveal idiom.
3b1b_videos/_2023/optics_puzzles/adding_waves.py	I-02, P02-S05	Wave interference pattern.
3b1b_videos/_2023/optics_puzzles/wave_machine.py	P04-S06	Latency-pulse propagation.
welchlabs/once_useful_constructs/graph_theory.py:56 DiscreteGraphScene	P03-S10	V2X graph topology.
welchlabs/once_useful_constructs/linear_algebra.py:32 vector_coordinate_label	P03-S04b	Vector / matrix labels.
7. IMPLEMENTATION SESSIONS
Each session ≤ ~14 scenes of code. Read the listed references once per session. Complexity: S (~30 min/scene), M (~60), L (~120), XL (>120).

Session 1 — studio/components/ package
Scenes: none (foundation only).
Files to build: all 10 component modules per Section 2.2 + config.py + __init__.py + a tiny _smoke_test.py that renders one of every component.
References to read: network_flow.py:5-260, model3d.py:68-310, light.py:32-220, p31_61_1.py:214 (embedding row), region.py:50, vector_space_scene.py:204.
Complexity: XL (foundation; one full session).
Dependencies: none.
Done when: _smoke_test.py renders at -ql showing every component once, no warnings, no missing fonts.
Session 2 — Intro + Part 1
Scenes: I-01, I-02, I-03, I-04, P01-S01..P01-S10 (14 total).
References to read: logo.py:103-216, opening_quote.py, vla/p31_61_1.py:43-671, generalization/p8_15.py.
Complexity: I-02 = XL (3D hero), P01-S07b/S08a = L each, others M/S. Estimate 2 sessions if budget tight.
Dependencies: Session 1 components.
Done when: all 14 scenes render -ql, frame-check at 35/60/85% each.
Session 3 — Part 2
Scenes: P02-S01..P02-S14 (14 total — S05 hero counts as 1 but XL).
References to read: model3d.py:260 (already read), adding_waves.py, decision_boundary_utils.py, region.py:50, e_field.py.
Complexity: S05 = XL (3D hero, the project's emotional climax), S11b = L, S09/S12 = L, others M/S.
Dependencies: Session 1 components.
Done when: all 14 P2 scenes render -ql.
Session 4 — Part 3
Scenes: P03-S01..P03-S15 (15 total).
References to read: vector_space_scene.py:204, linear_algebra.py:32, _2018/uncertainty.py, region.py, graph_theory.py:56, optics/objects.py.
Complexity: S04b/S07/S08/S12 = L each, others M/S.
Dependencies: Session 1 components.
Done when: all 15 P3 scenes render -ql; calibration matrix scene visibly correct.
Session 5 — Part 4
Scenes: P04-S01..P04-S10 (10 total).
References to read: spheres_talk/volumes.py:53, backprop_3/geometry_while_learning_2.py, backprop_3/decision_boundary_utils.py, network_flow.py:55, optics/wave_machine.py.
Complexity: S04/S08 = L each (P4 climax scenes), S05 = L, others M.
Dependencies: Session 1 components.
Done when: all 10 P4 scenes render -ql; CooPre reconstruction visually convincing.
Session 6 — Part 5 + Finale
Scenes: P05-S01..P05-S11 (11 total — S09 hero is XL).
References to read: logo.py:216 (already), opening_quote.py (already), covid.py:205-770, random_puzzles.py:18, model3d.py:260 (already), volumes.py:365.
Complexity: S09 = XL (3D living city — the visual climax), S04b/S04c/S06b/S07/S08 = L, others M.
Dependencies: Session 1 components.
Done when: all 11 P5 scenes render -ql; living city orbit smooth.
Session 7 — Render all + QA
Scenes: re-render the full 73 scenes at -qh (1080p60).
Tasks: run frame check protocol on every scene, fix bugs found, then concatenate per-part with merge_videos.ps1, then full video.
Complexity: depends on bug count.
Done when: one concatenated 50–60-minute MP4 at 1080p60.
8. RISK LOG
Risk	Likelihood	Impact	Mitigation
CMU Serif not installed on user machine	M	M (visual quality)	detect_primary_font() falls back to Latin Modern Roman; raise loudly if neither found, so user installs early. Document install steps in studio/DESIGN_SYSTEM.md.
MarkupText Pango markup escapes inconsistent (e.g., & in text)	M	S	Add a small markup_safe(s) helper in typography.py that escapes <, >, & outside spans.
3D scenes (I-02, P02-S05, P05-S09) hit OpenGL renderer perf issues on Windows	M	L	Limit shell count to ≤ 5 per source; cap drawn agents in P05-S09 to ~30; test on a single render very early in Session 2 (do I-02 first).
--renderer=opengl does not save video on some Manim CE versions	L	L	Confirm before Session 2 by rendering i02 skeleton; if broken, fall back to cairo 3D with ThreeDScene only (lower quality but reliable).
Reference files in Source_manim_reference/ use manimlib APIs that diverge from CE (e.g., LaggedStartMap, VFadeIn, DotCloud)	H	M	The audit already flagged this. Always port the visual idea — never from manimlib import .... Use Succession, LaggedStart(*[FadeIn(m) for m in mobs]), OpenGLPointCloudDot analogs.
Image-patch references in vla/p31_61_1.py depend on Welch's local image assets	H	S	Replace patch images with generated colored squares via boost_colors_hsv adapted helper. Already noted in audit.
Scene count (73) exceeds time-budget if each takes ~1h	M	M	Sessions 2-6 each have ≤ 15 scenes. If overrunning, push P03-S13 (InfraX) and P03-S14 (summary) to Session 7. They are low-stakes.
Quote scenes (I-02, P02-S05, P05-S04a, P05-S11) need fonts that render italic well	L	S	Both CMU Serif and LMR include italic variants; verify by rendering a 5-glyph italic test in Session 1 smoke test.
manim-voiceover integration deferred but scripts already in scene files	L	S	Top-of-file SCRIPT = """...""" literal — no API call — costs nothing to keep.
Cross-platform path separators in render scripts	L	S	Use forward slashes in Manim file paths even on Windows; PowerShell accepts both.
Unicode glyphs (✓, ★, →) in text break Pango on some font fallbacks	M	S	Replace with [OK], *, -> per the prompt's anti-patterns. Already in MarkupText Pattern E.
Live demos / poster requests pull from studio/ mid-build	L	M	Keep beyond/ intact as reference snapshot per CLAUDE.md instruction. Do not delete.
User changes part order or speaker list	L	L	Plan keeps speaker names in title-card scene only — single edit per part.
End of plan. Total: 73 scenes designed, 10 components specified, 7 implementation sessions scoped, full reference reuse map, all script drift notes captured. Ready for Session 1 (components) to start in a fresh Claude Code session, referring only to this document plus the listed reference files.