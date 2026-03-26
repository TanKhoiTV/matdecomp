from typing import List, Tuple


def back_substitution(U: List[List[float]], c: List[float], eps: float = 1e-12) -> List[float]:
    """
    Solves an upper-triangular system Ux = c.
    Note: For m x n, this typically solves the square part or consistent systems.
    """
    n = len(U[0])  # Number of variables
    m = len(U)  # Number of equations
    x = [0.0] * n

    # Back substitution starts from the last pivot row
    for i in range(min(m, n) - 1, -1, -1):
        if abs(U[i][i]) < eps:
            # Skip if zero diagonal (underdetermined or inconsistent)
            continue

        sum_ax = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (c[i] - sum_ax) / U[i][i]
    return x


def gaussian_eliminate(
        A: List[List[float]], b: List[float], eps: float = 1e-12
) -> Tuple[List[List[float]], List[float], int]:
    """
    Performs Gaussian elimination with partial pivoting on an m x n matrix.

    Parameters
    ----------
    A : List[List[float]]  - m x n coefficient matrix.
    b : List[float]        - Right-hand side vector of length m.
    eps : float            - Pivot threshold.

    Returns
    -------
    M : List[List[float]]  - The reduced augmented matrix [U|c] in REF.
    x : List[float]        - A potential solution vector.
    swaps : int            - Count of row swaps performed.
    """
    m = len(A)
    n = len(A[0])
    # Create augmented matrix [A|b] of size m x (n+1)
    M = [row[:] + [bi] for row, bi in zip(A, b)]
    swaps = 0
    pivot_row = 0

    for j in range(n):  # Iterate through columns
        if pivot_row >= m:
            break

        # 1. Partial Pivoting: Find max in current column j from pivot_row down
        max_row = pivot_row
        for r in range(pivot_row + 1, m):
            if abs(M[r][j]) > abs(M[max_row][j]):
                max_row = r

        # 2. Skip column if no valid pivot exists (Matrix might be rank-deficient)
        if abs(M[max_row][j]) < eps:
            continue

        # 3. Swap rows
        if max_row != pivot_row:
            M[pivot_row], M[max_row] = M[max_row], M[pivot_row]
            swaps += 1

        # 4. Forward Elimination
        for r in range(pivot_row + 1, m):
            factor = M[r][j] / M[pivot_row][j]
            # Neutralize element at column j
            M[r][j] = 0.0  # Set explicitly to zero
            for k in range(j + 1, n + 1):
                M[r][k] -= factor * M[pivot_row][k]

        pivot_row += 1

    # 5. Extract U and c for back substitution
    U = [row[:n] for row in M]
    c = [row[n] for row in M]
    x = back_substitution(U, c, eps)

    return M, x, swaps
