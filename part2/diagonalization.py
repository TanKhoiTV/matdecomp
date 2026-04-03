from typing import List, Tuple
import cmath

def diagonalize(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]], List[List[float]]]:
    """
    Chéo hóa ma trận vuông A sao cho:
        A = P D P^-1

    trong đó:
    - D: là ma trận đường chéo chứa các giá trị riêng,
    - P: chứa các vector riêng tương ứng dưới dạng các cột,
    - P_inv: là ma trận nghịch đảo của P.

    Điều kiện để chéo hóa được:
    - A phải là ma trận vuông.
    - A chéo hóa được khi nó có đủ số lượng vector riêng độc lập tuyến tính
    (tương đương tổng bội hình học bằng kích thước ma trận).

    Giá trị trả về:
        tuple: (P, D, P_inv) 
    P: ma trận chứa các vector riêng dưới dạng các cột
    D: ma trận đường chéo chứa các giá trị riêng
    P_inv: ma trận nghịch đảo của P
    """

    # Validate square matrix
    if not isinstance(A, list) or len(A) == 0 or any(not isinstance(row, list) for row in A):
        raise ValueError("A must be a non-empty matrix (list of lists).")
    n = len(A)
    if any(len(row) != n for row in A):
        raise ValueError("A must be a square matrix.")

    # This implementation supports 2x2 matrices without external libraries.
    if n != 2:
        raise NotImplementedError("This pure-Python implementation currently supports only 2x2 matrices.")

    a, b = A[0][0], A[0][1]
    c, d = A[1][0], A[1][1]

    # Characteristic polynomial: λ^2 - (a+d)λ + (ad-bc) = 0
    tr = a + d
    det = a * d - b * c
    disc = tr * tr - 4 * det
    root = cmath.sqrt(disc)
    lam1 = (tr + root) / 2
    lam2 = (tr - root) / 2

    if abs(lam1.imag) > 1e-12 or abs(lam2.imag) > 1e-12:
        raise ValueError("A is not diagonalizable over real numbers (complex eigenvalues found).")
    lam1 = lam1.real
    lam2 = lam2.real

    def eigenvector_for(lam):
        # Solve (A - λI)v = 0 for v != 0.
        m11 = a - lam
        m12 = b
        m21 = c
        m22 = d - lam

        # Choose a stable direction vector orthogonal to a non-zero row.
        if abs(m11) > 1e-12 or abs(m12) > 1e-12:
            v = [-m12, m11]
        elif abs(m21) > 1e-12 or abs(m22) > 1e-12:
            v = [-m22, m21]
        else:
            # A - λI = 0, any non-zero vector works.
            v = [1, 0]
        return v

    v1 = eigenvector_for(lam1)
    v2 = eigenvector_for(lam2)

    # Build P with eigenvectors as columns.
    P = [
        [v1[0], v2[0]],
        [v1[1], v2[1]],
    ]

    # Check invertibility of P (independent eigenvectors).
    pdet = P[0][0] * P[1][1] - P[0][1] * P[1][0]
    if abs(pdet) < 1e-12:
        raise ValueError("A is not diagonalizable (eigenvectors are not linearly independent).")

    D = [
        [lam1, 0],
        [0, lam2],
    ]

    P_inv = [
        [P[1][1] / pdet, -P[0][1] / pdet],
        [-P[1][0] / pdet, P[0][0] / pdet],
    ]

    def matmul(X, Y):
        return [
            [X[i][0] * Y[0][j] + X[i][1] * Y[1][j] for j in range(2)]
            for i in range(2)
        ]

    def frobenius_norm(M):
        return (
            abs(M[0][0]) ** 2
            + abs(M[0][1]) ** 2
            + abs(M[1][0]) ** 2
            + abs(M[1][1]) ** 2
        ) ** 0.5

    reconstructed = matmul(matmul(P, D), P_inv)
    diff = [
        [reconstructed[i][j] - A[i][j] for j in range(2)]
        for i in range(2)
    ]
    rel_err = frobenius_norm(diff) / max(frobenius_norm(A), 1e-30)
    if rel_err >= 1e-10:
        raise ValueError(f"Decomposition verification failed: relative error = {rel_err}")

    return P, D, P_inv