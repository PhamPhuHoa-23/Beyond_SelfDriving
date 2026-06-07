"""Re-exports from studio.reference — do NOT hand-code substitutes here.

Always import from this module in scenes; implementations live in
Source_manim_reference ports under studio/reference/.
"""
from studio.reference.transformers_helpers import (
    EmbeddingArray,
    NumericEmbedding,
    RandomizeMatrixEntries,
    WeightMatrix,
)
from studio.reference.network_attention import play_simple_attention_animation
from studio.reference.vla_patches import make_embedding_row, make_embedding_row_stack
from studio.reference.light import AmbientLight, inverse_quadratic
from studio.reference.network_mlp import mlp_synapse_block, mention_repetitions_brace
from studio.reference.bev_grid import lidar_point_cloud_side, bev_token_grid, waypoint_polyline, qformer_stack

__all__ = [
    "EmbeddingArray",
    "NumericEmbedding",
    "RandomizeMatrixEntries",
    "WeightMatrix",
    "play_simple_attention_animation",
    "make_embedding_row",
    "make_embedding_row_stack",
    "AmbientLight",
    "inverse_quadratic",
    "mlp_synapse_block",
    "mention_repetitions_brace",
    "lidar_point_cloud_side",
    "bev_token_grid",
    "waypoint_polyline",
    "qformer_stack",
]
