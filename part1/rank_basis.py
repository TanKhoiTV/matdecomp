from typing import List, Tuple


def compute_rref(A: List[List[float]], eps: float = 1e-12) -> Tuple[List[List[float]], List[int]]:
    """
    Biến đổi một ma trận về Dạng bậc thang rút gọn (Reduced Row Echelon Form - RREF).

    Mục đích: Sử dụng để xác định các vị trí phần tử trụ (pivot) nhằm tính toán hạng (rank) và cơ sở (basis).
    Tham số:
        A: Ma trận đầu vào kích thước m x n (Danh sách lồng nhau).
        eps: Ngưỡng sai số để so sánh với 0.
    Trả về:
        M: Ma trận ở dạng RREF.
        pivot_cols: Danh sách các chỉ số cột chứa phần tử trụ.
    Ngoại lệ (Raises):
        ValueError: Nếu ma trận A rỗng hoặc các hàng có độ dài không nhất quán.
    """
    if not A or not A[0]:
        raise ValueError("Matrix cannot be empty.")  # Ma trận không được rỗng

    num_cols = len(A[0])
    if any(len(row) != num_cols for row in A):
        raise ValueError("Inconsistent row lengths.")  # Độ dài các hàng không nhất quán

    m_matrix = [row[:] for row in A]
    rows, cols = len(m_matrix), num_cols
    pivot_row = 0
    pivot_cols = []

    for j in range(cols):
        if pivot_row >= rows:
            break

        max_val = -1.0
        max_row = -1
        for r in range(pivot_row, rows):
            if abs(m_matrix[r][j]) > max_val:
                max_val = abs(m_matrix[r][j])
                max_row = r

        if max_row == -1 or max_val < eps:
            continue

        m_matrix[pivot_row], m_matrix[max_row] = m_matrix[max_row], m_matrix[pivot_row]

        pivot_val = m_matrix[pivot_row][j]
        m_matrix[pivot_row] = [x / pivot_val for x in m_matrix[pivot_row]]

        for i in range(rows):
            if i != pivot_row:
                factor = m_matrix[i][j]
                m_matrix[i] = [m_matrix[i][k] - factor * m_matrix[pivot_row][k] for k in range(cols)]

        pivot_cols.append(j)
        pivot_row += 1

    return m_matrix, pivot_cols


def rank_and_basis(
        A: List[List[float]], eps: float = 1e-12
) -> Tuple[int, List[List[float]], List[List[float]], List[List[float]]]:
    """
    Tính toán hạng (rank) và các vector cơ sở cho Không gian cột, Không gian hàng và Không gian hạt nhân (Null).

    Mục đích: Đáp ứng các yêu cầu của GitHub Issue #18 về các không gian con cơ bản.
    Tham số:
        A: Ma trận đầu vào kích thước m x n.
        eps: Ngưỡng sai số để so sánh với 0.
    Trả về:
        rank: Số lượng phần tử trụ (hạng của ma trận).
        col_space: Các vector cơ sở cho Không gian cột (trích từ ma trận A ban đầu).
        row_space: Các vector cơ sở cho Không gian hàng (các hàng khác 0 của ma trận RREF).
        null_space: Các vector cơ sở cho Không gian hạt nhân (các nghiệm tham số).
    """
    rows = len(A)
    cols = len(A[0]) if rows > 0 else 0
    rref_matrix, pivot_cols = compute_rref(A, eps)
    rank = len(pivot_cols)

    # 1. Cơ sở không gian cột (Các cột của ma trận A ban đầu tại các chỉ số có phần tử trụ)
    col_space = [[A[i][j] for i in range(rows)] for j in pivot_cols]

    # 2. Cơ sở không gian hàng (Các hàng khác 0 của ma trận RREF)
    row_space = [row[:] for row in rref_matrix if any(abs(x) > eps for x in row)]

    # 3. Cơ sở không gian hạt nhân (Nghiệm tham số của phương trình Ax = 0)
    null_space = []
    free_vars = [j for j in range(cols) if j not in pivot_cols]

    for f_col in free_vars:
        vec = [0.0] * cols
        vec[f_col] = 1.0  # Đặt biến tự do hiện tại bằng 1
        for i, p_col in enumerate(pivot_cols):
            # Biến cơ sở (pivot variable) x_p = - (R_i,f1 * x_f1 + R_i,f2 * x_f2 ...)
            vec[p_col] = -rref_matrix[i][f_col]
        null_space.append(vec)

    return rank, col_space, row_space, null_space
