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
