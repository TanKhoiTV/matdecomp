# Render: manim -q[quality: l-low, m-medium, h-high] [file name] [scene name] --disable_caching

from typing import Tuple, cast, List
import manim as mn
import theme
import numpy as np
from pathlib import Path
from dataclasses import dataclass


@dataclass
class TransformationStep:
    matrix: List[List[float]]
    label: str
    description: str


class DiagonalizationIntro(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()
        self.plane.get_axes().set_color(theme.MUTED)

        # 1. Setup the plane

        self.i_hat.set_opacity(0)
        self.j_hat.set_opacity(0)

        matrix = np.array([[2, 1], [0, 1.5]])
        matrix_tex = mn.MathTex(
            "A = \\begin{bmatrix} 2 & 1 \\\\ 0 & 1.5 \\end{bmatrix}", color=theme.TEXT
        ).to_corner(mn.UL)
        matrix_tex.set_opacity(0)

        with self.voiceover(
            text="Every linear transformation, no matter how complex-looking, is an ordemn.red sequence of a few simple moves."
        ) as tracker:
            self.play(
                mn.FadeIn(self.plane),
                mn.FadeIn(self.background_plane),
                mn.FadeIn(self.i_hat),
                mn.FadeIn(self.j_hat),
                mn.Write(matrix_tex),
                run_time=tracker.duration * 0.6,
            )

        self.bring_to_front(matrix_tex)
        self.wait(0.5)

        # 2. Adding vectors

        with self.voiceover(
            text="Let's take some vectors and transform them with the matrix on the top left. Pay attention to the vectors' directions."
        ) as tracker:
            v1 = self.add_vector([1, 0], color=mn.BLUE, animate=False)
            v2 = self.add_vector([-2, 1], color=mn.BLUE, animate=False)
            v_off1 = self.add_vector([0, 1], color=mn.GREY, animate=False)
            v_off2 = self.add_vector([-1, 1], color=mn.GREY, animate=False)
            span1 = mn.DashedLine((-10, 0, 0), (10, 0, 0), color=mn.GREY, stroke_opacity=0.5)
            span2 = mn.DashedLine((-10, 5, 0), (10, -5, 0), color=mn.GREY, stroke_opacity=0.5)
            self.play(
                mn.GrowArrow(v1),
                mn.GrowArrow(v2),
                mn.GrowArrow(v_off1),
                mn.GrowArrow(v_off2),
                mn.Create(span1),
                mn.Create(span2),
                matrix_tex.animate.set_opacity(1),
                run_time=tracker.duration * 0.6,
            )

        # 3. Transformation

        self.apply_matrix(matrix, run_time=2, path_arc=0)
        self.wait(1)

        with self.voiceover(
            text="Some vectors changed their directions, some didn't."
        ) as tracker:
            self.wait(tracker.duration)

        self.wait(0.5)

        # 4. Eigenvectors

        with self.voiceover(
            text="We call those that didn't, eigenvectors."
        ) as tracker:
            # Re-color the eigenvectors to mn.RED as they are named
            self.play(
                v1.animate.set_color(mn.RED),
                v2.animate.set_color(mn.RED),
                v_off1.animate.set_opacity(0.2),
                v_off2.animate.set_opacity(0.2),
                self.i_hat.animate.set_opacity(0),
                self.j_hat.animate.set_opacity(0),
                run_time=tracker.duration * 0.6,
            )
            self.play(
                mn.Indicate(mn.VGroup(v1, v2), color=mn.RED), run_time=tracker.duration * 0.4
            )

        # 5. Eigenvalues

        with self.voiceover(
            text="And how much the vectors stretched in their directions, eigenvalues."
        ) as tracker:
            # Show the scaling factor
            val1 = mn.MathTex("\\lambda_1 = 2", color=mn.RED)
            val1.next_to(v1.get_end(), mn.UP)
            val2 = mn.MathTex("\\lambda_2 = 1.5", color=mn.RED)
            val2.next_to(v2.get_end(), mn.DOWN, buff=0.7)
            self.play(
                mn.Write(val1),
                mn.Write(val2),
                run_time=min(tracker.duration, 1.5),
            )

        # 6. Basis & Diagonalization

        # Full equation
        pdp_tex = (
            mn.MathTex(
                "A",
                "=",
                "P",
                "D",
                "P^{-1}",
                substrings_to_isolate=["A", "P", "D", "P^{-1}"],
                color=theme.TEXT,
            )
            .scale(1.1)
            .center()
        )

        # Values below
        p_val = mn.MathTex(
            "P = \\begin{bmatrix} 1 & -2 \\\\ 0 & 1 \\end{bmatrix}",
            color=theme.TEXT,
        ).scale(0.8)
        d_val = mn.MathTex(
            "D = \\begin{bmatrix} 2 & 0 \\\\ 0 & 1.5 \\end{bmatrix}",
            color=mn.RED,
        ).scale(0.8)
        pinv_val = mn.MathTex(
            "P^{-1} = \\begin{bmatrix} 1 & 2 \\\\ 0 & 1 \\end{bmatrix}",
            color=theme.TEXT,
        ).scale(0.8)

        with self.voiceover(text="And here is the interesting part.") as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="If a matrix happens to have a complete set of eigenvectors, we can use them to form a new basis."
        ) as tracker:
            self.wait(tracker.duration * 0.3)
            fade_targets = mn.VGroup(
                self.plane,
                self.i_hat,
                self.j_hat,
                v1,
                v2,
                v_off1,
                v_off2,
                val1,
                val2,
                span1,
                span2,
            )
            self.play(mn.FadeOut(fade_targets), run_time=0.5)

            values_group = (
                mn.VGroup(p_val, d_val, pinv_val)
                .arrange(mn.RIGHT, buff=0.6)
                .next_to(pdp_tex, mn.DOWN, buff=0.7)
            )

            self.play(mn.Write(pdp_tex), run_time=min(tracker.duration * 0.4, 1.5))
            self.play(mn.FadeIn(values_group), run_time=min(tracker.duration * 0.3, 1.0))

        with self.voiceover(text="And we call the process diagonalization.") as tracker:
            # Emphasize D: dim P and P⁻¹, highlight D
            self.play(
                pdp_tex[2].animate.set_opacity(0.3),  # P
                pdp_tex[4].animate.set_opacity(0.3),  # P^{-1}
                p_val.animate.set_opacity(0.3),
                pinv_val.animate.set_opacity(0.3),
                pdp_tex[3].animate.set_color(mn.RED),  # D
                mn.Indicate(d_val, color=mn.RED),
                run_time=min(tracker.duration * 0.3, 1.2),
            )

        self.wait(1)  # Final breathe


