# Giới hạn số lượng phiên của một khách hàng trên BRAS Juniper (session-limit-per-username)

Anh gửi CV chi tiết về lỗi này nhé. Liên quan đến lỗi này cũng như workaround anh xin phép summarize lại như sau

* *Điều kiện bị hit lỗi**

- Sử dụng Junos OS version 18.4R3-S7
- Có sử dụng tính năng limit session trên BRAS (session-limit-per-username)

* *Trigger:**

- Khi thực hiện bất kỳ thay đổi cấu hình nào liên quan đến BRAS (ví dụ khai báo pool, bật trace-options cho các process như authen hay dhcpv6), và có commit. Khi lỗi xảy ra thì BRAS sẽ không cấp được IPv6 cho các thuê bao mới.

* *Cách kiểm tra khi bị lỗi:**

- Để xác định box có bị hit lỗi hay không sau khi thực hiện commit, có thể sử dụng câu lệnh như sau

|  |
| --- |
| juniper@NAN-PE1\_RE0> show network-access aaa statistics  session-limit-per-username detail | last 5  Oct 11 17:20:06  vt9996                 local                0                      1  vt9997                 local                0                      1  vt9998                 local                0                      1  vt9999                 local                0                      1  **local               0                     1**          >>> Entry  này chỉ xuất hiện khi gặp lỗi |

* *Work around:**

- Để khôi phục lại việc cấp phát DHCPv6, có thể restart lại process smg bằng câu lệnh như dưới đây.

|  |
| --- |
| juniper@NAN-PE1\_RE0> restart smg-service gracefully |

Lưu ý: Sau khi restart smg-service, cần chờ khoảng 2-3 phút để thiết bị có thể cấp phát lại DHCPv6 như bình thường. SVT đã test thử nhiều lần trong lab với điều kiện khoảng 80K thuê bao, disable các trace-options, thì thời gian khoảng từ 45-70s. Quá trình restart smg service không thấy ảnh hưởng gì đến các thuê bao hiện tại.

* *Verify lại trạng thái của box**

|  |
| --- |
| juniper@NAN-PE1\_RE0> show network-access aaa statistics  session-limit-per-username detail | last 5  Oct 11 20:28:58  vt9995                 local                0                      1  vt9996                 local                0                      1  vt9997                 local                0                      1  vt9998                 local                0                      1  vt9999                 local                0                      1 |

Vậy bên anh báo lại để Minh cùng các anh chị Viettel trao đổi và xem xét thêm về WA này nhé.
