"""
Chéo hóa ma trận vuông thực A ≈ P D P^{-1} (triển khai thuần list, không NumPy).

Thuật toán: QR (Modified Gram–Schmidt) + QR có shift Wilkinson + deflation → trị riêng;
gom cụm trị riêng gần nhau; cơ sở ker(A - λI); Gauss–Jordan cho P^{-1}; kiểm tra Frobenius.

Phạm vi: ma trận thực chéo hóa được trên R. Phổ phức được bắt sớm cho n == 2 (biệt thức).
"""

from __future__ import annotations

from typing import List, Optional, Tuple
import math

__all__ = [
    "diagonalize",
    "matmul",
    "identity",
    "subtract",
    "scalar_mult",
    "norm",
    "qr_decomposition",
    "wilkinson_shift",
    "qr_algorithm",
    "null_space_basis",
    "null_space",
    "inverse",
]

EPS = 1e-10
MAX_ITER = 3000
RECON_TOL = 1e-10
CLUSTER_ABS_TOL = 1e-7
CLUSTER_REL_TOL = 1e-6


def matmul(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    n = len(A)
    m = len(B[0])
    p = len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(m)] for i in range(n)]


def identity(n: int) -> List[List[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def subtract(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def scalar_mult(A: List[List[float]], c: float) -> List[List[float]]:
    n = len(A)
    return [[c * A[i][j] for j in range(n)] for i in range(n)]


def norm(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def _has_nonreal_eigenvalues(A: List[List[float]], n: int) -> bool:
    """2*2: phân biệt thực / phức qua biệt thức. n>2: không kiểm tra (không NumPy)."""
    if n != 2:
        return False
    a, b = A[0][0], A[0][1]
    c, d = A[1][0], A[1][1]
    trace = a + d
    det = a * d - b * c
    disc = trace * trace - 4.0 * det
    return disc < -1e-9


def _cluster_eigenvalue_indices(vals: List[float]) -> List[List[int]]:
    """Gom chỉ số cột có trị riêng gần nhau (sắp xếp theo giá trị)."""
    n = len(vals)
    if n == 0:
        return []
    order = sorted(range(n), key=lambda i: vals[i])
    clusters: List[List[int]] = []
    k = 0
    while k < n:
        grp = [order[k]]
        mu = vals[order[k]]
        k += 1
        while k < n:
            i = order[k]
            v = vals[i]
            thresh = CLUSTER_ABS_TOL + CLUSTER_REL_TOL * max(1.0, abs(mu))
            if abs(v - mu) <= thresh:
                grp.append(i)
                mu = sum(vals[j] for j in grp) / len(grp)
                k += 1
            else:
                break
        clusters.append(grp)
    return clusters


def qr_decomposition(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """Modified Gram–Schmidt: A = Q R."""
    n = len(A)
    Q = [[0.0] * n for _ in range(n)]
    R = [[0.0] * n for _ in range(n)]

    V = [list(col) for col in zip(*A)]

    for i in range(n):
        R[i][i] = norm(V[i])
        if R[i][i] < EPS:
            continue

        Q_col = [x / R[i][i] for x in V[i]]
        for r in range(n):
            Q[r][i] = Q_col[r]

        for j in range(i + 1, n):
            R[i][j] = sum(Q[r][i] * V[j][r] for r in range(n))
            V[j] = [V[j][r] - R[i][j] * Q[r][i] for r in range(n)]

    return Q, R


def wilkinson_shift(A: List[List[float]]) -> float:
    """Trị riêng góc 2*2 dưới gần A_nn hơn (ổn định khi biệt thức âm do số học)."""
    n = len(A)
    if n < 2:
        return A[0][0]

    a = A[n - 2][n - 2]
    b = A[n - 2][n - 1]
    c = A[n - 1][n - 2]
    d = A[n - 1][n - 1]

    trace = a + d
    det2 = a * d - b * c
    disc = trace * trace - 4.0 * det2
    if disc < 0:
        disc = 0.0
    s = math.sqrt(disc)
    r1 = (trace + s) / 2.0
    r2 = (trace - s) / 2.0
    return r1 if abs(r1 - d) <= abs(r2 - d) else r2


def qr_algorithm(A: List[List[float]]) -> List[float]:
    n = len(A)
    Ak = [row[:] for row in A]
    eigenvalues: List[float] = []

    size = n
    while size > 0:
        if size == 1:
            eigenvalues.append(Ak[0][0])
            break

        converged = False
        for _ in range(MAX_ITER):
            if abs(Ak[size - 1][size - 2]) < EPS:
                eigenvalues.append(Ak[size - 1][size - 1])
                size -= 1
                Ak = [row[:size] for row in Ak[:size]]
                converged = True
                break

            mu = wilkinson_shift(Ak)
            I = identity(size)
            shifted = subtract(Ak, scalar_mult(I, mu))
            Q, R = qr_decomposition(shifted)
            Ak = matmul(R, Q)
            Ak = subtract(Ak, scalar_mult(I, -mu))

        if not converged:
            eigenvalues.append(Ak[size - 1][size - 1])
            size -= 1
            Ak = [row[:size] for row in Ak[:size]]

    return eigenvalues


def null_space_basis(A: List[List[float]]) -> List[List[float]]:
    """Cơ sở ker(A): mỗi biến tự do → một vector độc lập (RREF)."""
    n = len(A)
    m = len(A[0])

    M = [row[:] for row in A]

    pivot_col: List[int] = []
    row = 0

    for col in range(m):
        pivot = None
        for r in range(row, n):
            if abs(M[r][col]) > EPS:
                pivot = r
                break

        if pivot is None:
            continue

        M[row], M[pivot] = M[pivot], M[row]

        pivot_val = M[row][col]
        M[row] = [x / pivot_val for x in M[row]]

        for r in range(n):
            if r != row:
                factor = M[r][col]
                M[r] = [M[r][c] - factor * M[row][c] for c in range(m)]

        pivot_col.append(col)
        row += 1

    free_vars = [j for j in range(m) if j not in pivot_col]
    if not free_vars:
        return []

    rank = len(pivot_col)
    basis: List[List[float]] = []
    for free in free_vars:
        v = [0.0] * m
        v[free] = 1.0
        for i in reversed(range(rank)):
            col = pivot_col[i]
            v[col] = -sum(M[i][j] * v[j] for j in range(m))
        basis.append(v)
    return basis


def null_space(A: List[List[float]]) -> List[float]:
    b = null_space_basis(A)
    return b[0] if b else []


def inverse(A: List[List[float]]) -> List[List[float]]:
    """Gauss–Jordan trên [A | I]."""
    n = len(A)
    M = [A[i][:] + identity(n)[i][:] for i in range(n)]

    for i in range(n):
        pivot = i
        while pivot < n and abs(M[pivot][i]) < EPS:
            pivot += 1
        if pivot == n:
            raise ValueError("Matrix not invertible")

        M[i], M[pivot] = M[pivot], M[i]

        pivot_val = M[i][i]
        M[i] = [x / pivot_val for x in M[i]]

        for r in range(n):
            if r != i:
                factor = M[r][i]
                M[r] = [M[r][c] - factor * M[i][c] for c in range(2 * n)]

    return [row[n:] for row in M]


def diagonalize(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]], List[List[float]]]:
    """
    Chéo hóa A = P D P^{-1} (trên R): QR có shift + deflation, cơ sở không gian riêng, kiểm tra Frobenius.

    Ném ValueError nếu ma trận không hợp lệ, phổ phức (2*2), không chéo hóa được,
    hoặc sai số tái tạo vượt RECON_TOL.
    """
    if not isinstance(A, list) or len(A) == 0:
        raise ValueError("Invalid matrix")

    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("Matrix must be square")

    if _has_nonreal_eigenvalues(A, n):
        raise ValueError(
            "Matrix has complex eigenvalues; cannot diagonalize over the real numbers"
        )

    eigenvalues = qr_algorithm(A)
    if len(eigenvalues) != n:
        raise ValueError("A is not diagonalizable")

    clusters = _cluster_eigenvalue_indices(eigenvalues)
    eigenvector_cols: List[Optional[List[float]]] = [None] * n

    for grp in clusters:
        lam = sum(eigenvalues[i] for i in grp) / len(grp)
        M = subtract(A, scalar_mult(identity(n), lam))
        basis = null_space_basis(M)
        m = len(grp)
        if len(basis) < m:
            raise ValueError("A is not diagonalizable")

        for t, col_idx in enumerate(sorted(grp)):
            eigenvector_cols[col_idx] = basis[t]

    if any(v is None for v in eigenvector_cols):
        raise ValueError("A is not diagonalizable")

    cols = [v for v in eigenvector_cols if v is not None]
    P = [[cols[j][i] for j in range(n)] for i in range(n)]

    try:
        P_inv = inverse(P)
    except ValueError as e:
        raise ValueError(
            "A is not diagonalizable (eigenvectors are linearly dependent)"
        ) from e

    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = eigenvalues[i]

    reconstructed = matmul(matmul(P, D), P_inv)
    diff = subtract(reconstructed, A)

    err = math.sqrt(sum(diff[i][j] ** 2 for i in range(n) for j in range(n)))
    base = math.sqrt(sum(A[i][j] ** 2 for i in range(n) for j in range(n)))

    rel = err / max(base, 1e-30)
    if rel > RECON_TOL:
        raise ValueError(
            f"Decomposition verification failed: relative Frobenius error {rel:.3e} "
            f"exceeds tolerance {RECON_TOL:.3e}"
        )

    return P, D, P_inv
