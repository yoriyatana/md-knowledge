# switch EX2300 không commit được

Qua kiểm tra thông tin RSI, thiết bị hiện đang có cảnh báo đầy ổ cứng:

|  |
| --- |
| root@SW\_ACC\_IDC\_53>  show chassis alarms no-forwarding    2 alarms currently  active  Alarm  time                Class  Description  1970-06-09  06:15:38 UTC  Minor  RE 0 /var partition usage is high  1970-06-09  06:15:38 UTC  Major  RE 0 /var partition is full |

Nhờ anh Huy thực hiện giúp em câu lệnh “>request system storage cleanup dry-run” và gửi lại giúp em kết quả anh nhé. Câu lệnh này không xóa file mà chỉ list ra danh sách các file sẽ xóa nên anh có thể thực hiện luôn mà không ảnh hưởng hệ thống ạ.
