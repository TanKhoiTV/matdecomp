from typing import Sequence

def inverse(A: Sequence[Sequence[float | int]]) -> list[list[float]]:
    """Tính ma trận nghịch đảo của A bằng thuật toán Gauss-Jordan."""
    n = len(A)
    # Tạo ma trận bổ sung [A | I]
    combined = [[float(val) for val in row] + [(1.0 if i == j else 0.0) for j in range(n)] 
                for i, row in enumerate(A)]

    for i in range(n):
        # Tìm hàng có giá trị lớn nhất ở cột i để làm pivot
        pivot_row = i
        for j in range(i + 1, n):
            if abs(combined[j][i]) > abs(combined[pivot_row][i]):
                pivot_row = j

        # Kiểm tra ma trận suy biến
        if abs(combined[pivot_row][i]) < 1e-12:
            raise ValueError("Ma trận suy biến, không thể tìm nghịch đảo.")

        # Hoán đổi hàng
        combined[i], combined[pivot_row] = combined[pivot_row], combined[i]

        # Chuẩn hóa hàng i (đưa pivot về 1)
        pivot_val = combined[i][i]
        combined[i] = [val / pivot_val for val in combined[i]]

        # Khử các cột khác về 0
        for j in range(n):
            if i != j:
                factor = combined[j][i]
                combined[j] = [v_j - factor * v_i for v_j, v_i in zip(combined[j], combined[i])]

    # Tách ma trận I đã trở thành A^-1 ra
    return [row[n:] for row in combined]
