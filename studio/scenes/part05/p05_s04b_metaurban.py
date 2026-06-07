"""P05-S04b MetaUrban Generator."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_PINK, GOLD_RICH, CYAN_RADAR, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    pipeline_block, contribution_badge, key_number,
)
SCRIPT = """MetaUrban generates urban scenes from a script: layout, intersections, objects. No two scenes alike."""


class P05S04BMetaUrban(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "MetaUrban Generator"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        input_block = pipeline_block("generate_scene(\nparams...)", fill="#F0FDF4", stroke="#10B981", width=3.0, height=1.2)
        input_block.move_to(LEFT * 3.5 + UP * 0.3)
        gear = Circle(radius=0.5, fill_color=CYAN_RADAR, fill_opacity=0.2, stroke_color=CYAN_RADAR, stroke_width=2.5)
        gear_lbl = Text("Generator", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=CYAN_RADAR)
        gear_grp = VGroup(gear, gear_lbl).arrange(DOWN, buff=0.08)
        gear_grp.move_to(ORIGIN + UP * 0.3)
        self.play(FadeIn(input_block), GrowFromCenter(gear_grp))
        gen_arrow = Arrow(input_block.get_right() + RIGHT * 0.08, gear_grp.get_left() + LEFT * 0.08,
                          fill_color=CYAN_RADAR, thickness=2.6, buff=0)
        out_arrow = Arrow(gear_grp.get_right() + RIGHT * 0.08, RIGHT * 2.25 + UP * 0.3,
                          fill_color=ACCENT_PINK, thickness=2.6, buff=0)
        self.play(ShowCreation(gen_arrow), ShowCreation(out_arrow))
        # Output scenes cycling
        scene_labels = ["Urban Scene 1", "Urban Scene 2", "Urban Scene 3", "Urban Scene ..."]
        colors = [ACCENT_PINK, GOLD_RICH, CYAN_RADAR, INK_MID]
        last_scene = None
        for lbl, col in zip(scene_labels, colors):
            s = pipeline_block(lbl, fill=BG_PAPER, stroke=col, width=2.4, height=0.7)
            s.move_to(RIGHT * 3.5 + UP * 0.3)
            if last_scene is None:
                self.play(FadeIn(s, scale=1.08, run_time=0.3))
            else:
                self.play(FadeOut(last_scene, scale=0.92, run_time=0.18), FadeIn(s, scale=1.08, run_time=0.22))
            self.wait(0.2)
            last_scene = s
        kn = key_number("many", "generated environments", color=ACCENT_PINK)
        kn.to_corner(DR, buff=0.5)
        self.play(FadeIn(kn))
        self.wait(2)
        self._close()
