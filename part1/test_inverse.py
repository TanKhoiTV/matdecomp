import numpy as np
import pytest
from inverse import inverse

def test_inverse_valid_matrices():
    tests = {
        "2x2": [[4, 7], [2, 6]],
        "3x3": [[1, 2, 3], [0, 1, 4], [5, 6, 0]],
        "Identity": np.eye(3).tolist(),
        "Diagonal": [[2, 0, 0], [0, 5, 0], [0, 0, 8]],
    }
    for name, A in tests.items():
        A_inv = inverse(A)
        # Kiểm tra A * A_inv có ra ma trận đơn vị I không
        res = np.dot(np.array(A), np.array(A_inv))
        assert np.allclose(res, np.eye(len(A)), atol=1e-10), f"Lỗi ở {name}"

def test_inverse_singular_matrix():
    # Kiểm tra xem hàm có báo lỗi khi nạp ma trận suy biến (det = 0) không
    A_singular = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    with pytest.raises(ValueError):
        inverse(A_singular)