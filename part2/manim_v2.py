from typing import Tuple, cast
from manim import (
    Line,
    bezier,
    Circle,
    Vector,
    NumberPlane,
    DashedLine,
    Tex,
    MathTex,
    Arrow,
    Rectangle,
    ImageMobject,
    SVGMobject,
    Axes,
    Dot,
    Ellipse,
    Text,
    Square,
    SurroundingRectangle,
    Create,
    FadeIn,
    FadeOut,
    ApplyMatrix,
    Rotate,
    ReplacementTransform,
    Indicate,
    interpolate_color,
    config,
    Write,
    Transform,
    VMobject,
    VGroup,
    BLUE,
    GREEN,
    RED,
    WHITE,
    YELLOW,
    ORANGE,
    GREY,
    TAU,
    PI,
    ORIGIN,
    LEFT,
    RIGHT,
    UP,
    DOWN,
    UR,
    UL,
    DL,
    GrowArrow,
    PURE_CYAN
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import theme
import numpy as np
import copy
from pathlib import Path

# Assuming theme.py defines standard styles, but adhering to your specific color rules:
# Input: BLUE, Eigen-stuff: RED, Labels: WHITE


class DiagonalizationIntro(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()
        self.plane.get_axes().set_color(theme.MUTED)

        # 1. SETUP THE PLANE (Lead/Medium)

        self.i_hat.set_opacity(0)
        self.j_hat.set_opacity(0)

        matrix = np.array([[2, 1], [0, 1.5]])
        matrix_tex = MathTex(
            "A = \\begin{bmatrix} 2 & 1 \\\\ 0 & 1.5 \\end{bmatrix}",
            color=theme.TEXT
        ).to_corner(UL)
        matrix_tex.set_opacity(0)

        with self.voiceover(
            text="Every linear transformation, no matter how complex-looking, is an ordered sequence of a few simple moves."
        ) as tracker:
            self.play(
                FadeIn(self.plane),
                FadeIn(self.background_plane),
                FadeIn(self.i_hat),
                FadeIn(self.j_hat),
                Write(matrix_tex),
                run_time=tracker.duration * 0.6
            )

        self.bring_to_front(matrix_tex)
        self.wait(0.5)

        # 2. VECTORS (Lead/Medium)
        with self.voiceover(text="Let's take some vectors and transform them with the matrix on the top left. Pay attention to the vectors' directions.") as tracker:  # noqa: E501
            v1 = self.add_vector([1, 0],   color=BLUE, animate=False)
            v2 = self.add_vector([-2, 1],  color=BLUE, animate=False)
            v_off1 = self.add_vector([0, 1],  color=GREY, animate=False)
            v_off2 = self.add_vector([-1, 1], color=GREY, animate=False)
            span1 = DashedLine((-10, 0, 0), (10, 0, 0), color=GREY, stroke_opacity=0.5)
            span2 = DashedLine((-10, 5, 0), (10, -5, 0), color=GREY, stroke_opacity=0.5)
            self.play(
                GrowArrow(v1),
                GrowArrow(v2),
                GrowArrow(v_off1),
                GrowArrow(v_off2),
                Create(span1), Create(span2),
                matrix_tex.animate.set_opacity(1),
                run_time=tracker.duration * 0.6,
            )

        self.apply_matrix(matrix, run_time=2, path_arc=0)
        self.wait(1)

        with self.voiceover(text="Some changed their directions, some didn't.") as tracker:
            self.wait(tracker.duration)

        self.wait(0.5)

        # 4. EIGENVECTORS (Follow/Short)
        with self.voiceover(
            text="We call those vectors that didn't, eigenvectors."
        ) as tracker:
            # Re-color the eigenvectors to RED as they are named
            self.play(
                v1.animate.set_color(RED),
                v2.animate.set_color(RED),
                v_off1.animate.set_opacity(0.2),
                v_off2.animate.set_opacity(0.2),
                self.i_hat.animate.set_opacity(0),
                self.j_hat.animate.set_opacity(0),
                run_time=tracker.duration * 0.6,
            )
            self.play(Indicate(VGroup(v1, v2), color=RED), run_time=tracker.duration * 0.4)

        # 5. EIGENVALUES (Follow/Medium)
        with self.voiceover(
            text="And how much the vectors stretched in their directions, we call eigenvalues."
        ) as tracker:
            # Show the scaling factor
            val1 = MathTex("\\lambda_1 = 2", color=RED)
            val1.next_to(v1.get_end(), UP)
            val2 = MathTex("\\lambda_2 = 1.5", color=RED)
            val2.next_to(v2.get_end(), DOWN, buff=0.7)
            self.play(
                Write(val1), Write(val2),
                run_time=min(tracker.duration, 1.5),
            )

        # 6. BASIS & DIAGONALIZATION (Hold/Breathe)
        # Full equation
        pdp_tex = MathTex(
            "A", "=", "P", "D", "P^{-1}",
            substrings_to_isolate=["A", "P", "D", "P^{-1}"],
            color=theme.TEXT,
        ).scale(1.1).center()

        # Values below
        p_val = MathTex(
            "P = \\begin{bmatrix} 1 & -2 \\\\ 0 & 1 \\end{bmatrix}",
            color=theme.TEXT,
        ).scale(0.8)
        d_val = MathTex(
            "D = \\begin{bmatrix} 2 & 0 \\\\ 0 & 1.5 \\end{bmatrix}",
            color=RED,
        ).scale(0.8)
        pinv_val = MathTex(
            "P^{-1} = \\begin{bmatrix} 1 & 2 \\\\ 0 & 1 \\end{bmatrix}",
            color=theme.TEXT,
        ).scale(0.8)

        with self.voiceover(text="And here is the interesting part.") as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="If a matrix happens to have a complete set of eigenvectors, we can use them to form a new basis."  # noqa E501
        ) as tracker:
            self.wait(tracker.duration * 0.3)
            fade_targets = VGroup(
                self.plane, self.i_hat, self.j_hat,
                v1, v2, v_off1, v_off2,
                val1, val2, span1, span2,
            )
            self.play(FadeOut(fade_targets), run_time=0.5)

            values_group = VGroup(p_val, d_val, pinv_val).arrange(RIGHT, buff=0.6).next_to(pdp_tex, DOWN, buff=0.7)

            self.play(Write(pdp_tex), run_time=min(tracker.duration * 0.4, 1.5))
            self.play(FadeIn(values_group), run_time=min(tracker.duration * 0.3, 1.0))

        with self.voiceover(
            text="And we call the process diagonalization."  # noqa E501
        ) as tracker:
            # Emphasize D: dim P and P⁻¹, highlight D
            self.play(
                pdp_tex[2].animate.set_opacity(0.3),   # P in equation
                pdp_tex[4].animate.set_opacity(0.3),   # P⁻¹ in equation
                p_val.animate.set_opacity(0.3),
                pinv_val.animate.set_opacity(0.3),
                pdp_tex[3].animate.set_color(RED),      # D in equation
                Indicate(d_val, color=RED),
                run_time=min(tracker.duration * 0.3, 1.2),
            )

        self.wait(2)  # Final breathe


class RotationFailure(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()
        self.plane.get_axes().set_color(theme.MUTED)

        self.plane.set_opacity(0)
        self.background_plane.set_opacity(0)
        self.i_hat.set_opacity(0)
        self.j_hat.set_opacity(0)

        pika = ImageMobject(Path("img") / "Surprised_Pikachu.jpg")
        with self.voiceover(text="But there's a catch.") as tracker:
            pika.set(height=7)
            self.add(pika)
            self.wait(tracker.duration)

        self.remove(pika)
        self.play(
            self.plane.animate.set_opacity(1),
            self.background_plane.animate.set_opacity(0.5),
            self.i_hat.animate.set_opacity(1),
            self.j_hat.animate.set_opacity(1),
            run_time=0.5
        )
        self.wait(0.5)

        # 1. SETUP THE ROTATION MATRIX (Lead/Medium)
        # 90-degree rotation matrix
        matrix = np.array([[0, -1], [1, 0]])
        matrix_tex = MathTex("A = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}", color=theme.TEXT).to_corner(UL)

        with self.voiceover(
            text="Diagonalization only works for some specific square matrices."
        ) as tracker:
            self.play(Write(matrix_tex), run_time=tracker.duration * 0.5)

        # 2. VECTORS AND STATIC SPANS (Lead/Medium)
        v1 = Vector(np.array([2, 1]), color=BLUE)
        v2 = Vector(np.array([-1, 1.5]), color=BLUE)
        vectors = VGroup(v1, v2)

        # We draw the spans they start on. These will NOT be transformed.
        span1 = DashedLine([-10, -5, 0], [10, 5, 0], color=theme.MUTED, stroke_opacity=0.5)
        span2 = DashedLine([10, -15, 0], [-10, 15, 0], color=theme.MUTED, stroke_opacity=0.5)
        spans = VGroup(span1, span2)

        # Register vectors to be warped by the matrix, but leave the spans out of it
        self.add_transformable_mobject(vectors)
        self.play(Create(vectors), run_time=1.5)

        with self.voiceover(
            text="Other matrices, even if they are square, simply don't have enough eigenvectors to form a basis..."
        ) as tracker:
            self.play(Create(spans), run_time=tracker.duration * 0.4)

        # 3. THE FAILURE TRANSFORMATION (Sync/Medium)
        with self.voiceover(text="...which is a requirement for diagonalization.") as tracker:
            # The vectors rotate, visually abandoning their static dashed spans
            self.apply_matrix(matrix, run_time=tracker.duration)

        self.wait(0.5)

        # 4. LABEL THE FAILURE (Follow/Short)
        with self.voiceover(text="This leaves us with a nagging question:") as tracker:
            failure_label = Tex("No Real Eigenvectors", color=RED).to_corner(UR)
            self.play(Write(failure_label), run_time=tracker.duration * 0.5)
            # self.play(Indicate(failure_label, color=RED), run_time=tracker.duration * 0.5)

        self.wait(0.5)

        # 5. TRANSITION TO SVD (Lead/Medium)
        with self.voiceover(text="Is there a way to find a useful diagonal version of any linear transformation?") as tracker:
            svd_q = MathTex("A = ?", color=theme.TEXT).scale(1.5).next_to(matrix_tex, DOWN, buff=1)
            self.play(Write(svd_q), run_time=tracker.duration * 0.7)

        self.wait(2)


class SVDIntroductionBridge(theme.ProjectVOScene):
    def construct(self):
        super().construct()

        # 1. SETUP OBJECTS
        # Line is slightly below center to accommodate text sitting at ORIGIN
        line = Line(LEFT * 4, RIGHT * 4, color=theme.TEXT).shift(DOWN * 0.5)

        # We use your theme helpers
        full_text = self.body_text("Singular Value Decomposition", scale=0.8)
        # Position it exactly at center (y=0) for the final state
        full_text.move_to(ORIGIN)
        full_text.shift(DOWN * 1.5)

        # The Acronym sits at the same center point
        svd_text = self.accent_text("SVD", scale=1.5).move_to(ORIGIN)

        # MASK: A rectangle the color of the background to hide text below the line
        # This creates the "emerging from the line" effect
        mask = Rectangle(
            width=10, height=3,
            fill_color=theme.BG, fill_opacity=1, stroke_width=0
        ).next_to(line, DOWN, buff=0)

        self.add(full_text)
        self.add(mask)

        # Comparison components
        # diag_label = self.accent_text("Diagonalization", 0.7)
        diag_label = Tex(r"Diagonlization", color=theme.TEXT)
        gear = SVGMobject(Path("svg") / "noun-gear-21438.svg")
        gear.height = 0.8
        gear.set_color(theme.TEXT)
        diag_group = VGroup(diag_label, Arrow(LEFT, RIGHT, color=theme.MUTED), gear).arrange(RIGHT)
        diag_group.shift(UP * 1.5)

        key = SVGMobject(Path("svg") / "noun-key-8371021.svg")
        key.height = 0.8
        key.set_color(theme.ACCENT)
        # SVD will move into this group later
        svd_arrow = Arrow(LEFT, RIGHT, color=theme.ACCENT)
        svd_comparison_group = VGroup(svd_arrow, key).arrange(RIGHT)

        # 2. ANIMATION

        # SEGMENT 1: Entrance
        with self.voiceover(text="Indeed, there is. This is where Singular Value Decomposition...") as tracker:
            self.play(Create(line), run_time=tracker.duration * 0.3)

            # Text starts below the line (behind the mask) and moves up to center
            self.play(
                full_text.animate.shift(UP * 1.5),
                run_time=tracker.duration * 0.4,
                rate_func=bezier(np.array([0, 0, 1, 1]))  # Smooth entrance
            )

        # SEGMENT 2: Morph to SVD
        with self.voiceover(text="...or SVD, enters the stage.") as tracker:
            self.play(
                line.animate.scale(0),
                ReplacementTransform(full_text, svd_text),
                run_time=tracker.duration
            )
            self.remove(line, mask)

        # SEGMENT 3: The Comparison
        with self.voiceover(text="If diagonalization is a specialized tool for a specific class of problems...") as tracker:
            # Move SVD down slightly to make room
            self.play(svd_text.animate.shift(DOWN * 0.5), run_time=tracker.duration * 0.3)

            # Show Diagonalization at the top
            self.play(FadeIn(diag_group, shift=DOWN), run_time=tracker.duration * 0.3)

        with self.voiceover(text="...SVD is the master key.") as tracker:
            # Move SVD to the left to form the "SVD Group"
            # Final position: y-level -0.5, shifted left
            target_pos = LEFT * 1.5 + DOWN * 0.5
            svd_comparison_group.next_to(target_pos, RIGHT, buff=1)

            self.play(
                svd_text.animate.move_to(target_pos).scale(0.6),  # Shrink to label size
                FadeIn(svd_comparison_group),
                run_time=tracker.duration * 0.7
            )

        # SEGMENT 4: The Three Steps
        with self.voiceover(text="It allows us to take any transformation and break it down into three clear steps.") as tracker:
            # Group everything to fade out together
            everything = VGroup(diag_group, svd_text, svd_comparison_group)

            boxes = VGroup(*[
                Rectangle(width=2.5, height=1.8, color=theme.MUTED)
                for _ in range(3)
            ]).arrange(RIGHT, buff=0.5).shift(DOWN * 0.5)

            self.play(everything.animate.shift(UP * 2).set_opacity(0), run_time=tracker.duration * 0.2)
            self.play(
                Create(boxes),
                run_time=tracker.duration * 0.7
            )

        self.wait(2)
