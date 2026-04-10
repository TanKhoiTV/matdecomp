from typing import Tuple, Sequence, List, cast
from manim import (
    Scene, VGroup, Line, Circle, Vector, NumberPlane, 
    DashedLine, Tex, MathTex, Arrow, Rectangle, 
    ImageMobject, Axes, Dot, Ellipse, Text, Square, 
    SurroundingRectangle, Create, FadeIn, FadeOut, 
    ApplyMatrix, Rotate, ReplacementTransform, Indicate, 
    interpolate_color, config, Write, Transform, VMobject, VGroup,
    BLUE, GREEN, RED, WHITE, YELLOW, ORANGE, GREY, 
    TAU, PI, ORIGIN, LEFT, RIGHT, UP, DOWN, UR
)
from manim.utils.color import ManimColor, ParsableManimColor
import numpy as np

config.media_width = "75%"
config.verbosity = "WARNING"

def create_gradient_circle(radius: float = 1.0, n_segments: int = 100) -> VGroup:
    segments = VGroup()

    for i in range(n_segments):
        t1 = i / n_segments
        t2 = (i + 1) / n_segments

        theta1 = TAU * t1
        theta2 = TAU * t2

        p1 = np.array([np.cos(theta1), np.sin(theta1), 0]) * radius
        p2 = np.array([np.cos(theta2), np.sin(theta2), 0]) * radius

        color = interpolate_color(BLUE, GREEN, t1)

        segment = Line(p1, p2, color=color)
        segments.add(segment)

    return segments

class SVDIntro(Scene):
    def construct(self) -> None:
        plane = NumberPlane(
            background_line_style={
                "stroke_opacity": 0.3
            }
        )
        
        circle = create_gradient_circle()
        
        self.plane = plane
        self.circle = circle

        # CUE 01
        self.play(Create(plane), run_time=1.5)
        self.play(Create(circle), run_time=1.5)
        self.wait()

        # CUE 02
        v1 = Vector(np.array([2, 0, 0]), color=RED)
        v2 = Vector(np.array([0, 2, 0]), color=RED)

        self.play(Create(v1), Create(v2), run_time=0.8)
        self.wait()

        # CUE 03
        A = np.array([[1.5, 0.5], [0.5, 1.2]])

        self.play(ApplyMatrix(A, VGroup(plane, circle)), run_time=1.5)

        plane.set_color(GREEN)
        circle.set_color(GREEN)

        self.wait()

        self.play(FadeOut(v1, v2))
        self.play(FadeOut(plane), FadeOut(circle))

        plane = NumberPlane(
            background_line_style={
                "stroke_opacity": 0.3
            }
        )
        circle = Circle(color=BLUE)

        self.play(FadeIn(plane), FadeIn(circle))
        
        # CUE 04
        target_axes = DashedLine(LEFT * 3, RIGHT * 3, color=WHITE)
        target_axes.set_opacity(0.5)

        self.play(Create(target_axes), run_time=1)

        self.play(Rotate(VGroup(plane, circle), angle=PI/6), run_time=1.5)
        self.wait()

        # CUE 05
        sigma = np.array([[2, 0], [0, 0.5]])

        self.play(ApplyMatrix(sigma, circle), run_time=1.5)
        self.play(plane.animate.set_opacity(0.2), run_time=0.5)

        self.wait()

        # CUE 06
        sigma_label = Tex(r"$\sigma_1, \sigma_2$", color=YELLOW)
        sigma_label.next_to(circle, RIGHT * 1.5)

        self.play(FadeIn(sigma_label), run_time=0.6)
        self.wait()

        # CUE 07
        self.play(Rotate(circle, angle=-PI/8), run_time=1.5)

        circle.set_color(GREEN)
        self.wait()

        # CUE 08
        self.wait(4)

        # CUE 09
        pdp = MathTex("A = PDP^{-1}", color=WHITE).to_corner(UR)

        self.play(Write(pdp), run_time=1.5)
        self.wait()

        # CUE 10
        svd = MathTex("A = U \\Sigma V^T", substrings_to_isolate=["\\Sigma"]).to_corner(UR)
        svd.set_color_by_tex("\\Sigma", YELLOW)

        self.play(ReplacementTransform(pdp, svd), run_time=1.5)
        self.wait()

        # CUE 11
        ata = MathTex("A^T A", color=WHITE)
        aat = MathTex("AA^T", color=WHITE)

        group = VGroup(ata, aat).arrange(RIGHT, buff=1)
        group.next_to(svd, DOWN)

        self.play(FadeIn(group), run_time=0.8)
        self.wait()

        # CUE 12
        self.play(
            Indicate(ata, color=ORANGE),
            Indicate(aat, color=ORANGE),
            run_time=0.8
        )
        self.wait()

