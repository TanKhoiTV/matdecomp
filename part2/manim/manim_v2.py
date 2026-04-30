from typing import Tuple, cast
from manim import (
    Line,
    NumberLine,
    bezier,
    Circle,
    Vector,
    NumberPlane,
    DashedLine,
    Tex,
    MathTex,
    Arrow,
    Triangle,
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
    PURPLE,
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
    PURE_CYAN,
    RightAngle,
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

        # 1. Setup the plane

        self.i_hat.set_opacity(0)
        self.j_hat.set_opacity(0)

        matrix = np.array([[2, 1], [0, 1.5]])
        matrix_tex = MathTex(
            "A = \\begin{bmatrix} 2 & 1 \\\\ 0 & 1.5 \\end{bmatrix}", color=theme.TEXT
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
                run_time=tracker.duration * 0.6,
            )

        self.bring_to_front(matrix_tex)
        self.wait(0.5)

        # 2. Adding vectors

        with self.voiceover(
            text="Let's take some vectors and transform them with the matrix on the top left. Pay attention to the vectors' directions."
        ) as tracker:
            v1 = self.add_vector([1, 0], color=BLUE, animate=False)
            v2 = self.add_vector([-2, 1], color=BLUE, animate=False)
            v_off1 = self.add_vector([0, 1], color=GREY, animate=False)
            v_off2 = self.add_vector([-1, 1], color=GREY, animate=False)
            span1 = DashedLine((-10, 0, 0), (10, 0, 0), color=GREY, stroke_opacity=0.5)
            span2 = DashedLine((-10, 5, 0), (10, -5, 0), color=GREY, stroke_opacity=0.5)
            self.play(
                GrowArrow(v1),
                GrowArrow(v2),
                GrowArrow(v_off1),
                GrowArrow(v_off2),
                Create(span1),
                Create(span2),
                matrix_tex.animate.set_opacity(1),
                run_time=tracker.duration * 0.6,
            )

        # 3. Transformation

        self.apply_matrix(matrix, run_time=2, path_arc=0)
        self.wait(1)

        with self.voiceover(
            text="Some changed their directions, some didn't."
        ) as tracker:
            self.wait(tracker.duration)

        self.wait(0.5)

        # 4. Eigenvectors

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
            self.play(
                Indicate(VGroup(v1, v2), color=RED), run_time=tracker.duration * 0.4
            )

        # 5. Eigenvalues

        with self.voiceover(
            text="And how much the vectors stretched in their directions, we call eigenvalues."
        ) as tracker:
            # Show the scaling factor
            val1 = MathTex("\\lambda_1 = 2", color=RED)
            val1.next_to(v1.get_end(), UP)
            val2 = MathTex("\\lambda_2 = 1.5", color=RED)
            val2.next_to(v2.get_end(), DOWN, buff=0.7)
            self.play(
                Write(val1),
                Write(val2),
                run_time=min(tracker.duration, 1.5),
            )

        # 6. Basis & Diagonalization

        # Full equation
        pdp_tex = (
            MathTex(
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
            text="If a matrix happens to have a complete set of eigenvectors, we can use them to form a new basis."
        ) as tracker:
            self.wait(tracker.duration * 0.3)
            fade_targets = VGroup(
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
            self.play(FadeOut(fade_targets), run_time=0.5)

            values_group = (
                VGroup(p_val, d_val, pinv_val)
                .arrange(RIGHT, buff=0.6)
                .next_to(pdp_tex, DOWN, buff=0.7)
            )

            self.play(Write(pdp_tex), run_time=min(tracker.duration * 0.4, 1.5))
            self.play(FadeIn(values_group), run_time=min(tracker.duration * 0.3, 1.0))

        with self.voiceover(text="And we call the process diagonalization.") as tracker:
            # Emphasize D: dim P and P⁻¹, highlight D
            self.play(
                pdp_tex[2].animate.set_opacity(0.3),  # P
                pdp_tex[4].animate.set_opacity(0.3),  # P^{-1}
                p_val.animate.set_opacity(0.3),
                pinv_val.animate.set_opacity(0.3),
                pdp_tex[3].animate.set_color(RED),  # D
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
            run_time=0.5,
        )
        self.wait(0.5)

        # 1. Rotation matrix

        # 90-degree counterclockwise rotation matrix

        matrix = np.array([[0, -1], [1, 0]])
        matrix_tex = MathTex(
            "A = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}", color=theme.TEXT
        ).to_corner(UL)

        with self.voiceover(
            text="Diagonalization only works for some specific square matrices."
        ) as tracker:
            self.play(Write(matrix_tex), run_time=tracker.duration * 0.5)

        # 2. Vectors and static spans

        v1 = Vector(np.array([2, 1]), color=BLUE)
        v2 = Vector(np.array([-1, 1.5]), color=BLUE)
        vectors = VGroup(v1, v2)

        # We draw the spans they start on. These will NOT be transformed.
        span1 = DashedLine(
            [-10, -5, 0], [10, 5, 0], color=theme.MUTED, stroke_opacity=0.5
        )
        span2 = DashedLine(
            [10, -15, 0], [-10, 15, 0], color=theme.MUTED, stroke_opacity=0.5
        )
        spans = VGroup(span1, span2)

        # Register vectors to be warped by the matrix, but leave the spans out of it

        self.add_transformable_mobject(vectors)
        self.play(Create(vectors), run_time=1.5)

        with self.voiceover(
            text="Other matrices, even if they are square, simply don't have enough eigenvectors to form a basis..."
        ) as tracker:
            self.play(Create(spans), run_time=tracker.duration * 0.4)

        # 3. Transformation (rotation)

        with self.voiceover(
            text="...which is a requirement for diagonalization."
        ) as tracker:
            # The vectors rotate, visually abandoning their static dashed spans
            self.apply_matrix(matrix, run_time=tracker.duration)

        self.wait(0.5)

        # 4. Labeling

        with self.voiceover(text="This leaves us with a nagging question:") as tracker:
            failure_label = Tex("No Real Eigenvectors", color=RED).to_corner(UR)
            self.play(Write(failure_label), run_time=tracker.duration * 0.5)
            # self.play(Indicate(failure_label, color=RED), run_time=tracker.duration * 0.5)

        self.wait(0.5)

        # 5. Transition TO SVD

        with self.voiceover(
            text="Is there a way to find a useful diagonal version of any linear transformation?"
        ) as tracker:
            svd_q = (
                MathTex("A = ?", color=theme.TEXT)
                .scale(1.5)
                .next_to(matrix_tex, DOWN, buff=1)
            )
            self.play(Write(svd_q), run_time=tracker.duration * 0.7)

        self.wait(2)


class SVDIntroductionBridge(theme.ProjectVOScene):
    def construct(self):
        super().construct()

        # 1. Setup

        # Line is slightly below center to accommodate text sitting at ORIGIN
        line = Line(LEFT * 4, RIGHT * 4, color=theme.TEXT).shift(DOWN * 0.5)

        full_text = self.body_text("Singular Value Decomposition", scale=0.8)

        # Position it exactly at center (y=0) for the final state
        full_text.move_to(ORIGIN)
        full_text.shift(DOWN * 1.5)

        # The Acronym sits at the same center point
        svd_text = self.accent_text("SVD", scale=1.5).move_to(ORIGIN)

        # Mask: A rectangle the color of the background to hide text below the line
        # This creates the "emerging from the line" effect
        mask = Rectangle(
            width=10, height=3, fill_color=theme.BG, fill_opacity=1, stroke_width=0
        ).next_to(line, DOWN, buff=0)

        self.add(full_text)
        self.add(mask)

        # Comparison components
        # diag_label = self.accent_text("Diagonalization", 0.7)
        diag_label = Tex(r"Diagonalization", color=theme.TEXT)
        gear = SVGMobject(Path("svg") / "noun-gear-21438.svg")
        gear.height = 0.8
        gear.set_color(theme.TEXT)
        diag_group = VGroup(
            diag_label, Arrow(LEFT, RIGHT, color=theme.MUTED), gear
        ).arrange(RIGHT)
        diag_group.shift(UP * 1.5)

        key = SVGMobject(Path("svg") / "noun-key-8371021.svg")
        key.height = 0.8
        key.set_color(theme.ACCENT)
        # SVD will move into this group later
        svd_arrow = Arrow(LEFT, RIGHT, color=theme.ACCENT)
        svd_comparison_group = VGroup(svd_arrow, key).arrange(RIGHT)

        # 2. Animating

        with self.voiceover(
            text="Indeed, there is. This is where Singular Value Decomposition..."
        ) as tracker:
            self.play(Create(line), run_time=tracker.duration * 0.3)

            # Text starts below the line (behind the mask) and moves up to center
            self.play(
                full_text.animate.shift(UP * 1.5),
                run_time=tracker.duration * 0.4,
                rate_func=bezier(np.array([0, 0, 1, 1])),  # Smooth entrance
            )

        with self.voiceover(text="...or SVD, enters the stage.") as tracker:
            self.play(
                line.animate.scale(0),
                ReplacementTransform(full_text, svd_text),
                run_time=tracker.duration,
            )
            self.remove(line, mask)

        with self.voiceover(
            text="If diagonalization is a specialized tool for a specific class of problems..."
        ) as tracker:
            # Move SVD down slightly to make room
            self.play(
                svd_text.animate.shift(DOWN * 0.5), run_time=tracker.duration * 0.3
            )

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
                run_time=tracker.duration * 0.7,
            )

        with self.voiceover(
            text="It allows us to take any transformation and break it down into identifiable steps."
        ) as tracker:
            # Group everything to fade out together
            everything = VGroup(diag_group, svd_text, svd_comparison_group)

            boxes = VGroup(
                *[Rectangle(width=2.5, height=1.8, color=theme.MUTED) for _ in range(3)]
            ).arrange(RIGHT, buff=0.5)
            boxes.move_to(ORIGIN)

            shape1 = (
                Triangle(color=RED, fill_opacity=0.8)
                .scale(0.3)
                .move_to(boxes[0].get_center())
                .scale(1.5)
            )
            shape2 = (
                Circle(color=GREEN, fill_opacity=0.8)
                .scale(0.3)
                .move_to(boxes[1].get_center())
                .scale(1.5)
            )
            shape3 = (
                Square(color=BLUE, fill_opacity=0.8)
                .scale(0.3)
                .move_to(boxes[2].get_center())
                .scale(1.5)
            )
            shapes = VGroup(shape1, shape2, shape3)

            self.play(
                everything.animate.shift(UP * 2).set_opacity(0),
                run_time=tracker.duration * 0.2,
            )
            self.play(Create(boxes), FadeIn(shapes), run_time=tracker.duration * 0.7)

        self.wait(2)


class SVDGeometry(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()
        self.plane.get_axes().set_color(theme.MUTED)

        # Hide auto-created objects initially
        self.plane.set_opacity(0)
        self.background_plane.set_opacity(0)
        self.i_hat.set_opacity(0)
        self.j_hat.set_opacity(0)

        unit_circle = Circle(radius=1, color=theme.ACCENT, stroke_width=4)
        matrix_a = np.array([[2, 1], [0.5, 1.5]])

        # 1. FADE IN
        with self.voiceover(
            text="To understand what SVD is actually doing, let's think about how a linear transformation affects the space it lives in."
        ) as tracker:
            self.play(
                self.plane.animate.set_opacity(1),
                self.background_plane.animate.set_opacity(0.5),
                self.i_hat.animate.set_opacity(1),
                self.j_hat.animate.set_opacity(1),
                run_time=tracker.duration * 0.8,
            )

        # Register circle BEFORE apply_matrix
        self.add_transformable_mobject(unit_circle)

        with self.voiceover(
            text="Imagine a unit circle in a 2D input space. When we apply a linear transformation to this space..."
        ) as tracker:
            # Show the orthogonal basis here with a fade in or create, reduce their opacity so they don't distract
            self.play(Create(unit_circle), run_time=tracker.duration * 0.5)

        with self.voiceover(
            text="...that circle usually gets stretched and tilted into an ellipse in the output space."
        ) as tracker:
            self.apply_matrix(matrix_a, run_time=tracker.duration * 0.6, path_arc=0)
            self.wait(tracker.duration * 0.4)

        with self.voiceover(
            text="The core insight is this: no matter how distorted that ellipse looks, we can always find a set of perpendicular vectors in our input space..."
        ) as tracker:
            self.wait(tracker.duration)

        U, s, Vt = np.linalg.svd(matrix_a)
        axis1_end = U[:, 0] * s[0]  # major axis
        axis2_end = U[:, 1] * s[1]  # minor axis
        ellipse_axis1 = DashedLine(
            start=[-axis1_end[0], -axis1_end[1], 0],
            end=[axis1_end[0], axis1_end[1], 0],
            color=theme.ACCENT2,
        )
        ellipse_axis2 = DashedLine(
            start=[-axis2_end[0], -axis2_end[1], 0],
            end=[axis2_end[0], axis2_end[1], 0],
            color=theme.ACCENT2,
        )

        with self.voiceover(
            text="...which become the axes of the ellipse after transformation."
        ) as tracker:
            self.play(
                Create(ellipse_axis1),
                Create(ellipse_axis2),
                run_time=tracker.duration * 0.5,
            )
            self.wait(tracker.duration * 0.5)

        self.play(
            FadeOut(unit_circle, ellipse_axis1, ellipse_axis2),
            self.plane.animate.set_opacity(0),
            self.background_plane.animate.set_opacity(0),
            self.i_hat.animate.set_opacity(0),
            self.j_hat.animate.set_opacity(0),
            run_time=0.5,
        )

        self.wait(1)


class SVDBreakdown(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()
        self.plane.get_axes().set_color(theme.MUTED)

        # Hide auto-created objects initially
        self.plane.set_opacity(0)
        self.background_plane.set_opacity(0)
        self.i_hat.set_opacity(0)
        self.j_hat.set_opacity(0)

        def update_label(label, vector):
            label.next_to(vector.get_end(), UR, buff=0.1)

        unit_circle = Circle(radius=1, color=theme.ACCENT, stroke_width=4)

        theta_v = PI / 6
        sigma_vals = [2.0, 0.8]
        theta_u = PI / 4

        R_v = np.array(
            [
                [np.cos(theta_v), -np.sin(theta_v)],
                [np.sin(theta_v), np.cos(theta_v)],
            ]
        )
        Sigma = np.array(
            [
                [sigma_vals[0], 0],
                [0, sigma_vals[1]],
            ]
        )
        R_u = np.array(
            [
                [np.cos(theta_u), -np.sin(theta_u)],
                [np.sin(theta_u), np.cos(theta_u)],
            ]
        )

        A = R_u @ Sigma @ R_v
        U, s, Vt = np.linalg.svd(A)
        V = Vt.T

        # Set i_hat and j_hat to v1, v2 from the start
        self.i_hat.put_start_and_end_on(ORIGIN, np.append(V[:, 0], 0))
        self.j_hat.put_start_and_end_on(ORIGIN, np.append(V[:, 1], 0))
        self.i_hat.set_color(theme.ACCENT)
        self.j_hat.set_color(theme.ACCENT2)

        # RightAngle symbol
        right_angle = RightAngle(
            self.i_hat,  # type: ignore
            self.j_hat,  # type: ignore
            length=0.2,
            color=theme.MUTED,
            fill_opacity=0,
            stroke_width=2,
        )
        right_angle.set_opacity(0)

        def update_right_angle(m):
            new = RightAngle(
                self.i_hat,  # type: ignore
                self.j_hat,  # type: ignore
                length=0.2,
                color=theme.MUTED,
                fill_opacity=0,
                stroke_width=2,
            )
            new.set_opacity(m.get_stroke_opacity())
            m.become(new)

        right_angle.add_updater(update_right_angle)
        self.add(right_angle)

        # Labels that follow the vector tips
        v1_label = MathTex("v_1", color=theme.ACCENT).scale(0.7)
        v2_label = MathTex("v_2", color=theme.ACCENT2).scale(0.7)
        v1_label.add_updater(lambda m: m.next_to(self.i_hat.get_end(), UL, buff=0.1))
        v2_label.add_updater(lambda m: m.next_to(self.j_hat.get_end(), UP, buff=0.1))

        svd_formula = (
            MathTex(
                "A",
                "=",
                "U",
                "\\Sigma",
                "V^T",
                color=theme.TEXT,
            )
            .to_corner(UL)
            .shift(DOWN)
        )

        # Helper: apply a 2D matrix to a mobject via ApplyMatrix animation,
        # syncing i_hat, j_hat, and the plane via self.apply_matrix,
        # but keeping svd_formula untouched as a plain scene mobject.
        def transform_scene(matrix, run_time, path_arc=None):
            kwargs = {"run_time": run_time}
            if path_arc is not None:
                kwargs["path_arc"] = path_arc

            # Embed 2x2 into 3x3 for ApplyMatrix
            m3 = np.eye(3)
            m3[:2, :2] = matrix

            anim = ApplyMatrix(m3, unit_circle, path_arc=path_arc or 0)
            self.play(
                anim,
                ApplyMatrix(
                    m3,
                    self.i_hat,
                    rate_func=anim.get_rate_func(),
                    run_time=anim.get_run_time(),
                ),
                ApplyMatrix(
                    m3,
                    self.j_hat,
                    rate_func=anim.get_rate_func(),
                    run_time=anim.get_run_time(),
                ),
                ApplyMatrix(
                    m3,
                    self.plane,
                    rate_func=anim.get_rate_func(),
                    run_time=anim.get_run_time(),
                ),
                **kwargs,
            )

        # 1. Fade In
        self.play(
            self.plane.animate.set_opacity(1),
            self.background_plane.animate.set_opacity(0.5),
            run_time=1,
        )

        with self.voiceover(
            text="We describe this process as a sequence of three distinct motions: U, Sigma, and V transpose."
        ) as tracker:
            svd_formula.set_color(theme.ACCENT)
            self.play(Create(unit_circle), run_time=tracker.duration * 0.2)
            self.play(Write(svd_formula), run_time=tracker.duration * 0.3)
            self.play(
                svd_formula.animate.set_color(theme.TEXT),
                run_time=tracker.duration * 0.2,
            )
            self.play(
                self.i_hat.animate.set_opacity(1),
                self.j_hat.animate.set_opacity(1),
                right_angle.animate.set_stroke(opacity=0.8),
                run_time=tracker.duration * 0.3,
            )

        # 2. Step 1: V^T (Input Rotation)

        with self.voiceover(
            text="Going right to left, we begin with V transpose, a rotation in the input space."
        ) as tracker:
            self.play(
                svd_formula[4].animate.set_color(theme.ACCENT2),
                run_time=tracker.duration,
            )

        with self.voiceover(
            text="We rotate our coordinate system so our basis vectors align with the directions that will become the axes of our ellipse."
        ) as tracker:
            target_axes = DashedLine(LEFT * 3, RIGHT * 3, color=theme.MUTED)
            target_axes.set_opacity(0.5)
            self.play(Create(target_axes), run_time=0.5)
            transform_scene(R_v, run_time=tracker.duration * 0.7)
            self.play(
                FadeIn(v1_label),
                FadeIn(v2_label),
                run_time=min(0.4, tracker.duration * 0.3),
            )
            self.wait(max(0, tracker.duration * 0.3 - 0.4))

        with self.voiceover(
            text="Visually, the unit circle spins but doesn't look any different."
        ) as tracker:
            self.wait(tracker.duration)

        # 3. Step 2: Sigma (Scaling)

        sigma_label1 = MathTex("\\sigma_1 = 2.0", color=theme.ACCENT2)
        sigma_label2 = MathTex("\\sigma_2 = 0.8", color=theme.ACCENT2)

        with self.voiceover(
            text="Next, Sigma scales these vectors. The factors by which we stretch or squish are called the singular values."
        ) as tracker:
            self.play(
                svd_formula[4].animate.set_color(theme.TEXT),
                svd_formula[3].animate.set_color(theme.ACCENT2),
                right_angle.animate.set_stroke(opacity=0),
                run_time=0.5,
            )
            transform_scene(Sigma, run_time=tracker.duration * 0.7, path_arc=0)
            self.play(
                right_angle.animate.set_stroke(opacity=0.8),
                run_time=tracker.duration * 0.2,
            )
            # Add sigma labels after scaling
            sigma_label1.next_to(self.i_hat.get_end(), LEFT * 1.5)
            sigma_label2.next_to(self.j_hat.get_end(), UP * 1.5)
            self.play(
                Write(sigma_label1),
                Write(sigma_label2),
                FadeOut(v1_label, v2_label),
                run_time=min(tracker.duration, 1.5),
            )

        with self.voiceover(
            text="Now the circle deforms into an ellipse. If a singular value is zero, that entire dimension collapses. The number of nonzero singular values is the rank of the matrix."
        ) as tracker:
            self.wait(tracker.duration * 0.8)
            self.play(
                FadeOut(sigma_label1, sigma_label2),
                FadeIn(v1_label, v2_label),
                run_time=tracker.duration * 0.1,
            )

        # 4. Step 3: U (Output Rotation)

        with self.voiceover(
            text="Finally, U rotates the scaled vectors into their final orientation in the output space."
        ) as tracker:
            self.play(
                svd_formula[3].animate.set_color(theme.TEXT),
                svd_formula[2].animate.set_color(theme.ACCENT2),
                run_time=0.5,
            )
            transform_scene(R_u, run_time=tracker.duration - 0.5)
            self.play(FadeOut(v1_label), FadeOut(v2_label), run_time=0.3)
            # After transform_scene(R_u):
            u1_label = MathTex("u_1", color=theme.ACCENT).scale(0.7)
            u2_label = MathTex("u_2", color=theme.ACCENT2).scale(0.7)
            u1_label.add_updater(
                lambda m: m.next_to(self.i_hat.get_end(), DL, buff=0.1)
            )
            u2_label.add_updater(
                lambda m: m.next_to(self.j_hat.get_end(), UL, buff=0.1)
            )
            self.play(
                ReplacementTransform(v1_label, u1_label),
                ReplacementTransform(v2_label, u2_label),
                run_time=0.4,
            )

        # 5. Conclusion

        with self.voiceover(
            text="Notice the elegance. SVD allows the input basis and output basis to be different, as long as both are orthonormal."
        ) as tracker:
            self.play(
                svd_formula[2].animate.set_color(theme.TEXT),
                run_time=tracker.duration,
            )

        with self.voiceover(
            text="This flexibility is exactly why SVD works for every single matrix in existence."
        ) as tracker:
            self.play(
                svd_formula.animate.set_color(theme.ACCENT),
                run_time=tracker.duration * 0.5,
            )
            self.play(
                svd_formula.animate.set_color(theme.TEXT),
                run_time=tracker.duration * 0.5,
            )

        self.wait(2)


class ComputationSideNote(theme.ProjectVOScene):
    def construct(self):
        super().construct()

        # ── OBJECTS ───────────────────────────────────────────────────────────

        # Side note title
        title = self.accent_text("Side Note: Computing SVD", scale=0.6).to_corner(UL)

        # A^T A and AA^T
        ata = MathTex("A^T A", color=theme.TEXT).scale(1.2)
        aat = MathTex("A A^T", color=theme.TEXT).scale(1.2)
        both = VGroup(ata, aat).arrange(RIGHT, buff=1.5).shift(UP * 0.5)

        symmetric_label = MathTex(
            "\\text{always symmetric}", color=theme.ACCENT
        ).scale(0.7).next_to(both, DOWN, buff=0.4)

        # Symmetric matrix example with color-matched entries
        sym_matrix = MathTex(
            "\\begin{bmatrix} a & b \\\\ b & c \\end{bmatrix}",
            color=theme.TEXT,
        ).scale(1.1)
        sym_label = MathTex(
            "\\text{mirror entries}", color=theme.ACCENT
        ).scale(0.6).next_to(sym_matrix, DOWN, buff=0.3)

        # Orthogonal eigenvectors — right angle symbol hint
        perp_hint = MathTex(
            "\\text{eigenvectors} \\perp",
            color=theme.TEXT,
        ).scale(0.9)

        # Result shortcut (no derivation)
        result = MathTex(
            "A^T A = V \\Sigma^2 V^T",
            color=theme.TEXT,
        ).scale(1.0)
        result_note = self.body_text("(result, not derived here)", scale=0.5)
        result_note.set_color(theme.MUTED)
        result_note.next_to(result, DOWN, buff=0.2)

        # Numerical instability example
        A_example = MathTex(
            "A = \\begin{bmatrix} 10^8 & 0 \\\\ 0 & 1 \\end{bmatrix}",
            color=theme.TEXT,
        ).scale(0.9)
        ATA_example = MathTex(
            "A^T A = \\begin{bmatrix} 10^{16} & 0 \\\\ 0 & 1 \\end{bmatrix}",
            color=theme.TEXT,
        ).scale(0.9)
        precision_lost = MathTex(
            "\\text{small entries lost to floating point}",
            color=RED,
        ).scale(0.6)

        # Convergence sketch — number line with bouncing value
        nline = NumberLine(
            x_range=[0, 1, 0.25],
            length=5,
            color=theme.MUTED,
            include_tip=True,
        ).shift(DOWN * 0.5)
        target_dot = Dot(nline.n2p(0.618), color=theme.ACCENT)
        target_label = MathTex("\\sigma^*", color=theme.ACCENT).scale(0.6)
        target_label.next_to(target_dot, UP, buff=0.1)
        iter_dot = Dot(nline.n2p(0.1), color=theme.ACCENT2)
        converge_label = self.body_text("iterative algorithm converges", scale=0.5)
        converge_label.set_color(theme.MUTED).next_to(nline, DOWN, buff=0.3)

        # ── SEGMENT 1: INTRO ─────────────────────────────────────────────────
        with self.voiceover(
            text="As a side note, to find the U and V matrices, we look at two special products: A transpose A, and A A transpose."
        ) as tracker:
            self.play(FadeIn(title), run_time=0.4)
            self.play(
                Write(ata), Write(aat),
                run_time=tracker.duration - 0.4,
            )

        # ── SEGMENT 2: SYMMETRY ──────────────────────────────────────────────
        with self.voiceover(
            text="Why them? Because they are always symmetric."
        ) as tracker:
            self.play(
                FadeIn(symmetric_label),
                run_time=tracker.duration,
            )

        with self.voiceover(
            text="A symmetric matrix mirrors its entries across the diagonal."
        ) as tracker:
            self.play(
                FadeOut(both, symmetric_label),
                run_time=0.3,
            )
            self.play(
                FadeIn(sym_matrix),
                run_time=tracker.duration * 0.5,
            )
            # Highlight the mirrored b entries
            self.play(
                FadeIn(sym_label),
                run_time=tracker.duration * 0.5,
            )

        # ── SEGMENT 3: ORTHOGONAL EIGENVECTORS ──────────────────────────────
        with self.voiceover(
            text="And symmetric matrices always diagonalize with orthogonal eigenvectors — meaning perpendicular."
        ) as tracker:
            self.play(
                FadeOut(sym_matrix, sym_label),
                run_time=0.3,
            )
            self.play(
                Write(perp_hint),
                run_time=tracker.duration - 0.3,
            )

        with self.voiceover(
            text="That perpendicularity is exactly what gives us the V and U matrices in SVD."
        ) as tracker:
            self.play(
                ReplacementTransform(perp_hint, result),
                run_time=tracker.duration * 0.6,
            )
            self.play(
                FadeIn(result_note),
                run_time=tracker.duration * 0.4,
            )

        # ── SEGMENT 4: ITERATIVE ALGORITHM ──────────────────────────────────
        with self.voiceover(
            text="However, finding these eigenvalues requires solving a polynomial equation of degree n."
        ) as tracker:
            self.play(
                FadeOut(result, result_note),
                run_time=0.3,
            )
            self.play(
                Create(nline),
                FadeIn(target_dot, target_label),
                FadeIn(converge_label),
                run_time=tracker.duration - 0.3,
            )

        with self.voiceover(
            text="For n of 5 or higher, there is no closed-form solution."
        ) as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="So in practice, SVD uses an iterative algorithm — one that bounces toward the answer rather than computing it exactly."
        ) as tracker:
            # Animate the dot bouncing and converging toward target
            checkpoints = [0.9, 0.4, 0.75, 0.55, 0.65, 0.618]
            per_step = tracker.duration / len(checkpoints)
            for val in checkpoints:
                self.play(
                    iter_dot.animate.move_to(nline.n2p(val)),
                    run_time=per_step,
                )

        # ── SEGMENT 5: NUMERICAL INSTABILITY ────────────────────────────────
        with self.voiceover(
            text="There is also a deeper problem: computing A transpose A on a computer is numerically unstable."
        ) as tracker:
            self.play(
                FadeOut(nline, target_dot, target_label, iter_dot, converge_label),
                run_time=0.3,
            )
            self.play(
                FadeIn(A_example),
                run_time=tracker.duration - 0.3,
            )

        with self.voiceover(
            text="Take a matrix with a very large entry and a small one."
        ) as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="When you compute A transpose A, the large entry gets squared to ten to the sixteen."
        ) as tracker:
            self.play(
                ReplacementTransform(A_example, ATA_example),
                run_time=tracker.duration * 0.6,
            )
            self.wait(tracker.duration * 0.4)

        with self.voiceover(
            text="At that scale, floating point arithmetic simply cannot represent the small entry accurately anymore — precision is lost."
        ) as tracker:
            self.play(
                FadeIn(precision_lost.next_to(ATA_example, DOWN, buff=0.3)),
                run_time=tracker.duration * 0.4,
            )
            self.wait(tracker.duration * 0.6)

        with self.voiceover(
            text="This is why modern SVD implementations work directly on A, never forming A transpose A at all."
        ) as tracker:
            self.play(
                FadeOut(ATA_example, precision_lost),
                run_time=tracker.duration * 0.3,
            )
            self.wait(tracker.duration * 0.7)

        self.wait(2)


def compute_pca_arrows(
    dots: VGroup, scale1: float = 2.5, scale2: float = 1.2
) -> tuple:
    """Return (pc1_arrow, pc2_arrow, angle_of_pc1, singular_values)."""
    points = np.array([dot.get_center()[:2] for dot in dots])
    mean = points.mean(axis=0)
    centered = points - mean
    _, S, Vt = np.linalg.svd(centered, full_matrices=False)
    pc1_dir = Vt[0]
    pc2_dir = Vt[1]
    pc1 = Arrow(
        ORIGIN,
        np.append(pc1_dir * scale1, 0),
        color=theme.ACCENT2,
        buff=0,
        tip_length=0.18,
        stroke_width=5,
    )
    pc2 = Arrow(
        ORIGIN,
        np.append(pc2_dir * scale2, 0),
        color=theme.ACCENT2,
        buff=0,
        tip_length=0.18,
        stroke_width=5,
    )
    angle = float(np.arctan2(pc1_dir[1], pc1_dir[0]))
    return pc1, pc2, angle, S


def make_matrix_grid(
    data: np.ndarray,
    cell_size: float = 0.5,
    cell_gap: float = 0.6,
    color: str = theme.ACCENT,
) -> VGroup:
    """Build a heatmap VGroup from a 2-D numpy array, normalised to [0,1]."""
    grid = VGroup()
    max_val = data.max() or 1
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            cell = Square(cell_size)
            cell.set_fill(color, opacity=float(data[i, j]) / max_val)
            cell.set_stroke(width=0)
            cell.move_to(RIGHT * j * cell_gap + DOWN * i * cell_gap)
            grid.add(cell)
    grid.move_to(ORIGIN)
    return grid


class SVDDiagMockery(theme.ProjectVOScene):
    def construct(self):
        super().construct()

        bonk_meme = ImageMobject(Path("img") / "gthj_bonk.jpg")
        bonk_meme.set(height=7)

        with self.voiceover(text="It’s natural to wonder how this relates to the diagonalization process.") as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="Is SVD simply an improved version, a mathematical update that we all need? Unfortunately..."
        ) as tracker:
            self.play(
                FadeIn(bonk_meme),
                run_time=tracker.duration * 0.5
            )

        no_text = MathTex("No.").set_color(theme.TEXT).scale(2)

        with self.voiceover(
            text="...No."
        ) as tracker:
            self.remove(bonk_meme)
            self.add(no_text)
            self.wait(tracker.duration)

        self.remove(no_text)


class SVDandDiagContrast(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()

        # 1. SETUP (Decoupled)
        self.i_hat.set_color(BLUE)
        self.j_hat.set_color(BLUE)

        # 2. DIAGONALIZATION REVIEW
        with self.voiceover(text="You can think of diagonalization as a search for fixed directions.") as tracker:
            self.apply_matrix([[2, 0], [0, 1]], run_time=max(1, tracker.duration))

        # 3. ROTATION FAILURE
        with self.voiceover(text="A rotation matrix, for instance, has no real eigenvectors because every vector is moved off its span.") as tracker:
            self.i_hat.set_color(RED)
            self.j_hat.set_color(RED)
            self.apply_matrix([[0, -1], [1, 0]], run_time=max(1, tracker.duration))

        # 4. SVD PIVOT
        with self.voiceover(text="However, SVD doesn't care if the vectors stay on their span. It only cares that we can find a perpendicular set of vectors.") as tracker:
            # Reset grid and color
            self.plane.restore()

            # Highlight orthogonality
            perp_symbol = RightAngle(self.i_hat, self.j_hat, length=0.2, color=GREEN)  # type: ignore
            self.play(FadeIn(perp_symbol), run_time=max(1, tracker.duration))

        self.wait(2)


class SVDApplications(theme.ProjectVOScene):
    """
    Narration section: 'The Power of SVD in the Real World'
    Three applications: image compression, PCA, and latent semantic analysis.
    """

    def construct(self):
        super().construct()

        # ══════════════════════════════════════════════════════════════════
        # APPLICATION 1 — Image Compression
        # ══════════════════════════════════════════════════════════════════

        section_title = self.accent_text("Image Compression", scale=0.75).to_corner(UL)

        # Singular value decay curve
        axes = (
            Axes(
                x_range=[0, 50, 10],
                y_range=[0, 5, 1],
                x_length=4.5,
                y_length=2.8,
                axis_config={"color": theme.MUTED, "stroke_width": 1.5},
                tips=False,
            )
            .to_edge(RIGHT, buff=0.8)
            .shift(DOWN * 0.3)
        )
        x_label = self.body_text("singular value rank k", scale=0.45).next_to(axes, DOWN, buff=0.15)
        decay_curve = axes.plot(
            lambda x: 5 * np.exp(-0.1 * x),
            color=theme.ACCENT,
            stroke_width=3,
        )

        # Image placeholder panels (left side)
        img_panel = Rectangle(
            width=3.2, height=2.8,
            fill_color=theme.TEXT, fill_opacity=0.08,
            stroke_color=theme.MUTED, stroke_width=1.5,
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)

        img_label = self.body_text("original image\n(full matrix)", scale=0.45).next_to(img_panel, DOWN, buff=0.15)

        # The images — load them; fall back to a placeholder rectangle if file missing
        try:
            img_base = ImageMobject(Path("img") / "base.png").scale(1.1).move_to(img_panel)
            img_k1   = ImageMobject(Path("img") / "k-1.png").scale(1.1).move_to(img_panel)
            img_k10  = ImageMobject(Path("img") / "k-10.png").scale(1.1).move_to(img_panel)
            img_k50  = ImageMobject(Path("img") / "k-50.png").scale(1.1).move_to(img_panel)
        except Exception:
            # Graceful fallback: coloured rectangles representing quality steps
            def placeholder(fill, label_str):
                r = Rectangle(width=3.0, height=2.6, fill_color=fill, fill_opacity=0.25, stroke_color=theme.MUTED, stroke_width=1)
                r.move_to(img_panel)
                return r
            img_base = placeholder(theme.ACCENT,  "original")
            img_k1   = placeholder(theme.MUTED,   "k=1")
            img_k10  = placeholder(theme.ACCENT2, "k=10")
            img_k50  = placeholder(theme.ACCENT,  "k=50")

        # Cut line + shaded tail
        def make_cut_and_tail(k):
            cut = DashedLine(axes.c2p(k, 0), axes.c2p(k, 5),
                             color=theme.ACCENT2, stroke_width=2)
            # Shaded "discarded" tail
            left_pt  = axes.c2p(k, 0)
            right_pt = axes.c2p(50, 5)
            w = right_pt[0] - left_pt[0]
            h = right_pt[1] - left_pt[1]
            tail = Rectangle(
                width=w, height=h,
                fill_color=theme.MUTED, fill_opacity=0.18, stroke_width=0
            ).move_to(((left_pt[0] + right_pt[0]) / 2, (left_pt[1] + right_pt[1]) / 2, 0))
            return cut, tail

        cut1,  tail1  = make_cut_and_tail(1)
        cut10, tail10 = make_cut_and_tail(10)
        cut50, tail50 = make_cut_and_tail(50)

        k_label = self.body_text("k = 1", scale=0.5).set_color(theme.ACCENT2)

        # ── Animate application 1 ─────────────────────────────────────────

        with self.voiceover(
            text="Because SVD isolates the most important directions of a transformation, "
                 "it acts as a perfect filter for information. "
                 "This is the secret behind many technologies we use daily."
        ) as tracker:
            self.play(FadeIn(section_title), run_time=tracker.duration * 0.2)
            self.play(
                FadeIn(img_panel), FadeIn(img_base), FadeIn(img_label),
                run_time=tracker.duration * 0.4,
            )
            self.play(
                Create(axes), Create(decay_curve), FadeIn(x_label),
                run_time=tracker.duration * 0.4,
            )

        with self.voiceover(
            text="Think of a high-resolution photograph. To a computer, that's just a massive matrix of color values. "
                 "By performing an SVD, we isolate the largest singular values — "
                 "which capture the primary structure of the image."
        ) as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="If we keep only the top k singular values and throw away the rest, "
                 "we reconstruct an image that looks nearly identical to the original, "
                 "but stores only a fraction of the data."
        ) as tracker:
            # k = 1
            k_label.next_to(cut1, UP, buff=0.1)
            self.play(
                Transform(img_base, img_k1),
                Create(cut1), FadeIn(tail1), FadeIn(k_label),
                run_time=tracker.duration * 0.4,
            )
            self.wait(tracker.duration * 0.15)

            # k = 10
            k_label_10 = self.body_text("k = 10", scale=0.5).set_color(theme.ACCENT2).next_to(cut10, UP, buff=0.1)
            self.play(
                Transform(img_base, img_k10),
                Transform(cut1, cut10),
                Transform(tail1, tail10),
                ReplacementTransform(k_label, k_label_10),
                run_time=tracker.duration * 0.3,
            )
            self.wait(tracker.duration * 0.15)

            # k = 50
            k_label_50 = self.body_text("k = 50", scale=0.5).set_color(theme.ACCENT2).next_to(cut50, UP, buff=0.1)
            self.play(
                Transform(img_base, img_k50),
                Transform(cut1, cut50),
                Transform(tail1, tail50),
                ReplacementTransform(k_label_10, k_label_50),
                run_time=tracker.duration * 0.2,
            )

        with self.voiceover(
            text="We're essentially telling the computer: ignore the noise and tiny details — "
                 "just give me the primary structural components. "
                 "The big shapes, the lighting, the contrasting lines."
        ) as tracker:
            self.wait(tracker.duration)

        # Clear for next application
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════
        # APPLICATION 2 — PCA
        # ══════════════════════════════════════════════════════════════════

        pca_title = self.accent_text("Principal Component Analysis (PCA)", scale=0.65).to_corner(UL)

        # Dot cloud: elongated ellipse rotated PI/6
        rng = np.random.default_rng(42)
        angle_val = PI / 6
        dots = VGroup()
        for _ in range(280):
            x = rng.normal(scale=2.0)
            y = rng.normal(scale=0.55)
            px = x * np.cos(angle_val) - y * np.sin(angle_val)
            py = x * np.sin(angle_val) + y * np.cos(angle_val)
            dots.add(Dot(np.array([px, py, 0]), color=theme.ACCENT, radius=0.035, fill_opacity=0.7))

        pc1, pc2, pc_angle, _ = compute_pca_arrows(dots)
        center = dots.get_center()
        pc1.shift(center)
        pc2.shift(center)

        ellipse = Ellipse(width=5.5, height=1.6, color=theme.ACCENT2, stroke_width=3)
        ellipse.rotate(pc_angle).move_to(center)

        pc1_label = MathTex("PC_1", color=theme.ACCENT2).scale(0.65).next_to(pc1.get_end(), UR, buff=0.1)
        pc2_label = MathTex("PC_2", color=theme.ACCENT2).scale(0.65).next_to(pc2.get_end(), UP, buff=0.1)

        dim_note = (
            self.body_text("largest singular value direction = most variance", scale=0.5)
            .set_color(theme.MUTED)
            .to_edge(DOWN, buff=0.35)
        )

        with self.voiceover(
            text="Beyond images, SVD is the engine behind Principal Component Analysis — "
                 "or PCA — one of the most widely used tools in data science."
        ) as tracker:
            self.play(FadeIn(pca_title), run_time=tracker.duration * 0.2)
            self.play(FadeIn(dots), run_time=tracker.duration * 0.8)

        with self.voiceover(
            text="Imagine a dataset of hundreds of people, each described by dozens of measurements. "
                 "That's a cloud of points in a very high-dimensional space — impossible to visualize."
        ) as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="PCA uses SVD to find the directions along which your data varies the most — "
                 "the axes of greatest spread."
        ) as tracker:
            self.play(
                GrowArrow(pc1), GrowArrow(pc2),
                FadeIn(pc1_label), FadeIn(pc2_label),
                run_time=tracker.duration * 0.7,
            )
            self.wait(tracker.duration * 0.3)

        with self.voiceover(
            text="Those principal components are exactly the axes of the ellipse that your data cloud forms. "
                 "SVD finds them the same way it always does — "
                 "by identifying the directions that carry the most information."
        ) as tracker:
            self.play(
                dots.animate.set_opacity(0.45),
                Create(ellipse),
                run_time=tracker.duration * 0.5,
            )
            self.play(FadeIn(dim_note), run_time=tracker.duration * 0.3)
            self.wait(tracker.duration * 0.2)

        with self.voiceover(
            text="By projecting everything onto just the top two or three directions, "
                 "you can collapse that high-dimensional cloud into something you can plot and reason about, "
                 "while preserving as much structure as possible. "
                 "The dimensions it keeps are those with the largest singular values; "
                 "the ones it discards are the noise."
        ) as tracker:
            self.wait(tracker.duration)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.wait(0.3)

        # ══════════════════════════════════════════════════════════════════
        # APPLICATION 3 — Latent Semantic Analysis
        # ══════════════════════════════════════════════════════════════════

        lsa_title = self.accent_text("Latent Semantic Analysis (LSA)", scale=0.65).to_corner(UL)

        # ── Term-document matrix ──────────────────────────────────────────
        raw_data = np.array([
            [5, 4, 0, 0],
            [3, 5, 0, 0],
            [4, 4, 1, 0],
            [0, 0, 3, 5],
            [0, 0, 4, 4],
        ])

        raw_grid = make_matrix_grid(raw_data, cell_size=0.5, cell_gap=0.62, color=theme.ACCENT)
        raw_grid.shift(LEFT * 0.5 + DOWN * 0.2)

        words = ["marathon", "sprint", "run", "feline", "cat"]
        docs  = ["D1", "D2", "D3", "D4"]
        rows_n, cols_n = raw_data.shape

        row_labels = VGroup(*[
            self.body_text(word, scale=0.45).next_to(raw_grid[i * cols_n], LEFT, buff=0.25)
            for i, word in enumerate(words)
        ])
        col_labels = VGroup(*[
            self.body_text(doc, scale=0.45).next_to(raw_grid[j], UP, buff=0.25)
            for j, doc in enumerate(docs)
        ])

        # Sigma result (middle step)
        sigma_tex = MathTex(
            r"\Sigma = \begin{bmatrix} \sigma_1 & 0 & 0 \\ 0 & \sigma_2 & 0 \\ 0 & 0 & \sigma_3 \end{bmatrix}",
            color=theme.TEXT,
        ).scale(0.9)

        # Smooth reconstruction grid
        smooth_data = np.array([
            [5, 4, 0, 0],
            [4, 5, 0, 0],
            [4, 4, 1, 0],
            [0, 0, 4, 5],
            [0, 0, 5, 4],
        ])
        smooth_grid = make_matrix_grid(smooth_data, cell_size=0.5, cell_gap=0.62, color=theme.ACCENT)
        smooth_grid.shift(LEFT * 0.5 + DOWN * 0.2)

        # Highlight boxes for semantic clusters
        running_cells = VGroup(*[cast(VMobject, smooth_grid[i]) for i in [0, 1, 4, 5, 8, 9]])
        feline_cells  = VGroup(*[cast(VMobject, smooth_grid[i]) for i in [14, 15, 18, 19]])

        hl_running = SurroundingRectangle(running_cells, color=theme.ACCENT2, stroke_width=2.5, buff=0.05)
        hl_feline  = SurroundingRectangle(feline_cells,  color=theme.ACCENT2, stroke_width=2.5, buff=0.05)

        running_tag = self.body_text('"running"', scale=0.5).set_color(theme.ACCENT2).next_to(hl_running, RIGHT, buff=0.2)
        feline_tag  = self.body_text('"feline"',  scale=0.5).set_color(theme.ACCENT2).next_to(hl_feline,  RIGHT, buff=0.2)

        # Query illustration
        query_note = (
            self.body_text('query: "feline"  →  returns docs about cats', scale=0.5)
            .set_color(theme.MUTED)
            .to_edge(DOWN, buff=0.35)
        )

        # ── Animate application 3 ─────────────────────────────────────────

        with self.voiceover(
            text="Perhaps the most counterintuitive application is in human language itself — "
                 "fabulously called Latent Semantic Analysis."
        ) as tracker:
            self.play(FadeIn(lsa_title), run_time=tracker.duration * 0.2)
            self.play(
                Create(raw_grid),
                FadeIn(row_labels), FadeIn(col_labels),
                run_time=tracker.duration * 0.8,
            )

        with self.voiceover(
            text="We start with a term-document matrix. "
                 "Every row is a unique word, every column is a document, "
                 "and each entry records how often that word appears."
        ) as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="The problem is that language is noisy. "
                 "Synonyms — different words for the same concept — "
                 "and polysemy — one word with multiple meanings — "
                 "make two related documents look unrelated to a computer."
        ) as tracker:
            # Briefly flash the row labels to highlight the synonym problem
            self.play(
                Indicate(row_labels[0], color=theme.ACCENT2),  # marathon
                Indicate(row_labels[1], color=theme.ACCENT2),  # sprint
                Indicate(row_labels[2], color=theme.ACCENT2),  # run
                run_time=tracker.duration * 0.5,
            )
            self.play(
                Indicate(row_labels[3], color=theme.ACCENT2),  # feline
                Indicate(row_labels[4], color=theme.ACCENT2),  # cat
                run_time=tracker.duration * 0.5,
            )

        with self.voiceover(
            text="By applying SVD to this matrix, we decompose it and keep only the top k singular values — "
                 "effectively compressing and smoothing the data."
        ) as tracker:
            self.play(
                ReplacementTransform(VGroup(raw_grid, row_labels, col_labels), sigma_tex),
                run_time=tracker.duration * 0.6,
            )
            self.wait(tracker.duration * 0.4)

        with self.voiceover(
            text="This ignores the minor, accidental word choices of an author "
                 "and focuses on the primary semantic structure."
        ) as tracker:
            self.play(
                ReplacementTransform(sigma_tex, smooth_grid),
                run_time=tracker.duration * 0.5,
            )
            self.play(
                FadeIn(row_labels), FadeIn(col_labels),
                run_time=tracker.duration * 0.3,
            )
            self.wait(tracker.duration * 0.2)

        with self.voiceover(
            text="SVD has grouped words by where they appear together. "
                 "Marathon, sprint, and run cluster into a latent concept of running."
        ) as tracker:
            self.play(Create(hl_running), FadeIn(running_tag), run_time=tracker.duration * 0.6)
            self.wait(tracker.duration * 0.4)

        with self.voiceover(
            text="Feline and cat cluster into the concept of cats — "
                 "even though they never appeared in the same documents."
        ) as tracker:
            self.play(Create(hl_feline), FadeIn(feline_tag), run_time=tracker.duration * 0.6)
            self.wait(tracker.duration * 0.4)

        with self.voiceover(
            text="Now we can compare documents not by whether they share exact words, "
                 "but by whether they share the same conceptual space. "
                 "A search for 'feline' can return documents about cats, "
                 "even if the word feline never appears in them."
        ) as tracker:
            self.play(FadeIn(query_note), run_time=tracker.duration * 0.3)
            self.wait(tracker.duration * 0.7)

        self.wait(0.5)

        # ── Closing thought ───────────────────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)

        closing1 = self.accent_text("The same geometry.", scale=0.9).arrange(DOWN, buff=0.55)
        closing2 = self.body_text(
                "A circle becoming an ellipse — the same principle that\n"
                "compresses images, finds structure in data, and lets\n"
                "a computer understand the meaning of human language.",
                scale=0.6,
            ).arrange(DOWN, buff=0.55)

        with self.voiceover(
            text="It's a profound thought: the same geometric principle that describes how a circle turns into an ellipse "
                 "is the same principle that allows a computer to understand the underlying structure of human preferences, "
                 "or the essence of a digital photograph. "
                 "SVD transforms a chaotic, high-dimensional world into a structured, geometric landscape "
                 "where meaning is defined by proximity — not just spelling."
        ) as tracker:
            self.play(Write(closing1), run_time=tracker.duration * 0.2)
            self.play(FadeIn(closing2), run_time=tracker.duration * 0.3)
            self.wait(tracker.duration * 0.5)

        self.wait(2)
