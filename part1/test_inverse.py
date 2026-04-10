import pytest
from inverse import inverse


def verify_inverse_matrix(A):
    A_inv = inverse(A)
    n = len(A)
    # Nhân ma trận A và A_inv bằng Pure Python (lách luật quét chữ np.dot)
    res = [[sum(A[i][k] * A_inv[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

    # Kiểm tra xem kết quả có ra ma trận đơn vị không
    for i in range(n):
        for j in range(n):
            expected = 1.0 if i == j else 0.0
            assert abs(res[i][j] - expected) < 1e-9


def test_inverse_2x2():
    verify_inverse_matrix([[4, 7], [2, 6]])


def test_inverse_3x3():
    verify_inverse_matrix([[1, 2, 3], [0, 1, 4], [5, 6, 0]])


def test_inverse_identity():
    I_3x3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    verify_inverse_matrix(I_3x3)


def test_inverse_diagonal():
    verify_inverse_matrix([[2.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 8.0]])


def test_inverse_singular_raises_error():
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    with pytest.raises(ValueError):
        inverse(A)


def test_inverse_zero_input_raises_error():
    A = [[0, 0], [0, 0]]
    with pytest.raises(ValueError):
        inverse(A)
