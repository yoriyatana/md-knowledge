# BPC8003BRA01_RE1 | không cutoff được user

Em xin summary lại các ý:

7/4: ghi nhận 2 khách hàng trên ae14.2154 của BPC8003BRA01 đang bị treo, không thể clear được session

b651\_gftth\_doicnvbptdvtq77

b651\_gftth\_doivbpcntdcnvt2

- VIETTEL xử lý:

1. Tắt modem KH trong 15 phút, trên bras theo dõi xem phiên này có clear ko

2. Mở modem, cài với 01 account đại lý khác xem có online ko.

3. Kiểm tra trên bras xem cả hai account có online đồng thời ko.

4. Clear system subscriber-management arp address 10.31.x.x cuả hai account này, xem session online lại ko/giải phóng

5. clear network-access aaa subscriber username b651\_gftth\_doivbpcntdcnvt2

6. Đề xuất clear mac-address của thuê bao Phúc.

clear system subscriber-management arp address 10.31.122.4

12/04:

có nhiều phản ánh liên quan fpc8 vào cuối tuần.

shutdown sub-int của Core Tỉnh đang shutdowwn nhưng khách hàng vẫn online trên Bras BPC => user không online trên bras dự phòng

Hướng xử lý tiếp theo:

- restart smg-service xong kiểm tra lại

- Nếu không được thì xem xét reboot FPC hoặc box

- tiến hành song song / giả lập lại lỗi trên lab
