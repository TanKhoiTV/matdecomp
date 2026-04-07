---
name: SVD Cue Sheet - Draft #2
description: Second draft of the cue sheet for the video explaining SVD, addressing most structural changes. Animator use this sheet directly. For any question, ask the Creative Director.
notes: See `svd-animation-refs.md` for ordered list of references.
---

# Section 1: The Geometry of SVD

[CUE 01]
Narration trigger: "Every linear transformation, no matter how complex, is secretly just a few simple moves in disguise."
Timing: lead
Object(s): NumberPlane → Create, Circle → Create
Color: BLUE
Duration: medium
Camera: static
Notes: Establish the standard 2D input space. The NumberPlane should be subtle to ensure the unit circle is the focal point.
[/CUE]

[CUE 02]
Narration trigger: "looking for the 'special' directions... which we called eigenvectors."
Timing: sync
Object(s): Vector → Create (two spanning arrows)
Color: RED
Duration: short
Camera: static
Notes: Two static eigenvectors appear on the circle. Do not animate the shear yet to avoid overloading the visual introduction.
[/CUE]

[CUE 03]
Narration trigger: "stretches and tilts into an ellipse in the output space."
Timing: sync
Object(s): ApplyMatrix (Circle → Ellipse), NumberPlane → ApplyMatrix
Color: GREEN
Duration: medium
Camera: static
Notes: The space transforms smoothly. The BLUE grid lines and circle morph into a GREEN tilted ellipse.
[/CUE]

[CUE 04]
Narration trigger: "1. V-transpose (Rotation in the input space):"
Timing: lead
Object(s): Rotate (NumberPlane, Circle)
Color: BLUE
Duration: medium
Camera: static
Notes: Show the original unit circle spinning. Use DashedLine to show the "target" axes that will eventually align with the ellipse.
[/CUE]

[CUE 05]
Narration trigger: "2. Sigma (Scaling):"
Timing: sync
Object(s): Circle → Transform (Ellipse)
Color: YELLOW
Duration: medium
Camera: static
Notes: The circle stretches along the target axes. The scaling happens along the orthogonal vectors identified in the previous step.
[/CUE]

[CUE 06]
Narration trigger: "called the singular values."
Timing: follow
Object(s): Tex("$\sigma\_1, \sigma\_2$") → FadeIn
Color: YELLOW
Duration: short
Camera: static
Notes: Labels appear at the tips of the ellipse semi-axes.
[/CUE]

[CUE 07]
Narration trigger: "3. U (Rotation in the output space):"
Timing: sync
Object(s): Rotate (Ellipse)
Color: GREEN
Duration: medium
Camera: static
Notes: The scaled ellipse tilts into its final orientation in the GREEN output space.
[/CUE]

[CUE 08]
Narration trigger: "This flexibility is exactly why SVD works for every single matrix in existence."
Timing: hold
Object(s): none
Color: n/a
Duration: breathe
Camera: static
Notes: Pause on the final tilted GREEN ellipse. Let the geometric intuition of "Rotate-Scale-Rotate" settle before moving to the technical comparison.
[/CUE]

[CUE 09]
Narration trigger: "diagonalization is incredibly picky. It only works for square matrices"
Timing: lead
Object(s): MathTex("A = PDP^{-1}") → Write
Color: WHITE
Duration: medium
Camera: static
Notes: Formula appears in the top-right corner. It should look rigid/static to reflect the "picky" nature described.
[/CUE]

[CUE 10]
Narration trigger: "break it down into three simple, intuitive steps."
Timing: sync
Object(s): ReplacementTransform (MathTex("A = PDP^{-1}") → MathTex("A = U \Sigma V^T"))
Color: WHITE (U, V), YELLOW (Σ)
Duration: medium
Camera: static
Notes: The SVD formula replaces the diagonalization formula. 
[/CUE]

