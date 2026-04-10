import warnings
from typing import Sequence, List


def is_diagonally_dominant(A: Sequence[Sequence[float]]) -> bool:
    n: int = len(A)
    if n == 0:
        return False

    for row in A:
        if len(row) != n:
            return False

    for i in range(n):
        sum_other: float = sum(abs(A[i][j]) for j in range(n) if j != i)
        if abs(A[i][i]) < sum_other:
            return False

    return True


def residual(
    A: Sequence[Sequence[float]],
    x: Sequence[float],
    b: Sequence[float]
) -> float:
    n: int = len(x)
    return max(
        abs(sum(A[i][j] * x[j] for j in range(n)) - b[i])
        for i in range(n)
    )


def gauss_seidel(
    A: Sequence[Sequence[float]],
    b: Sequence[float],
    tolerance: float = 1e-6,
    max_iter: int = 1000
) -> List[float]:
    n: int = len(A)

    if n == 0:
        return []

    if len(b) != n:
        raise ValueError("Kích thước A và b không khớp.")

    for row in A:
        if len(row) != n:
            raise ValueError("Ma trận A phải vuông.")

    for i in range(n):
        if A[i][i] == 0:
            raise ValueError(f"A[{i}][{i}] = 0 → không thể chia.")

    if not is_diagonally_dominant(A):
        warnings.warn("Ma trận không chéo trội. Có thể không hội tụ.", stacklevel=2)

    x: List[float] = [0.0] * n

    for _ in range(max_iter):
        err: float = 0.0

        for i in range(n):
            old_xi: float = x[i]

            sum1: float = sum(A[i][j] * x[j] for j in range(i))
            sum2: float = sum(A[i][j] * x[j] for j in range(i + 1, n))

            x[i] = (b[i] - sum1 - sum2) / A[i][i]

            diff: float = abs(x[i] - old_xi)
            if diff > err:
                err = diff

        if err < tolerance:
            res: float = residual(A, x, b)
            if res < tolerance:
                return x

    warnings.warn(f"Không hội tụ sau {max_iter} vòng lặp.", stacklevel=2)
    return x
