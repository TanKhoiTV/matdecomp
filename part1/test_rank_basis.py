import numpy as np
from rank_basis import rank_and_basis


def verify_null_space(A, ns):
    """Kiểm tra Av = 0."""
    if not ns:
        return True
    A_np = np.array(A)
    for v in ns:
        if not np.allclose(A_np @ np.array(v), 0, atol=1e-10):
            return False
    return True


def run_tests():
    # --- TEST 1: Full Rank Square ---
    try:
        A1 = [[1, 2], [3, 4]]
        r, cs, rs, ns = rank_and_basis(A1)
        if r == 2 and len(ns) == 0:
            print("Test 1 (Full Rank Square): PASSED")
    except Exception:
        print("Test 1: FAILED")

    # --- TEST 2: Rank-Deficient Square ---
    try:
        A2 = [[1, 2, 3], [2, 4, 6], [1, 0, 1]]
        r, cs, rs, ns = rank_and_basis(A2)
        if r == 2 and len(ns) == 1 and verify_null_space(A2, ns):
            print("Test 2 (Rank-Deficient Square): PASSED")
    except Exception:
        print("Test 2: FAILED")

    # --- TEST 3: Rectangular Wide ---
    try:
        A3 = [[1, 2, 1, 1], [2, 4, 2, 2], [3, 6, 3, 3]]
        r, cs, rs, ns = rank_and_basis(A3)
        if r == 1 and len(ns) == 3 and verify_null_space(A3, ns):
            print("Test 3 (Rectangular Wide): PASSED")
    except Exception:
        print("Test 3: FAILED")

    # --- TEST 4: Rectangular Tall ---
    try:
        A4 = [[1, 0], [0, 1], [1, 1]]
        r, cs, rs, ns = rank_and_basis(A4)
        if r == 2 and len(ns) == 0:
            print("Test 4 (Rectangular Tall): PASSED")
    except Exception:
        print("Test 4: FAILED")

    # --- TEST 5: Zero Matrix ---
    try:
        A5 = [[0, 0, 0], [0, 0, 0]]
        r, cs, rs, ns = rank_and_basis(A5)
        if r == 0 and len(ns) == 3 and verify_null_space(A5, ns):
            print("Test 5 (Zero Matrix): PASSED")
    except Exception:
        print("Test 5: FAILED")


if __name__ == "__main__":
    run_tests()
