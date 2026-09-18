# auto-bandwidth notes

Nếu auto-bandwidth mà LSP cấu hình no-cspf:

- Khi trigger auto-bandwidth xảy ra sẽ thực hiện gửi gói PATH msg theo best route bảng định tuyến:

- Khi có ECMP: gửi random ra 1 hướng, không phụ thuộc best route hướng nào (cho dù có LB hay không)
- khi không có ECMP: gửi ra theo hướng best route.

Trong statistic cần bật auto-bandwidth nếu không sẽ không hoạt động
