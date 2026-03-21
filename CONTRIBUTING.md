# Contributing Guide

This document covers everything you need to work on this project without breaking things for the team. Read it fully before pushing your first branch.

---

## Environment Setup

### 1. Check your Python version

Manim v0.20.1 supports Python 3.9–3.13. Run:

```bash
python --version
```

Any version from 3.10 to 3.13 is fine. If you are below 3.10, upgrade before continuing.

> **Anaconda users:** do not use an Anaconda environment for this project. Anaconda ships its own Cairo library that conflicts with the version pycairo that Manim requires. Use plain Python with a venv instead (see step 3).

### 2. Clone the repo

```bash
git clone https://github.com/TanKhoiTV/matdecomp.git
cd matdecomp
```
### 3. Create and activate a virtual environment

Always work inside a venv — keeps project dependencies isolated from your system Python.

```bash
python -m venv .venv
```

**Activate — Windows:**
```bash
.venv\Scripts\activate
```

**Activate — WSL2 / Linux:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt. Run all subsequent commands with the venv active.

> The `.venv` folder is already in `.gitignore` — do not commit it.

### 4. Windows only — set line endings

Run this once after cloning, outside or inside the venv:

```bash
git config --global core.autocrlf false
```

Line endings are normalized to LF via `.gitattributes`. This config prevents Windows from converting them back to CRLF on your machine.

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

> **WSL2 users:** if Manim fails to install, ensure FFmpeg is installed first:
> ```bash
> sudo apt update && sudo apt install ffmpeg
> ```
> Then re-run `pip install -r requirements.txt`.

### 6. Verify Manim

```bash
manim --version
# Expected: Manim Community v0.20.1
```

---

## Branch Naming

Always create a new branch for every issue. Never work directly on `main` or `dev`.

| Prefix | Use for |
|--------|---------|
| `feat/` | New implementation or feature |
| `fix/` | Bug fix |
| `docs/` | Report, notebook, README, or script changes |
| `test/` | Adding or updating test cases |

**Format:** `prefix/short-description`

```bash
# Good
feat/gaussian-eliminate
fix/singular-matrix-edge-case
docs/part1-report-section
test/inverse-edge-cases

# Bad
my-branch
fix
dev-copy
```

Branch names should be lowercase, hyphen-separated, no spaces.

---

## Commit Messages

Use conventional commit format. One logical change per commit.

```
feat: add partial pivoting to gaussian_eliminate
fix: handle singular matrix in determinant
test: add 5 edge cases for inverse()
docs: draft Part 1 theory section
refactor: extract back_substitution into separate function
```

**Rules:**
- Lowercase after the colon
- Present tense — "add" not "added"
- No period at the end
- No vague messages: "fix stuff", "wip", "asdf" are not acceptable
- Do not commit commented-out code
- Do not commit debugging print statements

---

## Pull Request Workflow

### Before opening a PR

- [ ] All acceptance criteria on the linked issue are checked off
- [ ] Code runs without errors
- [ ] No hardcoded file paths — use `pathlib.Path` only
- [ ] No `numpy.linalg`, `scipy.linalg`, or `sympy` solver calls in implementation code (verification calls are fine)
- [ ] At least 5 test cases per function

### Opening a PR

1. Push your branch to origin
2. Open a PR against `dev` — **never directly against `main`**
3. Title format: `feat: short description (#issue-number)`
4. Fill in the PR description: what you implemented, how you tested it, anything the reviewer should know
5. Assign at least one reviewer — rotate so everyone reviews across sprints
6. Move your issue card to **In Review** on the project board

### Review rules

- **Do not merge your own PR** — even if you are the PO or SM
- Reviewer must check: correctness, edge case coverage, code clarity, pathlib usage
- Leave specific comments, not just approvals
- All review comments must be marked resolved before merging
- Reviewer merges after approval — not the author

### After merge

- Delete your feature branch
- Move the issue card to **Done**
- Close the linked issue

---

## Code Standards

### File paths

```python
# Always
from pathlib import Path
results = Path("part3") / "results.csv"

# Never
results = "part3\\results.csv"
results = "part3/results.csv"
```

### No built-in solvers in implementation

```python
# Not allowed in implementation code
numpy.linalg.solve(A, b)
numpy.linalg.inv(A)
scipy.linalg.qr(A)
scipy.linalg.lu(A)
sympy.linsolve(...)
matrix.rref()
matrix.echelon_form()

# Allowed only in verify_solution() and test/verification cells
numpy.linalg.solve(A, b)  # for comparison only
```

### Function docstrings

Every function must have a docstring covering: purpose, parameters, return values, and any exceptions raised.

```python
def gaussian_eliminate(A, b, eps=1e-12):
    """
    Solve Ax = b via Gaussian elimination with partial pivoting.

    Parameters
    ----------
    A : list[list[float]]  — n x n coefficient matrix
    b : list[float]        — right-hand side vector of length n
    eps : float            — pivot threshold below which matrix is singular

    Returns
    -------
    x : list[float]        — solution vector
    s : int                — number of row swaps performed

    Raises
    ------
    ValueError             — if |pivot| < eps (singular or near-singular matrix)
    """
```

---

## Notebook Standards

- All cells must run top-to-bottom without errors before committing
- No empty cells left in the middle of a notebook
- Markdown cells above each code section explaining what it does
- Output cells committed with results visible — do not clear outputs before committing

---

## Report Workflow (Prism → Git)

The report is written in Prism (cloud LaTeX). It does not sync automatically to Git.

**SM responsibility at end of each sprint:**
1. Export `report.tex` source and compiled `report.pdf` from Prism
2. Open a PR committing both files to `report/`
3. PO reviews and merges

No one else should commit to `report/` directly — all report changes go through Prism and the SM's export PR.

---

## Project Board

The GitHub Projects board is the single source of truth for sprint progress — not a chat thread, not a spreadsheet.

| Column | Meaning |
|--------|---------|
| Backlog | Not yet in a sprint |
| In Progress | Assigned and actively being worked on |
| In Review | PR open, waiting for review |
| Done | Merged, issue closed, all criteria met |

Move your own cards across In Progress → In Review → Done. Only the PO moves cards from Backlog into a sprint.

---

## Questions?

Open a GitHub Issue with the label `question` and assign the PO or SM.
