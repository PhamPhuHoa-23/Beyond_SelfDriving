"""P01-S03c — Hybrid: ML vs classical modules (color-coded + legend)."""
from manimlib import *
from studio.components import (
    StudioScene, PURPLE_MODEL, INK_DARK, INK_MID, INK_LIGHT, ACCENT_BLUE,
    RED_ERROR, PASTEL_BLUE, PASTEL_AMBER,
    FONT_PRIMARY, SIZE_LABEL, SIZE_BODY, SIZE_CAPS,
    pipeline_block, CONTENT_TOP, TITLE_Y, v_arrow,
    error_propagation_marker,
)

# name, kind, stroke, fill
MODULES = [
    ("Perception", "ml", PURPLE_MODEL, "#EDE9FE"),
    ("Localization", "classical", INK_MID, PASTEL_BLUE),
    ("Prediction", "classical", INK_MID, PASTEL_BLUE),
    ("Planning", "ml", PURPLE_MODEL, "#EDE9FE"),
    ("Control", "classical", INK_MID, PASTEL_AMBER),
]


def _rectangular_glow(rect: Mobject, *, color: str, max_dilation: float = 0.28, n_levels: int = 8) -> VGroup:
    """Creates a fading halo that matches the rectangular shape of the target."""
    glow = VGroup()
    w = rect.get_width()
    h = rect.get_height()
    cr = rect.corner_radius if hasattr(rect, "corner_radius") else 0.18
    
    for i in range(1, n_levels + 1):
        dilation = max_dilation * (i / n_levels)
        alpha = 0.35 * (1.0 - i / (n_levels + 1)) ** 2
        
        glow_step = RoundedRectangle(
            width=w + 2 * dilation,
            height=h + 2 * dilation,
            corner_radius=cr + dilation,
            fill_color=color,
            fill_opacity=alpha,
            stroke_width=0,
        )
        glow_step.move_to(rect.get_center())
        glow.add(glow_step)
    return glow


def _legend_row(stroke: str, fill: str, title: str, stroke_width: float = 2.8) -> VGroup:
    swatch = RoundedRectangle(
        width=0.32, height=0.32, corner_radius=0.06,
        fill_color=fill, fill_opacity=1.0,
        stroke_color=stroke, stroke_width=stroke_width,
    )
    title_mob = Text(title, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
    return VGroup(swatch, title_mob).arrange(RIGHT, buff=0.14)


class P01S03CHybrid(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "Hybrid Systems"

    def construct(self):
        header = self._open(self.SCENE_TITLE)

        # Three recall chips (modular, end-to-end, hybrid)
        chips = VGroup(*(
            Circle(
                radius=0.07,
                fill_color=color, fill_opacity=opacity,
                stroke_color=stroke, stroke_width=1.2,
            )
            for color, stroke, opacity in [
                (INK_LIGHT, INK_MID, 0.25),      # Modular: greyed
                (INK_LIGHT, INK_MID, 0.25),      # E2E: greyed
                (ACCENT_BLUE, ACCENT_BLUE, 1.0), # Hybrid: lit
            ]
        )).arrange(RIGHT, buff=0.15)
        chips.move_to([5.5, TITLE_Y, 0])
        self.play(FadeIn(chips, run_time=0.3))

        blocks_list = []
        for name, kind, stroke, fill in MODULES:
            block = pipeline_block(name, width=2.55, height=0.62, fill=fill, stroke=stroke)
            if kind == "ml":
                block[0].set_stroke(width=3.5)
            else:
                block[0].set_stroke(width=1.5)
            blocks_list.append(block)

        blocks = VGroup(*blocks_list)
        blocks.arrange(DOWN, buff=0.20)

        # Construct legend
        legend = VGroup(
            _legend_row(PURPLE_MODEL, "#EDE9FE", "Learning", stroke_width=3.5),
            _legend_row(INK_MID, PASTEL_BLUE, "Estimation", stroke_width=1.5),
            _legend_row(INK_MID, PASTEL_AMBER, "Control", stroke_width=1.5),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)

        legend.next_to(blocks, RIGHT, buff=0.6)
        legend.move_to([legend.get_center()[0], blocks.get_center()[1], 0])

        col_x = blocks_list[0].get_center()[0]
        stack_arrows = VGroup(*(v_arrow(a, b, x=col_x) for a, b in zip(blocks_list[:-1], blocks_list[1:])))

        # Center combined blocks, stack_arrows, and legend vertically and horizontally
        diagram = VGroup(blocks, stack_arrows, legend)
        diagram.move_to([0, 0.6, 0])

        # Create rectangular glows for ML blocks (Perception = blocks_list[0][0], Planning = blocks_list[3][0])
        glow_perception = _rectangular_glow(blocks_list[0][0], color=PURPLE_MODEL)
        glow_planning = _rectangular_glow(blocks_list[3][0], color=PURPLE_MODEL)
        ml_glows = VGroup(glow_perception, glow_planning)

        # Pre-register glows to the scene with 0 opacity so they render behind the blocks
        for glow in ml_glows:
            for level in glow:
                level.target_opacity = float(level.get_fill_opacity())
                level.set_opacity(0)
        self.add(ml_glows)

        # Animate block fade ins: classical blocks first, then ML blocks + glows
        classical_blocks = VGroup(blocks_list[1], blocks_list[2], blocks_list[4])
        ml_blocks = VGroup(blocks_list[0], blocks_list[3])

        self.play(LaggedStart(*(FadeIn(b) for b in classical_blocks), lag_ratio=0.15))
        self.play(
            LaggedStart(*(FadeIn(b) for b in ml_blocks), lag_ratio=0.15),
            LaggedStart(*(
                level.animate.set_opacity(float(level.target_opacity))
                for glow in ml_glows
                for level in glow
            ), lag_ratio=0.05)
        )
        self.play(ShowCreation(stack_arrows))
        self.play(FadeIn(legend))
        self.wait(1.5)

        # Perform selective dimming to maintain text contrast
        dim_anims = []
        for b in blocks_list:
            dim_anims.append(b[0].animate.set_opacity(0.25)) # dim rectangles
            dim_anims.append(b[1].animate.set_opacity(0.55)) # dim labels but keep readable
            if len(b) > 2:
                dim_anims.append(b[2].animate.set_opacity(0.02)) # dim shadows
        for arr in stack_arrows:
            dim_anims.append(arr.animate.set_opacity(0.25)) # dim arrows
        for row in legend:
            dim_anims.append(row[0].animate.set_opacity(0.25)) # dim swatches
            dim_anims.append(row[1].animate.set_opacity(0.55)) # dim legend texts but keep readable
        for glow in ml_glows:
            for level in glow:
                dim_anims.append(level.animate.set_opacity(float(level.target_opacity * 0.25))) # dim glows
                
        self.play(*dim_anims, run_time=0.6)

        # Show payoff warning badge + "One shared weakness."
        warning_badge = error_propagation_marker(radius=0.18)
        weakness_text = Text(
            "One shared weakness.",
            font=FONT_PRIMARY, font_size=SIZE_BODY, color=RED_ERROR, weight=BOLD,
        )
        payoff = VGroup(warning_badge, weakness_text).arrange(RIGHT, buff=0.25)
        payoff.move_to([0, -2.1, 0])

        self.play(
            FadeIn(weakness_text, shift=0.1 * UP),
            GrowFromCenter(warning_badge),
            run_time=0.7
        )
        self.wait(2.5)
        self._close()

