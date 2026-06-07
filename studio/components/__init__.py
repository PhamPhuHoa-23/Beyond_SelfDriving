"""Re-export all studio component symbols."""
from studio.components.colors import *
from studio.components.typography import (
    FONT_PRIMARY, FONT_MONO,
    SIZE_HERO, SIZE_TITLE, SIZE_H1, SIZE_BODY, SIZE_LABEL, SIZE_CAPS, SIZE_MICRO,
    text, markup, math, gold_key_number, bold_text, italic_text,
)
from studio.components.layout import (
    TITLE_Y, SEP_Y, CONTENT_TOP, CONTENT_BOTTOM, FOOTER_Y,
    LEFT_X, RIGHT_X, CENTER_X, MAX_TEXT_X,
    place_title, place_left, place_right, place_footer,
    two_column, three_column, grid_4,
    content_row, content_column, match_left_edges, fm_three_lane,
)
from studio.components.base_scene import StudioScene, Studio3DScene
from studio.components.pipeline import (
    pipeline_block, pipeline_row, pipeline_column, pipeline_arrow,
    pipeline_flow, stage_panel, h_arrow, v_arrow, link_rect,
)
from studio.components.charts import (
    axes_deploy, bar_reveal, bar_group_labels, curve_trace, scatter_rain,
    place_chart, chart_mount, chart_labels, CHART_WIDTH, CHART_HEIGHT,
)
from studio.components.model_viz import (
    EmbeddingArray, NumericEmbedding, RandomizeMatrixEntries, WeightMatrix,
    play_simple_attention_animation,
    make_embedding_row, make_embedding_row_stack,
    AmbientLight, inverse_quadratic,
)
from studio.reference.network_mlp import mlp_synapse_block, mention_repetitions_brace
from studio.components.agents import (
    vehicle_icon, vehicle_icon_3d, pedestrian_icon, rsu_icon, rsu_tower_3d,
    drone_icon, agent_trail,
)
from studio.components.signals import (
    radar_shells_2d, radar_shells_3d, sensor_cone,
    v2x_link, ambient_glow, interference_pattern, sort_spherical_waves_to_camera,
    spherical_coverage_3d,
)
from studio.components.annotations import (
    callout, error_callout, error_propagation_marker,
    thought_bubble, contribution_badge, key_number, failure_icon,
)
from studio.components.assets import img_or_placeholder
from studio.components.animations import (
    forge_text, particle_assemble, fivefold_assemble,
    scan_reveal, dust_dissolve, write_chiseled,
)
