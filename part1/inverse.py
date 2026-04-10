from typing import Sequence


def inverse(A: Sequence[Sequence[float | int]]) -> list[list[float]]:
    """
    Tính ma trận nghịch đảo A^-1 bằng phương pháp Gauss-Jordan trên ma trận ghép [A|I].
    Ném lỗi ValueError nếu ma trận suy biến (det = 0).
    """
    n = len(A)
    # 1. Kiểm tra ma trận vuông
    for row in A:
        if len(row) != n:
            raise ValueError("Ma trận phải là ma trận vuông.")

    # 2.ma trận ghép [A | I]
    # mat sẽ là ma trận n hàng, 2n cột
    mat: list[list[float]] = []
    for i in range(n):
        identity_row = [1.0 if j == i else 0.0 for j in range(n)]
        mat.append([float(x) for x in A[i]] + identity_row)

    # 3.khử Gauss-Jordan
    for i in range(n):
        # Tìm pivot lớn nhất để tránh sai số và chia cho 0
        pivot_row = i
        max_val = abs(mat[i][i])
        for k in range(i + 1, n):
            if abs(mat[k][i]) > max_val:
                max_val = abs(mat[k][i])
                pivot_row = k

        # Kiểm tra ma trận suy biến
        if abs(mat[pivot_row][i]) < 1e-12:
            raise ValueError("Ma trận suy biến (định thức bằng 0), không có nghịch đảo.")

        # Hoán đổi hàng
        mat[i], mat[pivot_row] = mat[pivot_row], mat[i]

        # Chuẩn hóa hàng i
        pivot_val = mat[i][i]
        for j in range(i, 2 * n):
            mat[i][j] /= pivot_val

        # Khử các phần tử ở các hàng khác
        for k in range(n):
            if k != i:
                factor = mat[k][i]
                for j in range(i, 2 * n):
                    mat[k][j] -= factor * mat[i][j]

    # 4. Tách lấy vế phải
    inv_matrix = [row[n:] for row in mat]
    return inv_matrix