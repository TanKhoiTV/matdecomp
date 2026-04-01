# Narration Script: The Geometry of SVD

## Scene 1: Giới thiệu về SVD và cách tiếp cận "Rotate-Scale-Rotate"

Chào mừng các bạn. Trong phần này, chúng ta sẽ khám phá phân rã giá trị suy biến, hay còn gọi là SVD - một trong những công cụ mạnh mẽ nhất của đại số tuyến tính.

    Hiện title: Singular Value Decomposition (SVD)
    Fade in nhẹ (tạo cảm giác mở đầu video)

Định lý SVD phát biểu rằng, mọi ma trận $A$ với kích thước $m \times n$ đều có thể được phân tách thành ba phép biến đổi hình học cơ bản: xoay, co giãn và xoay một lần nữa.

    Hiện 1 ma trận 2x2 cụ thể
    Transform từ ma trận -> công thức A = U\SigmaV^T
    Zoom nhẹ vào công thức

Hãy quan sát ma trận $A$ cụ thể mà nhóm mình đã cài đặt trên màn hình. Thay vì nhìn nó như một sự biến đổi hỗn loạn, SVD giúp ta thấy đươc cấu trúc ẩn bên trong qua công thức $A = U \Sigma V^T$.

    Highlight từng phần V^T, \Sigma và U
    Sử dụng hiệu ứng "glow", "indicate"

Đầu tiên, ma trận $V^T$...

    Hiện hệ trục Oxy và hình tròn đơn vị
    Label: Input space

...thực hiện một phép xoay trong không gian đầu vào để căn chỉnh các vector cơ sở theo các hướng quan trọng nhất của dữ liệu.

    Xoay toàn bộ đường tròn (rotation), hình dạng KHÔNG đổi, thêm mũi tên quay

Tiếp theo, ma trận $\Sigma$ thực hiện co giãn các vector này dọc theo các trục tương ứng.

    Biến đường tròn → ellipse
    Co giãn theo 2 trục khác nhau: trục dài = σ₁, trục ngắn = σ₂
    Animate chậm

Cuối cùng, ma trận $U$ xoay kết quả đó thêm một lần nữa để đưa về không gian đích.

    Xoay ellipse lần nữa
    Label: “Output space”
    Đây là trạng thái cuối cùng của phép biến đổi A

Đây chính là chìa khóa để hiểu cách dữ liệu được kéo giãn và định hướng trong không gian.

    Hiện pipeline: x → Vᵀx → ΣVᵀx → UΣVᵀx
    Highlight từng bước theo thời gian

## Scene 2: Chéo hóa, trị riêng và sự kết nối với SVD

SVD có mối quan hệ mật thiết với việc chéo hóa ma trận, một yêu cầu quan trọng trong đồ án này.

    Hiện A = PDP^-1 và fade sang A= UΣV^T
    So sánh 2 công thức (đặt cạnh nhau)

Nếu chéo hóa $A = PDP^{-1}$ chỉ áp dụng cho ma trận vuông, thì SVD là phiên bản tổng quát hơn cho mọi loại ma trận.

    Highlight: “square matrix” cho diagonalization, “any matrix” cho SVD

Các giá trị trên đường chéo của $\Sigma$, gọi là các giá trị suy biến $\sigma$, thực chất là căn bậc hai của các giá trị riêng từ ma trận $A^T A$.

    Hiện công thức: σi​=sqrt(λi​(ATA))
    Animation: A -> A^T*A -> eigenvalues -> sqrt -> σ
​
Trên màn hình, các bạn có thể thấy các vector riêng mà nhóm mình đã tính toán. Chúng chính là các trục chính giúp xác định hình dạng của ellipse khi không gian bị biến đổi.

    Hiện các vector riêng (eigenvectors) dưới dạng mũi tên
    Các vector này: align với trục ellipse
    Animate: vector xoay theo transformation

Việc tìm ra các thành phần này không chỉ giúp ta chéo hóa ma trận mà còn giảm đáng kể chi phí tính toán khi xử lý các lũy thừa ma trận lớn.

    Hiện phép nâng lũy thừa: 𝐴^𝑘
    Sau đó transform thành: P * D^k * P^-1
    Nhấn mạnh: "giảm chi phí tính toán"

## Scene 3: Ứng dụng thực tế - Xấp xỉ hạng thấp

Vậy tại sao chúng ta cần phân tách ma trận phức tạp như vậy? Câu trả lời nằm ở ứng dụng nén dữ liệu và xấp xỉ hạng thấp.

    Hiện một ma trận lớn (hoặc hình ảnh grayscale nếu muốn nâng cao)
    Label: “Original data”

Bằng cách chỉ giữ lại các giá trị suy biến lớn nhất trong $\Sigma$ và loại bỏ các thành phần nhỏ hơn,

    Hiện công thức: Σ = diag(σ1, σ2, ..., σn)
    Sau đó: fade out các σ nhỏ, giữ lại top k

chúng ta có thể tái cấu trúc lại một ma trận gần đúng với bản gốc nhưng tốn ít bộ nhớ hơn rất nhiều.

    Hiện: A_k = \Sigma(\sigma * u_i * v^T_i)
    Animation: build lại ma trận từ từng thành phần, từng rank-1 component xuất hiện

<!-- Nhóm mình đã thực nghiệm cài đặt thuật toán này hoàn toàn từ đầu bằng Python, không sử dụng các hàm có sẵn của NumPy để đảm bảo tính học thuật cao nhất của đồ án. -->

Hy vọng qua video trực quan này, các bạn đã hiểu rõ hơn về vẻ đẹp hình học của SVD và sức mạnh của nó trong tính toán khoa học. Cảm ơn các bạn đã theo dõi.

    Hiện: thanks for watching