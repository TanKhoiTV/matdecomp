import numpy as np
import math
from determinant import determinant


def is_close(a, b, rel_tol=1e-9, abs_tol=1e-9):
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def run_tests():
    # 1. Ma trận 2x2
    A_2x2 = [[3, 8], [4, 6]]
    assert is_close(determinant(A_2x2), np.linalg.det(A_2x2)), "Lỗi: Test ma trận 2x2 thất bại!"

    # 2. Ma trận 3x3
    A_3x3 = [[6, 1, 1], [4, -2, 5], [2, 8, 7]]
    assert is_close(determinant(A_3x3), np.linalg.det(A_3x3)), "Lỗi: Test ma trận 3x3 thất bại!"

    # 3. Ma trận suy biến
    A_singular = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert is_close(determinant(A_singular), 0.0), "Lỗi: Test ma trận suy biến thất bại!"

    # 4. Ma trận đơn vị
    A_identity = np.eye(4).tolist()
    assert is_close(determinant(A_identity), np.linalg.det(A_identity)), "Lỗi: Test ma trận đơn vị thất bại!"

    # 5. Ma trận có định thức âm
    A_negative = [[0, 1], [1, 0]]
    assert is_close(determinant(A_negative), np.linalg.det(A_negative)), "Lỗi: Test định thức âm thất bại!"

    print("Tuyệt vời! Toàn bộ 5 test cases đã PASS.")


if __name__ == "__main__":
    run_tests()
    