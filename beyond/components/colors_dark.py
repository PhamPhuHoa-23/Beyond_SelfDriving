# beyond/components/colors_dark.py
# ─────────────────────────────────────────────────────────────────
# Dark-theme palette (Space Navy) — from BEYOND_SELFDRIVING_ANIMATION_GUIDE.md
# Default theme for the "Beyond Self-Driving" video.
# ─────────────────────────────────────────────────────────────────

# ── Backgrounds ──────────────────────────────────────────────────
BG_SPACE     = "#090E1A"   # Body scene default
BG_VOID      = "#030508"   # Part title card (darkest)
BG_GRID_LINE = "#0D1829"   # Grid / road surface tone
BG_PANEL     = "#0F1A2E"   # Info box fill

# ── Primary Text ─────────────────────────────────────────────────
TEXT_WHITE = "#E8EDF4"   # Main body text
TEXT_DIM   = "#6B7A99"   # Secondary / caption
TEXT_GHOST = "#2A3550"   # Background label, subtitle dim

# ── Brand Accents ────────────────────────────────────────────────
GOLD       = "#FFD100"   # UCLA Gold — title highlights
GOLD_GLOW  = "#FFE566"   # Lighter gold for glow
CYAN_NEON  = "#00E5FF"   # LiDAR beams, radar waves
CYAN_DIM   = "#0097A7"   # Dimmed sensor / secondary
BLUE_ELECTRIC = "#4D9FFF"  # V2X arrows, comm links
BLUE_SOFT  = "#1565C0"   # Agent box fill
GREEN_SIGNAL = "#00E676" # Success, ✓, AP gain
GREEN_DIM  = "#00796B"   # Background success fill
RED_ALERT  = "#FF1744"   # Error, miss, danger
RED_DIM    = "#B71C1C"   # Background danger fill
ORANGE_INFRA = "#FF6D00" # RSU / infrastructure nodes
PURPLE_MODEL = "#CE93D8" # Neural net / model blocks
PURPLE_DEEP  = "#4A148C" # Model fill background

# ── Part-Specific ────────────────────────────────────────────────
P1_FOUNDATION = "#7986CB"  # Indigo — Foundation Models
P2_COOP       = "#00BCD4"  # Teal — Cooperative Perception
P3_SIM        = "#4CAF50"  # Green — Sim-to-Real
P4_EFFICIENT  = "#FFC107"  # Amber — Efficiency / Quantization
P5_PHYSICAL   = "#F06292"  # Pink — Physical AI / Pedestrians

# ── Special Effects ──────────────────────────────────────────────
WAVE_CORE    = "#00E5FF"   # Center of radar / gravitational wave
WAVE_MID     = "#00607A"   # Mid-ring
WAVE_EDGE    = "#003344"   # Outer ring (fades)
GRID_LINE    = "#112233"   # BEV map grid lines
VOXEL_MASKED = "#1A237E"   # Masked voxel (dark blue)
VOXEL_ACTIVE = "#82B1FF"   # Active / visible voxel
LIDAR_BEAM   = "#80DEEA"   # LiDAR scan beam
COMM_LINK    = "#40C4FF"   # Vehicle-to-vehicle link
FP32_HEAVY   = "#FF5252"   # Full precision — expensive
INT8_LIGHT   = "#69F0AE"   # Quantized — fast, light

# ── UCLA Brand (title cards only) ────────────────────────────────
UCLA_BLUE = "#2774AE"
UCLA_GOLD = "#FFD100"

# ── Typography (sizes in Manim font_size units) ──────────────────
SIZE_HERO    = 52
SIZE_TITLE   = 38
SIZE_BODY    = 26
SIZE_LABEL   = 20
SIZE_CAPTION = 16
SIZE_MICRO   = 13

# ── Alias helpers used by older code ─────────────────────────────
BG_DARK   = BG_SPACE
BG_BLACK  = BG_VOID
BG_NIGHT  = BG_SPACE
COL_NAVY  = TEXT_WHITE   # "white text on dark bg" → TEXT_WHITE
COL_BLUE  = BLUE_ELECTRIC
COL_GOLD  = GOLD
COL_WHITE = TEXT_WHITE
COL_RED   = RED_ALERT
COL_GREEN = GREEN_SIGNAL
COL_PURPLE = PURPLE_MODEL
COL_LIGHT_BLUE = CYAN_DIM
COL_INFRA_ORANGE = ORANGE_INFRA
COL_ROAD_GRAY    = TEXT_DIM
COL_SENSOR_CYAN  = CYAN_NEON
COL_INT8_GREEN   = INT8_LIGHT
COL_FP32_RED     = FP32_HEAVY
COL_ENERGY_YELLOW = GOLD
COL_DEEP_PURPLE  = PURPLE_DEEP
COL_DEEP_GREEN   = GREEN_DIM
COL_DEEP_BLUE    = BG_PANEL
COL_GRAY_FILL    = BG_GRID_LINE
COL_DANGER_FILL  = RED_DIM
COL_SOFT_PURPLE  = PURPLE_MODEL

# Part 05 extras (not in original drivex/components/colors.py)
COL_PEDESTRIAN = P5_PHYSICAL
COL_ROBOT_TEAL = "#1ABC9C"
COL_SIM_PURPLE = "#9B59B6"
COL_MESH_GRAY  = "#7F8C8D"
