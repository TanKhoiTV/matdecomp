import warnings
from typing import Sequence

def is_diagonally_dominant(A: Sequence[Sequence[float]]) -> bool:
    """Kiểm tra ma trận chéo trội hàng (Row Diagonal Dominance)."""
    n = len(A)
    for i in range(n):
        sum_other = sum(abs(A[i][j]) for j in range(n) if j != i)
        if abs(A[i][i]) < sum_other:
            return False
    return True

def gauss_seidel(
    A: Sequence[Sequence[float]], 
    b: Sequence[float], 
    tolerance: float = 1e-6, 
    max_iter: int = 1000
) -> list[float]:
    """
    Giải hệ phương trình Ax = b bằng phương pháp Gauss-Seidel.
    """
    n = len(A)
    if len(b) != n:
        raise ValueError("Kích thước ma trận A và vector b không khớp.")

    for i in range(n):
        if A[i][i] == 0:
            raise ValueError(f"Phần tử trên đường chéo chính A[{i}][{i}] bằng 0, không thể chia được.")

    # Tiêu chí 3: Kiểm tra chéo trội và cảnh báo
    if not is_diagonally_dominant(A):
        warnings.warn("Ma trận không chéo trội. Phương pháp Gauss-Seidel có thể không hội tụ.")

    x = [0.0] * n  # Khởi tạo nghiệm ban đầu là vector 0
    
    for k in range(max_iter):
        x_new = x[:]  # Sao chép x hiện tại
        
        for i in range(n):
            # Tiêu chí 1: Áp dụng công thức Gauss-Seidel
            # sum_new: tổng các phần tử đã cập nhật ở vòng lặp hiện tại (j < i)
            sum_new = sum(A[i][j] * x_new[j] for j in range(i))
            # sum_old: tổng các phần tử chưa cập nhật (j > i)
            sum_old = sum(A[i][j] * x[j] for j in range(i + 1, n))
            
            x_new[i] = (b[i] - sum_new - sum_old) / A[i][i]
            
        # Tiêu chí 2: Kiểm tra hội tụ (tính chuẩn khoảng cách ||x^(k+1) - x^(k)||)
        # Sử dụng chuẩn vô cùng (max absolute difference)
        diff = max(abs(x_new[i] - x[i]) for i in range(n))
        if diff < tolerance:
            return x_new  # Đạt đủ độ chính xác thì dừng
            
        x = x_new
        
    warnings.warn(f"Thuật toán không hội tụ sau {max_iter} vòng lặp (sai số hiện tại: {diff}).")
    return x
