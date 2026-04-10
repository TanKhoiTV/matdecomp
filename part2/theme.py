# pip install manim-fonts
from manim import Scene, Matrix, Text, Color # type: ignore
from typing import List, Any

# Palette
BG        = '#F5F4EF'   # warm off-white
TEXT      = '#1A1A2E'   # near-black navy, not pure black
ACCENT    = '#2E7D6B'   # deep teal — primary highlight
ACCENT2   = '#C97B2A'   # warm amber — secondary, used sparingly
MUTED     = '#6B6B6B'   # gray for labels and annotations
HIGHLIGHT = '#E8F4F1'   # very light teal for background fills

class ProjectScene(Scene):
    def setup(self) -> None:
        self.camera.background_color = BG # type: ignore

    def make_matrix(self, data: List[List[Any]], color: str = TEXT) -> Matrix:
        m = Matrix(data)
        m.set_color(color)
        return m

    def accent_text(self, text: str, scale: float = 1.0) -> Text:
        return Text(text, font='IBM Plex Sans',
                    color=ACCENT).scale(scale)

    def body_text(self, text: str, scale: float = 0.7) -> Text:
        return Text(text, font='IBM Plex Sans',
                    color=TEXT).scale(scale)