[CUE 11]
Narration trigger: "involves looking at the matrices $A^T A$ and $A A^T$."
Timing: lead
Object(s): MathTex("A^T A", "AA^T") → FadeIn
Color: WHITE
Duration: short
Camera: static
Notes: Place these terms below the SVD formula.
[/CUE]

[CUE 12]
Narration trigger: "use an iterative algorithm that converges toward the answer"
Timing: sync
Object(s): MathTex("A^T A", "AA^T") → Indicate
Color: ORANGE
Duration: short
Camera: static
Notes: Pulse the matrices to acknowledge the computational reality of finding these bases. 
[/CUE]

---

**Director’s Note**

The most critical part of this sequence is CUE 04 through CUE 07. We must ensure the `NumberPlane` remains visible but fades in intensity during the "Scaling" phase (CUE 05) so the viewer focuses on the deformation of the `Circle`. The transition from $PDP^{-1}$ to $U\Sigma V^T$ in CUE 10 must be a `ReplacementTransform` to signal that SVD is the evolution/extension of the previous concept. The animator should ensure the "input" and "output" colors (BLUE/GREEN) are distinct to visually reinforce that SVD maps between different spaces.

---

The color-continuity trick from **REF-01** (gradient on the circle) and the side-by-side comparison layout from **REF-02/REF-05** are now the primary directives for this section. We will move away from a single-plane view to a dual-pane "Input Space" vs. "Output Space" setup to make the mapping clear.

# Section 2: SVD vs. Diagonalization

[CUE 13]
Narration trigger: "It’s natural to wonder how this relates to the diagonalization process."
Timing: lead
Object(s): NumberPlane (Left) → FadeIn, NumberPlane (Right) → FadeIn
Color: BLUE (Left), GREEN (Right)
Duration: medium
Camera: static
Notes: Create a split-screen view. Label the left "Input Space ($V$)" and the right "Output Space ($U$)."
[/CUE]

[CUE 14]
Narration trigger: "diagonalization ($A = PDP^{-1}$) as a search for 'fixed' directions."
Timing: sync
Object(s): MathTex("A = PDP^{-1}") → Write (Centered Top)
Color: WHITE
Duration: short
Camera: static
Notes: Position the formula above the split panes.
[/CUE]

[CUE 15]
Narration trigger: "a basis where the input and output are the same"
Timing: sync
Object(s): Vector (Left), Vector (Right) → Create
Color: RED
Duration: short
Camera: static
Notes: Draw the same two eigenvectors in both panes. Use the `leave_ghost_vectors=True` logic from **REF-03** to show they don't change direction, only length.
[/CUE]

[CUE 16]
Narration trigger: "A rotation matrix, for instance, has no real eigenvectors"
Timing: lead
Object(s): ApplyMatrix (Rotation Matrix) → NumberPlane (Left)
Color: RED
Duration: medium
Camera: static
Notes: Rotate the left pane first. The red vector spins off its original "ghost" span.
[/CUE]

[CUE 17]
Narration trigger: "because every vector is moved off its span."
Timing: sync
Object(s): ApplyMatrix (Rotation Matrix) → NumberPlane (Right)
Color: RED
Duration: medium
Camera: static
Notes: Rotate the right pane to match the left.
[/CUE]

[CUE 18]
Narration trigger: "SVD doesn't care if the vectors stay on their span."
Timing: sync
Object(s): ReplacementTransform (MathTex("A = PDP^{-1}") → MathTex("A = U \Sigma V^T"))
Color: WHITE
Duration: short
Camera: static
Notes: The SVD formula takes center stage again.
[/CUE]

[CUE 19]
Narration trigger: "perpendicular set of vectors that ends up as another perpendicular set of vectors"
Timing: lead
Object(s): Vector (Left: $v\_1, v\_2$), Vector (Right: $u\_1, u\_2$) → Create
Color: BLUE (Left), GREEN (Right)
Duration: medium
Camera: static
Notes: In the left pane, show two orthogonal BLUE vectors. In the right pane, show two different orthogonal GREEN vectors (the axes of the eventual ellipse). Use a small "right-angle" square symbol to confirm orthogonality.
[/CUE]

