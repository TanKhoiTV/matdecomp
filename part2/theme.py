# pip install manim-fonts

from manim import * # type: ignore

# Palette — do not use 3B1B default blues/yellows
BG        = '#F5F4EF'   # warm off-white
TEXT      = '#1A1A2E'   # near-black navy, not pure black
ACCENT    = '#2E7D6B'   # deep teal — primary highlight
ACCENT2   = '#C97B2A'   # warm amber — secondary, used sparingly
MUTED     = '#6B6B6B'   # gray for labels and annotations
HIGHLIGHT = '#E8F4F1'   # very light teal for background fills

class ProjectScene(Scene):
    def setup(self):
        self.camera.background_color = BG # type: ignore

    def make_matrix(self, data, color=TEXT):
        m = Matrix(data)
        m.set_color(color)
        return m

    def accent_text(self, text, scale=1.0):
        return Text(text, font='IBM Plex Sans',
                    color=ACCENT).scale(scale)

    def body_text(self, text, scale=0.7):
        return Text(text, font='IBM Plex Sans',
                    color=TEXT).scale(scale)