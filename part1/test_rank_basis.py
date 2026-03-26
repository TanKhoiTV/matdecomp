import unittest
from rank_basis import rank_and_basis


class TestRankBasis(unittest.TestCase):

    def test_full_rank_square(self):
        """Case 1: Full rank square matrix (Identity)"""
        A = [[1.0, 0.0], [0.0, 1.0]]
        rank, col, row, null = rank_and_basis(A)
        self.assertEqual(rank, 2)
        self.assertEqual(len(null), 0)

    def test_rank_deficient_square(self):
        """Case 2: Rank-deficient square matrix"""
        A = [[1.0, 2.0], [2.0, 4.0]]
        rank, col, row, null = rank_and_basis(A)
        self.assertEqual(rank, 1)
        self.assertEqual(len(null), 1)
        # Check if null vector satisfies Ax=0
        self.assertAlmostEqual(null[0][0] + 2*null[0][1], 0)

    def test_rectangular_wide(self):
        """Case 3: Rectangular (more columns than rows)"""
        A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        rank, col, row, null = rank_and_basis(A)
        self.assertEqual(rank, 2)
        self.assertEqual(len(null), 1) # n=3, r=2 => n-r=1

    def test_rectangular_tall(self):
        """Case 4: Rectangular (more rows than columns)"""
        A = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
        rank, col, row, null = rank_and_basis(A)
        self.assertEqual(rank, 2)
        self.assertEqual(len(null), 0)

    def test_zero_matrix(self):
        """Case 5: Zero matrix"""
        A = [[0.0, 0.0], [0.0, 0.0]]
        rank, col, row, null = rank_and_basis(A)
        self.assertEqual(rank, 0)
        self.assertEqual(len(null), 2)
        self.assertEqual(len(col), 0)

if __name__ == "__main__":
    unittest.main()
