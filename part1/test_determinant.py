import numpy as np
import math
from determinant import determinant


def test_determinant_2x2():
    A = [[3, 8], [4, 6]]
    assert math.isclose(determinant(A), float(np.linalg.det(A)), abs_tol=1e-9)


def test_determinant_3x3():
    A = [[6, 1, 1], [4, -2, 5], [2, 8, 7]]
    assert math.isclose(determinant(A), float(np.linalg.det(A)), abs_tol=1e-9)


def test_determinant_singular():
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert math.isclose(determinant(A), 0.0, abs_tol=1e-9)


def test_determinant_identity():
    A = np.eye(4).tolist()
    assert math.isclose(determinant(A), float(np.linalg.det(A)), abs_tol=1e-9)


def test_determinant_negative():
    A = [[0, 1], [1, 0]]
    assert math.isclose(determinant(A), float(np.linalg.det(A)), abs_tol=1e-9)


def test_determinant_zero_input():
    A = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert math.isclose(determinant(A), 0.0, abs_tol=1e-9)
