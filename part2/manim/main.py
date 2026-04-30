# Render: manim -q[quality: l, m, h] final_render.py --disable_caching
# To render all scenes: manim -pql final_render.py -a

from typing import Tuple, cast, List
import manim as mn
import numpy as np
from pathlib import Path

# Assuming your theme.py contains ProjectLTVOScene and ProjectVOScene
import theme 

# --- SECTION 1: DIAGONALIZATION & THE "WHY" ---

class DiagonalizationIntro(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()
        # [Insert logic from your DiagonalizationIntro source]
        # (Fades in plane, shows eigenvectors, explains A = PDP⁻¹)

class RotationFailure(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()
        # [Insert logic from your RotationFailure source]
        # (Shows the Pikachu image and the failure of rotation matrices to diagonalize)

class SVDIntroductionBridge(theme.ProjectVOScene):
    def construct(self):
        super().construct()
        # [Insert logic from your SVDIntroductionBridge source]
        # (Visualizes SVD as the "Master Key" vs the "Specialized Tool")

# --- SECTION 2: THE GEOMETRY OF SVD ---

class SVDGeometry(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()
        # [Insert logic from your SVDGeometry source]
        # (Visualizes the unit circle transforming into an ellipse)

class SVDBreakdown(theme.ProjectLTVOScene):
    def construct(self):
        super().construct()
        # [Insert logic from your SVDBreakdown source]
        # (Detailed Vᵀ, Σ, and U step-by-step breakdown)

# --- SECTION 3: TECHNICAL CAVEATS ---

class ComputationSideNote(theme.ProjectVOScene):
    def construct(self):
        super().construct()
        # [Insert logic from your ComputationSideNote source]
        # (Explains symmetry, iterative algorithms, and numerical stability)