[CUE 20]
Narration trigger: "There is a beautiful bridge between the two: if you have a symmetric matrix"
Timing: lead
Object(s): MathTex("A = A^T") → FadeIn (Below formula)
Color: ORANGE
Duration: short
Camera: static
Notes: Highlight the condition for the bridge.
[/CUE]

[CUE 21]
Narration trigger: "singular values are just the absolute values of the eigenvalues."
Timing: sync
Object(s): SurroundingRectangle → Create around $\Sigma$ and $D$
Color: ORANGE
Duration: short
Camera: static
Notes: Pulse the diagonal components of both systems to show their equivalence.
[/CUE]

[CUE 22]
Narration trigger: "U and V collapse into one matrix."
Timing: sync
Object(s): Transform (Vector Left → Vector Right)
Color: WHITE
Duration: medium
Camera: static
Notes: Execute two separate transforms simultaneously or group them in a VGroup. The left basis morphs to visually match the right basis.
[/CUE]

[CUE 23]
Narration trigger: "especially when dealing with 'tall' or 'wide' matrices"
Timing: follow
Object(s): Tex("m \times n matrix") → FadeIn
Color: WHITE
Duration: short
Camera: static
Notes: Label appears centered below the split view to indicate non-square dimensions without altering the base NumberPlanes.
[/CUE]

---

**Director’s Note**

The dual-pane approach established in CUE 13 is essential here to contrast with Scene 1's single-pane transformation. By showing the eigenvectors failing in CUE 16 and CUE 17 (spinning off-span) and the SVD bases succeeding in CUE 19 (remaining perpendicular), we provide the visual "proof" of the script's claim. Per **REF-05**, I have opted to include the symmetry condition as an orange highlight in CUE 20 to ensure it stands out as a "special case" rather than the rule. Using `leave_ghost_vectors` is a non-negotiable requirement for the animator in CUE 15 to show the "span" effectively.

---

Based on **REF-06** and **REF-07**, the visual strategy here shifts from abstract geometry to data-driven evidence. We will use a "Top-Down" approach: first showing the mathematical reason why SVD works for compression (the decay of singular values), and then showing the result on an actual image.

## Section 3: The Power of SVD in the Real World

[CUE 24]
Narration trigger: "Because the SVD isolates the most important directions... it acts as a perfect filter for information."
Timing: lead
Object(s): MathTex("\Sigma") → Write
Color: YELLOW
Duration: medium
Camera: static
Notes: Show the diagonal Sigma matrix. Animate the smallest singular values fading to zero to visually represent the "filter."
[/CUE]

[CUE 25]
Narration trigger: "Take image compression. Think of a high-resolution photograph."
Timing: sync
Object(s): ImageMobject (Grayscale Photo) → FadeIn
Color: n/a
Duration: short
Camera: static
Notes: Place a high-detail grayscale image (e.g., a building or face) on the left half of the screen.
[/CUE]

[CUE 26]
Narration trigger: "By performing an SVD on that matrix, we can isolate the largest singular values."
Timing: lead
Object(s): Axes → Create, Graph (Exponential Decay) → Create
Color: YELLOW
Duration: medium
Camera: static
Notes: Per **REF-06**, show the singular value decay curve on the right half of the screen. The Y-axis represents magnitude, the X-axis represents the rank $k$.
[/CUE]

[CUE 27]
Narration trigger: "If we throw away the thousands of tiny singular values,"
Timing: sync
Object(s): DashedLine (Vertical cut-off on graph) → Create
Color: ORANGE
Duration: short
Camera: static
Notes: A vertical line slides from right to left on the decay graph, "shading out" the tail of the curve.
[/CUE]

