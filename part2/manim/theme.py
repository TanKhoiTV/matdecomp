# pip install manim-fonts
from manim import LinearTransformationScene, Matrix, Text, Scene
from typing import List, Any
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover.services.pyttsx3 import PyTTSX3Service
from manim_voiceover.services.recorder import RecorderService

# Palette
BG = "#F5F4EF"  # warm off-white
TEXT = "#1A1A2E"  # near-black navy, not pure black
ACCENT = "#2E7D6B"  # deep teal — primary highlight
ACCENT2 = "#C97B2A"  # warm amber — secondary, used sparingly
MUTED = "#6B6B6B"  # gray for labels and annotations
HIGHLIGHT = "#E8F4F1"  # very light teal for background fills


VoiceService = RecorderService(silence_threshold=-40.0)


class ProjectScene(Scene):
    def setup(self) -> None:
        self.camera.background_color = BG  # type: ignore

    def accent_text(self, text: str, scale: float = 1.0) -> Text:
        return Text(text, font="Inter", color=ACCENT).scale(scale)

    def body_text(self, text: str, scale: float = 0.7) -> Text:
        return Text(text, font="Inter", color=TEXT).scale(scale)
    
    def get_capped_run_time(self, duration: float, limit: float) -> float:
        return min(duration, limit)
    
    # Time constants in seconds
    T_BRIEF = 0.5
    T_SHORT = 1
    T_MEDIUM = 2
    T_LONG = 4



class ProjectVOScene(VoiceoverScene, ProjectScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        VoiceoverScene.__init__(self, **kwargs)

    def setup(self) -> None:
        super().setup()
        self.set_speech_service(VoiceService)  # Standard service for prototyping


class ProjectLTVOScene(LinearTransformationScene, VoiceoverScene, ProjectScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        LinearTransformationScene.__init__(
            self,
            include_background_plane=True,
            include_foreground_plane=True,
            **kwargs
        )
        VoiceoverScene.__init__(self, **kwargs)

    def setup(self) -> None:
        super().setup()
        self.set_speech_service(VoiceService)
        self.background_plane.set_opacity(0.5)
        self.plane.get_axes().set_color(MUTED)

    def make_matrix(self, data: List[List[Any]], color: str = TEXT) -> Matrix:
        m = Matrix(data)
        m.set_color(color)
        return m
