import numpy as np
import math
from determinant import determinant

def test_determinant():
    A_2x2 = [[3, 8], [4, 6]]
    assert math.isclose(determinant(A_2x2), np.linalg.det(A_2x2)), "Lỗi 2x2"

    A_3x3 = [[6, 1, 1], [4, -2, 5], [2, 8, 7]]
    assert math.isclose(determinant(A_3x3), np.linalg.det(A_3x3)), "Lỗi 3x3"

    A_singular = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert math.isclose(determinant(A_singular), 0.0), "Lỗi suy biến"

    A_identity = np.eye(4).tolist()
    assert math.isclose(determinant(A_identity), np.linalg.det(A_identity)), "Lỗi đơn vị"

    A_negative = [[0, 1], [1, 0]]
    assert math.isclose(determinant(A_negative), np.linalg.det(A_negative)), "Lỗi âm"