import numpy as np
from gaussian_eliminate import gaussian_eliminate

def verify_solution(A, b, x_custom):
    """
    Sử dụng numpy.linalg.solve để xác minh tính chính xác
    """
    try:
        x_np = np.linalg.solve(np.array(A), np.array(b)).tolist()
        # So sánh sai số giữa kết quả custom và numpy
        return np.allclose(x_custom, x_np, atol=1e-8)
    except np.linalg.LinAlgError:
        return None

def run_tests():
    print("--- Bắt đầu kiểm thử Gaussian Elimination ---\n")

    # Test Case 1: Hệ phương trình cơ bản 3x3
    A1 = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
    b1 = [8, -11, -3]
    print("Test 1 (Cơ bản 3x3):", end=" ")
    x1, _ = gaussian_eliminate(A1, b1)
    assert verify_solution(A1, b1, x1), "Kết quả không khớp với NumPy"
    print("PASSED")

    # Test Case 2: Ma trận cần hoán đổi hàng (Partial Pivoting)
    # Pivot tại hàng đầu tiên bằng 0
    A2 = [[0, 1, 1], [2, 4, -2], [0, 3, 15]]
    b2 = [4, 2, 36]
    print("Test 2 (Cần đổi hàng - Pivot=0):", end=" ")
    x2, swaps = gaussian_eliminate(A2, b2)
    assert swaps > 0, "Lẽ ra phải có hoán đổi hàng"
    assert verify_solution(A2, b2, x2), "Kết quả không khớp với NumPy"
    print(f"PASSED (Swaps: {swaps})")

    # Test Case 3: Ma trận đơn vị (Identity Matrix)
    A3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    b3 = [5, -2, 10]
    print("Test 3 (Ma trận đơn vị):", end=" ")
    x3, _ = gaussian_eliminate(A3, b3)
    assert x3 == b3, "Kết quả phải bằng vector b"
    print("PASSED")

    # Test Case 4: Ma trận suy biến (Singular Matrix - Vô nghiệm hoặc vô số nghiệm)
    A4 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    b4 = [1, 1, 1]
    print("Test 4 (Ma trận suy biến):", end=" ")
    try:
        gaussian_eliminate(A4, b4)
        print("FAILED (Không bắt được lỗi Singular)")
    except ValueError as e:
        print(f"PASSED (Lỗi mong đợi: {e})")

    # Test Case 5: Hệ phương trình 4x4 số thực ngẫu nhiên
    A5 = [[10, -7, 0, 1], [-3, 2, 6, 2], [5, -1, 5, -1], [2, 1, 0, 5]]
    b5 = [7, 4, 6, 28]
    print("Test 5 (Hệ 4x4 phức tạp):", end=" ")
    x5, _ = gaussian_eliminate(A5, b5)
    assert verify_solution(A5, b5, x5), "Kết quả không khớp với NumPy"
    print("PASSED")

    print("\n--- Tất cả 5 test cases đã hoàn thành thành công! ---")

if __name__ == "__main__":
    run_tests()