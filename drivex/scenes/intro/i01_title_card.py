# drivex/scenes/intro/i01_title_card.py
# ─────────────────────────────────────────────────────────────────
# SCENE I-01: Title Card & Team Introduction  (~45s)
#
# Spec: spec_intro_part01.md → SCENE I-01
#   - NAVY background
#   - Title "Beyond Self-Driving" in GOLD
#   - Subtitle, presenter name, org/lab
#   - UCLA logo (placeholder)
#   - Divider line
#   - Contact / permission note
#   - CAR mascot bottom-right, idle
# ─────────────────────────────────────────────────────────────────

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from manim import *
from drivex.components.colors import (
    COL_NAVY, COL_BLUE, COL_GOLD, COL_LIGHT_BLUE,
    COL_WHITE, BG_DARK,
)
from drivex.components.mascots import create_car_mascot, idle_bounce
from drivex.components.slide_helper import SlideImage


class I01TitleCard(Scene):
    """SCENE I-01 — Title Card & Team Introduction"""

    def construct(self):
        self.camera.background_color = COL_NAVY

        # ── Background rect (explicit for FadeIn) ────────────────
        bg = Rectangle(
            width=config.frame_width, height=config.frame_height,
            fill_color=COL_NAVY, fill_opacity=1,
            stroke_width=0,
        )

        # ── UCLA logo (placeholder) ───────────────────────────────
        logo = SlideImage("intro/ucla_logo.png", width=1.5, height=0.8)
        logo.to_corner(UL, buff=0.4)

        # ── Title ─────────────────────────────────────────────────
        title = Text(
            "Beyond Self-Driving",
            font_size=52, color=COL_GOLD, weight=BOLD,
        ).center().shift(UP * 1.4)

        # ── Subtitle ──────────────────────────────────────────────
        subtitle = Text(
            "ICCV 2025 Tutorial — Team Summary",
            font_size=24, color=COL_WHITE,
        ).next_to(title, DOWN, buff=0.3)

        # ── Presenter ─────────────────────────────────────────────
        presenter = Text(
            "[Presenter Name] · UCLA",
            font_size=20, color=COL_LIGHT_BLUE,
        ).next_to(subtitle, DOWN, buff=0.25)

        # ── Org label ─────────────────────────────────────────────
        org = Text(
            "[Lab Name] · UCLA Mobility Lab",
            font_size=18, color=COL_WHITE,
        ).set_opacity(0.7).next_to(presenter, DOWN, buff=0.15)

        # ── Divider ───────────────────────────────────────────────
        divider = Line(LEFT * 4.0, RIGHT * 4.0,
                       stroke_color=COL_BLUE, stroke_width=2.5)
        divider.next_to(org, DOWN, buff=0.35)

        # ── Contact note ──────────────────────────────────────────
        contact = Text(
            "For questions about the original material: UCLA Mobility Lab",
            font_size=15, color=COL_WHITE,
        ).set_opacity(0.6).next_to(divider, DOWN, buff=0.3)

        # ── CAR mascot ────────────────────────────────────────────
        car = create_car_mascot(height=1.6)
        car.to_corner(DR, buff=0.5)

        # ── Animation sequence ────────────────────────────────────
        self.add(bg)
        self.play(Write(title), run_time=1.2)
        self.play(
            FadeIn(subtitle, shift=UP * 0.15),
            run_time=0.5,
        )
        self.play(FadeIn(logo), run_time=0.4)
        self.play(
            FadeIn(presenter),
            FadeIn(org),
            run_time=0.5,
        )
        self.play(Create(divider), run_time=0.4)
        self.play(FadeIn(contact), run_time=0.4)
        self.play(FadeIn(car, shift=LEFT * 0.3), run_time=0.6)

        # Idle bounce animation for mascot
        self.play(idle_bounce(car, amplitude=0.07, run_time=0.9))
        self.wait(1.5)

        # Outro fade
        self.play(FadeOut(VGroup(
            title, subtitle, presenter, org, divider, contact, logo, car
        )), run_time=0.6)
        self.wait(0.3)
