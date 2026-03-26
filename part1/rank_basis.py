import numpy as np


def compute_rref(A, eps=1e-12):
    """Đưa ma trận A về dạng Bậc thang rút gọn (RREF) dùng khử toàn phần."""
    M = np.array(A, dtype=float).copy()
    rows, cols = M.shape
    pivot_row = 0
    pivot_cols = []

    for j in range(cols):
        if pivot_row >= rows:
            break

        # 1. Tìm Pivot (phần tử lớn nhất trong cột để ổn định số học)
        max_row = pivot_row + np.argmax(np.abs(M[pivot_row:, j]))
        if abs(M[max_row, j]) < eps:
            continue

        # 2. Đổi hàng
        M[[pivot_row, max_row]] = M[[max_row, pivot_row]]
        pivot_cols.append(j)

        # 3. Chuẩn hóa hàng pivot về 1
        M[pivot_row] = M[pivot_row] / M[pivot_row, j]

        # 4. Khử tất cả các hàng khác (cả trên và dưới)
        for i in range(rows):
            if i != pivot_row:
                M[i] = M[i] - M[i, j] * M[pivot_row]

        pivot_row += 1

    return M, pivot_cols


def rank_and_basis(A, eps=1e-12):
    """Tính toán Rank và Cơ sở cho 3 không gian con."""
    A_np = np.array(A, dtype=float)
    rows, cols = A_np.shape
    RREF, pivot_cols = compute_rref(A_np, eps)

    rank = len(pivot_cols)

    # Column Space: Lấy cột của ma trận GỐC tại vị trí pivot
    col_space = [A_np[:, j].tolist() for j in pivot_cols]

    # Row Space: Các hàng khác không của RREF
    row_space = [row.tolist() for row in RREF if np.any(np.abs(row) > eps)]

    # Null Space: Nghiệm của Rx = 0
    null_space = []
    free_vars = [j for j in range(cols) if j not in pivot_cols]

    for f_col in free_vars:
        vec = [0.0] * cols
        vec[f_col] = 1.0
        for i, p_col in enumerate(pivot_cols):
            # i là chỉ số hàng chứa pivot của cột p_col trong RREF
            vec[p_col] = -RREF[i, f_col]
        null_space.append(vec)

    return rank, col_space, row_space, null_space
