# beyond/components/colors_white.py
# ─────────────────────────────────────────────────────────────────
# White-theme palette — from plans/01_DESIGN_SYSTEM.md & CLAUDE.md.
# Clean/academic look for slide-style presentation.
# ─────────────────────────────────────────────────────────────────

# ── Backgrounds ──────────────────────────────────────────────────
BG_SPACE     = "#FFFFFF"   # Body scene default (pure white)
BG_VOID      = "#0F172A"   # Part title card (deep navy)
BG_GRID_LINE = "#F1F5F9"   # Subtle grid tint
BG_PANEL     = "#EFF6FF"   # Info box fill (light blue)

# ── Primary Text ─────────────────────────────────────────────────
TEXT_WHITE = "#334155"   # Main text (slate navy — not pure black)
TEXT_DIM   = "#64748B"   # Secondary / caption
TEXT_GHOST = "#CBD5E1"   # Faint background labels

# ── Brand Accents ────────────────────────────────────────────────
GOLD         = "#D97706"   # Amber emphasis (visible on white)
GOLD_GLOW    = "#F59E0B"   # Lighter amber
CYAN_NEON    = "#0891B2"   # Cyan — sensor / LiDAR
CYAN_DIM     = "#06B6D4"   # Lighter cyan
BLUE_ELECTRIC = "#2563EB"  # Blue arrows / links
BLUE_SOFT    = "#DBEAFE"   # Agent box fill (light blue)
GREEN_SIGNAL = "#16A34A"   # Success, ✓
GREEN_DIM    = "#DCFCE7"   # Background success fill
RED_ALERT    = "#DC2626"   # Error, danger
RED_DIM      = "#FEE2E2"   # Background danger fill
ORANGE_INFRA = "#EA580C"   # RSU / infrastructure
PURPLE_MODEL = "#7C3AED"   # Neural net blocks
PURPLE_DEEP  = "#EDE9FE"   # Light purple fill

# ── Part-Specific ────────────────────────────────────────────────
P1_FOUNDATION = "#4F46E5"   # Indigo
P2_COOP       = "#0891B2"   # Teal
P3_SIM        = "#16A34A"   # Green
P4_EFFICIENT  = "#D97706"   # Amber
P5_PHYSICAL   = "#DB2777"   # Pink

# ── Special Effects (visible on white) ───────────────────────────
WAVE_CORE    = "#0891B2"
WAVE_MID     = "#BAE6FD"
WAVE_EDGE    = "#E0F2FE"
GRID_LINE    = "#E2E8F0"
VOXEL_MASKED = "#C7D2FE"
VOXEL_ACTIVE = "#4F46E5"
LIDAR_BEAM   = "#06B6D4"
COMM_LINK    = "#3B82F6"
FP32_HEAVY   = "#EF4444"
INT8_LIGHT   = "#10B981"

# ── UCLA Brand ───────────────────────────────────────────────────
UCLA_BLUE = "#2774AE"
UCLA_GOLD = "#FFD100"

# ── Typography ───────────────────────────────────────────────────
SIZE_HERO    = 48
SIZE_TITLE   = 34
SIZE_BODY    = 24
SIZE_LABEL   = 18
SIZE_CAPTION = 14
SIZE_MICRO   = 12

# ── Alias helpers (mirror dark names for cross-theme code) ────────
BG_DARK   = BG_SPACE
BG_BLACK  = BG_VOID
BG_NIGHT  = BG_SPACE
COL_NAVY  = TEXT_WHITE
COL_BLUE  = BLUE_ELECTRIC
COL_GOLD  = GOLD
COL_WHITE = TEXT_WHITE
COL_RED   = RED_ALERT
COL_GREEN = GREEN_SIGNAL
COL_PURPLE = PURPLE_MODEL
COL_LIGHT_BLUE   = BLUE_SOFT
COL_INFRA_ORANGE = ORANGE_INFRA
COL_ROAD_GRAY    = TEXT_DIM
COL_SENSOR_CYAN  = CYAN_NEON
COL_INT8_GREEN   = INT8_LIGHT
COL_FP32_RED     = FP32_HEAVY
COL_ENERGY_YELLOW = GOLD
COL_DEEP_PURPLE  = PURPLE_DEEP
COL_DEEP_GREEN   = GREEN_DIM
COL_DEEP_BLUE    = BLUE_SOFT
COL_GRAY_FILL    = "#F1F5F9"
COL_DANGER_FILL  = RED_DIM
COL_SOFT_PURPLE  = "#A78BFA"

COL_PEDESTRIAN = P5_PHYSICAL
COL_ROBOT_TEAL = "#0D9488"
COL_SIM_PURPLE = "#7C3AED"
COL_MESH_GRAY  = "#94A3B8"
