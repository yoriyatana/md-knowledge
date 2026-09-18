# lỗi không ping được mpls ldp

Dear các anh chị VNPT.

Liên quan đến lỗi ping mpls ldp từ box HCM-ASBR2 về box HGG-PE2, bên em xin phép summarize lại như sau

**Mô hình vật lý hiện tại và logic hiện tại.**

![](image/1e8d7efec4533fe12fed2dc00468c267.PNG)

- Từ HCM-ASBR2 có các label-switched-path về HCM-P2, trên các lsp này sử dụng tính năng ldp-tunnelling.
- HCM-P2 cũng sẽ có các label-switched-path về HNI-P2, trên các lsp này sử dụng tính năng ldp-tunneling, tương tự từ HNI-P2 cũng dùng mô hình này về HGG-P2.

èNhư vậy, HCM-ASBR2 sẽ học được loopback 123.29.4.65 qua LDP over lsp (LDP over RSVP).

**Hiện tượng lỗi**

- Từ box HCM-ASBR2, khi thực hiện ping ldp về loopback 123.29.4.65 thì không thấy respond (bị stuck) như log dưới đây

|  |
| --- |
| nmcuong@HCM-ASBR2-RE0> ping mpls ldp 123.29.4.65  May 22 11:37:21  .....  --- lsping statistics ---  5 packets transmitted, 0 packets received, 100% packet loss |

- Tuy nhiên khi thực hiên ping đến các IP phía sau box HGG-PE2 (Các IP thuê bao online) thì ping bình thường

|  |
| --- |
| nmcuong@HCM-ASBR2-RE0> ping 14.224.122.103 source  123.29.12.214 count 5  PING 14.224.122.103 (14.224.122.103): 56 data bytes  64 bytes from 14.224.122.103: icmp\_seq=0 ttl=61 time=28.309 ms  --- 14.224.122.103 ping statistics ---  5 packets transmitted, 5 packets received, 0% packet loss  round-trip min/avg/max/stddev = 27.677/28.109/28.684/0.354 ms  {master}  nmcuong@HCM-ASBR2-RE0> ping 14.228.145.33 source  123.29.12.214 count 5  PING 14.228.145.33 (14.228.145.33): 56 data bytes  64 bytes from 14.228.145.33: icmp\_seq=4 ttl=61 time=31.888 ms    --- 14.228.145.33 ping statistics ---  5 packets transmitted, 5 packets received, 0% packet loss  round-trip min/avg/max/stddev = 31.888/32.176/32.546/0.215 ms  {master}  nmcuong@HCM-ASBR2-RE0> ping 14.228.145.125 source  123.29.12.214 count 5  PING 14.228.145.125 (14.228.145.125): 56 data bytes  64 bytes from 14.228.145.125: icmp\_seq=4 ttl=60 time=30.907 ms    nmcuong@HCM-ASBR2-RE0> show route 14.224.122.103 detail |  match protoco  **Protocol next  hop: 123.29.4.65**  {master}  nmcuong@HCM-ASBR2-RE0> show route 14.228.145.33 detail |  match protoco  **Protocol next  hop: 123.29.4.65**  {master}  nmcuong@HCM-ASBR2-RE0> show route 14.228.145.125 detail |  match protoco  **Protocol next  hop: 123.29.4.65** |

- Đồng thời, theo như thông tin từ INOC thì không thấy phản ánh dịch vụ gì trên box HGG-PE2

**Các phân tích và hướng xử lý tiếp theo**

- SVT+Juniper ATAC đã check trực tiếp trên các box liên quan và chưa phát hiện gì bất thường.
- Các quá trình push nhãn và swap nhãn toàn trình (về mặt control plane) đều đúng thông tin, không có hiện tượng hay log thể hiện bị stuck hay failed việc swap nhãn (vì trên thực tế data traffic vẫn đi qua bình thường).
- Hiện tại, bên em đang nghi ngờ lỗi này chỉ liên quan đến việc xử lý và hiển thị kết quả ping và traceroute mpls ldp, chứ không ảnh hưởng gì đến data plane thực.
- Để làm rõ và khoanh vùng chính xác, bên em đề xuất apply firewall filter để counter gói tin mpls ping khi được khởi tạo từ HCM-ASBR2, apply trên các box dọc tuyến đường để confirm chính xác gói tin đang bị drop ở đâu.

Bên em gửi cấu hình cho firewall này, và nhờ các anh chị sắp xếp thời gian phối hợp thực hiện ạ.
