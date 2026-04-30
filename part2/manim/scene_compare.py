# Render: manim -q[quality: l-low, m-medium, h-high] [file name] [scene name] --disable_caching

from typing import Tuple, cast, List
import manim as mn
import theme
import numpy as np
from pathlib import Path


class SVDDiagMockery(theme.ProjectVOScene):
    def construct(self):
        super().construct()

        bonk_meme = mn.ImageMobject(Path("img") / "gthj_bonk.jpg")
        bonk_meme.set(height=7)

        with self.voiceover(text="It is natural to wonder how this relates to the diagonalization process.") as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="Is SVD simply an improved version, a mathematical update that we all need? Unfortunately..."
        ) as tracker:
            self.play(
                mn.FadeIn(bonk_meme),
                run_time=self.get_capped_run_time(tracker.duration * 0.5, self.T_MEDIUM)
            )

        no_text = mn.MathTex("No.").set_color(theme.TEXT).scale(2)

        with self.voiceover(
            text="...No."
        ) as tracker:
            self.remove(bonk_meme)
            self.add(no_text)
            self.wait(tracker.duration)

        self.remove(no_text)

        self.wait(self.T_BRIEF)


class SVDandDiagContrast(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()

        # 1. SETUP (Decoupled)
        self.i_hat.set_color(mn.BLUE)
        self.j_hat.set_color(mn.BLUE)

        # 2. DIAGONALIZATION REVIEW
        matrix = np.array([[2, 0], [0, 1.5]])
        matrix_tex = mn.MathTex(
            "A = \\begin{bmatrix} 2 & 0 \\\\ 0 & \\frac{3}{2} \\end{bmatrix}", color=theme.TEXT
        ).to_corner(mn.UL)

        with self.voiceover(
            text="You can think of diagonalization as a search for fixed directions."
        ) as tracker:
            self.play(mn.Write(matrix_tex), run_time=self.get_capped_run_time(tracker.duration * 0.8, self.T_MEDIUM))
            
        with self.voiceover(
            text="We want to find a basis where the input and output are the same such that the transformation is just a scalar multiple."
        ) as tracker:
            self.apply_matrix(matrix, run_time=self.get_capped_run_time(tracker.duration, self.T_LONG))
        
        self.play(mn.Unwrite(matrix_tex), run_time=self.T_BRIEF)

        # 3. ROTATION FAILURE
        rot_matrix = np.array([[0, -1], [1, 0]])
        rot_matrix_tex = mn.MathTex(
            "B = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}", color=theme.TEXT
        ).to_corner(mn.UL)

        with self.voiceover(
            text="The problem is that for many transformations, such fixed directions don't exist in a way that captures the whole transformation."
        ) as tracker:
            self.wait(self.T_BRIEF)
            self.play(
                mn.Write(rot_matrix_tex),
                run_time=self.get_capped_run_time(tracker.duration * 0.5, self.T_MEDIUM)
            )

        with self.voiceover(
            text="A rotation matrix for instance, has no real eigenvectors because every vector is moved off its span."
        ) as tracker:
            self.i_hat.set_color(mn.RED)
            self.j_hat.set_color(mn.RED)
            self.apply_matrix(rot_matrix, run_time=self.get_capped_run_time(tracker.duration, self.T_LONG))

        # 4. SVD PIVOT
        with self.voiceover(
            text="However, SVD doesn't care if the vectors stay on their span. It only cares that we can find a perpendicular set of vectors that ends up as another perpendicular set of vectors, just potentially rotated and scaled."
        ) as tracker:
            # Reset grid and color
            # self.plane.restore()  # <--- This is what broke last time

            # Highlight orthogonality
            perp_symbol = mn.RightAngle(self.i_hat, self.j_hat, length=0.2, color=mn.GREEN)  # type: ignore
            self.play(mn.FadeIn(perp_symbol), run_time=self.get_capped_run_time(tracker.duration, self.T_MEDIUM))

        self.wait(self.T_SHORT)


class SVDDiagBridge(theme.ProjectVOScene):
    def construct(self):
        super().construct()

        # ── OBJECTS ───────────────────────────────────────────────────────────

        # Symmetric matrix condition
        sym_condition = mn.MathTex(
            "A = A^T", color=theme.TEXT
        ).scale(1.2)

        # SVD = Diag equation
        bridge_eq = mn.MathTex(
            "\\text{SVD} = \\text{Diagonalization}",
            color=theme.ACCENT,
        ).scale(1.0)

        # Collapse: U = V
        collapse = mn.VGroup(
            mn.MathTex("U = V", color=theme.TEXT).scale(0.9),
            mn.MathTex(
                "\\sigma_i = |\\lambda_i|", color=theme.TEXT
            ).scale(0.9),
        ).arrange(mn.RIGHT, buff=1.2)

        # Full equation for context
        svd_eq = mn.MathTex(
            "A", "=", "U", "\\Sigma", "V^T",
            color=theme.TEXT,
        ).scale(0.9)
        diag_eq = mn.MathTex(
            "A", "=", "P", "D", "P^{-1}",
            color=theme.TEXT,
        ).scale(0.9)
        equations = mn.VGroup(svd_eq, diag_eq).arrange(mn.DOWN, buff=0.6)

        # ── SEGMENT 1: SYMMETRIC CONDITION ───────────────────────────────────
        with self.voiceover(
            text="There is a beautiful bridge between the two."
        ) as tracker:
            self.play(
                mn.Write(sym_condition),
                run_time=self.get_capped_run_time(tracker.duration, self.T_MEDIUM),
            )

        with self.voiceover(
            text="If you have a symmetric matrix — one that equals its own transpose — SVD and diagonalization become the same thing."
        ) as tracker:
            self.play(
                sym_condition.animate.to_corner(mn.UL),
                run_time=self.get_capped_run_time(tracker.duration * 0.3, self.T_SHORT),
            )
            self.play(
                mn.Write(bridge_eq),
                run_time=self.get_capped_run_time(tracker.duration * 0.7, self.T_MEDIUM),
            )

        # ── SEGMENT 2: WHAT COLLAPSES ─────────────────────────────────────────
        with self.voiceover(
            text="In that specific case, the singular values are simply the absolute values of the eigenvalues."
        ) as tracker:
            self.play(
                mn.FadeOut(bridge_eq),
                run_time=self.get_capped_run_time(tracker.duration * 0.2, self.T_BRIEF),
            )
            self.play(
                mn.Write(collapse[1]),  # type: ignore
                run_time=self.get_capped_run_time(tracker.duration * 0.8, self.T_MEDIUM),
            )

        with self.voiceover(
            text="And the input and output rotations happen to be the same, so U and V collapse into one."
        ) as tracker:
            self.play(
                mn.Write(collapse[0]),  # type: ignore
                run_time=self.get_capped_run_time(tracker.duration * 0.6, self.T_MEDIUM),
            )
            self.wait(self.get_capped_run_time(tracker.duration * 0.4, self.T_SHORT))

        # ── SEGMENT 3: VISUAL COLLAPSE ────────────────────────────────────────
        with self.voiceover(
            text="Visually, the two decompositions look the same — both rows collapse to the same formula."
        ) as tracker:
            self.play(
                mn.FadeOut(collapse, sym_condition),
                run_time=self.get_capped_run_time(tracker.duration * 0.2, self.T_BRIEF),
            )
            self.play(
                mn.Write(equations),
                run_time=self.get_capped_run_time(tracker.duration * 0.8, self.T_MEDIUM),
            )
            # Highlight U and V^T collapsing — same color
            self.play(
                svd_eq[2].animate.set_color(theme.ACCENT),   # U
                svd_eq[4].animate.set_color(theme.ACCENT),   # V^T
                diag_eq[2].animate.set_color(theme.ACCENT),  # P
                diag_eq[4].animate.set_color(theme.ACCENT),  # P^{-1}
                svd_eq[3].animate.set_color(theme.ACCENT2),  # Sigma
                diag_eq[3].animate.set_color(theme.ACCENT2), # D
                run_time=self.get_capped_run_time(tracker.duration * 0.4, self.T_SHORT),
            )

        self.wait(self.T_SHORT)


class SVDDiagApplicationDistinction(theme.ProjectVOScene):
    def construct(self):
        super().construct()

        # ── OBJECTS ───────────────────────────────────────────────────────────

        # Two-column layout: Diagonalization vs SVD
        diag_header = self.accent_text("Diagonalization", scale=0.6)
        svd_header = self.accent_text("SVD", scale=0.6)
        headers = mn.VGroup(diag_header, svd_header).arrange(mn.RIGHT, buff=3.5)
        headers.to_edge(mn.UP, buff=0.8)

        divider = mn.DashedLine(
            mn.UP * 3, mn.DOWN * 3, color=theme.MUTED, stroke_opacity=0.5
        )

        # Diagonalization use case
        diag_use = mn.VGroup(
            mn.MathTex("\\text{repeating process}", color=theme.TEXT).scale(0.7),
            mn.MathTex("\\text{(Markov chains, interest rates)}", color=theme.MUTED).scale(0.55),
        ).arrange(mn.DOWN, buff=0.2)

        diag_insight = mn.VGroup(
            mn.MathTex("\\text{follow eigenvectors}", color=theme.ACCENT2).scale(0.7),
            mn.MathTex("\\text{long-term behavior}", color=theme.MUTED).scale(0.55),
        ).arrange(mn.DOWN, buff=0.2)

        diag_col = mn.VGroup(diag_use, diag_insight).arrange(mn.DOWN, buff=0.6)
        diag_col.next_to(divider, mn.LEFT, buff=0.5)

        # SVD use case
        svd_use = mn.VGroup(
            mn.MathTex("\\text{single snapshot of data}", color=theme.TEXT).scale(0.7),
            mn.MathTex("\\text{(images, deformations)}", color=theme.MUTED).scale(0.55),
        ).arrange(mn.DOWN, buff=0.2)

        svd_insight = mn.VGroup(
            mn.MathTex("\\text{follow singular vectors}", color=theme.ACCENT).scale(0.7),
            mn.MathTex("\\text{dominant distortion}", color=theme.MUTED).scale(0.55),
        ).arrange(mn.DOWN, buff=0.2)

        svd_col = mn.VGroup(svd_use, svd_insight).arrange(mn.DOWN, buff=0.6)
        svd_col.next_to(divider, mn.RIGHT, buff=0.5)

        # Always exist note
        always_exist = mn.MathTex(
            "\\text{singular vectors always exist}",
            color=theme.ACCENT,
        ).scale(0.75).to_edge(mn.DOWN, buff=0.8)

        # ── SEGMENT 1: DIAGONALIZATION USE CASE ──────────────────────────────
        with self.voiceover(
            text="In every other case, there is a distinction to draw."
        ) as tracker:
            self.play(
                mn.Write(headers),
                mn.Create(divider),
                run_time=self.get_capped_run_time(tracker.duration, self.T_MEDIUM),
            )

        with self.voiceover(
            text="If you are analyzing a process that repeats — like interest rates or a Markov chain — follow the eigenvectors."
        ) as tracker:
            self.play(
                mn.FadeIn(diag_use),
                run_time=self.get_capped_run_time(tracker.duration, self.T_MEDIUM),
            )

        with self.voiceover(
            text="They tell you where the system will end up after many, many steps."
        ) as tracker:
            self.play(
                mn.FadeIn(diag_insight),
                run_time=self.get_capped_run_time(tracker.duration, self.T_MEDIUM),
            )

        # ── SEGMENT 2: SVD USE CASE ───────────────────────────────────────────
        with self.voiceover(
            text="If you are analyzing a single snapshot of data or a physical deformation, follow the singular vectors."
        ) as tracker:
            self.play(
                mn.FadeIn(svd_use),
                run_time=self.get_capped_run_time(tracker.duration, self.T_MEDIUM),
            )

        with self.voiceover(
            text="They tell you how the shape is distorted, and where the most significant information is stored — the direction that is stretched the most."
        ) as tracker:
            self.play(
                mn.FadeIn(svd_insight),
                run_time=self.get_capped_run_time(tracker.duration, self.T_MEDIUM),
            )

        # ── SEGMENT 3: ALWAYS EXIST ───────────────────────────────────────────
        with self.voiceover(
            text="And it is helpful to know that singular vectors always exist — for every single matrix, without exception."
        ) as tracker:
            self.play(
                mn.Write(always_exist),
                run_time=self.get_capped_run_time(tracker.duration * 0.5, self.T_MEDIUM),
            )
            self.play(
                always_exist.animate.set_color(theme.ACCENT),
                run_time=self.get_capped_run_time(tracker.duration * 0.5, self.T_SHORT),
            )

        self.wait(self.T_SHORT)
