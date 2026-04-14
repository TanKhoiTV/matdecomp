from typing import Sequence, List
import numpy as np
import warnings


def gauss_seidel(
    A: Sequence[Sequence[float]],
    b: Sequence[float],
    tolerance: float = 1e-8,
    max_iter: int = 100000,
) -> List[float]:

    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)

    n = A_np.shape[0]

    if A_np.shape[0] != A_np.shape[1]:
        raise ValueError("A phải là ma trận vuông.")
    if b_np.shape[0] != n:
        raise ValueError("Kích thước A và b không khớp.")

    if np.any(np.diag(A_np) == 0):
        raise ValueError("Có phần tử trên đường chéo bằng 0.")

    # check chéo trội
    diag = np.abs(np.diag(A_np))
    off_diag_sum = np.sum(np.abs(A_np), axis=1) - diag
    if not np.all(diag >= off_diag_sum):
        warnings.warn("Ma trận không chéo trội. Có thể không hội tụ.", stacklevel=2)

    x = np.zeros(n)

    for _ in range(max_iter):
        x_old = x.copy()

        for i in range(n):
            s1 = np.dot(A_np[i, :i], x[:i])
            s2 = np.dot(A_np[i, i+1:], x_old[i+1:])
            x[i] = (b_np[i] - s1 - s2) / A_np[i, i]

        iter_error = np.linalg.norm(x - x_old, ord=2)

        if iter_error < tolerance:
            residual = np.linalg.norm(A_np @ x - b_np, ord=2)
            if residual < tolerance:
                return x.tolist()

    warnings.warn(f"Không hội tụ sau {max_iter} vòng lặp.", stacklevel=2)
    return x.tolist()