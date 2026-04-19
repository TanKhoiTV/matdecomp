# SVD Video — Visual Reference Library

*For use by the Technical Creative Director agent.*
*Each entry includes source, reference type, and
extracted design decisions.*

---

## Section 1: Core Geometry (Unit Circle → Ellipse)

### REF-01: Sturluson Unit Circle / Ellipse Diagram

**Source:** surluson.github.io/blog/2021/01/11/visualizing-svd/
**Type:** Static image + Julia/matplotlib code
**Access:** Viewable at URL; code available in linked
  notebook

**Design Decisions to Extract:**

- Unit circle and output ellipse shown side-by-side
  in two subplots, not overlaid
- Circle is color-coded by position (continuous
  color gradient around circumference)
- Same color gradient is preserved on the ellipse,
  so the audience can visually track where each
  point on the circle lands after transformation
- Singular vectors shown as arrows from origin in
  both subplots, scaled to stop just before the
  circle/ellipse boundary
- No grid shown — clean white background with axes
  only

**Director's Note:** The color-continuity trick
(matching colors between circle and ellipse) is
the strongest design idea here. It makes the
transformation feel traceable rather than abstract.
Worth adopting for the Vᵀ → Σ → U pipeline.

---

### REF-02: Yuki Shizuya Medium Article Animations

**Source:** medium.com/intuition/the-mathematical-and-
  geographic-understanding-of-singular-value-
  decomposition-svd-8da2297797c6
**Type:** Embedded Manim animations (rendered video
  frames in article)
**Access:** Viewable at URL

**Design Decisions to Extract:**

- Shows eigendecomposition and SVD side-by-side
  as two parallel animation tracks — one basis
  vs. two bases
- Vᵀ rotation shown first in isolation before
  Σ scaling is introduced
- Arrow objects used for basis vectors, animated
  sequentially not simultaneously
- Formula terms highlighted with color as each
  matrix is introduced

**Director's Note:** This is the closest existing
reference to your Scene 1 pipeline. The
side-by-side layout for the SVD vs.
diagonalization comparison (your Scene 2) is
directly borrowed here. Animated, so key frames
need human description before agent can use them.

---

### REF-03: LinearTransformationScene — Manim

  Community Built-in
**Source:** docs.manim.community/en/stable/reference/
  manim.scene.vector_space_scene
  .LinearTransformationScene.html
**Type:** Manim documentation + code example

**Relevant Capabilities:**

- `apply_matrix(matrix)` animates the full
  NumberPlane deforming under a 2×2 matrix
- `leave_ghost_vectors=True` leaves faded copies
  of original vectors after transformation —
  useful for showing before/after
- `add_vector()` adds tracked vectors that
  transform with the plane
- `get_unit_square()` adds a unit square that
  deforms with the transformation

**Minimal Working Example:**

```python
class SVDScene(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
            **kwargs
        )
    def construct(self):
        matrix = [[1, 1], [0, 1]]
        self.apply_matrix(matrix)
        self.wait()
```

**Director's Note:** This is the correct base class
for Scene 1. The three-step SVD pipeline should
call `apply_matrix` three times sequentially —
once for Vᵀ, once for Σ, once for U — with
`hold` beats between each.

---

### REF-04: ApplyMatrix Animation

**Source:** docs.manim.community/en/stable/reference/
  manim.animation.transform.ApplyMatrix.html
**Type:** Manim documentation + code example

**Relevant Capabilities:**

- Applies a matrix transform to any individual
  mobject (not just the full plane)
- Can be applied to Circle object directly to
  animate the deformation step by step
- `about_point` parameter controls the origin
  of transformation

**Minimal Working Example:**

```python
class ApplyMatrixExample(Scene):
    def construct(self):
        matrix = [[1, 1], [0, 2/3]]
        self.play(
            ApplyMatrix(matrix, Circle()),
            ApplyMatrix(matrix, NumberPlane())
        )
```

