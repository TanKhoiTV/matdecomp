# pip install manim-fonts
from manim import LinearTransformationScene, Matrix, Text, Scene
from typing import List, Any
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import inspect

# Palette
BG = "#F5F4EF"  # warm off-white
TEXT = "#1A1A2E"  # near-black navy, not pure black
ACCENT = "#2E7D6B"  # deep teal — primary highlight
ACCENT2 = "#C97B2A"  # warm amber — secondary, used sparingly
MUTED = "#6B6B6B"  # gray for labels and annotations
HIGHLIGHT = "#E8F4F1"  # very light teal for background fills


class ProjectScene(Scene):
    def setup(self) -> None:
        self.camera.background_color = BG  # type: ignore

    def accent_text(self, text: str, scale: float = 1.0) -> Text:
        return Text(text, font="Inter", color=ACCENT).scale(scale)

    def body_text(self, text: str, scale: float = 0.7) -> Text:
        return Text(text, font="Inter", color=TEXT).scale(scale)


class ProjectVOScene(VoiceoverScene, ProjectScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        VoiceoverScene.__init__(self, **kwargs)

    def setup(self) -> None:
        super().setup()
        self.set_speech_service(GTTSService())  # Standard service for prototyping


class ProjectLTVOScene(LinearTransformationScene, ProjectVOScene):
    def __init__(self, **kwargs):
        # for cls in type(self).__mro__:
        #     if hasattr(cls, 'setup') and 'setup' in cls.__dict__:
        #         print(cls.__name__, inspect.getsource(cls.setup))

        # print("MRO:", [c.__name__ for c in type(self).__mro__])
        # print("Before LT init")
        LinearTransformationScene.__init__(
            self,
            include_background_plane=True,
            include_foreground_plane=True,
            **kwargs
        )
        # print("Before VO init")
        VoiceoverScene.__init__(self, **kwargs)
        # print("After VO init, speech_service exists:", hasattr(self, 'speech_service'))

    def setup(self) -> None:
        # print("setup called, speech_service exists:", hasattr(self, 'speech_service'))
        super().setup()
        self.camera.background_color = BG  # type: ignore
        self.set_speech_service(GTTSService())
        # print("after super().setup(), speech_service exists:", hasattr(self, 'speech_service'))
        self.background_plane.set_opacity(0.5)

    def make_matrix(self, data: List[List[Any]], color: str = TEXT) -> Matrix:
        m = Matrix(data)
        m.set_color(color)
        return m
