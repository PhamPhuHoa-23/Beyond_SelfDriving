"""Phase 1 3D smoke test — Studio3DScene with rsu_tower_3d + radar_shells_3d."""
from manimlib import *
from studio.components import (
    Studio3DScene, rsu_tower_3d, radar_shells_3d,
    ORANGE_INFRA, CYAN_RADAR,
)


class Smoke3D(Studio3DScene):
    PART_NUM = 2
    SCENE_TITLE = "3D Smoke Test"

    def construct(self):
        tower = rsu_tower_3d(color=ORANGE_INFRA, height=2.0)
        tower.move_to(ORIGIN)
        self.play(ShowCreation(tower, run_time=1.5))

        shells, shell_anim = radar_shells_3d(
            ORIGIN, color=CYAN_RADAR, n_shells=4, max_radius=3.0,
        )
        self.play(shell_anim)

        # manimgl uses frame.add_ambient_rotation (angular_speed in DEG/s)
        self.frame.add_ambient_rotation(1 * DEG)
        self.wait(2)
        self.frame.clear_updaters()

        self.play(FadeOut(VGroup(tower, shells)))
