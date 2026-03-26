def determinant(A):
    """
    Tính định thức của ma trận vuông A bằng phép khử Gauss.
    Trả về 0.0 nếu ma trận suy biến.
    """
    # 1. Kiểm tra ma trận vuông
    n = len(A)
    for row in A:
        if len(row) != n:
            raise ValueError("Ma trận phải là ma trận vuông.")
            
    # 2. Tạo một bản sao kiểu float để không làm hỏng ma trận gốc A
    mat = [[float(val) for val in row] for row in A]
    
    swap_count = 0
    
    # 3.Khử Gauss
    for i in range(n):
        pivot_row = i
        max_val = abs(mat[i][i])
        for j in range(i + 1, n):
            if abs(mat[j][i]) > max_val:
                max_val = abs(mat[j][i])
                pivot_row = j
                
        # Nếu pivot cực kỳ nhỏ (gần 0), ma trận suy biến -> định thức = 0.0
        if abs(mat[pivot_row][i]) < 1e-12:
            return 0.0
            
        # Hoán đổi hàng
        if pivot_row != i:
            mat[i], mat[pivot_row] = mat[pivot_row], mat[i]
            swap_count += 1
            
        # Phép khử
        for j in range(i + 1, n):
            factor = mat[j][i] / mat[i][i]
            for k in range(i, n):
                mat[j][k] -= factor * mat[i][k]
                
    # 4. Tính tích các phần tử trên đường chéo chính
    det_val = 1.0
    for i in range(n):
        det_val *= mat[i][i]
        
    # Trả về kết quả với đúng dấu
    return ((-1) ** swap_count) * det_val