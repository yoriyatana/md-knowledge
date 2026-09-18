# 1 số thông tin requirements để cắm đc card MPC7E/ MPC7E-MRATE trên  MX240/480/960

MPC7E-MRATE requirements:

1. Junos OS release 16.1R1 and later.

=> với các box version 15.1R6-S5 cần nâng cấp lên version >= 16.1R1 mới có thể tích hợp dc card MPC7E

=> với các box version 17.4R3-S2.4 có thể thực hiện tích hợp card MPC7E được.

2. Không khuyến nghị cắm MPC7E vào slot 0, 11 trên MX960

3. MPC7E-MRATE throughput line-rate được 480Gbps:

### Đối với MX960 sử dụng SCBE2 ở mode 2+1 sẽ hỗ trợ tối đã  340G/slot, để MPC7E chạy max dc 480G cần chuyển mode SCB thành 3+0.

Line-rate throughput of up to 480 Gbps on MX240, MX480, and MX960 routers.

### Đối với MX960 sử dụng SCBE3, do SCBE3 hỗ trợ up to 1 Tbps per slot nên khi SCBE3 ở mode fabric 2=1 hay 3+0 đều đáp ứng đươc throughput của MPC7E.

- --

MRATE sau khi thay đổi speed (pic-mode, port-mode) thì cần reboot lại linecard để nhận đúng.
