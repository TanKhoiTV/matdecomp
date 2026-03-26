import numpy as np

def determinant(A):
    """
    Tính định thức của ma trận vuông A bằng phép khử Gauss.
    Trả về 0.0 nếu ma trận suy biến.
    """
    # 
    mat = np.array(A, dtype=float)
    
    # KT MA TRẬN VUÔNG HAY KHÔNG
    if mat.shape[0] != mat.shape[1]:
        raise ValueError("Ma trận phải là ma trận vuông.")
        
    n = mat.shape[0]
    swap_count = 0  
    
    for i in range(n):
        # TÌM PHẦN TỬ LỚN NHẤT
        pivot_row = i
        for j in range(i + 1, n):
            if abs(mat[j, i]) > abs(mat[pivot_row, i]):
                pivot_row = j
                
        # 2. XỬ LÝ MA TRẬN SUY BIẾN NẾU PIVOT GẦN BẰNG 0
        if abs(mat[pivot_row, i]) < 1e-12:
            return 0.0
            
        # 3 ĐỔI HÀNG NẾU PHẦN TỬ LỚN NHẤT KHÔNG NẰM Ở I
        if pivot_row != i:
            mat[[i, pivot_row]] = mat[[pivot_row, i]]
            swap_count += 1
            
        #KHỬ VỀ 0
        for j in range(i + 1, n):
            factor = mat[j, i] / mat[i, i]
            mat[j, i:] -= factor * mat[i, i:]
            
    # TÍCH ĐƯỜNG CHÉO CHÍNH:
    det_val = 1.0
    for i in range(n):
        det_val *= mat[i, i]
        
    #KẾT QUẢ:
    return ((-1) ** swap_count) * det_val