def right_angle_marker(center: np.ndarray, size: float = 0.2, color: ParsableManimColor = WHITE) -> VGroup:
    return VGroup(
        Line(center, center + RIGHT * size, color=color),
        Line(center + RIGHT * size, center + RIGHT * size + UP * size, color=color),
        Line(center + RIGHT * size + UP * size, center + UP * size, color=color),
    )

class SVDComparisionScene(Scene):
    def construct(self) -> None:
        LEFT_POS = LEFT * 3.5
        RIGHT_POS = RIGHT * 3.5

        plane_L = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.4}
        ).scale(0.7).set_opacity(0.85).shift(LEFT_POS)
        plane_R = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.4}
        ).scale(0.7).set_opacity(0.85).shift(RIGHT_POS)

        plane_L.set_color(BLUE)
        plane_R.set_color(GREEN)

        label_L = Tex("Input space ($V$)", color=BLUE).next_to(plane_L, UP)
        label_R = Tex("Output space ($U$)", color=GREEN).next_to(plane_R, UP)

        # CUE 13
        self.play(
            FadeIn(plane_L),
            FadeIn(plane_R),
            run_time=1.5
        )
        self.play(FadeIn(label_L), FadeIn(label_R), run_time=0.8)
        self.wait()

        # CUE 14
        pdp = MathTex("A = PDP^{-1}", color=WHITE).to_edge(UP)
        self.play(Write(pdp), run_time=0.8)
        self.wait()

        # CUE 15
        v1_L = Vector(np.array([2, 0]), color=RED).shift(LEFT_POS)
        v2_L = Vector(np.array([0, 2]), color=RED).shift(LEFT_POS)

        v1_R = Vector(np.array([2, 0]), color=RED).shift(RIGHT_POS)
        v2_R = Vector(np.array([0, 2]), color=RED).shift(RIGHT_POS)

        self.play(
            Create(v1_L), Create(v2_L),
            Create(v1_R), Create(v2_R),
            run_time=0.8
        )
        self.wait()

        ghost_v1_L = v1_L.copy().set_opacity(0.5)
        ghost_v2_L = v2_L.copy().set_opacity(0.5)
        ghost_v1_R = v1_R.copy().set_opacity(0.5)
        ghost_v2_R = v2_R.copy().set_opacity(0.5)

        self.add(ghost_v1_L, ghost_v2_L, ghost_v1_R, ghost_v2_R)

        # CUE 16
        self.play(
            Rotate(
                VGroup(v1_L, v2_L),
                angle=PI / 2,
                about_point=plane_L.get_center()
            ),
            run_time=1.5
        )

        # CUE 17
        right_group = VGroup(plane_R, v1_R, v2_R)

        # self.play(
        #     # VGroup(v1_R, v2_R).animate.apply_matrix(plane_R, rot, about_point=RIGHT_POS),
        #     right_group.animate.rotate(90 * DEGREES, about_point=RIGHT_POS),
        #     run_time=1.5
        # )
        # self.wait()

        self.play(
            Rotate(
                VGroup(v1_R, v2_R),
                angle=PI / 2,
                about_point=plane_R.get_center()
            ),
            run_time=1.5
        )

        # CUE 18
        svd = MathTex(
            "A = U \\Sigma V^T",
            substrings_to_isolate=["\\Sigma"]
        ).to_edge(UP)
        svd.set_color_by_tex("\\Sigma", YELLOW)

        self.play(ReplacementTransform(pdp, svd), run_time=0.8)
        self.wait()

        self.play(
            FadeOut(v1_L), FadeOut(v2_L),
            FadeOut(v1_R), FadeOut(v2_R)
        )
        self.wait()

        # CUE 19
        vectors_L = VGroup(
            Vector(np.array([2, 0]), color=BLUE),
            Vector(np.array([0, 2]), color=BLUE)
        ).shift(plane_L.get_center())
        
        v1_L, v2_L = vectors_L

        vectors_R = VGroup(
            Vector(np.array([1.5, 0]), color=GREEN),
            Vector(np.array([0, 1]), color=GREEN)
        ).shift(plane_R.get_center())

        u1_R, u2_R = vectors_R

        self.play(Create(vectors_L), Create(vectors_R), run_time=1.5)
        self.wait()

        marker_L = right_angle_marker(plane_L.get_center(), color=BLUE)
        marker_R = right_angle_marker(plane_R.get_center(), color=GREEN)

        self.play(Create(marker_L), Create(marker_R), run_time=0.8)
        self.wait()

        label_v = Tex("$v_1, v_2$", color=BLUE).next_to(plane_L, DOWN)
        label_u = Tex("$u_1, u_2$", color=GREEN).next_to(plane_R, DOWN)

        self.play(FadeIn(label_v), FadeIn(label_u))
        self.wait()

        # CUE 20
        sym = MathTex("A = A^T", color=ORANGE).next_to(svd, DOWN)
        self.play(FadeIn(sym), run_time=0.8)
        self.wait()

        # CUE 21
        box = SurroundingRectangle(svd, color=ORANGE)
        self.play(Create(box), run_time=0.8)
        self.wait()

        # CUE 22
        self.play(
            Transform(
                v1_L,
                u1_R.copy().set_color(WHITE).shift(plane_L.get_center() - plane_R.get_center())
            ),
            Transform(
                v2_L,
                u2_R.copy().set_color(WHITE).shift(plane_L.get_center() - plane_R.get_center())
            ),
            run_time=1.5
        )
        self.wait()

        # CUE 23
        mn = MathTex(r"m \times n \text{ matrix}", color=WHITE).to_edge(DOWN)
        self.play(FadeIn(mn), run_time=0.8)
        self.wait()