class RotationFailure(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()
        self.plane.get_axes().set_color(theme.MUTED)

        self.plane.set_opacity(0)
        self.background_plane.set_opacity(0)
        self.i_hat.set_opacity(0)
        self.j_hat.set_opacity(0)

        pika = mn.ImageMobject(Path("img") / "Surprised_Pikachu.jpg")
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
            run_time=0.5,
        )
        self.wait(0.5)

        # 1. Rotation matrix

        # 90-degree counterclockwise rotation matrix

        matrix = np.array([[0, -1], [1, 0]])
        matrix_tex = mn.MathTex(
            "A = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}", color=theme.TEXT
        ).to_corner(mn.UL)

        with self.voiceover(
            text="Diagonalization only works for some specific square matrices."
        ) as tracker:
            self.play(mn.Write(matrix_tex), run_time=tracker.duration * 0.5)

        # 2. Vectors and static spans

        v1 = mn.Vector(np.array([2, 1]), color=mn.BLUE)
        v2 = mn.Vector(np.array([-1, 1.5]), color=mn.BLUE)
        vectors = mn.VGroup(v1, v2)

        # We draw the spans they start on. These will NOT be transformed.
        span1 = mn.DashedLine(
            [-10, -5, 0], [10, 5, 0], color=theme.MUTED, stroke_opacity=0.5
        )
        span2 = mn.DashedLine(
            [10, -15, 0], [-10, 15, 0], color=theme.MUTED, stroke_opacity=0.5
        )
        spans = mn.VGroup(span1, span2)

        # Register vectors to be warped by the matrix, but leave the spans out of it

        self.add_transformable_mobject(vectors)
        self.play(mn.Create(vectors), run_time=1.5)

        with self.voiceover(
            text="Other matrices, even if they are square, simply don't have enough eigenvectors to form a basis..."
        ) as tracker:
            self.play(mn.Create(spans), run_time=tracker.duration * 0.4)

        # 3. Transformation (rotation)

        with self.voiceover(
            text="...which is a requirement for diagonalization."
        ) as tracker:
            # The vectors rotate, visually abandoning their static dashed spans
            self.apply_matrix(matrix, run_time=tracker.duration)

        self.wait(0.5)

        # 4. Labeling

        with self.voiceover(text="This leaves us with a nagging question:") as tracker:
            failure_label = mn.Tex("No Real Eigenvectors", color=mn.RED).to_corner(mn.UR)
            self.play(mn.Write(failure_label), run_time=tracker.duration * 0.5)
            # self.play(Indicate(failure_label, color=mn.RED), run_time=tracker.duration * 0.5)

        self.wait(0.5)

        # 5. Transition TO SVD

        with self.voiceover(
            text="Is there a way to find a useful diagonal version of any linear transformation?"
        ) as tracker:
            svd_q = (
                mn.MathTex("A = ?", color=theme.TEXT)
                .scale(1.5)
                .next_to(matrix_tex, mn.DOWN, buff=1)
            )
            self.play(mn.Write(svd_q), run_time=tracker.duration * 0.7)

        self.wait(1)


