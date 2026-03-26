from typing import List, Tuple


def compute_rref(A: List[List[float]], eps: float = 1e-12) -> Tuple[List[List[float]], List[int]]:
    """
    Transforms a matrix into its Reduced Row Echelon Form (RREF).

    Purpose: Used to identify pivot positions for rank and basis calculations.
    Parameters:
        A: The input m x n matrix (List of Lists).
        eps: Threshold for zero-comparison.
    Returns:
        M: The matrix in RREF.
        pivot_cols: List of indices of columns containing pivots.
    Raises:
        ValueError: If matrix A is empty or rows have inconsistent lengths.
    """
    if not A or not A[0]:
        raise ValueError("Matrix cannot be empty.")

    num_cols = len(A[0])
    if any(len(row) != num_cols for row in A):
        raise ValueError("Inconsistent row lengths.")

    m_matrix = [row[:] for row in A]
    rows, cols = len(m_matrix), num_cols
    pivot_row = 0
    pivot_cols = []

    for j in range(cols):
        if pivot_row >= rows:
            break

        max_val = -1.0
        max_row = -1
        for r in range(pivot_row, rows):
            if abs(m_matrix[r][j]) > max_val:
                max_val = abs(m_matrix[r][j])
                max_row = r

        if max_row == -1 or max_val < eps:
            continue

        m_matrix[pivot_row], m_matrix[max_row] = m_matrix[max_row], m_matrix[pivot_row]

        pivot_val = m_matrix[pivot_row][j]
        m_matrix[pivot_row] = [x / pivot_val for x in m_matrix[pivot_row]]

        for i in range(rows):
            if i != pivot_row:
                factor = m_matrix[i][j]
                m_matrix[i] = [m_matrix[i][k] - factor * m_matrix[pivot_row][k] for k in range(cols)]

        pivot_cols.append(j)
        pivot_row += 1

    return m_matrix, pivot_cols


def rank_and_basis(
        A: List[List[float]], eps: float = 1e-12
) -> Tuple[int, List[List[float]], List[List[float]], List[List[float]]]:
    """
    Computes rank and basis vectors for Column, Row, and Null spaces.

    Purpose: Fulfills GitHub Issue #18 requirements for fundamental subspaces.
    Parameters:
        A: Input m x n matrix.
        eps: Zero-comparison threshold.
    Returns:
        rank: Number of pivots.
        col_space: Basis vectors for Column Space (from original A).
        row_space: Basis vectors for Row Space (non-zero RREF rows).
        null_space: Basis vectors for Null Space (parametric solutions).
    """
    rows = len(A)
    cols = len(A[0]) if rows > 0 else 0
    rref_matrix, pivot_cols = compute_rref(A, eps)
    rank = len(pivot_cols)

    # 1. Column Space Basis (Columns of original A at pivot indices)
    col_space = [[A[i][j] for i in range(rows)] for j in pivot_cols]

    # 2. Row Space Basis (Non-zero rows of RREF)
    row_space = [row[:] for row in rref_matrix if any(abs(x) > eps for x in row)]

    # 3. Null Space Basis (Parametric solution Ax = 0)
    null_space = []
    free_vars = [j for j in range(cols) if j not in pivot_cols]

    for f_col in free_vars:
        vec = [0.0] * cols
        vec[f_col] = 1.0  # Set current free variable to 1
        for i, p_col in enumerate(pivot_cols):
            # Pivot variable x_p = - (R_i,f1 * x_f1 + R_i,f2 * x_f2 ...)
            vec[p_col] = -rref_matrix[i][f_col]
        null_space.append(vec)

    return rank, col_space, row_space, null_space
