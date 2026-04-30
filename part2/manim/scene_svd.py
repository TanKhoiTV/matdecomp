# Render: manim -q[quality: l-low, m-medium, h-high] [file name] [scene name] --disable_caching

from typing import Tuple, cast, List
import manim as mn
import theme
import numpy as np
from pathlib import Path


class SVDGeometry(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()

        # 1. FADE IN
        with self.voiceover(
            text="To understand what SVD is actually doing, let's think about how a linear transformation affects the space it lives in."
        ) as tracker:
            self.play(
                mn.FadeIn(self.plane),
                mn.FadeIn(self.background_plane),
                mn.Create(self.basis_vectors),
                run_time=self.get_capped_run_time(tracker.duration, self.T_LONG)
            )
        
        self.wait(self.T_BRIEF)

        unit_circle = mn.Circle(radius=1, color=theme.ACCENT, stroke_width=4)
        matrix_a = np.array([[2, 1], [0.5, 1.5]])
        self.add_transformable_mobject(unit_circle)

        with self.voiceover(
            text="Imagine a unit circle in a 2D input space. When we apply a linear transformation to this space..."
        ) as tracker:
            self.play(mn.Create(unit_circle), run_time=self.get_capped_run_time(tracker.duration * 0.5, self.T_MEDIUM))

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
        ellipse_axis1 = mn.DashedLine(
            start=[-axis1_end[0], -axis1_end[1], 0],
            end=[axis1_end[0], axis1_end[1], 0],
            color=theme.ACCENT2,
        )
        ellipse_axis2 = mn.DashedLine(
            start=[-axis2_end[0], -axis2_end[1], 0],
            end=[axis2_end[0], axis2_end[1], 0],
            color=theme.ACCENT2,
        )
        ellipse_axes = mn.VGroup(ellipse_axis1, ellipse_axis2)

        with self.voiceover(
            text="...which become the axes of the ellipse after transformation."
        ) as tracker:
            self.play(
                mn.Create(ellipse_axes),
                run_time=tracker.duration * 0.5,
            )
            self.wait(tracker.duration * 0.5)

        self.play(
            mn.FadeOut(unit_circle, ellipse_axes),
            mn.FadeOut(self.plane),
            mn.FadeOut(self.background_plane),
            mn.FadeOut(self.basis_vectors),
            run_time=self.T_BRIEF,
        )

        self.wait(self.T_SHORT)


class SVDBreakdown(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()

        # Hide auto-created objects initially
        self.plane.set_opacity(0)
        self.background_plane.set_opacity(0)
        self.i_hat.set_opacity(0)
        self.j_hat.set_opacity(0)

        unit_circle = mn.Circle(radius=1, color=theme.ACCENT, stroke_width=4)

        theta_v = mn.PI / 6
        sigma_vals = [2.0, 0.8]
        theta_u = mn.PI / 4

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
        self.i_hat.put_start_and_end_on(mn.ORIGIN, np.append(V[:, 0], 0))
        self.j_hat.put_start_and_end_on(mn.ORIGIN, np.append(V[:, 1], 0))
        self.i_hat.set_color(theme.ACCENT)
        self.j_hat.set_color(theme.ACCENT2)

        # RightAngle symbol
        right_angle = mn.RightAngle(
            self.i_hat,  # type: ignore
            self.j_hat,  # type: ignore
            length=0.2,
            color=theme.MUTED,
            fill_opacity=0,
            stroke_width=2,
        )
        right_angle.set_opacity(0)

        def update_right_angle(m):
            new = mn.RightAngle(
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
        v1_label = mn.MathTex("v_1", color=theme.ACCENT).scale(0.7)
        v2_label = mn.MathTex("v_2", color=theme.ACCENT2).scale(0.7)
        v1_label.add_updater(lambda m: m.next_to(self.i_hat.get_end(), mn.UL, buff=0.1))
        v2_label.add_updater(lambda m: m.next_to(self.j_hat.get_end(), mn.UP, buff=0.1))
        v_annotations = mn.VGroup(v1_label, v2_label)

        svd_formula = (
            mn.MathTex("A", "=", "U", "\\Sigma", "V^T", color=theme.TEXT)
            .to_corner(mn.UL)
            .shift(mn.DOWN)
        )

        # Helper: apply a 2D matrix to a mobject via ApplyMatrix animation,
        # syncing i_hat, j_hat, and the plane via self.apply_matrix,
        # but keeping svd_formula untouched as a plain scene mobject.
        def transform_scene(matrix, u_run_time, path_arc=None):
            m3 = np.eye(3)
            m3[:2, :2] = matrix
            anim = mn.ApplyMatrix(m3, unit_circle, path_arc=path_arc or 0)
            rt = anim.get_run_time()
            rf = anim.get_rate_func()
            self.play(
                anim,
                mn.ApplyMatrix(m3, self.i_hat,  rate_func=rf, run_time=rt),
                mn.ApplyMatrix(m3, self.j_hat,  rate_func=rf, run_time=rt),
                mn.ApplyMatrix(m3, self.plane,  rate_func=rf, run_time=rt),
                run_time=u_run_time,
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
            self.play(mn.Create(unit_circle), run_time=tracker.duration * 0.2)
            self.play(mn.Write(svd_formula), run_time=tracker.duration * 0.3)
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
            target_axes = mn.DashedLine(mn.LEFT * 3, mn.RIGHT * 3, color=theme.MUTED)
            target_axes.set_opacity(0.5)
            self.play(mn.Create(target_axes), run_time=0.5)
            transform_scene(matrix=R_v, u_run_time=tracker.duration * 0.7)
            self.play(
                v_annotations.animate.set_opacity(0.8),
                run_time=self.get_capped_run_time(tracker.duration * 0.3, self.T_SHORT),
            )
            self.wait(max(0, tracker.duration * 0.3 - 0.4))

        with self.voiceover(
            text="Visually, the unit circle spins but doesn't look any different."
        ) as tracker:
            self.wait(tracker.duration)

        # 3. Step 2: Sigma (Scaling)

        sigma_label1 = mn.MathTex("\\sigma_1 = 2.0", color=theme.ACCENT2)
        sigma_label2 = mn.MathTex("\\sigma_2 = 0.8", color=theme.ACCENT2)

        with self.voiceover(
            text="Next, Sigma scales these vectors. The factors by which we stretch or squish are called the singular values."
        ) as tracker:
            self.play(
                svd_formula[4].animate.set_color(theme.TEXT),
                svd_formula[3].animate.set_color(theme.ACCENT2),
                right_angle.animate.set_stroke(opacity=0),
                run_time=self.T_BRIEF,
            )
            transform_scene(Sigma, tracker.duration * 0.7, path_arc=0)
            self.play(
                right_angle.animate.set_stroke(opacity=0.8),
                run_time=tracker.duration * 0.2,
            )
            # Add sigma labels after scaling
            sigma_label1.next_to(self.i_hat.get_end(), mn.LEFT * 1.5)
            sigma_label2.next_to(self.j_hat.get_end(), mn.UP * 1.5)
            self.play(
                mn.Write(sigma_label1),
                mn.Write(sigma_label2),
                mn.FadeOut(v_annotations),
                run_time=self.get_capped_run_time(tracker.duration, self.T_MEDIUM),
            )

        with self.voiceover(
            text="Now the circle deforms into an ellipse. If a singular value is zero, that entire dimension collapses. The number of nonzero singular values is the rank of the matrix."
        ) as tracker:
            self.wait(tracker.duration * 0.8)
            self.play(
                mn.FadeOut(sigma_label1, sigma_label2),
                mn.FadeIn(v1_label, v2_label),
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
            transform_scene(R_u, tracker.duration - 0.5)
            self.play(mn.FadeOut(v1_label), mn.FadeOut(v2_label), run_time=0.3)
            # After transform_scene(R_u):
            u1_label = mn.MathTex("u_1", color=theme.ACCENT).scale(0.7)
            u2_label = mn.MathTex("u_2", color=theme.ACCENT2).scale(0.7)
            u1_label.add_updater(
                lambda m: m.next_to(self.i_hat.get_end(), mn.DL, buff=0.1)
            )
            u2_label.add_updater(
                lambda m: m.next_to(self.j_hat.get_end(), mn.UL, buff=0.1)
            )
            self.play(
                mn.ReplacementTransform(v1_label, u1_label),
                mn.ReplacementTransform(v2_label, u2_label),
                run_time=0.4,
            )

        # 5. Conclusion

        with self.voiceover(
            text="Notice that SVD allows the input basis and output basis to be different, as long as both are orthonormal. The vectors form a basis, they are perpendicular, and their lengths are exactly one unit."
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

        self.wait(self.T_SHORT)


class ComputationSideNote(theme.ProjectVOScene):
    def construct(self):
        super().construct()

        # ── OBJECTS ───────────────────────────────────────────────────────────

        # Side note title
        title = self.accent_text("Side Note: Computing SVD", scale=0.6).to_corner(mn.UL)

        # A^T A and AA^T
        ata = mn.MathTex("A^T A", color=theme.TEXT).scale(1.2)
        aat = mn.MathTex("A A^T", color=theme.TEXT).scale(1.2)
        both = mn.VGroup(ata, aat).arrange(mn.RIGHT, buff=1.5).shift(mn.UP * 0.5)

        symmetric_label = mn.MathTex(
            "\\text{always symmetric}", color=theme.ACCENT
        ).scale(0.7).next_to(both, mn.DOWN, buff=0.4)

        # Symmetric matrix example with color-matched entries
        sym_matrix = mn.MathTex(
            "\\begin{bmatrix} a & b \\\\ b & c \\end{bmatrix}",
            color=theme.TEXT,
        ).scale(1.1)
        sym_label = mn.MathTex(
            "\\text{mirror entries}", color=theme.ACCENT
        ).scale(0.6).next_to(sym_matrix, mn.DOWN, buff=0.3)

        # Orthogonal eigenvectors — right angle symbol hint
        perp_hint = mn.MathTex(
            "\\text{eigenvectors} \\perp",
            color=theme.TEXT,
        ).scale(0.9)

        # Result shortcut (no derivation)
        result = mn.MathTex(
            "A^T A = V \\Sigma^2 V^T",
            color=theme.TEXT,
        ).scale(1.0)
        result_note = self.body_text("(result, not derived here)", scale=0.5)
        result_note.set_color(theme.MUTED)
        result_note.next_to(result, mn.DOWN, buff=0.2)

        # Numerical instability example
        A_example = mn.MathTex(
            "A = \\begin{bmatrix} 10^8 & 0 \\\\ 0 & 1 \\end{bmatrix}",
            color=theme.TEXT,
        ).scale(0.9)
        ATA_example = mn.MathTex(
            "A^T A = \\begin{bmatrix} 10^{16} & 0 \\\\ 0 & 1 \\end{bmatrix}",
            color=theme.TEXT,
        ).scale(0.9)
        precision_lost = mn.MathTex(
            "\\text{small entries lost to floating point}",
            color=mn.RED,
        ).scale(0.6)
        precision_lost.next_to(ATA_example, mn.DOWN, buff=0.3)

        # Convergence sketch — number line with bouncing value
        nline = mn.NumberLine(
            x_range=[0, 1, 0.25],
            length=5,
            color=theme.MUTED,
            include_tip=True,
        ).shift(mn.DOWN * 0.5)
        target_dot = mn.Dot(nline.n2p(0.618), color=theme.ACCENT)
        target_label = mn.MathTex("\\sigma^*", color=theme.ACCENT).scale(0.6)
        target_label.next_to(target_dot, mn.UP, buff=0.1)
        iter_dot = mn.Dot(nline.n2p(0.1), color=theme.ACCENT2)
        converge_label = self.body_text("iterative algorithm converges", scale=0.5)
        converge_label.set_color(theme.MUTED).next_to(nline, mn.DOWN, buff=0.3)

        # ── SEGMENT 1: INTRO ─────────────────────────────────────────────────
        with self.voiceover(
            text="As a side note, to find the U and V matrices, we look at two special products: A transpose, A, and, A, A transpose."
        ) as tracker:
            self.play(mn.FadeIn(title), run_time=0.4)
            self.play(
                mn.Write(ata), mn.Write(aat),
                run_time=self.get_capped_run_time(tracker.duration - 0.4, self.T_MEDIUM),
            )

        # ── SEGMENT 2: SYMMETRY ──────────────────────────────────────────────
        with self.voiceover(
            text="Why them specifically? Because they're always symmetric."
        ) as tracker:
            self.play(
                mn.FadeIn(symmetric_label),
                run_time=self.get_capped_run_time(tracker.duration, self.T_MEDIUM),
            )

        with self.voiceover(
            text="A symmetric matrix mirrors its entries across the diagonal."
        ) as tracker:
            self.play(
                mn.FadeOut(both, symmetric_label),
                run_time=self.T_BRIEF,
            )
            self.play(
                mn.FadeIn(sym_matrix),
                run_time=self.get_capped_run_time(tracker.duration * 0.4, self.T_SHORT),
            )
            # Highlight the mirrored b entries
            self.play(
                mn.FadeIn(sym_label),
                run_time=self.get_capped_run_time(tracker.duration * 0.4, self.T_SHORT),
            )

        # ── SEGMENT 3: ORTHOGONAL EIGENVECTORS ──────────────────────────────
        with self.voiceover(
            text="And symmetric matrices always diagonalize with orthogonal eigenvectors, meaning perpendicular."
        ) as tracker:
            self.play(
                mn.FadeOut(sym_matrix, sym_label),
                run_time=self.T_BRIEF,
            )
            self.play(
                mn.Write(perp_hint),
                run_time=self.get_capped_run_time(tracker.duration - 0.3, self.T_MEDIUM),
            )

        with self.voiceover(
            text="That perpendicularity is exactly what gives us the V and U matrices in SVD."
        ) as tracker:
            self.play(
                mn.ReplacementTransform(perp_hint, result),
                run_time=self.get_capped_run_time(tracker.duration * 0.6, self.T_MEDIUM),
            )
            self.play(
                mn.FadeIn(result_note),
                run_time=self.get_capped_run_time(tracker.duration * 0.4, self.T_MEDIUM),
            )

        # ── SEGMENT 4: ITERATIVE ALGORITHM ──────────────────────────────────
        with self.voiceover(
            text="However, finding these eigenvalues requires solving a polynomial equation of degree n."
        ) as tracker:
            self.play(
                mn.FadeOut(result, result_note),
                run_time=self.T_BRIEF,
            )
            self.play(
                mn.Create(nline),
                mn.FadeIn(target_dot, target_label),
                mn.FadeIn(converge_label),
                run_time=self.get_capped_run_time(tracker.duration - 0.3, self.T_MEDIUM),
            )

        with self.voiceover(
            text="For n of 5 or higher, there is no closed-form solution."
        ) as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="So in practice, SVD uses an iterative algorithm that converges toward the answer rather than computing it exactly."
        ) as tracker:
            # Animate the dot bouncing and converging toward target
            checkpoints = [0.9, 0.4, 0.75, 0.55, 0.65, 0.618]
            per_step = tracker.duration / len(checkpoints)
            for val in checkpoints:
                self.play(
                    iter_dot.animate.move_to(nline.n2p(val)),
                    run_time=self.get_capped_run_time(per_step, self.T_SHORT),
                )

        # ── SEGMENT 5: NUMERICAL INSTABILITY ────────────────────────────────
        with self.voiceover(
            text="There is also a deeper problem: computing products like this on a computer is numerically unstable."
        ) as tracker:
            self.play(
                mn.FadeOut(nline, target_dot, target_label, iter_dot, converge_label),
                run_time=self.T_BRIEF,
            )
            self.play(
                mn.FadeIn(A_example),
                run_time=self.get_capped_run_time(tracker.duration - 0.3, self.T_MEDIUM),
            )

        with self.voiceover(
            text="Take a matrix with a very large entry and a small one."
        ) as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="When you compute products, the large entry gets squared to enormous value."
        ) as tracker:
            self.play(
                mn.ReplacementTransform(A_example, ATA_example),
                run_time=self.get_capped_run_time(tracker.duration * 0.6, self.T_MEDIUM),
            )
            self.wait(tracker.duration * 0.4)

        with self.voiceover(
            text="At that scale, floating point arithmetic simply cannot represent the small entry accurately anymore, and all precision is lost."
        ) as tracker:
            self.play(
                mn.FadeIn(precision_lost),
                run_time=self.get_capped_run_time(tracker.duration * 0.4, self.T_MEDIUM),
            )
            self.wait(tracker.duration * 0.6)

        with self.voiceover(
            text="This is why modern SVD implementations work directly on the matrix A, never forming the product at all."
        ) as tracker:
            self.play(
                mn.FadeOut(ATA_example, precision_lost),
                run_time=tracker.duration * 0.3,
            )
            self.wait(tracker.duration * 0.7)

        self.wait(self.T_SHORT)