[CUE 28]
Narration trigger: "reconstruct an image that looks almost identical to the original but requires a fraction of the data."
Timing: follow
Object(s): ImageMobject (Rank-k Reconstruction) → Transform
Color: n/a
Duration: long
Camera: static
Notes: Sequence: k=1 holds for 1s (showing clear vertical/horizontal streaks), transforms to k=10 holds for 1s, transforms to k=50. Update the k-label via ReplacementTransform simultaneously with each step.
[/CUE]

[CUE 29]
Narration trigger: "Beyond images, SVD is the engine behind Principal Component Analysis, or PCA"
Timing: hold
Object(s): FadeOut (All)
Color: n/a
Duration: breathe
Camera: static
Notes: Clear the stage for the data science demonstration.
[/CUE]

[CUE 30]
Narration trigger: "Imagine you have a dataset of a thousand people... height, weight, age, income"
Timing: lead
Object(s): Dot (Array/Scatter) → FadeIn
Color: BLUE
Duration: medium
Camera: static
Notes: Generate a correlated 2D point cloud as described in **REF-08**. Do not use a grid yet; let the "cloud" float in space.
[/CUE]

[CUE 31]
Narration trigger: "PCA uses SVD to find the directions along which your data varies the most"
Timing: sync
Object(s): Arrow (Primary and Secondary Components) → Create
Color: YELLOW
Duration: short
Camera: static
Notes: Two arrows emerge from the center of the point cloud, aligned with the spread of the data.
[/CUE]

[CUE 32]
Narration trigger: "the principal components are exactly the axes of the ellipse that your data cloud forms"
Timing: sync
Object(s): Ellipse (Dashed) → Create
Color: ORANGE
Duration: medium
Camera: static
Notes: As suggested in **REF-08**, overlay a dashed orange ellipse that perfectly encloses the main density of the dots. This connects Scene 3 back to the Scene 1 geometry.
[/CUE]

[CUE 33]
Narration trigger: "In linguistics, we often deal with a 'Term-Document Matrix'"
Timing: lead
Object(s): VGroup (Rectangles) → Create
Color: BLUE (Heatmap variations)
Duration: medium
Camera: static
Notes: Draw a 5x4 grid. Rows: "marathon", "sprint", "run", "feline", "cat". Columns: D1-D4. Color intensity maps to frequency.
[/CUE]

[CUE 34]
Narration trigger: "By applying SVD to this matrix, we perform a sort of linguistic 'compression'."
Timing: lead
Object(s): VGroup (Rectangles) → FadeOut, MathTex("\Sigma") → FadeIn
Color: YELLOW
Duration: medium
Camera: static
Notes: The matrix dissolves into the Sigma diagonal. Small values fade out to zero, representing the truncation of noise.
[/CUE]

[CUE 35]
Narration trigger: "If 'marathon' and 'sprint' frequently appear in the same documents"
Timing: sync
Object(s): MathTex("\Sigma") → FadeOut, VGroup (Rectangles) → FadeIn
Color: GREEN (Heatmap variations)
Duration: medium
Camera: static
Notes: The "smoothed" reconstructed matrix appears. 
[/CUE]

[CUE 36]
Narration trigger: "SVD maps them to the same underlying concept of 'Running.'"
Timing: follow
Object(s): SurroundingRectangle → Create
Color: ORANGE
Duration: short
Camera: static
Notes: Draw an orange highlight box around both the "marathon" and "sprint" rows, which now share visually identical color patterns to signify they occupy the same conceptual space.
[/CUE]

---

**Director’s Note** 

The transition in CUE 28 is the "magic trick" of the video. The animator must ensure the $k=1$ image looks like vertical/horizontal streaks (revealing the $u_i v_i^T$ structure) before it resolves into a clear picture by $k=50$. For the PCA section, the Ellipse overlay in CUE 32 is the most important visual anchor—it proves that "data" is just "geometry" in disguise. If time permits, the animator should use `Indicate` on the singular value graph  in CUE 26 while the image in CUE 28 is updating to show the direct link between the two.