def create_tail_region(axes: Axes, k: float, x_max: float = 50, y_max: float = 5, color: ParsableManimColor = GREY) -> Rectangle:
    left = axes.c2p(k, 0)
    right = axes.c2p(x_max, y_max)

    width = right[0] - left[0]
    height = right[1] - left[1]

    rect = Rectangle(
        width=width,
        height=height,
        fill_color=color,
        fill_opacity=0.2,
        stroke_width=0
    )

    rect.move_to((
        left[0] + width / 2,
        left[1] + height / 2,
        0
    ))

    return rect

def compute_pca_arrows(dots: VGroup, scale1: float = 3, scale2: float = 2) -> Tuple[Arrow, Arrow, float, np.ndarray]:
    points = np.array([dot.get_center()[:2] for dot in dots])

    mean = points.mean(axis=0)
    centered = points - mean

    U, S, VT = np.linalg.svd(centered)

    pc1_direction = VT[0]
    pc2_direction = VT[1]

    pc1 = Arrow(
        ORIGIN,
        np.array([pc1_direction[0], pc1_direction[1], 0]) * scale1,
        color=YELLOW,
        buff=0,
        tip_length=0.15,
        stroke_width=5
    )

    pc2 = Arrow(
        ORIGIN,
        np.array([pc2_direction[0], pc2_direction[1], 0]) * scale2,
        color=YELLOW,
        buff=0,
        tip_length=0.15,
        stroke_width=5
    )

    angle = np.float64(np.arctan2(pc1_direction[1], pc1_direction[0]))

    return pc1, pc2, angle, S

