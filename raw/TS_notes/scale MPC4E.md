# scale MPC4E

Phối hợp kiểm tra, xử lý lỗi trên card MPC4E

Vấn đề này trước đây bên anh cũng đã phản hồi Viettel:

- MPC4 32x10G, MPC4 2x100G + 8x10G:

- Card dung trên MX2K: Có 2 PFE, BW qua Fabric mỗi PFE là 130G -> Tổng card là 260G
- Card dung trên MX960 (2+1 SCB): Có 2 PFE, BW qua Fabric mỗi PFE là 126G -> Tổng card là 252G
- Card dung trên MX960 (3+0 SCB): Có 2 PFE, BW qua Fabric mỗi PFE là 130G -> Tổng card là 260G

-> Khi toàn bộ traffic trên các port đều cần qua Fabric thì BW Fabric không đảm bảo khi card sử dụng quá 130G mỗi PFE
