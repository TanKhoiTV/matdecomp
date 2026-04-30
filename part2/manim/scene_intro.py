# Render: manim -q[quality: l-low, m-medium, h-high] [file name] [scene name] --disable_caching

from typing import Tuple, cast, List
import manim as mn
import theme
import numpy as np
from pathlib import Path


class DiagonalizationIntro(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()

        # 1. Setup the plane

        with self.voiceover(
            text="Every linear transformation, no matter how complex-looking, is an ordered sequence of a few simple moves."
        ) as tracker:
            self.play(
                mn.FadeIn(self.plane),
                mn.FadeIn(self.background_plane),
                mn.Create(self.basis_vectors),
                run_time=self.get_capped_run_time(tracker.duration, self.T_LONG)
            )

        self.wait(self.T_BRIEF)

        # 2. Adding vectors

        matrix = np.array([[2, 1], [0, 1.5]])
        matrix_tex = mn.MathTex(
            "A = \\begin{bmatrix} 2 & 1 \\\\ 0 & 1.5 \\end{bmatrix}", color=theme.TEXT
        ).to_corner(mn.UL)

        v1 = self.add_vector([-1, 1], color=mn.GREY, animate=False)
        v2 = self.add_vector([-2, 1], color=mn.BLUE, animate=False)
        new_vectors = mn.VGroup(v1, v2)
        eigenvectors = mn.VGroup(self.i_hat, v2)
        non_eigenvectors = mn.VGroup(self.j_hat, v1)

        span1 = mn.DashedLine((-10, 0, 0), (10, 0, 0), color=mn.GREY, stroke_opacity=0.5)
        span2 = mn.DashedLine((-10, 5, 0), (10, -5, 0), color=mn.GREY, stroke_opacity=0.5)
        spans = mn.VGroup(span1, span2)

        with self.voiceover(
            text="Let's take some vectors and transform them with the matrix on the top left. "
        ) as tracker:
            self.play(
                mn.Write(matrix_tex),
                mn.Create(new_vectors),
                run_time=self.get_capped_run_time(tracker.duration, self.T_LONG),
            )

        with self.voiceover(
            text="Pay attention to their directions."
        ) as tracker:
            self.play(
                mn.Create(spans),
                run_time=self.get_capped_run_time(tracker.duration, self.T_MEDIUM)
            )

        # 3. Transformation

        self.apply_matrix(matrix, run_time=self.T_MEDIUM, path_arc=0)
        self.wait(self.T_SHORT)

        with self.voiceover(
            text="Some vectors changed directions, some didn't."
        ) as tracker:
            self.play(
                eigenvectors.animate.set_color(theme.ACCENT2),
                non_eigenvectors.animate.set_color(theme.MUTED),
                run_time=self.get_capped_run_time(tracker.duration, self.T_SHORT)
            )

        self.wait(self.T_BRIEF)

        # 4. Eigenvectors

        with self.voiceover(
            text="We call those that didn't, eigenvectors."
        ) as tracker:
            self.play(
                mn.Indicate(eigenvectors, color=mn.RED, scale_factor=1.05), 
                run_time=self.get_capped_run_time(tracker.duration, self.T_SHORT)
            )

        # 5. Eigenvalues

        lambda_1 = mn.MathTex("\\lambda_1 = 2", color=mn.RED)
        lambda_1.next_to(self.i_hat.get_end(), mn.UP)
        lambda_2 = mn.MathTex("\\lambda_2 = 1.5", color=mn.RED)
        lambda_2.next_to(v2.get_end(), mn.DOWN, buff=0.7)
        eigenvalues = mn.VGroup(lambda_1, lambda_2)

        with self.voiceover(
            text="And how much the vectors stretched in their directions, eigenvalues."
        ) as tracker:
            self.play(
                non_eigenvectors.animate.set_opacity(0.2),
                mn.Write(eigenvalues),
                run_time=self.get_capped_run_time(tracker.duration, self.T_MEDIUM),
            )

        self.wait(self.T_BRIEF)

        # 6. Basis & Diagonalization

        # Full equation
        pdp_tex = (
            mn.MathTex("A", "=", "P", "D", "P^{-1}",
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

        fade_targets = mn.VGroup(
                self.plane,
                self.basis_vectors,
                new_vectors,
                eigenvalues,
                spans,
            )
        
        with self.voiceover(
            text="If a matrix have enough linearly independent eigenvectors, we can use them to form a new basis."
        ) as tracker:
            self.wait(self.get_capped_run_time(tracker.duration * 0.3, self.T_BRIEF))
            
            self.play(mn.FadeOut(fade_targets), run_time=self.T_BRIEF)

            values_group = (
                mn.VGroup(p_val, d_val, pinv_val)
                .arrange(mn.RIGHT, buff=0.6)
                .next_to(pdp_tex, mn.DOWN, buff=0.7)
            )

            self.play(
                mn.Write(pdp_tex), 
                run_time=self.get_capped_run_time(tracker.duration * 0.4, self.T_MEDIUM)
            )
            self.play(
                mn.FadeIn(values_group), 
                run_time=self.get_capped_run_time(tracker.duration * 0.3, self.T_SHORT)
            )

        with self.voiceover(text="And we call the process diagonalization.") as tracker:
            # Emphasize D: dim P and P⁻¹, highlight D
            self.play(
                pdp_tex[2].animate.set_opacity(0.3),  # P
                pdp_tex[4].animate.set_opacity(0.3),  # P^{-1}
                p_val.animate.set_opacity(0.3),
                pinv_val.animate.set_opacity(0.3),
                pdp_tex[3].animate.set_color(mn.RED),  # D
                run_time=self.get_capped_run_time(tracker.duration * 0.3, self.T_SHORT),
            )

        self.wait(self.T_SHORT)  # Final breathe


class RotationFailure(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()

        self.plane.set_opacity(0)
        self.background_plane.set_opacity(0)
        self.basis_vectors.set_opacity(0)

        pika = mn.ImageMobject(Path("img") / "Surprised_Pikachu.jpg")
        with self.voiceover(text="But there's a catch.") as tracker:
            pika.set(height=7)
            self.add(pika)
            self.wait(tracker.duration)

        self.remove(pika)
        self.play(
            self.plane.animate.set_opacity(1),
            self.background_plane.animate.set_opacity(0.5),
            self.basis_vectors.animate.set_opacity(1),
            run_time=self.T_BRIEF,
        )
        self.wait(self.T_BRIEF)

        # 1. Rotation matrix

        matrix = np.array([[0, -1], [1, 0]])
        matrix_tex = mn.MathTex(
            "A = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}", color=theme.TEXT
        ).to_corner(mn.UL)

        with self.voiceover(
            text="It only works for some specific square matrices."
        ) as tracker:
            self.play(
                mn.Write(matrix_tex), 
                run_time=self.get_capped_run_time(tracker.duration * 0.5, self.T_MEDIUM)
            )

        # 2. Vectors and static spans

        v1 = self.add_vector(np.array([2, 1]), color=mn.BLUE)
        v2 = self.add_vector(np.array([-1, 1.5]), color=mn.BLUE)
        vectors = mn.VGroup(v1, v2)

        span1 = mn.DashedLine([-10, -5, 0], [10, 5, 0], color=theme.MUTED, stroke_opacity=0.5)
        span2 = mn.DashedLine([10, -15, 0], [-10, 15, 0], color=theme.MUTED, stroke_opacity=0.5)
        spans = mn.VGroup(span1, span2)

        with self.voiceover(
            text="Other matrices, even if they are square, simply don't have enough eigenvectors to form a basis."
        ) as tracker:
            self.play(
                mn.Create(vectors),
                mn.Create(spans), 
                run_time=self.get_capped_run_time(tracker.duration * 0.4, self.T_MEDIUM)
            )

        # 3. Transformation (rotation)

        self.apply_matrix(matrix, run_time=self.T_LONG)
        self.wait(self.T_BRIEF)

        # 4. Labeling

        with self.voiceover(text="This leaves us with a nagging question:") as tracker:
            failure_label = mn.MathTex("\\nexists \\lambda \\in \\mathbb{R}", color=mn.RED).to_corner(mn.UR)
            self.play(
                mn.Write(failure_label), 
                run_time=self.get_capped_run_time(tracker.duration * 0.5, self.T_SHORT)
            )

        self.wait(self.T_BRIEF)

        # 5. Transition TO SVD

        with self.voiceover(
            text="Is there a way to find a useful diagonal matrix of any linear transformation?"
        ) as tracker:
            svd_q = (
                mn.MathTex("A = ?", color=theme.TEXT)
                .scale(1.5)
                .next_to(matrix_tex, mn.DOWN, buff=1)
            )
            self.play(
                mn.Write(svd_q), 
                run_time=self.get_capped_run_time(tracker.duration * 0.7, self.T_SHORT)
            )

        self.wait(self.T_SHORT)


class SVDIntroductionBridge(theme.ProjectVOScene):
    def construct(self):
        super().construct()

        # 1. Setup

        line = mn.Line(mn.LEFT * 4, mn.RIGHT * 4, color=theme.TEXT).shift(mn.DOWN * 0.5)
        full_text = self.body_text("Singular Value Decomposition", scale=0.8)
        full_text.move_to(mn.ORIGIN)
        full_text.shift(mn.DOWN * 1.5)

        svd_text = self.accent_text("SVD", scale=1.5).move_to(mn.ORIGIN)

        mask = mn.Rectangle(
            width=10, height=3, fill_color=theme.BG, fill_opacity=1, stroke_width=0
        ).next_to(line, mn.DOWN, buff=0)

        self.add(full_text)
        self.add(mask)

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
        svd_arrow = mn.Arrow(mn.LEFT, mn.RIGHT, color=theme.ACCENT)
        svd_comparison_group = mn.VGroup(svd_arrow, key).arrange(mn.RIGHT)

        # 2. Animating

        with self.voiceover(
            text="Yes, there is. This is where Singular Value Decomposition..."
        ) as tracker:
            self.play(
                mn.Create(line), 
                run_time=self.get_capped_run_time(tracker.duration * 0.3, self.T_MEDIUM)
            )

            self.play(
                full_text.animate.shift(mn.UP * 1.5),
                run_time=self.get_capped_run_time(tracker.duration * 0.4, self.T_SHORT),
                rate_func=mn.bezier(np.array([0, 0, 1, 1])),
            )

        with self.voiceover(text="...or SVD, enters the stage.") as tracker:
            self.play(
                line.animate.scale(0),
                mn.ReplacementTransform(full_text, svd_text),
                run_time=self.get_capped_run_time(tracker.duration, self.T_MEDIUM),
            )
            self.remove(line, mask)

        with self.voiceover(
            text="If diagonalization is a specialized tool for a specific class of problems..."
        ) as tracker:
            self.play(
                svd_text.animate.shift(mn.DOWN * 0.5), 
                run_time=self.get_capped_run_time(tracker.duration * 0.3, self.T_SHORT)
            )

            self.play(
                mn.FadeIn(diag_group, shift=mn.DOWN), 
                run_time=self.get_capped_run_time(tracker.duration * 0.3, self.T_SHORT)
            )

        with self.voiceover(text="...SVD is the master key.") as tracker:
            target_pos = mn.LEFT * 1.5 + mn.DOWN * 0.5
            svd_comparison_group.next_to(target_pos, mn.RIGHT, buff=1)

            self.play(
                svd_text.animate.move_to(target_pos).scale(0.6),
                mn.FadeIn(svd_comparison_group),
                run_time=self.get_capped_run_time(tracker.duration * 0.7, self.T_SHORT),
            )

        with self.voiceover(
            text="It allows us to take any transformation and break it down into identifiable steps."
        ) as tracker:
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
                run_time=self.get_capped_run_time(tracker.duration * 0.2, self.T_SHORT),
            )
            self.play(
                mn.Create(boxes), 
                mn.Create(shapes, lag_ratio=0.5), 
                run_time=self.get_capped_run_time(tracker.duration * 0.7, self.T_LONG)
            )

        self.wait(self.T_SHORT)