class SVDApplicationScene(Scene):
    def construct(self) -> None:
        # CUE 24
        sigma_tex = r"\Sigma = \begin{bmatrix} 5 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 0.2 \end{bmatrix}"
        sigma = MathTex(
            sigma_tex,
            substrings_to_isolate=["0.2"],
            color=YELLOW
        )
        self.play(Write(sigma), run_time=2)

        small_value = sigma.get_part_by_tex("0.2")

        if small_value != None:
            self.play(small_value.animate.set_opacity(0.2), run_time=1)
        self.wait()
        self.play(FadeOut(sigma))
        self.wait()

        # CUE 25
        img = ImageMobject("img/base.png").scale(1.25).to_edge(LEFT)
        self.play(FadeIn(img))
        self.wait()

        # CUE 26
        axes = Axes(
            x_range=[0, 50],
            y_range=[0, 5],
        ).scale(0.5).to_edge(RIGHT)

        graph = axes.plot(lambda x: 5 * np.exp(-0.1 * x), color=YELLOW)

        self.play(Create(axes), Create(graph))
        self.wait()

        # CUE 27
        cut = DashedLine(axes.c2p(20, 0), axes.c2p(20, 5), color=ORANGE)
        self.play(Create(cut))
        self.wait()
        self.play(FadeOut(cut))
        self.wait()

        # CUE 28
        k1 = ImageMobject("img/k-1.png").scale(1.25).to_edge(LEFT)
        k10 = ImageMobject("img/k-10.png").scale(1.25).to_edge(LEFT)
        k50 = ImageMobject("img/k-50.png").scale(1.25).to_edge(LEFT)

        cut = DashedLine(axes.c2p(1, 0), axes.c2p(1, 5), color=ORANGE)
        tail = create_tail_region(axes, k=1)

        self.play(
            Create(cut),
            Transform(img, k1),
            FadeIn(tail),
            run_time=1.5
        )
        self.wait(1)

        new_tail = create_tail_region(axes, k=10)
        self.play(
            Transform(tail, new_tail),
            cut.animate.put_start_and_end_on(
                axes.c2p(10, 0),
                axes.c2p(10, 5)
            ),
            Transform(img, k10),
            run_time=1.8          
        )
        self.wait(1)

        new_tail = create_tail_region(axes, k=50)
        self.play(
            Transform(tail, new_tail),
            cut.animate.put_start_and_end_on(
                axes.c2p(50, 0),
                axes.c2p(50, 5)
            ),
            Transform(img, k50),
            run_time=1.2
        )
        self.wait(1)
        
        # CUE 29
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()

        # CUE 30
        dots = VGroup()
        angle_val = PI / 6

        for _ in range(300):
            x = np.random.normal(scale=2.0)
            y = np.random.normal(scale=0.5)

            point = np.array([
                x * np.cos(angle_val) - y * np.sin(angle_val),
                x * np.sin(angle_val) + y * np.cos(angle_val),
                0
            ])

            dots.add(Dot(point, color=BLUE, radius=0.04))
        
        self.play(FadeIn(dots), run_time=1.5)
        self.wait()

        # CUE 31
        pc1, pc2, final_angle, S = compute_pca_arrows(dots)

        center = dots.get_center()
        pc1.shift(center)
        pc2.shift(center)

        group = VGroup(pc1, pc2)

        self.play(Create(group), run_time=1.5)
        self.wait() 

        # CUE 32
        ellipse = Ellipse(
            width=5,
            height=1.5,
            color=ORANGE,
            stroke_width=4
        )

        ellipse.rotate(final_angle)
        ellipse.move_to(center)

        self.play(
            dots.animate.set_opacity(0.75),
            FadeIn(ellipse),
            run_time=1.5
        )
        self.wait()

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

        # CUE 33
        data = np.array([
            [5, 4, 0, 0],
            [3, 5, 0, 0],
            [4, 4, 1, 0],
            [0, 0, 3, 5],
            [0, 0, 4, 4],
        ])

        max_val = data.max()
        grid = VGroup()
        rows, cols = data.shape

        for i in range(rows):
            for j in range(cols):
                val = data[i, j] / max_val
                cell = Square(0.5)
                cell.set_fill(BLUE, opacity=val)
                cell.set_stroke(width=0)
                cell.move_to(RIGHT * j * 0.6 + DOWN * i * 0.6)
                grid.add(cell)
        
        grid.move_to(ORIGIN)
        words = ["marathon", "sprint", "run", "feline", "cat"]
        row_labels = VGroup(*[
            Text(word, font_size=24).next_to(grid[i * cols], LEFT, buff=0.3)
            for i, word in enumerate(words)
        ])

        docs = ["D1", "D2", "D3", "D4"]
        col_labels = VGroup(*[
            Text(doc, font_size=24).next_to(grid[j], UP, buff=0.3)
            for j, doc in enumerate(docs)
        ])

        self.play(Create(grid), FadeIn(row_labels), FadeIn(col_labels), run_time=1.5)
        self.wait()

        # CUE 34
        sigma_matrix = r"\Sigma = \begin{bmatrix} 5 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 0.5 \end{bmatrix}"
        sigma_res = MathTex(sigma_matrix, color=YELLOW).scale(1.2)
        sigma_res.move_to(ORIGIN)

        matrix_group = VGroup(grid, row_labels, col_labels)
        self.play(ReplacementTransform(matrix_group, sigma_res), run_time=2)
        self.wait()

        # CUE 35
        smooth_data = np.array([
            [5, 4, 0, 0],
            [4, 5, 0, 0],
            [4, 4, 1, 0],
            [0, 0, 4, 5],
            [0, 0, 5, 4],
        ])

        max_val_smooth = smooth_data.max()
        smooth_grid = VGroup()
        s_rows, s_cols = smooth_data.shape

        for i in range(s_rows):
            for j in range(s_cols):
                val = smooth_data[i, j] / max_val_smooth
                cell = Square(0.5)
                cell.set_fill(GREEN, opacity=val)
                cell.set_stroke(width=0)
                cell.move_to(RIGHT * j * 0.6 + DOWN * i * 0.6)
                smooth_grid.add(cell)

        smooth_grid.move_to(ORIGIN)

        self.play(FadeOut(sigma_res), FadeIn(smooth_grid), run_time=1.5)
        self.wait()

        # CUE 36
        self.play(FadeIn(row_labels), FadeIn(col_labels), run_time=1)

        running_group = VGroup(*[
            cast(VMobject, smooth_grid[i]) for i in [0, 1, 4, 5, 8, 9]
        ])

        cat_group = VGroup(*[
            cast(VMobject, smooth_grid[i]) for i in [14, 15, 18, 19]
        ])

        highlight1 = SurroundingRectangle(running_group, color=ORANGE, stroke_width=3)
        highlight2 = SurroundingRectangle(cat_group, color=ORANGE, stroke_width=3)

        self.play(Create(highlight1), run_time=1)
        self.wait()
        self.play(Create(highlight2), run_time=1)
        self.wait()