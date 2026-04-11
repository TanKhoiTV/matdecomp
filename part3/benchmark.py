from typing import List, Tuple, Any, Dict, cast
import os
import sys
import time
import traceback
import warnings
import numpy as np
import pandas as pd

# Đảm bảo đường dẫn import đúng cấu trúc thư mục
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from part1.gaussian import gaussian_eliminate  # noqa: E402
from part2.decomposition import svd_decompose  # noqa: E402
from part3.solvers import gauss_seidel  # noqa: E402

np.random.seed(42)


# chuẩn hoá
def solve_gaussian_wrapper(A: List[List[float]], b: List[float]) -> np.ndarray:
    _, x, _ = gaussian_eliminate(A, b)
    return cast(np.ndarray, np.array(x))


def solve_svd_wrapper(A: List[List[float]], b: List[float]) -> np.ndarray:
    U, Sigma, VT = svd_decompose(A, max_iterations=2000000)  # max_iterations = 2000000 (jacobi)

    m: int = len(Sigma)
    n: int = len(Sigma[0])

    Sigma_inv: List[List[float]] = [[0.0] * m for _ in range(n)]
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


# hàm sinh ma trận
def generate_system(n: int, matrix_type: str = "SPD") -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if matrix_type == "SPD":
        M: np.ndarray = np.random.rand(n, n)
        A = M.T @ M + n * np.eye(n)

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
                        'solution_error': np.nan,
                        'status': 'Skipped'
                    })
                    continue

                # warm-up
                try:
                    with warnings.catch_warnings(record=True) as w:
                        warnings.simplefilter("always")
                        solver(A_list, b_list)

                        is_svd_non_converged = any("Failed to converge" in str(warn.message) for warn in w)
                        if is_svd_non_converged:
                            print(f"  Warning in {name} (warm-up): SVD non-convergence detected.")
                            results.append({
                                'matrix_type': mtype,
                                'n': n,
                                'solver': name,
                                'cond(A)': cond_A,
                                'mean_time_s': np.nan,
                                'std_time_s': np.nan,
                                'residual_error': np.nan,
                                'solution_error': np.nan,
                                'status': 'Failed: SVDNonConvergence'
                            })
                            continue

                except (ValueError, RuntimeError) as expected_err:
                    print(f"  Expected Error in {name} (warm-up):")
                    traceback.print_exc()
                    results.append({
                        'matrix_type': mtype,
                        'n': n,
                        'solver': name,
                        'cond(A)': cond_A,
                        'mean_time_s': np.nan,
                        'std_time_s': np.nan,
                        'residual_error': np.nan,
                        'solution_error': np.nan,
                        'status': f"Failed: {type(expected_err).__name__}"
                    })
                    continue
                except Exception:
                    print(f"  Unexpected fatal error in {name} (warm-up):")
                    traceback.print_exc()
                    raise

                times: List[float] = []
                x_hat: np.ndarray = np.array([])

                for _ in range(5):
                    start: float = time.perf_counter()
                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            curr_x_hat = solver(A_list, b_list)
                        times.append(time.perf_counter() - start)
                        x_hat = curr_x_hat
                    except Exception as e:
                        print(f"  Error during timed run in {name}: {e}")
                        times.append(float('nan'))

                valid_times = [t for t in times if not np.isnan(t)]
                if len(valid_times) > 0:
                    mean_time: float = float(np.mean(valid_times))
                    std_time: float = float(np.std(valid_times))
                else:
                    mean_time = float('nan')
                    std_time = float('nan')

                if x_hat.size > 0:
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

                    final_status = 'Success'
                else:
                    residual = float('nan')
                    solution_error = float('nan')
                    final_status = 'Failed during timed runs'

                results.append({
                    'matrix_type': mtype,
                    'n': n,
                    'solver': name,
                    'cond(A)': cond_A,
                    'mean_time_s': mean_time,
                    'std_time_s': std_time,
                    'residual_error': residual,
                    'solution_error': solution_error,
                    'status': final_status
                })

                print(f"  Done {name}")

    # save
    os.makedirs('part3', exist_ok=True)
    df = pd.DataFrame(results)
    df.to_csv('part3/results.csv', index=False)

    print("\n Saved to part3/results.csv")


if __name__ == "__main__":
    run_benchmark()
