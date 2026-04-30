# Render: manim -q[quality: l-low, m-medium, h-high] [file name] [scene name] --disable_caching

from typing import Tuple, cast, List
import manim as mn
import theme
import numpy as np
from pathlib import Path


class SVDImageApp(theme.ProjectVOScene):
    """
    Narration section: 'The Power of SVD in the Real World'
    Three applications: image compression, PCA, and latent semantic analysis.
    """

    def construct(self):
        super().construct()

        # ══════════════════════════════════════════════════════════════════
        # APPLICATION 1 — Image Compression
        # ══════════════════════════════════════════════════════════════════

        section_title = self.accent_text("Image Compression", scale=0.75).to_corner(mn.UL)

        # Singular value decay curve
        axes = (
            mn.Axes(
                x_range=[0, 50, 10],
                y_range=[0, 5, 1],
                x_length=4.5,
                y_length=2.8,
                axis_config={"color": theme.MUTED, "stroke_width": 1.5},
                tips=False,
            )
            .to_edge(mn.RIGHT, buff=0.8)
            .shift(mn.DOWN * 0.3)
        )
        x_label = mn.Tex("Singular value rank \\emph{k}").scale(0.45).set_color(theme.TEXT).next_to(axes, mn.DOWN, buff=0.35)
        decay_curve = axes.plot(
            lambda x: 5 * np.exp(-0.1 * x),
            color=theme.ACCENT,
            stroke_width=3,
        )

        # Image placeholder panels (left side)
        img_panel = mn.Rectangle(
            width=3.2, height=2.8,
            fill_color=theme.TEXT, fill_opacity=0.08,
            stroke_color=theme.MUTED, stroke_width=1.5
        ).to_edge(mn.LEFT, buff=1.4).shift(mn.DOWN * 0.3).set_stroke(opacity=0)

        img_label = mn.Tex("Original image").scale(0.45).set_color(theme.TEXT).next_to(img_panel, mn.DOWN, buff=0.5)

        # The images — load them; fall back to a placeholder rectangle if file missing
        try:
            img_base = mn.ImageMobject(Path("img") / "base.png").scale(1.1).move_to(img_panel)
            img_k1   = mn.ImageMobject(Path("img") / "k-1.png").scale(1.1).move_to(img_panel)
            img_k10  = mn.ImageMobject(Path("img") / "k-10.png").scale(1.1).move_to(img_panel)
            img_k50  = mn.ImageMobject(Path("img") / "k-50.png").scale(1.1).move_to(img_panel)
        except Exception:
            # Graceful fallback: coloured rectangles representing quality steps
            def placeholder(fill, label_str):
                r = mn.Rectangle(width=3.0, height=2.6, fill_color=fill, fill_opacity=0.25, stroke_color=theme.MUTED, stroke_width=1)
                r.move_to(img_panel)
                return r
            img_base = placeholder(theme.ACCENT,  "original")
            img_k1   = placeholder(theme.MUTED,   "k=1")
            img_k10  = placeholder(theme.ACCENT2, "k=10")
            img_k50  = placeholder(theme.ACCENT,  "k=50")

        # Cut line + shaded tail
        def make_cut_and_tail(k):
            cut = mn.DashedLine(axes.c2p(k, 0), axes.c2p(k, 5),
                             color=theme.ACCENT2, stroke_width=2)
            # Shaded "discarded" tail
            left_pt  = axes.c2p(k, 0)
            right_pt = axes.c2p(50, 5)
            w = right_pt[0] - left_pt[0]
            h = right_pt[1] - left_pt[1]
            tail = mn.Rectangle(
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
            self.play(mn.FadeIn(section_title), run_time=tracker.duration * 0.2)
            self.play(
                mn.FadeIn(img_panel), mn.FadeIn(img_base), mn.FadeIn(img_label),
                run_time=self.get_capped_run_time(tracker.duration * 0.4, self.T_MEDIUM)
            )
            self.play(
                mn.Create(axes), mn.Create(decay_curve), mn.FadeIn(x_label),
                run_time=self.get_capped_run_time(tracker.duration * 0.4, self.T_MEDIUM)
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
            k_label.next_to(cut1, mn.UP, buff=0.1)
            self.play(
                mn.Transform(img_base, img_k1),
                mn.Create(cut1), mn.FadeIn(tail1), mn.FadeIn(k_label),
                run_time=self.get_capped_run_time(tracker.duration * 0.4, self.T_MEDIUM)
            )
            self.wait(tracker.duration * 0.15)

            # k = 10
            k_label_10 = self.body_text("k = 10", scale=0.5).set_color(theme.ACCENT2).next_to(cut10, mn.UP, buff=0.1)
            self.play(
                mn.Transform(img_base, img_k10),
                mn.Transform(cut1, cut10),
                mn.Transform(tail1, tail10),
                mn.ReplacementTransform(k_label, k_label_10),
                run_time=tracker.duration * 0.3,
            )
            self.wait(tracker.duration * 0.15)

            # k = 50
            k_label_50 = self.body_text("k = 50", scale=0.5).set_color(theme.ACCENT2).next_to(cut50, mn.UP, buff=0.1)
            self.play(
                mn.Transform(img_base, img_k50),
                mn.Transform(cut1, cut50),
                mn.Transform(tail1, tail50),
                mn.ReplacementTransform(k_label_10, k_label_50),
                run_time=tracker.duration * 0.2,
            )

        with self.voiceover(
            text="We're essentially telling the computer: ignore the noise and tiny details — "
                 "just give me the primary structural components. "
                 "The big shapes, the lighting, the contrasting lines."
        ) as tracker:
            self.wait(tracker.duration)

        # Clear for next application
        self.play(*[mn.FadeOut(m) for m in self.mobjects], run_time=self.T_BRIEF)
        self.wait(self.T_SHORT)


def compute_pca_arrows(
    dots: mn.VGroup, scale1: float = 2.5, scale2: float = 1.2
) -> tuple:
    """Return (pc1_arrow, pc2_arrow, angle_of_pc1, singular_values)."""
    points = np.array([dot.get_center()[:2] for dot in dots])
    mean = points.mean(axis=0)
    centered = points - mean
    _, S, Vt = np.linalg.svd(centered, full_matrices=False)
    pc1_dir = Vt[0]
    pc2_dir = Vt[1]
    pc1 = mn.Arrow(
        mn.ORIGIN,
        np.append(pc1_dir * scale1, 0),
        color=theme.ACCENT2,
        buff=0,
        tip_length=0.18,
        stroke_width=5,
    )
    pc2 = mn.Arrow(
        mn.ORIGIN,
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
) -> mn.VGroup:
    """Build a heatmap VGroup from a 2-D numpy array, normalised to [0,1]."""
    grid = mn.VGroup()
    max_val = data.max() or 1
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            cell = mn.Square(cell_size)
            cell.set_fill(color, opacity=float(data[i, j]) / max_val)
            cell.set_stroke(width=0)
            cell.move_to(mn.RIGHT * j * cell_gap + mn.DOWN * i * cell_gap)
            grid.add(cell)
    grid.move_to(mn.ORIGIN)
    return grid


class SVDPCAApp(theme.ProjectVOScene):
    def construct(self):
        super().construct()
        # ══════════════════════════════════════════════════════════════════
        # APPLICATION 2 — PCA
        # ══════════════════════════════════════════════════════════════════

        pca_title = self.accent_text("Principal Component Analysis (PCA)", scale=0.65).to_corner(mn.UL)

        # Dot cloud: elongated ellipse rotated PI/6
        rng = np.random.default_rng(42)
        angle_val = mn.PI / 6
        dots = mn.VGroup()
        for _ in range(280):
            x = rng.normal(scale=2.0)
            y = rng.normal(scale=0.55)
            px = x * np.cos(angle_val) - y * np.sin(angle_val)
            py = x * np.sin(angle_val) + y * np.cos(angle_val)
            dots.add(mn.Dot(np.array([px, py, 0]), color=theme.ACCENT, radius=0.035, fill_opacity=0.7))

        pc1, pc2, pc_angle, _ = compute_pca_arrows(dots)
        center = dots.get_center()
        pc1.shift(center)
        pc2.shift(center)

        ellipse = mn.Ellipse(width=5.5, height=1.6, color=theme.ACCENT2, stroke_width=3)
        ellipse.rotate(pc_angle).move_to(center)

        pc1_label = mn.MathTex("PC_1", color=theme.ACCENT2).scale(0.65).next_to(pc1.get_end(), mn.DL, buff=0.3)
        pc2_label = mn.MathTex("PC_2", color=theme.ACCENT2).scale(0.65).next_to(pc2.get_end(), mn.DOWN, buff=0.3)

        dim_note = (
            self.body_text("largest singular value direction = most variance", scale=0.5)
            .set_color(theme.MUTED)
            .to_edge(mn.DOWN, buff=0.35)
        )

        with self.voiceover(
            text="Beyond images, SVD is the engine behind Principal Component Analysis — "
                 "or PCA — one of the most widely used tools in data science."
        ) as tracker:
            self.play(mn.FadeIn(pca_title), run_time=tracker.duration * 0.2)
            self.play(mn.FadeIn(dots), run_time=self.get_capped_run_time(tracker.duration * 0.8, self.T_LONG))

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
                mn.GrowArrow(pc1), mn.GrowArrow(pc2),
                mn.FadeIn(pc1_label), mn.FadeIn(pc2_label),
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
                mn.Create(ellipse),
                run_time=tracker.duration * 0.5,
            )
            self.play(mn.FadeIn(dim_note), run_time=tracker.duration * 0.3)
            self.wait(tracker.duration * 0.2)

        with self.voiceover(
            text="By projecting everything onto just the top two or three directions, "
                 "you can collapse that high-dimensional cloud into something you can plot and reason about, "
                 "while preserving as much structure as possible. "
                 "The dimensions it keeps are those with the largest singular values; "
                 "the ones it discards are the noise."
        ) as tracker:
            self.wait(tracker.duration)

        self.play(*[mn.FadeOut(m) for m in self.mobjects], run_time=self.T_BRIEF)
        self.wait(self.T_SHORT)


class SVDLSAApp(theme.ProjectVOScene):
    def construct(self):
        super().construct()
        # ══════════════════════════════════════════════════════════════════
        # APPLICATION 3 — Latent Semantic Analysis
        # ══════════════════════════════════════════════════════════════════

        lsa_title = self.accent_text("Latent Semantic Analysis (LSA)", scale=0.65).to_corner(mn.UL)

        # ── Term-document matrix ──────────────────────────────────────────
        raw_data = np.array([
            [5, 4, 0, 0],
            [3, 5, 0, 0],
            [4, 4, 1, 0],
            [0, 0, 3, 5],
            [0, 0, 4, 4],
        ])

        raw_grid = make_matrix_grid(raw_data, cell_size=0.5, cell_gap=0.62, color=theme.ACCENT)
        raw_grid.shift(mn.LEFT * 0.5 + mn.DOWN * 0.2)

        words = ["marathon", "sprint", "run", "feline", "cat"]
        docs  = ["D1", "D2", "D3", "D4"]
        rows_n, cols_n = raw_data.shape

        row_labels = mn.VGroup(*[
            self.body_text(word, scale=0.45).next_to(raw_grid[i * cols_n], mn.LEFT, buff=0.25)
            for i, word in enumerate(words)
        ])
        col_labels = mn.VGroup(*[
            self.body_text(doc, scale=0.45).next_to(raw_grid[j], mn.UP, buff=0.25)
            for j, doc in enumerate(docs)
        ])

        # Sigma result (middle step)
        sigma_tex = mn.MathTex(
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
        smooth_grid.shift(mn.LEFT * 0.5 + mn.DOWN * 0.2)

        # Highlight boxes for semantic clusters
        running_cells = mn.VGroup(*[cast(mn.VMobject, smooth_grid[i]) for i in [0, 1, 4, 5, 8, 9]])
        feline_cells  = mn.VGroup(*[cast(mn.VMobject, smooth_grid[i]) for i in [14, 15, 18, 19]])

        hl_running = mn.SurroundingRectangle(running_cells, color=theme.ACCENT2, stroke_width=2.5, buff=0.05)
        hl_feline  = mn.SurroundingRectangle(feline_cells,  color=theme.ACCENT2, stroke_width=2.5, buff=0.05)

        running_tag = self.body_text('"running"', scale=0.5).set_color(theme.ACCENT2).next_to(hl_running, mn.RIGHT, buff=0.2)
        feline_tag  = self.body_text('"feline"',  scale=0.5).set_color(theme.ACCENT2).next_to(hl_feline,  mn.RIGHT, buff=0.2)

        # Query illustration
        query_note = (
            self.body_text('query: "feline"  →  returns docs about cats', scale=0.5)
            .set_color(theme.MUTED)
            .to_edge(mn.DOWN, buff=0.35)
        )

        # ── Animate application 3 ─────────────────────────────────────────

        with self.voiceover(
            text="Perhaps the most counterintuitive application is in human language itself — "
                 "fabulously called Latent Semantic Analysis."
        ) as tracker:
            self.play(mn.FadeIn(lsa_title), run_time=tracker.duration * 0.2)
            self.play(
                mn.Create(raw_grid),
                mn.FadeIn(row_labels), mn.FadeIn(col_labels),
                run_time=self.get_capped_run_time(tracker.duration * 0.8, self.T_LONG),
            )

        with self.voiceover(
            text="What SVD tries to do here is uncover the hidden relationships between words and the concepts they represent."
        ) as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="In linguistics, we often deal with a term-document matrix where every row is a unique word, every column is a specific document, and each entry records how often that word appears."
        ) as tracker:
            self.wait(tracker.duration)

        with self.voiceover(
            text="The problem with these matrices is that they are incredibly messy. " \
                 "Language is full of synonyms (different words with the same meaning) and polysemy (the same word with different meanings), " \
                 "creating a noisy space where the computer sees two documents as unrelated just because they use different vocabulary to describe the same topic."
        ) as tracker:
            # Briefly flash the row labels to highlight the synonym problem
            self.play(
                mn.Indicate(row_labels[0], color=theme.ACCENT2),  # marathon
                mn.Indicate(row_labels[1], color=theme.ACCENT2),  # sprint
                mn.Indicate(row_labels[2], color=theme.ACCENT2),  # run
                run_time=self.get_capped_run_time(tracker.duration * 0.5, self.T_MEDIUM)
            )
            self.play(
                mn.Indicate(row_labels[3], color=theme.ACCENT2),  # feline
                mn.Indicate(row_labels[4], color=theme.ACCENT2),  # cat
                run_time=self.get_capped_run_time(tracker.duration * 0.5, self.T_MEDIUM)
            )

        with self.voiceover(
            text="By applying SVD to this matrix, we perform a sort of linguistic compression. "
            "Instead of seeing words as isolated units, it groups them into clusters based on where they appear. "
        ) as tracker:
            self.play(
                mn.ReplacementTransform(mn.VGroup(raw_grid, row_labels, col_labels), sigma_tex),
                run_time=self.get_capped_run_time(tracker.duration * 0.6, self.T_MEDIUM)
            )
            self.wait(tracker.duration * 0.4)

        with self.voiceover(
            text="Then, by keeping only the top k singular values, we effectively smooth the data. This ignores the minor, accidental word choices of an author and focuses on the primary semantic structure."
                 ""
        ) as tracker:
            self.play(
                mn.ReplacementTransform(sigma_tex, smooth_grid),
                run_time=tracker.duration * 0.5,
            )
            self.play(
                mn.FadeIn(row_labels), mn.FadeIn(col_labels),
                run_time=tracker.duration * 0.3,
            )
            self.wait(tracker.duration * 0.2)

        with self.voiceover(
            text="If marathon and sprint frequently appear in the same documents, SVD maps them to the same underlying concept of running."
        ) as tracker:
            self.play(mn.Create(hl_running), mn.FadeIn(running_tag), run_time=self.get_capped_run_time(tracker.duration * 0.6, self.T_MEDIUM))
            self.wait(tracker.duration * 0.4)

        with self.voiceover(
            text="We can now compare documents not by whether they share the exact same words, but by whether they share the same conceptual space. "
        ) as tracker:
            self.play(mn.Create(hl_feline), mn.FadeIn(feline_tag), run_time=self.get_capped_run_time(tracker.duration * 0.6, self.T_MEDIUM))
            self.wait(tracker.duration * 0.4)

        with self.voiceover(
            text="This allows a search engine to understand that a query for feline should return documents about cats, even if the word feline never appears in the text."
        ) as tracker:
            self.play(mn.FadeIn(query_note), run_time=tracker.duration * 0.3)
            self.wait(tracker.duration * 0.7)

        self.wait(0.5)

        # ── Closing thought ───────────────────────────────────────────────
        self.play(*[mn.FadeOut(m) for m in self.mobjects], run_time=self.T_BRIEF)


        with self.voiceover(
            text="It's a profound thought. The same geometric principle that describes how a circle turns into an ellipse "
                 "is the same principle that allows a computer to understand the underlying structure of human preferences, or the essence of a digital photograph. "
                 "SVD transforms a chaotic, high-dimensional world into a structured, geometric landscape where meaning is defined by semantic proximity, not just how they are presented."
        ) as tracker:
            self.wait(tracker.duration)

        self.wait(self.T_LONG)