# Close case

Dear Hoàng Anh!

 

Em cần thêm thông tin case này nữa không. Nếu không bên anh xin phép được close case này. 

Anh xin tổng hợp lại thông tin case: 

**Cảnh báo:**  

Trên thiết bị MX2010-THA00TXN xuất hiện cảnh báo: 

|May  9 04:21:22.269 2021    MX2010-THA00TXN_RE1 : %PFE-3: fpc6 Cmerror Op Set: XMCHIP(1): XMCHIP(1): FI:   Link sanity checks - Type 2, Seq Number 1864, Stream 13, Link0 0x80, Link1   0x6, Link2 0x10|
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

 

**Nguyên nhân**: 

- Do  lỗi hardware transient MCHIP.*FI.*Link sanity checks match KB31734. Khi gặp lỗi này script sẽ tự động disable PFE tương ứng để hạn chế ảnh hưởng.

 

**Phương án khắc phục:** 

- Thực hiện reboot FPC slot 6 để clear lỗi.
- Nếu lỗi còn lặp lại sau khi thực hiện restart FPC slot 6 thì thực hiện thay thế hardware

---

Đêm 11/6 tôi đã support nâng cấp xong thiết bị HNI001PER01.

Huy xem giúp tôi node mạng hiện tại có bất thường gì không?

Nếu không còn gì tôi xin phép close case này.
