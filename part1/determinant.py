import sys
from typing import Sequence


def determinant(A: Sequence[Sequence[float | int]]) -> float:
    """
    Tính định thức của ma trận vuông A bằng phép khử Gauss (Pure Python).
    Trả về 0.0 nếu ma trận suy biến.
    """
    n = len(A)
    if n == 0:
        return 1.0
    for row in A:
        if len(row) != n:
            raise ValueError("Ma trận phải là ma trận vuông.")

    mat: list[list[float]] = [[float(val) for val in row] for row in A]
    
    max_abs_val = 0.0
    for row in mat:
        for val in row:
            if abs(val) > max_abs_val:
                max_abs_val = abs(val)
    
    tol = max(max_abs_val, 1.0) * sys.float_info.epsilon * 10
    swap_count: int = 0

    for i in range(n):
        pivot_row = i
        max_val = abs(mat[i][i])
        for j in range(i + 1, n):
            if abs(mat[j][i]) > max_val:
                max_val = abs(mat[j][i])
                pivot_row = j

        if abs(mat[pivot_row][i]) <= tol:
            return 0.0

        if pivot_row != i:
            mat[i], mat[pivot_row] = mat[pivot_row], mat[i]
            swap_count += 1

        for j in range(i + 1, n):
            factor = mat[j][i] / mat[i][i]
            for k in range(i, n):
                mat[j][k] -= factor * mat[i][k]

    det_val: float = 1.0
    for i in range(n):
        det_val *= mat[i][i]

    return float(((-1) ** swap_count) * det_val)