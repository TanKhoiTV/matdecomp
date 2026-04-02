from typing import List, Tuple


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