class SVDIntroductionBridge(theme.ProjectVOScene):
    def construct(self):
        super().construct()

        # 1. Setup

        # Line is slightly below center to accommodate text sitting at ORIGIN
        line = mn.Line(mn.LEFT * 4, mn.RIGHT * 4, color=theme.TEXT).shift(mn.DOWN * 0.5)

        full_text = self.body_text("Singular Value Decomposition", scale=0.8)

        # Position it exactly at center (y=0) for the final state
        full_text.move_to(mn.ORIGIN)
        full_text.shift(mn.DOWN * 1.5)

        # The Acronym sits at the same center point
        svd_text = self.accent_text("SVD", scale=1.5).move_to(mn.ORIGIN)

        # Mask: A rectangle the color of the background to hide text below the line
        # This creates the "emerging from the line" effect
        mask = mn.Rectangle(
            width=10, height=3, fill_color=theme.BG, fill_opacity=1, stroke_width=0
        ).next_to(line, mn.DOWN, buff=0)

        self.add(full_text)
        self.add(mask)

        # Comparison components
        # diag_label = self.accent_text("Diagonalization", 0.7)
        diag_label = mn.Tex(r"Diagonalization", color=theme.TEXT)
        gear = mn.SVGMobject(Path("svg") / "noun-gear-21438.svg")
        gear.height = 0.8
        gear.set_color(theme.TEXT)
        diag_group = mn.VGroup(
            diag_label, mn.Arrow(mn.LEFT, mn.RIGHT, color=theme.MUTED), gear
        ).arrange(mn.RIGHT)
        diag_group.shift(mn.UP * 1.5)

        key = mn.SVGMobject(Path("svg") / "noun-key-8371021.svg")
        key.height = 0.8
        key.set_color(theme.ACCENT)
        # SVD will move into this group later
        svd_arrow = mn.Arrow(mn.LEFT, mn.RIGHT, color=theme.ACCENT)
        svd_comparison_group = mn.VGroup(svd_arrow, key).arrange(mn.RIGHT)

        # 2. Animating

        with self.voiceover(
            text="Indeed, there is. This is where Singular Value Decomposition..."
        ) as tracker:
            self.play(mn.Create(line), run_time=tracker.duration * 0.3)

            # Text starts below the line (behind the mask) and moves up to center
            self.play(
                full_text.animate.shift(mn.UP * 1.5),
                run_time=tracker.duration * 0.4,
                rate_func=mn.bezier(np.array([0, 0, 1, 1])),  # Smooth entrance
            )

        with self.voiceover(text="...or SVD, enters the stage.") as tracker:
            self.play(
                line.animate.scale(0),
                mn.ReplacementTransform(full_text, svd_text),
                run_time=tracker.duration,
            )
            self.remove(line, mask)

        with self.voiceover(
            text="If diagonalization is a specialized tool for a specific class of problems..."
        ) as tracker:
            # Move SVD down slightly to make room
            self.play(
                svd_text.animate.shift(mn.DOWN * 0.5), run_time=tracker.duration * 0.3
            )

            # Show Diagonalization at the top
            self.play(mn.FadeIn(diag_group, shift=mn.DOWN), run_time=tracker.duration * 0.3)

        with self.voiceover(text="...SVD is the master key.") as tracker:
            # Move SVD to the left to form the "SVD Group"
            # Final position: y-level -0.5, shifted left
            target_pos = mn.LEFT * 1.5 + mn.DOWN * 0.5
            svd_comparison_group.next_to(target_pos, mn.RIGHT, buff=1)

            self.play(
                svd_text.animate.move_to(target_pos).scale(0.6),  # Shrink to label size
                mn.FadeIn(svd_comparison_group),
                run_time=tracker.duration * 0.7,
            )

        with self.voiceover(
            text="It allows us to take any transformation and break it down into identifiable steps."
        ) as tracker:
            # Group everything to fade out together
            everything = mn.VGroup(diag_group, svd_text, svd_comparison_group)

            boxes = mn.VGroup(
                *[mn.Rectangle(width=2.5, height=1.8, color=theme.MUTED) for _ in range(3)]
            ).arrange(mn.RIGHT, buff=0.5)
            boxes.move_to(mn.ORIGIN)

            shape1 = (
                mn.Triangle(color=mn.RED, fill_opacity=0.8)
                .scale(0.3)
                .move_to(boxes[0].get_center())
                .scale(1.5)
            )
            shape2 = (
                mn.Circle(color=mn.GREEN, fill_opacity=0.8)
                .scale(0.3)
                .move_to(boxes[1].get_center())
                .scale(1.5)
            )
            shape3 = (
                mn.Square(color=mn.BLUE, fill_opacity=0.8)
                .scale(0.3)
                .move_to(boxes[2].get_center())
                .scale(1.5)
            )
            shapes = mn.VGroup(shape1, shape2, shape3)

            self.play(
                everything.animate.shift(mn.UP * 2).set_opacity(0),
                run_time=tracker.duration * 0.2,
            )
            self.play(mn.Create(boxes), mn.FadeIn(shapes), run_time=tracker.duration * 0.7)

        self.wait(1)