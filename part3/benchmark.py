from typing import List, Tuple, Any, Dict, cast
import sys
import time
import numpy as np
import pandas as pd
import os


# Đảm bảo đường dẫn import đúng cấu trúc thư mục
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from part1.gaussian import gaussian_eliminate
from part2.decomposition import svd_decompose
from part3.solvers import gauss_seidel

np.random.seed(42)

#chuẩn hoá
def solve_gaussian_wrapper(A: List[List[float]], b: List[float]) -> np.ndarray:
    _, x, _ = gaussian_eliminate(A, b)
    return cast(np.ndarray, np.array(x))


def solve_svd_wrapper(A: List[List[float]], b: List[float]) -> np.ndarray:
    U, Sigma, VT = svd_decompose(A, 20000) #max_iterations = 20000 (jacobi)

    m: int = len(Sigma)
    n: int = len(Sigma[0])

    Sigma_inv: List[List[float]] = [[0.0]*m for _ in range(n)]
    for i in range(min(m, n)):
        if abs(Sigma[i][i]) > 1e-12:
            Sigma_inv[i][i] = 1.0 / Sigma[i][i]

    U_arr: np.ndarray = np.array(U)
    Sigma_inv_arr: np.ndarray = np.array(Sigma_inv)
    VT_arr: np.ndarray = np.array(VT)
    b_arr: np.ndarray = np.array(b)

    res = VT_arr.T @ Sigma_inv_arr @ U_arr.T @ b_arr
    return cast(np.ndarray, res)


def solve_gauss_seidel_wrapper(A: List[List[float]], b: List[float]) -> np.ndarray:
    return cast(np.ndarray, np.array(gauss_seidel(A, b)))


#hàm sinh ma trận
def generate_system(n: int, matrix_type: str = "SPD") -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if matrix_type == "SPD":
        A: np.ndarray = np.random.rand(n, n)
        A = A + n * np.eye(n)

    elif matrix_type == "Hilbert":
        A = np.array([[1 / (i + j + 1) for j in range(n)] for i in range(n)])

    else:
        raise ValueError("Unknown matrix type")

    x_true: np.ndarray = np.random.rand(n)
    b: np.ndarray = A @ x_true

    return A, b, x_true


# benchmark
def run_benchmark() -> None:
    sizes: List[int] = [50, 100, 200, 500, 1000]
    matrix_types: List[str] = ["SPD", "Hilbert"]

    results: List[Dict[str, Any]] = []

    solvers: Dict[str, Any] = {
        'Gaussian': solve_gaussian_wrapper,
        'SVD': solve_svd_wrapper,
        'Gauss-Seidel': solve_gauss_seidel_wrapper
    }

    for mtype in matrix_types:
        for n in sizes:

            # hạn chế Hilbert quá lớn
            if mtype == "Hilbert" and n > 200:
                print(f"Skip Hilbert n={n}")
                continue

            print(f"\nRunning: {mtype}, n={n}")

            A, b, x_true = generate_system(n, mtype)
            cond_A: float = float(np.linalg.cond(A))

            A_list: List[List[float]] = A.tolist()
            b_list: List[float] = b.tolist()

            for name, solver in solvers.items():

                # skip khi SVD lớn có thể dẫn đến treo
                if name == 'SVD' and n >= 500:
                    print(f"  Skip {name}")
                    results.append({
                        'matrix_type': mtype,
                        'n': n,
                        'solver': name,
                        'cond(A)': cond_A,
                        'mean_time_s': np.nan,
                        'std_time_s': np.nan,
                        'residual_error': np.nan,
                        'solution_error': np.nan
                    })
                    continue

                times: List[float] = []

                # warm-up
                try:
                    solver(A_list, b_list)
                except Exception as e:
                    print(f"  Error: {e}")
                    continue

                x_hat: np.ndarray = np.array([])
                for _ in range(5):
                    start: float = time.perf_counter()
                    x_hat = solver(A_list, b_list)
                    times.append(time.perf_counter() - start)

                mean_time: float = float(np.mean(times))
                std_time: float = float(np.std(times))

                # residual
                norm_b: float = float(np.linalg.norm(b))
                if norm_b == 0:
                    residual: float = 0.0
                else:
                    residual = float(np.linalg.norm(A @ x_hat - b) / norm_b)

                # solution error
                norm_x: float = float(np.linalg.norm(x_true))
                if norm_x == 0:
                    solution_error: float = 0.0
                else:
                    solution_error = float(np.linalg.norm(x_hat - x_true) / norm_x)

                results.append({
                    'matrix_type': mtype,
                    'n': n,
                    'solver': name,
                    'cond(A)': cond_A,
                    'mean_time_s': mean_time,
                    'std_time_s': std_time,
                    'residual_error': residual,
                    'solution_error': solution_error
                })

                print(f"  Done {name}")

    # save
    os.makedirs('part3', exist_ok=True)
    df = pd.DataFrame(results)
    df.to_csv('part3/results_full.csv', index=False)

    print("\n Saved to part3/results_full.csv")



if __name__ == "__main__":
    run_benchmark()
