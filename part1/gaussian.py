from typing import List, Tuple


def back_substitution(U: List[List[float]], c: List[float], eps: float = 1e-12) -> List[float]:
    """
    Giải hệ phương trình tam giác trên Ux = c.
    Lưu ý: Đối với ma trận m x n, hàm này thường giải phần ma trận vuông hoặc các hệ phương trình có nghiệm.
    """
    n = len(U[0])  # Số lượng biến
    m = len(U)     # Số lượng phương trình
    x = [0.0] * n

    # Quá trình thế ngược bắt đầu từ hàng chứa phần tử trụ cuối cùng
    for i in range(min(m, n) - 1, -1, -1):
        if abs(U[i][i]) < eps:
            # Bỏ qua nếu phần tử trên đường chéo bằng 0 (hệ thiếu xác định hoặc vô nghiệm)
            continue

        sum_ax = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (c[i] - sum_ax) / U[i][i]
    return x


def gaussian_eliminate(
        A: List[List[float]], b: List[float], eps: float = 1e-12
) -> Tuple[List[List[float]], List[float], int]:
    """
    Thực hiện phép khử Gauss với kỹ thuật chọn phần tử trụ từng phần (partial pivoting) trên ma trận m x n.

    Tham số
    ----------
    A : List[List[float]]  - Ma trận hệ số kích thước m x n.
    b : List[float]        - Vế phải là một vector có độ dài m.
    eps : float            - Ngưỡng sai số cho phần tử trụ (pivot threshold).

    Trả về
    -------
    M : List[List[float]]  - Ma trận mở rộng đã được rút gọn [U|c] ở dạng bậc thang (REF).
    x : List[float]        - Một vector nghiệm tiềm năng.
    swaps : int            - Số lần hoán vị hàng đã thực hiện.
    """
    m = len(A)
    n = len(A[0])
    # Tạo ma trận mở rộng [A|b] kích thước m x (n+1)
    M = [row[:] + [bi] for row, bi in zip(A, b)]
    swaps = 0
    pivot_row = 0

    for j in range(n):  # Lặp qua các cột
        if pivot_row >= m:
            break

        # 1. Chọn phần tử trụ từng phần: Tìm giá trị lớn nhất trong cột hiện tại j từ pivot_row trở xuống
        max_row = pivot_row
        for r in range(pivot_row + 1, m):
            if abs(M[r][j]) > abs(M[max_row][j]):
                max_row = r

        # 2. Bỏ qua cột nếu không có phần tử trụ hợp lệ (Ma trận có thể bị suy biến/thiếu hạng)
        if abs(M[max_row][j]) < eps:
            continue

        # 3. Hoán vị các hàng
        if max_row != pivot_row:
            M[pivot_row], M[max_row] = M[max_row], M[pivot_row]
            swaps += 1

        # 4. Khử xuôi (Forward Elimination)
        for r in range(pivot_row + 1, m):
            factor = M[r][j] / M[pivot_row][j]
            # Triệt tiêu (đưa về 0) phần tử ở cột j
            M[r][j] = 0.0  # Gán trực tiếp bằng 0
            for k in range(j + 1, n + 1):
                M[r][k] -= factor * M[pivot_row][k]

        pivot_row += 1

    # 5. Trích xuất U và c để thực hiện thế ngược
    U = [row[:n] for row in M]
    c = [row[n] for row in M]
    x = back_substitution(U, c, eps)

    return M, x, swaps
