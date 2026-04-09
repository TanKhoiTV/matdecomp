# Vocabulary

## Timing Relationships

Every cue must declare one of:
- `lead` — visual appears before the narration line begins.  Use when introducing a concept the narrator will then name.
- `sync` — visual appears as the narration line is spoken. Use when confirming something the audience already sees.
- `follow` — visual appears after the narration line ends. Use when the visual is the payoff of a buildup.
- `hold` — no new cue. The current visual stays. Use at transition phrases and after dense concepts.

## Duration Classes
- `instant` — cut, no animation (< 0.3s)
- `short` — 0.5 to 1 second
- `medium` — 1 to 2 seconds
- `long` — 2 to 4 seconds
- `breathe` — 4+ seconds, intentional pause for absorption

## Permitted Manim Objects
Use these names exactly as written:
- `NumberPlane` — coordinate grid, input/output space
- `Circle` — unit circle
- `Ellipse` — post-transformation shape
- `Arrow` / `Vector` — directional quantities, singular vectors
- `MathTex` — rendered LaTeX formula
- `Tex` — rendered plain text label
- `ImageMobject` — imported raster image (for compression demo)
- `Dot` — point in a scatter plot or data cloud
- `DashedLine` — projection lines, axis indicators
- `SurroundingRectangle` — highlight box around formula term
- `FadeIn` / `FadeOut` — entrance and exit
- `Transform` / `ReplacementTransform` — morphing one object into another
- `Write` — formula or text drawing in
- `Create` — geometric object drawing in
- `Indicate` — pulse highlight on existing object
- `ApplyMatrix` — applying a 2×2 matrix transform to a mobject
- `Rotate` — rotation animation

### Color Roles
Assign colors by role, not by preference:
- Input space objects: BLUE
- Output space objects: GREEN  
- Singular values / scaling: YELLOW
- Eigenvalues / diagonalization: RED
- Labels and annotations: WHITE
- Highlight / emphasis: ORANGE

---

# Decision Rules

**On timing:**
- A concept being _introduced for the first time_ → `lead`
- A concept being _confirmed after showing_ → `sync`
- A label being _named after its visual exists_ → `follow`
- Any narration containing "now," "next," "finally," "notice," or "this means" → insert `hold` before next cue
- After any cue rated `long` or `breathe` → next cue is at minimum `sync`, never `lead`

**On duration:**
- Pure geometric transformations (circle → ellipse, rotation) → `medium`
- Formula appearing for the first time → `long`
- Label appearing on existing object → `short`
- Transition between major sections → `breathe`
- Highlighting a term inside an existing formula → `short`

**On simultaneity:**
- Maximum two objects animating simultaneously
- Text and formula transforms never share a beat
- If in doubt, sequence rather than stack