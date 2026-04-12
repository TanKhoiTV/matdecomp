"""
Chéo hóa ma trận vuông thực A ≈ P D P^{-1} (triển khai thuần list, không NumPy).

Thuật toán:
- Nếu A đối xứng: sử dụng Jacobi để tính trị riêng
  và vector riêng trực chuẩn (P^{-1} = P^T).
- Nếu A không đối xứng: sử dụng QR algorithm (Modified Gram-Schmidt) với
  Wilkinson shift và deflation để tính trị riêng, sau đó tìm vector riêng
  thông qua không gian nghiệm của (A - λI).

Các bước chính:
- Gom cụm trị riêng gần nhau (xử lý bội số)
- Tính cơ sở không gian riêng (null space)
- Xây dựng P, D và tính P^{-1} bằng Gauss-Jordan
- Kiểm tra lại A ≈ P D P^{-1} bằng chuẩn Frobenius

Phạm vi:
- Hỗ trợ ma trận vuông thực chéo hóa được trên R
- Phát hiện phổ phức:
  + Chính xác với ma trận 2*2 (qua biệt thức)
  + Với n > 2: không đảm bảo phát hiện đầy đủ, có thể fail ở bước kiểm tra

Lỗi (raises ValueError):
- Ma trận không vuông hoặc không hợp lệ
- Ma trận không chéo hóa được (thiếu vector riêng độc lập)
- Phát hiện trị riêng phức (trong trường hợp hỗ trợ)
- Sai số tái tạo vượt ngưỡng cho phép

Phù hợp cho ma trận kích thước nhỏ-trung bình với phổ thực.
"""

from __future__ import annotations

from typing import List, Optional, Tuple
import math

from part1.inverse import inverse

try:
    from .decomposition import jacobi_eigenvalues
except ImportError:
    from decomposition import jacobi_eigenvalues

__all__ = [
    "diagonalize",
    "jacobi_eigenvalues",
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
    """
    Multiply two matrices represented as nested lists.

    Parameters:
        A (List[List[float]]): Left matrix with shape n*p.
        B (List[List[float]]): Right matrix with shape p*m.

    Returns:
        List[List[float]]: Resulting matrix with shape n*m where element (i, j) is the sum over k of A[i][k] * B[k][j].

    Notes:
        No shape validation is performed; behavior is undefined if the inner dimensions do not match.
    """
    n = len(A)
    m = len(B[0])
    p = len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(m)] for i in range(n)]


