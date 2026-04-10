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
        
    if n == 0:
        return []
        
    for row in A:
        if len(row) != n:
            raise ValueError("Ma trận A phải là ma trận vuông.")
            
    if max_iter <= 0:
        raise ValueError("Số vòng lặp tối đa max_iter phải lớn hơn 0.")

    for i in range(n):
        if A[i][i] == 0:
            raise ValueError(f"Phần tử trên đường chéo chính A[{i}][{i}] bằng 0, không thể chia được.")

    if not is_diagonally_dominant(A):
        warnings.warn("Ma trận không chéo trội. Phương pháp Gauss-Seidel có thể không hội tụ.", stacklevel=2)

    x = [0.0] * n
    diff = float('inf')
    
    for k in range(max_iter):
        x_new = x[:]
        
        for i in range(n):
            sum_new = sum(A[i][j] * x_new[j] for j in range(i))
            sum_old = sum(A[i][j] * x[j] for j in range(i + 1, n))
            
            x_new[i] = (b[i] - sum_new - sum_old) / A[i][i]
            
        diff = max(abs(x_new[i] - x[i]) for i in range(n))
        if diff < tolerance:
            return x_new
            
        x = x_new
        
    warnings.warn(f"Thuật toán không hội tụ sau {max_iter} vòng lặp (sai số hiện tại: {diff}).", stacklevel=2)
    return x
