from manimlib.animation.fading import FadeIn, FadeOut

class FadeInFromDown(FadeIn):

    def __init__(self, mobject, **kwargs):
        super().__init__(mobject, UP, **kwargs)

class FadeOutAndShiftDown(FadeOut):

    def __init__(self, mobject, **kwargs):
        super().__init__(mobject, DOWN, **kwargs)

class FadeInFromLarge(FadeIn):

    def __init__(self, mobject, scale_factor=2, **kwargs):
        super().__init__(mobject, scale=1 / scale_factor, **kwargs)