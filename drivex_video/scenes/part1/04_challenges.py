from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT

class CornerCases(Scene):
    def construct(self):
        title = Text("The 'Long Tail' Challenge", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        
        # Mascot (Auto-updated since we use the same path)
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.0)
        mascot.to_corner(DR, buff=0.3)

        asset_dir = "../../../materials/images/part1_new/"
        # Correct mapping identified by viewing: 025 (Person), 026 (Truck), 027 (Snow)
        photo_names = ["p1_new-025.jpg", "p1_new-026.jpg", "p1_new-027.jpg"]
        captions = ["Interacting Pedestrians", "Ambiguous Objects", "Adverse Weather"]
        
        photos = []
        for i, img_name in enumerate(photo_names):
            p_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + img_name))
            img = ImageMobject(p_path)
            img.height = 2.5
            cap = Text(captions[i], font_size=14).next_to(img, DOWN, buff=0.15)
            photos.append(Group(img, cap))
            
        photo_grid = Group(*photos).arrange(RIGHT, buff=0.4).next_to(title, DOWN, buff=0.8)

        self.play(Write(title))
        self.play(FadeIn(mascot, shift=UP*0.3))
        self.wait(0.5)
        
        self.play(LaggedStart(*[FadeIn(p, shift=UP*0.2) for p in photos], lag_ratio=0.5))
        self.wait(1.5)
        
        tail_text = Text("We need contextual reasoning to solve these.", font_size=20, slant=ITALIC)
        tail_text.set_color(UCLA_GOLD).next_to(photo_grid, DOWN, buff=0.8)
        
        self.play(FadeIn(tail_text, shift=UP*0.2))
        self.play(Indicate(mascot))
        self.wait(3)
        
        self.play(FadeOut(Group(title, photo_grid, tail_text, mascot)))
        self.wait(0.5)
