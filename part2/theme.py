# pip install manim-fonts
from manim import LinearTransformationScene, Matrix, Text
from typing import List, Any
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

# Palette
BG = "#F5F4EF"  # warm off-white
TEXT = "#1A1A2E"  # near-black navy, not pure black
ACCENT = "#2E7D6B"  # deep teal — primary highlight
ACCENT2 = "#C97B2A"  # warm amber — secondary, used sparingly
MUTED = "#6B6B6B"  # gray for labels and annotations
HIGHLIGHT = "#E8F4F1"  # very light teal for background fills


class ProjectLTVOScene(LinearTransformationScene, VoiceoverScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            include_background_plane=True,
            include_foreground_plane=True,
            **kwargs
        )
        VoiceoverScene.__init__(self, **kwargs)

    def setup(self) -> None:
        super().setup()
        self.background_plane.set_opacity(0.5)
        self.camera.background_color = BG  # type: ignore
        self.set_speech_service(GTTSService())  # Standard service for prototyping

    def make_matrix(self, data: List[List[Any]], color: str = TEXT) -> Matrix:
        m = Matrix(data)
        m.set_color(color)
        return m

    def accent_text(self, text: str, scale: float = 1.0) -> Text:
        return Text(text, font="Inter", color=ACCENT).scale(scale)

    def body_text(self, text: str, scale: float = 0.7) -> Text:
        return Text(text, font="Inter", color=TEXT).scale(scale)


class ProjectVOScene(VoiceoverScene):
    def __init__(self, **kwargs):
        VoiceoverScene.__init__(self, **kwargs)

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = BG  # type: ignore
        self.set_speech_service(GTTSService())  # Standard service for prototyping

    def make_matrix(self, data: List[List[Any]], color: str = TEXT) -> Matrix:
        m = Matrix(data)
        m.set_color(color)
        return m

    def accent_text(self, text: str, scale: float = 1.0) -> Text:
        return Text(text, font="Inter", color=ACCENT).scale(scale)

    def body_text(self, text: str, scale: float = 0.7) -> Text:
        return Text(text, font="Inter", color=TEXT).scale(scale)