def identity(n: int) -> List[List[float]]:
    """
    Create an n*n identity matrix.

    Parameters:
        n (int): Size of the square identity matrix.

    Returns:
        List[List[float]]: n*n matrix with `1.0` on the diagonal and `0.0` elsewhere.
    """
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def subtract(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """
    Subtract two square matrices elementwise.

    Parameters:
        A (List[List[float]]): Left-hand n*n matrix.
        B (List[List[float]]): Right-hand n*n matrix (must have the same dimensions as `A`).

    Returns:
        List[List[float]]: New n*n matrix where each element is A[i][j] - B[i][j].
    """
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def scalar_mult(A: List[List[float]], c: float) -> List[List[float]]:
    """
    Multiply each element of a square matrix by a scalar.

    Parameters:
        A (List[List[float]]): Square matrix (n x n) represented as a list of n rows, each with n floats.
        c (float): Scalar multiplier.

    Returns:
        List[List[float]]: New n x n matrix where each element is equal to `c * A[i][j]`.
    """
    n = len(A)
    return [[c * A[i][j] for j in range(n)] for i in range(n)]


def transpose(A: List[List[float]]) -> List[List[float]]:
    """Return the transpose of a matrix."""
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def norm(v: List[float]) -> float:
    """
    Compute the Euclidean (L2) norm of a vector.

    Parameters:
        v (List[float]): Sequence of numeric components.

    Returns:
        float: The Euclidean norm (sqrt of the sum of squares of the components), which is greater than or equal to 0.
    """
    return math.sqrt(sum(x * x for x in v))


def _is_symmetric(A: List[List[float]]) -> bool:
    """Check whether A is symmetric within the module tolerance."""
    n = len(A)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(A[i][j] - A[j][i]) > EPS:
                return False
    return True


def _sort_eigendecomposition(
    eigenvalues: List[float], eigenvectors: List[List[float]]
) -> Tuple[List[float], List[List[float]]]:
    """Sort eigenvalues ascending and reorder eigenvector columns to match."""
    order = sorted(range(len(eigenvalues)), key=lambda i: eigenvalues[i])
    sorted_values = [eigenvalues[i] for i in order]
    sorted_vectors = [[eigenvectors[row][i] for i in order] for row in range(len(eigenvectors))]
    return sorted_values, sorted_vectors


def _verify_diagonalization(
    A: List[List[float]],
    P: List[List[float]],
    D: List[List[float]],
    P_inv: List[List[float]],
) -> None:
    """Raise ValueError if P D P^{-1} does not reconstruct A accurately enough."""
    n = len(A)
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


def _has_nonreal_eigenvalues(A: List[List[float]], n: int) -> bool:
    """
    Detects whether a 2*2 real matrix has complex (nonreal) eigenvalues by checking the characteristic discriminant.

    For n == 2, computes the discriminant of the characteristic polynomial (trace^2 - 4·det) and treats sufficiently negative values as indicating nonreal eigenvalues (threshold -1e-9). For n != 2 this function does not attempt detection and returns False.

    Returns:
        bool: `True` if the discriminant < -1e-9 (indicating complex eigenvalues), `False` otherwise.
    """
    if n != 2:
        return False
    a, b = A[0][0], A[0][1]
    c, d = A[1][0], A[1][1]
    trace = a + d
    det = a * d - b * c
    disc = trace * trace - 4.0 * det
    return disc < -1e-9


def _cluster_eigenvalue_indices(vals: List[float]) -> List[List[int]]:
    """
    Group indices of nearby eigenvalues into consecutive clusters ordered by eigenvalue.

    This function sorts indices by their corresponding values in `vals` and forms consecutive clusters
    where each new value is within CLUSTER_ABS_TOL + CLUSTER_REL_TOL * max(1.0, |mu|) of the cluster mean `mu`.

    Parameters:
        vals (List[float]): List of scalar values (typically eigenvalues).

    Returns:
        List[List[int]]: A list of clusters; each cluster is a list of indices from `vals`.
        Clusters are returned in ascending order of the associated eigenvalue(s).
    """
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


def _orthonormal_completion_column(Q: List[List[float]], col_idx: int) -> List[float]:
    """Complete Q with a unit vector orthogonal to the earlier columns."""
    n = len(Q)
    previous_cols = [[Q[row][j] for row in range(n)] for j in range(col_idx)]

    for basis_idx in range(n):
        candidate = [0.0] * n
        candidate[basis_idx] = 1.0

        for prev in previous_cols:
            proj = sum(candidate[r] * prev[r] for r in range(n))
            candidate = [candidate[r] - proj * prev[r] for r in range(n)]

        candidate_norm = norm(candidate)
        if candidate_norm > EPS:
            return [x / candidate_norm for x in candidate]

    raise ValueError(f"Failed to construct an orthonormal completion vector for column {col_idx}")


def qr_decomposition(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """
    Compute the QR decomposition of a square matrix using the modified Gram-Schmidt process.

    Returns:
        (Q, R): Tuple of n*n matrices where A = Q R. Q has orthonormal columns for those columns whose norm is >= EPS; R is upper-triangular. If a column of A has norm less than EPS, the corresponding diagonal R[i][i] is zero and the Q column is left as the zero vector.
    """
    n = len(A)
    Q = [[0.0] * n for _ in range(n)]
    R = [[0.0] * n for _ in range(n)]

    V = [list(col) for col in zip(*A)]

    for i in range(n):
        R[i][i] = norm(V[i])
        if R[i][i] < EPS:
            Q_col = _orthonormal_completion_column(Q, i)
            R[i][i] = 0.0
        else:
            Q_col = [x / R[i][i] for x in V[i]]

        for r in range(n):
            Q[r][i] = Q_col[r]

        for j in range(i + 1, n):
            R[i][j] = sum(Q[r][i] * V[j][r] for r in range(n))
            V[j] = [V[j][r] - R[i][j] * Q[r][i] for r in range(n)]

    return Q, R


def wilkinson_shift(A: List[List[float]]) -> float:
    """
    Selects a Wilkinson shift based on the bottom-right 2*2 block of matrix A.

    If A has size 1 returns A[0][0]. For larger A, computes the eigenvalues of the 2*2 submatrix
    formed by the last two rows/columns and returns the eigenvalue that is closer to the bottom-right
    diagonal element. If the 2*2 discriminant is negative due to rounding, it is treated as zero.
    Returns:
        The chosen Wilkinson shift (a scalar float).
    """
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
    """
    Compute the eigenvalues of a real square matrix using shifted QR iteration with Wilkinson shifts and deflation.

    Parameters:
        A (List[List[float]]): Square matrix (list of rows) whose eigenvalues are sought.

    Returns:
        List[float]: Approximated eigenvalues of A as floats. Values are returned in the order discovered by deflation (typically corresponding to bottom-right toward top-left of the working matrix).
    """
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
            I_mat = identity(size)
            shifted = subtract(Ak, scalar_mult(I_mat, mu))
            Q, R = qr_decomposition(shifted)
            Ak = matmul(R, Q)
            Ak = subtract(Ak, scalar_mult(I_mat, -mu))

        if not converged:
            raise ValueError(
                f"QR iteration failed to converge after {MAX_ITER} iterations "
                f"for the trailing {size}x{size} block"
            )

    return eigenvalues


def null_space_basis(A: List[List[float]]) -> List[List[float]]:
    """
    Compute a basis for the null space (kernel) of A.

    Each returned vector is a column vector (as a list) corresponding to one free variable in a reduced row-echelon form of A; the set spans ker(A). If A has full column rank (no free variables), an empty list is returned.

    Parameters:
        A (List[List[float]]): m-by-n matrix (list of rows) representing the linear map whose null space is sought.

    Returns:
        List[List[float]]: A list of basis vectors for ker(A); each vector has length equal to the number of columns of A.
    """
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
    """
    Return a single basis vector of the null space of matrix A, or an empty list if the null space is {0}.

    Parameters:
        A (List[List[float]]): Real matrix with m rows and n columns.

    Returns:
        List[float]: A vector of length n that spans (one element of) the null space of A if a nontrivial null space exists, otherwise an empty list.
    """
    b = null_space_basis(A)
    return b[0] if b else []


# Main function: diagonalize
def diagonalize(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]], List[List[float]]]:
    """
    Compute a real diagonalization A = P D P^{-1} for the square matrix A.

    This routine finds eigenvalues with a shifted QR iteration (Wilkinson shift + deflation),
    groups nearby eigenvalues, builds eigenvectors from null spaces of (A - λI), assembles
    P from those eigenvectors, computes P^{-1} by Gauss-Jordan, constructs the diagonal D,
    and verifies the decomposition by the relative Frobenius norm (compare reconstructed A to input).

    Returns:
        tuple: (P, D, P_inv) where each is an n*n matrix represented as a list of lists;
            P contains eigenvectors as columns, D is diagonal with the computed eigenvalues,
            and P_inv is the inverse of P.

    Raises:
        ValueError: if A is not a non-empty list matrix, not square, or invalid input;
        ValueError: if a 2*2 discriminant test indicates nonreal eigenvalues (diagonalization over R not possible);
        ValueError: if the algorithm determines A is not diagonalizable (insufficient null-space dimension or missing eigenvectors);
        ValueError: if eigenvectors are linearly dependent (P is noninvertible);
        ValueError: if the relative Frobenius reconstruction error exceeds RECON_TOL.
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

    if _is_symmetric(A):
        eigenvalues, eigenvectors = jacobi_eigenvalues([row[:] for row in A], EPS)
        eigenvalues, eigenvectors = _sort_eigendecomposition(eigenvalues, eigenvectors)

        P = eigenvectors
        P_inv = transpose(P)
        D = [[0.0] * n for _ in range(n)]
        for i in range(n):
            D[i][i] = eigenvalues[i]

        _verify_diagonalization(A, P, D, P_inv)
        return P, D, P_inv

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

    _verify_diagonalization(A, P, D, P_inv)

    return P, D, P_inv
