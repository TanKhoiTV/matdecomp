from pathlib import Path


def back_substitution(U, c, eps=1e-12):
    """
    Solve upper-triangular system Ux = c via backward substitution.

    Parameters
    ----------
    U : list[list[float]]  — n x n upper-triangular matrix
    c : list[float]        — right-hand side vector of length n
    eps : float            — pivot threshold below which matrix is singular

    Returns
    -------
    x : list[float]        — solution vector

    Raises
    ------
    ValueError             — if |diagonal element| < eps
    """
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        if abs(U[i][i]) < eps:
            raise ValueError(f"Near-zero diagonal element at index {i}.")

        sum_ax = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (c[i] - sum_ax) / U[i][i]
    return x


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
    M : list[list[float]]  — reduced augmented matrix [U|c]
    x : list[float]        — solution vector
    s : int                — number of row swaps performed

    Raises
    ------
    ValueError             — if |pivot| < eps (singular or near-singular matrix)
    """
    n = len(A)
    # Tạo ma trận bổ sung [A|b]
    M = [row[:] + [bi] for row, bi in zip(A, b)]
    swaps = 0

    for i in range(n):
        # 1. Partial pivoting: Chọn hàng có trị tuyệt đối lớn nhất tại cột i
        max_row = i
        for k in range(i + 1, n):
            if abs(M[k][i]) > abs(M[max_row][i]):
                max_row = k

        # 2. Kiểm tra ma trận suy biến
        if abs(M[max_row][i]) < eps:
            raise ValueError(f"Matrix is singular: pivot at index {i} is below epsilon {eps}")

        # 3. Hoán đổi hàng
        if max_row != i:
            M[i], M[max_row] = M[max_row], M[i]
            swaps += 1

        # 4. Khử xuôi (Forward Elimination)
        for k in range(i + 1, n):
            factor = M[k][i] / M[i][i]
            for j in range(i, n + 1):
                M[k][j] -= factor * M[i][j]

    # 5. Tách ma trận tam giác trên U và vector c từ ma trận bổ sung M
    U = [row[:n] for row in M]
    c = [row[n] for row in M]

    # 6. Thế ngược để tìm x
    x = back_substitution(U, c, eps)

    return M, x, swaps