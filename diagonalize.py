def diagonalize(A):
    """
    Chéo hóa ma trận vuông `A` sao cho:
        A = P D P^-1

    trong đó:
    - D: là ma trận đường chéo chứa các giá trị riêng,
    - P: chứa các vector riêng tương ứng dưới dạng các cột,
    - P_inv: là ma trận nghịch đảo của P.

    Điều kiện để chéo hóa được:
    - A phải là ma trận vuông.
    - A chéo hóa được khi nó có đủ số lượng vector riêng độc lập tuyến tính
    (tương đương tổng bội hình học bằng kích thước ma trận).

    Giá trị trả về:
        tuple: (P, D, P_inv) 
    P: ma trận chứa các vector riêng dưới dạng các cột
    D: ma trận đường chéo chứa các giá trị riêng
    P_inv: ma trận nghịch đảo của P
    """
    # Method: Sử dụng phương pháp lặp lũy thừa để tính toán giá trị riêng và vector riêng
    # Full implementation will be provided in the 2nd sprint.

    return None, None, None 