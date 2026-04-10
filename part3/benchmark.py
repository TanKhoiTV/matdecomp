import sys
import time
import numpy as np
import pandas as pd
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from part1.gaussian import gaussian_eliminate
from part2.decomposition import svd_decompose
from part3.solvers import gauss_seidel


np.random.seed(42)


# chuẩn hoá
def solve_gaussian_wrapper(A, b):
    _, x, _ = gaussian_eliminate(A, b)
    return np.array(x)


def solve_svd_wrapper(A, b):
    U, Sigma, VT = svd_decompose(A,20000)

    m = len(Sigma)
    n = len(Sigma[0])

    Sigma_inv = [[0.0]*m for _ in range(n)]
    for i in range(min(m, n)):
        if abs(Sigma[i][i]) > 1e-12:
            Sigma_inv[i][i] = 1.0 / Sigma[i][i]

    U = np.array(U)
    Sigma_inv = np.array(Sigma_inv)
    VT = np.array(VT)
    b = np.array(b)

    return VT.T @ Sigma_inv @ U.T @ b


def solve_gauss_seidel_wrapper(A, b):
    return np.array(gauss_seidel(A, b))


# hàm sinh ma trận
def generate_system(n, matrix_type="SPD"):
    if matrix_type == "SPD":
        A = np.random.rand(n, n)
        A = A + n * np.eye(n)

    elif matrix_type == "Hilbert":
        A = np.array([[1 / (i + j + 1) for j in range(n)] for i in range(n)])

    else:
        raise ValueError("Unknown matrix type")

    x_true = np.random.rand(n)
    b = A @ x_true

    return A, b, x_true


#benchmark
def run_benchmark():
    sizes = [50, 100, 200, 500, 1000]
    matrix_types = ["SPD", "Hilbert"]

    results = []

    solvers = {
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
            cond_A = np.linalg.cond(A)

            A_list = A.tolist()
            b_list = b.tolist()

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

                times = []

                solver(A_list, b_list)

                for _ in range(5):
                    start = time.perf_counter()
                    x_hat = solver(A_list, b_list)
                    times.append(time.perf_counter() - start)

                mean_time = np.mean(times)
                std_time = np.std(times)

                #residual
                norm_b = np.linalg.norm(b)
                if norm_b == 0:
                    residual = 0.0
                else:
                    residual = np.linalg.norm(A @ x_hat - b) / norm_b

                #solution error
                norm_x = np.linalg.norm(x_true)
                if norm_x == 0:
                    solution_error = 0.0
                else:
                    solution_error = np.linalg.norm(x_hat - x_true) / norm_x

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

    os.makedirs('part3', exist_ok=True)
    df = pd.DataFrame(results)
    df.to_csv('part3/results_full.csv', index=False)

    print("\n Saved to part3/results_full.csv")


if __name__ == "__main__":
    run_benchmark()
