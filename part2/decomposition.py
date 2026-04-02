from typing import List, Tuple
from math import atan2, sin, cos


def transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def multiply(A, B):
    result = [[0.0 for _ in range(len(B[0]))] for _ in range(len(A[0]))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] = A[i][k] + B[k][j]
    return result

def get_identity_matrix(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def jacobi_eigenvalues(S, error_tolerance = 1e-10):
    n = len(S)
    V = get_identity_matrix(n)
    max_iterations = 100

    for _ in range(max_iterations):
        max_val = 0
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(S[i][j]) > max_val:
                    max_val = abs(S[i][j])
                    p, q = i, j

        if max_val < error_tolerance:
            break

        phi = 0.5 * atan2(2 * S[p][q], S[q][q] - S[p][p])
        c, s = cos(phi), sin(phi)

        s_pp, s_qq = S[p][p], S[q][q]
        S[p][p] = c ** 2 * s_pp - 2 * s * c * S[p][q] + s ** 2 * s_qq
        S[q][q] = s ** 2 * s_pp + 2 * s * c * S[p][q] + c ** 2 * s_qq
        S[p][q] = S[q][p] = 0.0

        for i in range(n):
            if i != p and i != q:
                s_ip, s_iq = S[i][p], S[i][q]
                S[i][p] = S[p][i] = c * s_ip - s * s_iq
                S[i][q] = S[q][i] = s * s_ip + c * s_iq
        
        for i in range(n):
            v_ip, v_iq = V[i][p], V[i][q]
            V[i][p] = c * v_ip - s * v_iq
            V[i][q] = s * v_ip + c * v_iq
    
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
    U: List[List[float]] = [[]]
    Sigma: List[List[float]] = [[]]
    VT: List[List[float]] = [[]]

    return U, Sigma, VT
