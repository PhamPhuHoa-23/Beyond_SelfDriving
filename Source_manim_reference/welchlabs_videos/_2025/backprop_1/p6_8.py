from manimlib import *
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
asset_dir = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/graphics/'

class P6_8_v2(InteractiveScene):

    def construct(self):
        v = SVGMobject(asset_dir + 'intro_rewrite_graphics_2.svg')
        img_1 = ImageMobject(asset_dir + 'intro_rewrite_graphics_3.png')
        img_2 = ImageMobject(asset_dir + 'intro_rewrite_graphics_4.png')
        img_1.set_opacity(0.0)
        img_2.set_opacity(0.0)
        v.scale(2.0)
        self.add(img_1)
        self.add(img_2)
        self.frame.reorient(0, 0, 0, (-1.73, 0.07, 0.0), 2.35)
        r1 = RoundedRectangle(corner_radius=0.09, height=9.0 / 4.89, width=16.0 / 4.89)
        r1.set_stroke(color=CHILL_BROWN, width=4.0)
        r1.move_to([-1.735, -0.015, 0])
        self.play(ShowCreation(r1), run_time=2)
        self.play(FadeIn(v[2:14]))
        self.wait()
        img_1.set_opacity(1.0)
        self.wait()
        self.add(v[14:24])
        self.play(FadeIn(v[1]), img_2.animate.set_opacity(1.0), self.frame.animate.reorient(0, 0, 0, (0.0, 0.05, 0.0), 4.12), run_time=4.0)
        self.wait()
        self.embed()
        self.wait(20)