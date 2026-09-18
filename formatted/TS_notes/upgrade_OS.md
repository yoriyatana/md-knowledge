# upgrade OS

FreeBSD6: prio and JunOS14

FreeBSD10: JunOS 15 -> 17.

FreeBSD11: từ 18. -> nâng cấp khác kernel version - no-validate

release notes - upgrade/downgrade

Em gửi lại ae kết quả khi nâng cấp lên 18.4R3-S7.2 ạ :

- Bản 17.3R3-s2 validate fail

- Bản 17.4R3-S2 validate thành công

"Nếu upgrade qua 2 bước 17.3 -> 17.4 -> 18.4 thì anh nghĩ ko cần no-validate" => Hôm rồi anh Đăng có nói ý này ???????

help apropos versioning

- --

1. Từ 16 lên 18.4 (re thường)

- lên 17.4 sau đó lên 18.4, sử dụng option validate

2. Từ 17.3 lên 18.4 (re ng ở VTC)

- có thể nâng trực tiếp với option no-validate, test trên lab trước với cấu hình hiện tại

3. 17.4 lên 18.4 (re ng ở VNM)

- nâng trực tiếp với validate như bình thường
