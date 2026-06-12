"""P04-S09 Efficiency Summary: 3 gold cards."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_AMBER, GOLD_KEY, GOLD_RICH, GREEN_FIX,
    ACCENT_BLUE, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    contribution_badge, key_number,
)
SCRIPT = """Three efficiency contributions, three key numbers: 50% labels, 45 epochs, 300x."""


class P04S09EfficiencySummary(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "Part 4 Efficiency Contributions"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        cards_data = [
            ("Data", "CooPre", "50% labels \u2192 same performance", ACCENT_BLUE, "50%"),
            ("Training", "TurboTrain", "120 epochs \u2192 45 epochs", ACCENT_AMBER, "45 ep"),
            ("Inference", "QuantV2X", "100 MB \u2192 0.33 MB \u2192 300x smaller", GREEN_FIX, "300x"),
        ]
        cards = VGroup()
        for category, method, detail, color, key in cards_data:
            bg = RoundedRectangle(width=3.5, height=2.0, corner_radius=0.2,
                                  fill_color=BG_PAPER, fill_opacity=1.0,
                                  stroke_color=color, stroke_width=2.5)
            cat_lbl = Text(category, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=color, weight=BOLD)
            meth_lbl = Text(method, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
            detail_lbl = Text(detail, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID)
            if detail_lbl.get_width() > 3.1:
                detail_lbl.scale(3.1 / detail_lbl.get_width())
            key_lbl = Text(key, font=FONT_PRIMARY, font_size=40, color=GOLD_RICH, weight=BOLD)
            inner = VGroup(cat_lbl, meth_lbl, detail_lbl, key_lbl).arrange(DOWN, buff=0.08)
            inner.move_to(bg)
            cards.add(VGroup(bg, inner))
        cards.arrange(RIGHT, buff=0.4).move_to(ORIGIN + DOWN * 0.2)
        self.play(LaggedStart(*(FadeIn(c, scale=0.85) for c in cards), lag_ratio=0.25))
        self.wait(2)
        self._close()
