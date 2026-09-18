# Untitled Note

Bổ sung CoS (cho cả 4 và 6)

Bổ sung IPv6 - PROTECT-RE-v6, policy adv IPv6 (bổ sung song song với IPv4, rải vào hết các mô hình dịch vụ), monitor IPv6 (dùng OID trên BRAS monitor traffic IPv6 - có con được con không), cấu hình pppoe cho IPv6

Move phần DPI lên chung phần CGNAT

(chạy 6PE)

A.Quân: metric ISIS vuông thì giá trị metric bắt cặp link gần core sẽ tốt hơn (tài liệu hiện đang bằng nhau là 10)

Thọ: metric ISIS B-N cao hơn metric B-T/T-N do một số tỉnh nối về 2 miền khách nhau (DNG - HCM hoặc DNG - HNI)

Tách riêng 2 mặt phẳng định tuyến:

mặt SMC phục vụ cho khách hàng Broadband và các dịch vụ nội bộ

mặt MC phục vụ cho khách hàng FTI. Hiện mặt cặp MC ở khu vực DNG chưa hoàn chỉnh

Tại POP HKG và SGP: tách biệt lưu lượng cho 2 khối khách hàng và ưu tiên sử dụng tài nguyên của từng tập khách hàng

FTI users -> GW -> PE -> MC

Broadband users -> PE -> GW -> SMC

Trong tình huống cần ứng cứu lưu lượng cho FTI, tạo RSVP-LSP đến PE

Quan điểm thiết kế metric ISIS:

Tối ưu phần Multicast:

Loại bỏ Layer 2 thuần giữa các switch AGG multicast

Giám sát chất lượng kênh multicast khi đi qua hạ tầng sw