**Director's Note:** Use `ApplyMatrix` on the
Circle object directly for the SVD pipeline
rather than `apply_matrix` on the scene, because
you need to pause and add narration between each
of the three steps. `apply_matrix` transforms
everything at once.

---

## Section 2: SVD vs. Diagonalization

### REF-05: Alyssa SVD Visualisation

**Source:** alyssaq.github.io/2015/singular-value-
  decomposition-visualisation/
**Type:** Static plots + numpy code

**Design Decisions to Extract:**

- Shows transformation of a specific set of
  points (not a continuous circle) under
  each matrix step
- Rotation and scaling annotated separately
  with labeled axes
- Key mathematical properties verified
  numerically alongside visual (dot product
  = 0, column norms = 1)

**Extracted Property Table (useful for
  annotation overlays):**

| Property | Diagonalization | SVD |
| ---------- | ----------------- | ----- |
| Matrix shape | Square only | Any |
| Input basis | Eigenvectors (P) | Right singular vectors (V) |
| Output basis | Same as input | Left singular vectors (U) |
| Diagonal values | Eigenvalues (can be complex) | Singular values (always real, non-negative) |
| Basis orthogonal? | Not always | Always |

**Director's Note:** This property table is
the basis for the side-by-side comparison
visual in Scene 2. Consider a two-column
layout with the table appearing row by row
as each property is narrated.

---

## Section 3: Applications

### REF-06: Stansbury Singular Value Decay Chart

**Source:** dustinstansbury.github.io/theclevermachine/
  svd-data-compression
**Type:** Static chart (matplotlib)

**Design Decisions to Extract:**

- Two-panel figure: left panel shows singular
  values (blue) and their log (red) vs. rank k;
  right panel shows cumulative information
  encoded vs. rank k
- Singular values plotted on y-axis, rank index
  on x-axis — exponential decay curve is the
  key visual
- Cumulative curve shows rapid early rise
  (most information in first few components)
  then flattening

**Manim Implementation Path:**
Recreate using `Axes` + `Graph` objects. The
decay curve can be generated from actual SVD
of a sample image using numpy, then plotted
as a parametric curve. The cumulative panel
can be a second `Axes` object placed to the
right.

**Director's Note:** This chart is the
conceptual justification for why truncation
works. It should appear before the
rank-k reconstruction sequence, not after.
Show the curve, establish that most
information lives in early components, then
show what happens when you keep only those.

---

### REF-07: Rank-k Reconstruction Sequence

**Source:** dustinstansbury.github.io/theclevermachine/
  svd-data-compression + github.com/Tornadosky/
  svd-image-compression
**Type:** Static image grids (matplotlib output)

**Design Decisions to Extract:**

- Standard sequence: k=1, k=5, k=10, k=20,
  k=50 shown as progression
- Grayscale image preferred over color for
  first demonstration (simpler matrix,
  one channel)
- Each reconstruction labeled with k value
  and compression ratio

**Manim Implementation Path:**
Generate reference frames in Python using
numpy SVD on a chosen grayscale image.
Import each frame as `ImageMobject`. Animate
as a sequence of `Transform` or `FadeIn`
replacements with k label updating via
`ReplacementTransform` on a `MathTex` object.

**JPEG Caveat (for script honesty):**
SVD is not used in production image formats.
JPEG uses discrete cosine transform, which
operates on the same principle of discarding
high-frequency components. One sentence
acknowledgment is sufficient.

**Director's Note:** Choose a photograph
with strong edges and clear large-scale
structure — a face or a building works
better than a landscape because the k=1
reconstruction is more recognizably related
to the original.

---

### REF-08: VanderPlas PCA Scatter Plot

**Source:** jakevdp.github.io/PythonDataScienceHandbook/
  05.09-principal-component-analysis.html
**Type:** Static matplotlib plot + Python code

**Design Decisions to Extract:**

- 2D scatter plot of ~200 points with clear
  elongated distribution (not circular)
- Two principal component vectors shown as
  arrows from the data centroid
- Arrow length scaled to explained variance
  (longer arrow = more variance = more
  important component)
- Points colored uniformly — the structure
  comes from position, not color

