import numpy as np
from rank_basis import rank_and_basis

def verify_null_space(A, null_space):
    """Kiểm tra thuộc tính Av = 0 cho các vector trong Null Space."""
    if not null_space: return True
    A_np = np.array(A, dtype=float)
    for v in null_space:
        res = A_np @ np.array(v, dtype=float)
        if not np.allclose(res, 0, atol=1e-10):
            return False
    return True

def run_tests():
    # --- TEST 1: Full Rank (Square) ---
    try:
        A1 = [[1, 2], [3, 4]]
        rank, cs, rs, ns = rank_and_basis(A1)
        if rank == 2 and len(ns) == 0:
            print("Test 1 (Full Rank Square): PASSED")
    except Exception as e:
        print(f"Test 1 (Full Rank Square): FAILED ({e})")

    # --- TEST 2: Rank-Deficient (Square) ---
    try:
        A2 = [[1, 2, 3], [2, 4, 6], [1, 0, 1]]
        rank, cs, rs, ns = rank_and_basis(A2)
        if rank == 2 and len(ns) == 1 and verify_null_space(A2, ns):
            print("Test 2 (Rank-Deficient Square): PASSED")
    except Exception as e:
        print(f"Test 2 (Rank-Deficient Square): FAILED ({e})")

    # --- TEST 3: Rectangular Wide (m < n) ---
    try:
        A3 = [[1, 2, 1, 1], [2, 4, 2, 2], [3, 6, 3, 3]]
        rank, cs, rs, ns = rank_and_basis(A3)
        if rank == 1 and len(ns) == 3 and verify_null_space(A3, ns):
            print("Test 3 (Rectangular Wide): PASSED")
    except Exception as e:
        print(f"Test 3 (Rectangular Wide): FAILED ({e})")

    # --- TEST 4: Rectangular Tall (m > n) ---
    try:
        A4 = [[1, 0], [0, 1], [1, 1]]
        rank, cs, rs, ns = rank_and_basis(A4)
        if rank == 2 and len(ns) == 0:
            print("Test 4 (Rectangular Tall): PASSED")
    except Exception as e:
        print(f"Test 4 (Rectangular Tall): FAILED ({e})")

    # --- TEST 5: Zero Matrix ---
    try:
        A5 = [[0, 0, 0], [0, 0, 0]]
        rank, cs, rs, ns = rank_and_basis(A5)
        if rank == 0 and len(ns) == 3 and verify_null_space(A5, ns):
            print("Test 5 (Zero Matrix): PASSED")
    except Exception as e:
        print(f"Test 5 (Zero Matrix): FAILED ({e})")

if __name__ == "__main__":
    run_tests()