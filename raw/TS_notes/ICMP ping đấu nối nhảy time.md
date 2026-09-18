# ICMP ping đấu nối nhảy time

Bản tin ICMP (Ping) là bản tin có độ ưu tiên thấp trong Junos, vì vậy thiết bị sẽ phản hồi và xử lý các bản tin có độ ưu tiên cao hơn (ví dụ như update route) trước khi xử lý bản tin ICMP. Vì vậy khi ping có thể sẽ có một vài bản tin ICMP được phản hồi trễ hơn so với các bản tin ICMP khác, gây ra hiện tượng nhảy time khi ping như trường hợp này của CMC.

Thông tin về hiện tượng này em xem thêm trong KB anh gửi kèm nhé.

![](image/140cfceba9d50ea321b5c43f53e5ca4f.pdf)
