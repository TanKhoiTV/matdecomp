import numpy as np


def compute_rref(A, eps=1e-12):
    """Đưa ma trận A về dạng Bậc thang rút gọn (RREF)."""
    M = [row[:] for row in A]
    rows = len(M)
    cols = len(M[0])
    pivot_row = 0
    pivot_cols = []

    for j in range(cols):
        if pivot_row >= rows:
            break

        # Tìm hàng có giá trị lớn nhất ở cột j (Partial Pivoting)
        max_row = pivot_row
        for i in range(pivot_row + 1, rows):
            if abs(M[i][j]) > abs(M[max_row][j]):
                max_row = i

        if abs(M[max_row][j]) < eps:
            continue

        M[pivot_row], M[max_row] = M[max_row], M[pivot_row]
        pivot_cols.append(j)

        # Đưa phần tử chốt (pivot) về 1
        pivot_val = M[pivot_row][j]
        M[pivot_row] = [val / pivot_val for val in M[pivot_row]]

        # Khử các phần tử ở các hàng khác (cả trên và dưới pivot)
        for i in range(rows):
            if i != pivot_row:
                factor = M[i][j]
                M[i] = [M[i][k] - factor * M[pivot_row][k] for k in range(cols)]

        pivot_row += 1

    return M, pivot_cols


def rank_and_basis(A, eps=1e-12):
    """
    Compute rank and basis vectors for fundamental subspaces.

    Returns: rank, column_space, row_space, null_space
    """
    A_array = np.array(A, dtype=float)
    rows, cols = A_array.shape
    RREF, pivot_cols = compute_rref(A)

    rank = len(pivot_cols)

    # 1. Row Space Basis (Các hàng khác không của RREF)
    row_space = [row for row in RREF if any(abs(val) > eps for val in row)]

    # 2. Column Space Basis (Các cột của ma trận GỐC tại vị trí pivot)
    col_space = [A_array[:, j].tolist() for j in pivot_cols]

    # 3. Null Space Basis (Nghiệm tham số Rx = 0)
    null_space = []
    free_vars = [j for j in range(cols) if j not in pivot_cols]

    for free_col in free_vars:
        vec = [0.0] * cols
        vec[free_col] = 1.0
        for i, p_col in enumerate(pivot_cols):
            # i là chỉ số hàng của pivot thứ i trong RREF
            vec[p_col] = -RREF[i][free_col]
        null_space.append(vec)

    return rank, col_space, row_space, null_space