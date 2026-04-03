import unittest
import importlib.util

from diagonalization import diagonalize

np_spec = importlib.util.find_spec("numpy")
if np_spec is not None:  # pragma: no cover - environment dependent
    np = __import__("numpy")
else:  # pragma: no cover - environment dependent
    np = None


def matmul(A, B):
    rows = len(A)
    cols = len(B[0])
    inner = len(B)
    result = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            s = 0
            for k in range(inner):
                s += A[i][k] * B[k][j]
            result[i][j] = s
    return result


def frobenius_norm(M):
    s = 0.0
    for row in M:
        for x in row:
            s += abs(x) ** 2
    return s ** 0.5


def relative_error(A_ref, A_test):
    diff = []
    for i in range(len(A_ref)):
        row = []
        for j in range(len(A_ref[0])):
            row.append(A_test[i][j] - A_ref[i][j])
        diff.append(row)
    return frobenius_norm(diff) / max(frobenius_norm(A_ref), 1e-30)


class TestDiagonalize(unittest.TestCase):
    def assert_reconstruction_ok(self, A):
        P, D, P_inv = diagonalize(A)
        reconstructed = matmul(matmul(P, D), P_inv)
        err = relative_error(A, reconstructed)
        self.assertLess(err, 1e-10, msg=f"relative error too high: {err}")
        return P, D, P_inv

    def test_general_2x2(self):
        A = [[4, 1], [0, 2]]
        self.assert_reconstruction_ok(A)

    def test_symmetric_matrix(self):
        A = [[2, 1], [1, 2]]
        self.assert_reconstruction_ok(A)

    def test_diagonal_matrix(self):
        A = [[5, 0], [0, 3]]
        P, D, P_inv = self.assert_reconstruction_ok(A)
        # For already diagonal A, the eigenvalues should be 5 and 3.
        vals = sorted([D[0][0], D[1][1]])
        self.assertAlmostEqual(vals[0], 3.0, places=12)
        self.assertAlmostEqual(vals[1], 5.0, places=12)
        self.assertEqual(len(P), 2)
        self.assertEqual(len(P_inv), 2)

    def test_real_eigenvalues_only(self):
        A = [[3, 1], [0, 1]]
        _, D, _ = self.assert_reconstruction_ok(A)
        self.assertIsInstance(D[0][0], (int, float))
        self.assertIsInstance(D[1][1], (int, float))

    def test_non_square_matrix_raises(self):
        A = [[1, 2, 3], [4, 5, 6]]
        with self.assertRaises(ValueError):
            diagonalize(A)

    def test_not_diagonalizable_raises(self):
        # Jordan block: only one independent eigenvector.
        A = [[1, 1], [0, 1]]
        with self.assertRaisesRegex(ValueError, "not diagonalizable"):
            diagonalize(A)

    def test_complex_eigenvalues_rejected(self):
        # Rotation matrix has complex eigenvalues (+/- i) over R.
        A = [[0, -1], [1, 0]]
        with self.assertRaisesRegex(ValueError, "complex eigenvalues"):
            diagonalize(A)

    @unittest.skipIf(np is None, "NumPy not available in this environment")
    def test_verified_against_numpy_eig(self):
        A = [[7, 2], [0, 3]]
        _, D, _ = self.assert_reconstruction_ok(A)
        eig = getattr(np.linalg, "eig")
        array = getattr(np, "array")
        np_vals, _ = eig(array(A, dtype=float))
        got = sorted([D[0][0], D[1][1]])
        expected = sorted([float(np_vals[0]), float(np_vals[1])])
        for g, e in zip(got, expected):
            self.assertAlmostEqual(g, e, places=10)


if __name__ == "__main__":
    unittest.main()
