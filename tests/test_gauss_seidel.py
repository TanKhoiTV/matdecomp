import pytest
import numpy as np
import warnings
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from part3.solvers import gauss_seidel

def test_diagonally_dominant():
    A1 = [[4.0, 1.0, -1.0], [2.0, 7.0, 1.0], [1.0, -3.0, 12.0]]
    b1 = [3.0, 19.0, 31.0]
    x1 = gauss_seidel(A1, b1)
    expected_x1 = np.linalg.solve(A1, b1)
    assert np.allclose(x1, expected_x1, atol=1e-5)

def test_spd_matrix():
    A2 = [[2.0, -1.0, 0.0], [-1.0, 2.0, -1.0], [0.0, -1.0, 2.0]]
    b2 = [1.0, 0.0, 1.0]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        x2 = gauss_seidel(A2, b2)
    expected_x2 = np.linalg.solve(A2, b2)
    assert np.allclose(x2, expected_x2, atol=1e-5)

def test_non_convergent_warning():
    A3 = [[1.0, 3.0], [4.0, 1.0]]
    b3 = [4.0, 5.0]
    # [FIX] Đổi từ khóa match dài ra để chỉ bắt trúng cảnh báo hết max_iter
    with pytest.warns(UserWarning, match="Thuật toán không hội tụ sau"):
        gauss_seidel(A3, b3, max_iter=50)

def test_comparison_to_gauss():
    A4 = [[10., -1., 2., 0.], [-1., 11., -1., 3.], [2., -1., 10., -1.], [0., 3., -1., 8.]]
    b4 = [6., 25., -11., 15.]
    x4_gs = gauss_seidel(A4, b4, tolerance=1e-8)
    x4_gauss = np.linalg.solve(A4, b4)
    assert np.allclose(x4_gs, x4_gauss, atol=1e-6)

def test_zero_on_diagonal():
    A5 = [[0.0, 2.0], [3.0, 4.0]]
    b5 = [1.0, 2.0]
    with pytest.raises(ValueError, match="bằng 0, không thể chia được"):
        gauss_seidel(A5, b5)
