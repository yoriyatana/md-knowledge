# switch EX2300 bị cao tải CPU -SNMP

Dear anh Huy,

Em xin phép tổng hợp thông tin case hỗ trợ này ạ.

```text
Tối 08/06 em đã online phối hợp bỏ cấu hình traceoption, deactivate cấu hình snmp và debug. Kết quả CPU thiết bị chỉ giảm khi deactivate snmp à kết luận
Qua kiểm tra message log, thiết bị đang ghi nhận rất nhiều log “Failed to get vlan id”
```
|  |
| --- |
| Jun   7 02:00:00 SW\_ACC\_IDC\_44 newsyslog[45251]: logfile turned over due to  size>1024K  Jun   7 02:00:03  SW\_ACC\_IDC\_44 dc-pfe:  LBCM-L2,brcm\_irb\_egress\_cntr\_get(),8609:brcm\_irb\_egress\_cntr\_get Failed to get vlan id  4294967295 for ifl index 545  Jun   7 02:00:03  SW\_ACC\_IDC\_44 fpc0  LBCM-L2,brcm\_irb\_egress\_cntr\_get(),8609:brcm\_irb\_egress\_cntr\_get Failed to get vlan id  4294967295 for ifl index 545  Jun   7 02:00:14  SW\_ACC\_IDC\_44 dc-pfe:  LBCM-L2,brcm\_irb\_egress\_cntr\_get(),8609:brcm\_irb\_egress\_cntr\_get Failed to get vlan id  4294967295 for ifl index 545  Jun   7 02:00:14  SW\_ACC\_IDC\_44 fpc0  LBCM-L2,brcm\_irb\_egress\_cntr\_get(),8609:brcm\_irb\_egress\_cntr\_get Failed to get vlan id 4294967295  for ifl index 545  …… |

- Thông tin log message trên match với kb số [KB35480](https://kb.juniper.net/InfoCenter/index?page=content&id=KB35480&actp=METADATA) của Juniper. Cụ thể, log này ghi nhận khi thiết bị thu thập thông số của các interface không có thật trên thiết bị (ví dụ thông tin interface vlan đã xóa khỏi cấu hình, hoặc các sub-interface chưa được định nghĩa…)

|  |
| --- |
| When the statistic  retrieval of the interfaces is done, the device attempts to retrieve the  statistics of all the interfaces including pseudo interfaces from the  hardware. For example, IRB interfaces which are not physically present |

- Cũng theo thông tin từ KB, lỗi này không gây ảnh hưởng đến hoạt động của thiết bị nhưng sẽ được fix trong các bản OS mới hơn:

|  |
| --- |
| The error has no  functional impact and is fixed in the following releases:  junos:18.1R3-S1  junos:18.2R2  junos:18.3R2  junos:18.4R1  junos:19.1R1 |

- Qua phiên remote support tối 08/06, SVTECH ghi nhận response time cao bất thường với query từ server SNMP với các thông số liên quan đến logical interface

|  |
| --- |
| root@SW\_ACC\_IDC\_44>  show snmp stats-response-statistics    Average  response time statistics:  Stats                 Stats                     Average  Type                  Responses         Response  Time (ms)  ifd(non  ae)      7947951                45.75  ifd(ae)               49034                     94.07  ifl(non  ae)        3232866                 536.86  ifl(ae)                94716                     615.76  firewall              0                             0.00 |

- Thông tin Average response time tương đồng với thông tin xuất hiện trong log message: cùng liên quan đến ifl (logical interface). SVTECH tạm thời kết luận việc trao đổi thông tin logical interface giữa thiết bị và server quản trị tập trung đang gây cao tải CPU.
- Để giải quyết triệt để vấn đề, SVTECH đề xuất upgrade thiết bị lên version mới như thông tin KB (hoặc upgrade lên OS recommend của hãng 18.2R3).
- Trong thời gian lên kế hoạch upgarde, để tạm thời giảm CPU thiết bị, SVTECH đề xuất cấu hình lại thông tin trên SNMP server đối với SW\_ACC\_44: chỉ lấy thông tin các interface cần thiết (các interface có cấu hình và đang chạy dịch vụ), tránh việc gửi nhận thông tin pseudo interface gây cao tải.

Anh Huy thử giúp em các giải pháp như trên anh nhé. Em cảm ơn ạ!