**Manim Implementation Path:**
Generate point positions in Python using
numpy (correlated Gaussian), import
coordinates, render each point as a `Dot`.
Principal component arrows drawn as `Arrow`
objects from centroid. Animate arrows
appearing after scatter plot is established.

**Ellipse Echo Opportunity:**
After showing the two PC arrows, optionally
overlay a `DashedLine` ellipse fitted to
the point cloud. This visually connects
the PCA scatter plot back to the unit circle
→ ellipse metaphor from Scene 1 — the data
cloud forms an ellipse, and SVD finds its axes.

**Director's Note:** The ellipse overlay is
the most important visual in the PCA section
because it closes the geometric loop. Time
it to appear exactly when the narration says
"the principal components are exactly the
axes of the ellipse your data cloud forms."

---

### REF-09: LSA Term-Document Matrix Visual

**Source:** No direct Manim asset found. Design
  from first principles.
**Type:** Original design required

**Recommended Visual Approach:**
A simplified 5×4 term-document matrix shown
as a colored grid (heatmap style), where:

- Rows = words (labeled: "marathon," "sprint,"
  "run," "feline," "cat")
- Columns = documents (labeled D1–D4)
- Cell color intensity = frequency (darker =
  more frequent)
- Implemented as a VGroup of Rectangle objects
  with opacity scaled to value

**Transformation Sequence:**

1. Show full noisy matrix (all words,
   varying frequencies)
2. Apply SVD — animate Σ with small values
   fading to zero
3. Show reconstructed matrix — "marathon"
   and "sprint" rows now visually similar
   (same color pattern)
4. Highlight similarity with a
   SurroundingRectangle across both rows

**Semantic Space Alternative:**
If the matrix approach feels too algebraic,
an alternative is a 2D semantic space scatter
plot with word labels as Dot + Tex pairs.
Cluster proximity shows conceptual grouping.
Easier to animate but less directly connected
to the SVD machinery.

**Director's Note:** Decide between matrix
view and semantic space view before
animating — they require different scene
setups and cannot be easily swapped late
in production. The matrix view is more
honest to the mathematics; the semantic
space view is more surprising and
memorable for a general audience.

---

### REF-10: Casey Li PCA-with-Manim Article

**Source:** medium.com/@sometimescasey/pca-visualized-
  for-human-beings-47d19a122734
**Type:** Article with embedded Manim-fork animations

**Design Decisions to Extract:**

- Uses image data rather than scatter plots
  for PCA demonstration (MNIST digits)
- Shows eigenvectors as visual basis images
  (what each component "looks like" as an image)
- Reconstruction sequence mirrors the image
  compression rank-k sequence

**Director's Note:** The image-based PCA
approach is more visually striking than
the scatter plot but requires more setup.
Only pursue if production timeline allows.
The scatter plot from REF-08 is sufficient
and more consistent with the script's
existing framing.

---

## Quick Reference: Implementation Risk by Scene

| Scene | Reference | Risk Level | Reason |
| ------- | ----------- | ------------ | -------- |
| Unit circle → ellipse | REF-01, REF-03, REF-04 | Low | Built-in Manim support |
| SVD pipeline (3 steps) | REF-04 | Low | Sequential ApplyMatrix calls |
| SVD vs. diagonalization | REF-02, REF-05 | Medium | Side-by-side layout needs care |
| Singular value decay chart | REF-06 | Low | Standard Axes + Graph |
| Rank-k image reconstruction | REF-07 | Low | ImageMobject sequence |
| PCA scatter + arrows | REF-08 | Low | Dot array + Arrow |
| PCA ellipse overlay | REF-08 | Low | Ellipse + DashedLine |
| LSA matrix heatmap | REF-09 | Medium | Custom Rectangle grid |
| LSA semantic space | REF-09 | Low | Dot + Tex scatter |

---

## Version Note

All Manim code references target **Manim Community
Edition v0.18+**. Verify version before use. Do not
mix with ManimGL syntax — the two versions are
incompatible and fail silently in some cases.
