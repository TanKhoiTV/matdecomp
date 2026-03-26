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
    n = len(A)
    # Tạo ma trận bổ sung [A|b] để thao tác hàng dễ dàng hơn
    M = [row[:] + [bi] for row, bi in zip(A, b)]
    swaps = 0

    # Giai đoạn 1: Khử xuôi (Forward Elimination)
    for i in range(n):
        # 1. Tìm hàng có phần tử lớn nhất ở cột i (Partial Pivoting)
        max_row = i
        for k in range(i + 1, n):
            if abs(M[k][i]) > abs(M[max_row][i]):
                max_row = k

        # Kiểm tra ma trận suy biến
        if abs(M[max_row][i]) < eps:
            raise ValueError("Matrix is singular or near-singular.")

        # 2. Hoán đổi hàng (nếu cần)
        if max_row != i:
            M[i], M[max_row] = M[max_row], M[i]
            swaps += 1

        # 3. Loại bỏ các phần tử dưới pivot
        for k in range(i + 1, n):
            factor = M[k][i] / M[i][i]
            # Cập nhật các phần tử còn lại của hàng k (bao gồm cả b)
            for j in range(i, n + 1):
                M[k][j] -= factor * M[i][j]

    # Giai đoạn 2: Thế ngược (Back Substitution)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        # Tính tổng các phần tử đã biết: sum(A[i][j] * x[j]) cho j > i
        sum_ax = sum(M[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (M[i][n] - sum_ax) / M[i][i]

    return x, swaps


# Ví dụ kiểm tra (Verification)
if __name__ == "__main__":
    # Hệ phương trình:
    # 2x + y - z = 8
    # -3x - y + 2z = -11
    # -2x + y + 2z = -3

    A_test = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
    b_test = [8, -11, -3]

    try:
        solution, total_swaps = gaussian_eliminate(A_test, b_test)
        print(f"Solution: {solution}")
        print(f"Total row swaps: {total_swaps}")
    except ValueError as e:
        print(f"Error: {e}")