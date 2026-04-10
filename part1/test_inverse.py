import numpy as np
import pytest
from inverse import inverse


def verify_inverse_matrix(A):
    """Hàm hỗ trợ: Nhân A với A^-1 và kiểm tra xem có ra ma trận đơn vị I không."""
    A_inv = inverse(A)
    res = np.dot(np.array(A), np.array(A_inv))
    assert np.allclose(res, np.eye(len(A)), atol=1e-9)


def test_inverse_2x2():
    verify_inverse_matrix([[4, 7], [2, 6]])


def test_inverse_3x3():
    verify_inverse_matrix([[1, 2, 3], [0, 1, 4], [5, 6, 0]])


def test_inverse_identity():
    verify_inverse_matrix(np.eye(3).tolist())


def test_inverse_diagonal():
    verify_inverse_matrix([[2, 0, 0], [0, 5, 0], [0, 0, 8]])


def test_inverse_singular_raises_error():
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    with pytest.raises(ValueError):
        inverse(A)


def test_inverse_zero_input_raises_error():
    A = [[0, 0], [0, 0]]
    with pytest.raises(ValueError):
        inverse(A)
