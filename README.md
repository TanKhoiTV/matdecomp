# matdecomp

From-scratch Python implementations of Gaussian elimination, QR decomposition, and matrix diagonalization — with a narrated Manim video and performance analysis.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Parts](#parts)
  - [Part 1 — Gaussian Elimination](#part-1--gaussian-elimination)
  - [Part 2 — QR Decomposition + Manim Video](#part-2--qr-decomposition--manim-video)
  - [Part 3 — Performance Analysis](#part-3--performance-analysis-bonus)
- [Running the Notebooks](#running-the-notebooks)
- [Team](#team)
- [Contributing](#contributing)

---

## Overview

This project covers three core areas of numerical linear algebra, implemented from scratch in Python without the use of `numpy.linalg`, `scipy.linalg`, or `sympy` solver functions. NumPy and SciPy are used only for result verification.

| Part | Topic | Status |
|------|-------|--------|
| 1 | Gaussian elimination, determinant, inverse, rank/basis | Mandatory |
| 2 | QR decomposition (Modified Gram-Schmidt), diagonalization, Manim video with narration | Mandatory |
| 3 | Iterative solvers, benchmarks, stability analysis | Bonus |

---

## Project Structure

```
matdecomp/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── requirements.txt
├── manim.cfg                   # Custom Manim theme
├── part1/
│   ├── gaussian.py             # gaussian_eliminate, back_substitution
│   ├── determinant.py          # determinant
│   ├── inverse.py              # inverse (Gauss-Jordan)
│   ├── rank_basis.py           # rank_and_basis
│   └── part1_demo.ipynb        # Walkthrough notebook
├── part2/
│   ├── decomposition.py        # qr_decompose (Modified Gram-Schmidt)
│   ├── diagonalization.py      # diagonalize (A = PDP⁻¹)
│   ├── theme.py                # Shared Manim color/font config
│   ├── manim_scene.py          # All 3 Manim scenes
│   ├── narration_script.md     # Full narration script
│   └── demo_video.mp4          # Exported video (≥1080p, ≥2 min)
├── part3/                      # Bonus — only present if activated
│   ├── solvers.py              # Gauss-Seidel iterative solver
│   ├── benchmark.py            # Benchmark harness
│   ├── results.csv             # Benchmark results
│   └── analysis.ipynb          # Performance analysis notebook
└── report/
    ├── report.tex              # LaTeX source
    ├── report.pdf              # Compiled report
    └── sections/
        ├── part1.tex
        ├── part2.tex
        └── conclusion.tex
```

---

## Setup

### Requirements

- Python 3.10 or higher
- Manim Community v0.20.1
- WSL2 (Ubuntu) or Windows — see note below

### Install dependencies

```bash
pip install -r requirements.txt
```

### WSL2 / Windows mixed environment

This project is developed across WSL2 (Ubuntu) and Windows. Line endings are normalized via `.gitattributes`. If you are on Windows, run the following once after cloning:

```bash
git config --global core.autocrlf false
```

All file paths in the codebase use `pathlib.Path` — no hardcoded OS separators.

### Verify Manim install

```bash
manim --version
# Expected: Manim Community v0.20.1
```

If Manim installation fails on Windows, refer to the [official Windows installation guide](https://docs.manim.community/en/stable/installation/windows.html). WSL2 users generally have fewer install issues.

---

## Parts

### Part 1 — Gaussian Elimination

Implementations in `part1/`:

| Function | Description |
|----------|-------------|
| `gaussian_eliminate(A, b)` | Gaussian elimination with partial pivoting. Returns reduced matrix, solution `x`, swap count `s`. |
| `back_substitution(U, c)` | Backward substitution for upper-triangular systems. |
| `determinant(A)` | Computes det(A) = (−1)ˢ × ∏ uᵢᵢ via elimination. |
| `inverse(A)` | Finds A⁻¹ via Gauss-Jordan on [A\|I]. |
| `rank_and_basis(A)` | Returns rank, column space basis, row space basis, and null space basis from RREF. |
| `verify_solution(A, x, b)` | Computes residual ‖Ax̂−b‖₂/‖b‖₂ and compares against NumPy. |

Each function has at least 5 test cases including edge cases. See `part1/part1_demo.ipynb` for a full walkthrough.

### Part 2 — QR Decomposition + Manim Video

**Python implementation** in `part2/decomposition.py` and `part2/diagonalization.py`:

- `qr_decompose(A)` — Modified Gram-Schmidt. Returns Q (orthonormal columns) and R (upper triangular, positive diagonal).
- `diagonalize(A)` — Returns P, D, P_inv satisfying A = PDP⁻¹.

**Manim video** (`part2/demo_video.mp4`):

The video is a narrated educational animation in the style of a math explainer, with a custom light theme distinct from 3Blue1Brown defaults.

| Scene | Content |
|-------|---------|
| 1 | Introduction to QR — Gram-Schmidt orthogonalization animated step by step |
| 2 | Diagonalization — eigenvalues, eigenvectors, A = PDP⁻¹ |
| 3 | Application — least squares fitting using QR |

Recording gear: Audio-Technica AT2020 USB + ATH-M40x. Narration script at `part2/narration_script.md`.

### Part 3 — Performance Analysis (Bonus)

Present only if activated during Sprint 3 planning. Compares Gaussian elimination, QR solver, and Gauss-Seidel across matrix sizes n ∈ {50, 100, 200, 500, 1000}. Includes log-log plots and stability analysis on Hilbert matrices vs random SPD matrices. See `part3/analysis.ipynb`.

---

## Running the Notebooks

```bash
# Part 1 demo
jupyter notebook part1/part1_demo.ipynb

# Part 3 analysis (if present)
jupyter notebook part3/analysis.ipynb
```

All notebooks run top-to-bottom without manual intervention.

## Rendering the Manim video

```bash
cd part2
manim manim_scene.py QRDecompositionScene -qh
manim manim_scene.py DiagonalizationScene -qh
manim manim_scene.py LeastSquaresScene -qh
```

The `-qh` flag renders at 1080p. Output goes to `media/videos/`. The pre-rendered export with narration is at `part2/demo_video.mp4`.

---

## Team

| Member | Role | Responsibilities |
|--------|------|-----------------|
| Trần Văn Tấn Khôi | Product Owner + Repo Owner | Backlog, GitHub Projects, `rank_and_basis`, `verify_solution`, `part1_demo.ipynb` |
| Lê Thành Đạt | Scrum Master | Sprint ceremonies, retros, report Prism → Git commits, diagonalization skeleton |
| Cao Việt Cường | Developer A | `gaussian_eliminate`, `back_substitution`, `rank_and_basis` |
| Nguyễn Phú Đạt | Developer B | `determinant`, `inverse`, benchmark harness |
| Trần Văn Tấn Khôi | Developer C | QR decomposition (full implementation) |
| Mai Phan Nhật Hoàng | Developer D | Diagonalization (complete), report sections |
| Lê Thành Đạt | Developer E | All Manim scenes, narration script, audio recording and sync, video export |

*Fill in names and student IDs before submission.*

---

## Contributing

This project uses a structured GitHub workflow. Please read before pushing anything.

### Branch naming

```
feat/short-description     # new implementation or feature
fix/short-description      # bug fix
docs/short-description     # report, notebook, or README changes
```

### Commit format

```
feat: add partial pivoting to gaussian_eliminate
fix: handle singular matrix edge case in determinant
test: add 5 edge cases for inverse()
docs: draft Part 1 theory section
```

One logical change per commit. Do not commit commented-out code or debugging print statements.

### Pull request rules

- Open a PR against `dev`, not `main`
- Title must reference the issue: `feat: gaussian_eliminate (#3)`
- At least one reviewer required — **do not merge your own PR**
- All acceptance criteria on the linked issue must be checked before requesting review
- `main` is protected and only receives merges from `dev` at sprint close

### Issue workflow

Every story has a corresponding GitHub Issue. Before starting work:
1. Assign the issue to yourself
2. Move the card to **In Progress** on the project board
3. Create a branch linked to the issue

---

---

## Tổng Quan (Tiếng Việt)

Đây là đồ án cài đặt bằng Python các kỹ thuật đại số tuyến tính số, bao gồm phép khử Gauss, phân rã QR, và chéo hóa ma trận, kèm video Manim có thuyết minh và phân tích hiệu năng.

### Các Phần

**Phần 1 — Phép Khử Gauss và Ứng Dụng**
Cài đặt: `gaussian_eliminate` (có partial pivoting), `back_substitution`, `determinant`, `inverse` (Gauss-Jordan), `rank_and_basis`. Không sử dụng `numpy.linalg` hoặc `scipy.linalg` trong phần cài đặt — chỉ dùng để kiểm chứng.

**Phần 2 — Phân Rã QR + Video Manim**
Phân rã QR bằng Modified Gram-Schmidt. Chéo hóa ma trận A = PDP⁻¹. Video Manim có thuyết minh (≥2 phút, ≥1080p) với theme tùy chỉnh — nền sáng, font IBM Plex Sans, màu teal. Thiết bị thu âm: AT2020 USB + ATH-M40x.

**Phần 3 — Phân Tích Hiệu Năng**
So sánh các phương pháp giải Ax = b: Gauss, QR, Gauss-Seidel. Thực nghiệm với n ∈ {50, 100, 200, 500, 1000}. Đồ thị log-log, phân tích ma trận Hilbert. Chỉ thực hiện nếu có đủ thời gian sau Phần 1 và 2.

### Cài Đặt

```bash
pip install -r requirements.txt
```

Yêu cầu Python 3.10 trở lên và Manim Community v0.20.1.

### Lưu Ý Môi Trường

Dự án phát triển trên cả WSL2 (Ubuntu) và Windows. File `.gitattributes` đã cấu hình thống nhất line ending (LF). Thành viên dùng Windows chạy lệnh sau sau khi clone:

```bash
git config --global core.autocrlf false
```

### Quy Trình Làm Việc

Mỗi story tương ứng một GitHub Issue. Làm việc trên branch riêng, tạo Pull Request vào `dev`, cần ít nhất 1 người review trước khi merge. Không ai merge PR của chính mình. Xem hướng dẫn đầy đủ ở phần Contributing phía trên.
