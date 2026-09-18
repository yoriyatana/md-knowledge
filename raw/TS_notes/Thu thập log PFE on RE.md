# Thu thập log PFE on RE

[ June 26, 2023 16:51 ] ⁨SVT.Ngọc.NĐ⁩: ![](image/4cf53408f984e44add864680982e46c6)

[ June 26, 2023 16:54 ] ⁨SVT.Ngọc.NĐ⁩: Xác nhận:

- Bật syslog \*pfe any\* thì những log ghi nhận ở dưới linecard/pfe sẽ được ghi nhận ở phần syslog tương ứng (sẽ chèn thêm chính xác fpc raise log - và ở lab thì ghi nhận độ trễ ghi nhận ở phần syslog chậm hơn 2s so với ghi log ở dưới FPC như hình chụp trên)

- log messages nếu bật any any cũng ghi đc log pfe này

[ June 26, 2023 16:54 ] ⁨SVT.Ngọc.NĐ⁩: Nếu vậy, sắp tới chắc các thiết kế/tối ưu, AE đề xuất ghi riêng file log cho phần log pfe này để hạn chế những lỗi dưới linecard mà SVTECH chưa kịp vào thì khách hàng/card reboot rồi.
