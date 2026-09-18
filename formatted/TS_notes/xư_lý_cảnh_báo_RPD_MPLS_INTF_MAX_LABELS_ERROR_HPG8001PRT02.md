# xư lý cảnh báo RPD_MPLS_INTF_MAX_LABELS_ERROR HPG8001PRT02

* *Do trên interface ae0.1 mình đang thiếu cấu hình maximum-labels 5 (default là 3). Khi một số dịch vụ được truyền qua LSP HPG8001PRT02-PDL9102CKV02, sử dụng đường bypass qua ae0.1, thì số lượng label mà thiết bị phải xử lý sẽ lớn hơn 3.**

* *Trường hợp này nhờ anh bổ sung cấu hình theo DT sau:**

- **Thực hiện shutdown interface ae0 (các cấu hình thay đổi family mpls khuyến nghị nên shutdown interface trước khi thực hiện)**

* *config private**

* *set interfaces ae0 disable**

* *commit**

- **Cấu hình bổ sung**

* *set interfaces ae0.1 family mpls maximum-labels 5**

* *commit**

- **Mở lại interface**

* *delete interfaces ae0 disable**

* *commit**

* *exit**

* *Nhờ anh thực hiện và giám sát xem log còn xuất hiện không nhé ạ.**
