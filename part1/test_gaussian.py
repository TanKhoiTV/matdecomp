import numpy as np
import pytest
from gaussian import gaussian_eliminate

def test_gaussian_all_cases():
    print("\n--- Running 5 mandatory test cases ---")

    # 1. Regular Case (Hệ 3x3 bình thường)
    A1 = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
    b1 = [8, -11, -3]
    _, x1, _ = gaussian_eliminate(A1, b1)
    assert np.allclose(x1, np.linalg.solve(A1, b1)), "Failed Regular Case"
    print("Test 1 (Regular): PASSED")

    # 2. Identity Matrix (Ma trận đơn vị)
    A2 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    b2 = [5, -2, 10]
    _, x2, _ = gaussian_eliminate(A2, b2)
    assert x2 == b2, "Failed Identity Case"
    print("Test 2 (Identity): PASSED")

    # 3. Singular Matrix (Ma trận suy biến - Phải báo lỗi)
    A3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    b3 = [1, 1, 1]
    with pytest.raises(ValueError, match="Matrix is singular"):
        gaussian_eliminate(A3, b3)
    print("Test 3 (Singular): PASSED (Caught ValueError)")

    # 4. Near-singular (Mọi phần tử trong cột chốt đều < epsilon)
    # Với eps mặc định là 1e-12
    A4 = [[1e-13, 0.5], [1e-14, 1.0]]  # Cả 1e-13 và 1e-14 đều nhỏ hơn 1e-12
    b4 = [1, 2]
    with pytest.raises(ValueError):
        gaussian_eliminate(A4, b4)
    print("Test 4 (Near-singular): PASSED (Caught ValueError)")

    # 5. Rectangular-like / Swaps check
    # Hệ cần đổi hàng: hàng 1 có pivot = 0
    A5 = [[0, 1], [1, 1]]
    b5 = [1, 2]
    M5, x5, s5 = gaussian_eliminate(A5, b5)
    assert s5 > 0, "Should have performed at least 1 swap"
    assert np.allclose(x5, [1.0, 1.0]), "Failed Swap Case"
    print("Test 5 (Swaps/Pivot): PASSED")

if __name__ == "__main__":
    test_gaussian_all_cases()