# BUG Hold-time down không hoạt động được nếu cấu hình nhỏ hơn 1s trên interface chạy WANPHY

Hi Team,

 

Junos từ 18 đến 20.4R3-S4 đang có bug với các interface đang bật **WANPHY** đồng thời cấu hìn**h hold-time down với thời gian nhỏ hơn 1 giây** thì sẽ gây flap interface nếu nháy truyền dẫn, tức là hold-time down không hoạt động đúng mong đợi. Hiện tại, lỗi này chưa biết được trigger nên chưa có kế hoạch để có thể fix trên Junos.

 

Hiện tại ghi nhận được bug không gặp trong các trường hợp sau:

    - Ở Junos 17.x 

    - Interface chạy mode LANPHY

    - Chạy WANPHY nhưng không cấu hình hold-time down hoặc có cấu hình nhưng thời gian tầm 2 giây trở lên.

 

Workaround cho lỗi này thì có thể cân nhắc 2 option bên dưới:

1/. Thay đổi thành interface từ mode WANPHY -> LANPHY. giải pháp này cần kiểm tra thêm đầu truyền dẫn xem có hỗ trợ mode này hay không

2/. Tăng hold-time down lên khoảng 2s: giải pháp này thì có thể sẽ gây blackhole traffic trong khoảng thời gian hold-time down. (thực tế test ở lab, theo Hoàng NWHNI kiểm tra thì khi set hold-time down tầm 1,5 giây thì vẫn gây flap).

 

Chi tiết về case này, Hoàng NWHNI có làm việc với JTAC qua case **2022-0731-520372** - đồng thời thực hiện test Lab với kết quả rất chi tiết ở mail dưới. AE xem thêm để nắm bug của lỗi này để tránh/hạn chế gặp trên các Junos hiện tại.
