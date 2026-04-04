from typing import List, Tuple
from math import atan2, sin, cos, sqrt


def transpose(A: List[List[float]]) -> List[List[float]]:
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    m, p = len(A), len(B[0])
    n = len(B)
    result = [[0.0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def get_identity_matrix(n: int) -> List[List[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def jacobi_eigenvalues(S: List[List[float]], error_tolerance: float = 1e-10) -> Tuple[List[float], List[List[float]]]:
    n = len(S)

    # V tích lũy các phép quay -> cuối cùng chứa vector riêng
    V = get_identity_matrix(n)

    max_iterations = 100
    is_converged = False

    for _ in range(max_iterations):
        # tìm phần tử lớn nhất nằm ngoài đường chéo
        max_val = 0.0
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(S[i][j]) > max_val:
                    max_val = abs(S[i][j])
                    p, q = i, j

        # nếu tất cả các phần tử đủ nhỏ -> đã hội tụ
        if max_val < error_tolerance:
            is_converged = True
            break

        # tính góc xoay Jacobi
        # tan(2 * theta) = 2 * S[p][q] / (S[q][q] - S[p][p])
        phi = 0.5 * atan2(2 * S[p][q], S[q][q] - S[p][p])
        # cos và sin của góc xoay
        c, s = cos(phi), sin(phi)

        s_pp, s_qq = S[p][p], S[q][q]
        # công thức biến đổi tương tự A' = J^T * A * J
        S[p][p] = c ** 2 * s_pp - 2 * s * c * S[p][q] + s ** 2 * s_qq
        S[q][q] = s ** 2 * s_pp + 2 * s * c * S[p][q] + c ** 2 * s_qq
        S[p][q] = S[q][p] = 0.0

        # cập nhật các hàng và cột p và q
        for i in range(n):
            if i != p and i != q:
                s_ip, s_iq = S[i][p], S[i][q]
                # áp dụng phép xoay lên các phần tử
                S[i][p] = S[p][i] = c * s_ip - s * s_iq
                S[i][q] = S[q][i] = s * s_ip + c * s_iq
        
        # tích lũy phép quay
        for i in range(n):
            v_ip, v_iq = V[i][p], V[i][q]
            V[i][p] = c * v_ip - s * v_iq
            V[i][q] = s * v_ip + c * v_iq
    
    if not is_converged:
        raise ValueError(f"Numerical instability: Failed to converge within {max_iterations} iterations")
    
    # sau khi hội tụ, ma trận S gần như chéo -> các phần tử nằm trên đường chéo là trị riêng
    eigenvalues = [S[i][i] for i in range(n)]
    
    return eigenvalues, V

def svd_decompose(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]], List[List[float]]]:
    """
    Phân tách giá trị suy biến (Singular Value Decomposition - SVD) của một ma trận.

    Phân tách một ma trận A kích thước (m x n) thành tích của ba ma trận:
        A = U * Σ * V^T

    trong đó:
    - U: Ma trận trực giao (m x m) chứa các vector suy biến trái (left singular vectors).
        Các cột của U là vector riêng của ma trận (A * A^T).
    - Σ: Ma trận đường chéo (m x n) chứa các giá trị suy biến (singular values).
        Sắp xếp giảm dần trên đường chéo chính.
    - V^T: Chuyển vị của ma trận trực giao V (n x n) chứa các vector suy biến phải (right singular vectors).
        Các cột của V là các vector riêng của ma trận (A^T * A).

    Mối liên hệ với Eigen-decomposition:
    - Các giá trị suy biến σ_i là căn bậc hai của các trị riêng không âm của ma trận (A^T * A).
    - SVD là dạng tổng quát hóa của Diagonalization áp dụng được cho cả ma trận không vuông và ma trận thiếu hạng.

    Thuật toán:
        1. Tính ma trận tích (A^T * A)
        2. Phân tách trị riêng trên (A^T * A) để tìm ma trận V và các trị riêng λ.
        3. Tính các giá trị suy biến σ_i bằng cách lấy căn bậc hai λ_i. Xây dựng ma trận Σ.
        4. Tính ma trận U bằng công thức u_i = (1/σ_i) * A * v_i cho các σ_i > 0.
        5. Xử lý các trường hợp đặc biệt: ma trận chữ nhật (m != n) và ma trận thiếu hạng.
    
    Độ phức tạp:
    - Phân tách: O(n^3) hoặc O(m * n^2) tùy thuộc thuật toán thực thi cụ thể.
    - Giải hệ: O(n^2) sau khi đã có dạng phân tách SVD.
    """
    if not A or not A[0]:
        raise ValueError("Input matrix is empty")
    
    m = len(A)
    n = len(A[0])

    AT = transpose(A)
    ATA = multiply(AT, A)

    try:
        lambdas, V = jacobi_eigenvalues(ATA)
    except ValueError as e:
        raise RuntimeError(f"SVD failed due to Jacobi eigenvalue error: {e}")
    
    for l in lambdas:
        if l != l:
            raise ArithmeticError("Numerical instability: NaN values proceed during decomposition")

    sigmas = [sqrt(max(0.0, l)) for l in lambdas]

    indices = list(range(n))
    indices.sort(key=lambda i: sigmas[i], reverse=True)

    sorted_sigmas = [sigmas[i] for i in indices]
    V_sorted = [[V[row][i] for i in indices] for row in range(n)]

    Sigma = [[0.0 for _ in range(n)] for _ in range(m)]
    for i in range(min(m, n)):
        Sigma[i][i] = sorted_sigmas[i]

    U = [[0.0 for _ in range(m)] for _ in range(m)]

    for i in range(min(m, n)):
        if sorted_sigmas[i] > 1e-10:
            for r in range(m):
                col_sum = 0.0
                for c in range(n):
                    col_sum += A[r][c] * V_sorted[c][i]
                U[r][i] = col_sum / sorted_sigmas[i]

            norm = sqrt(sum(U[r][i] ** 2 for r in range(m)))
            if norm > 1e-10:
                for r in range(m):
                    U[r][i] /= norm

    for i in range(min(m, n), m):
        U[i][i] = 1.0

        for j in range(i):
            product = sum(U[r][i] * U[r][j] for r in range(m))
            for r in range(m):
                U[r][i] -= product * U[r][j]
        
        norm = sqrt(sum(U[r][i] ** 2 for r in range(m)))
        if norm > 1e-10:
            for r in range(m):
                U[r][i] /= norm

    VT = transpose(V_sorted)

    return U, Sigma, VT
