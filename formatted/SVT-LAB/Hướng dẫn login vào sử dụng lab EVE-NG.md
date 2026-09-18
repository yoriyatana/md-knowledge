# Hướng dẫn login vào sử dụng lab EVE-NG

Hướng dẫn sử dụng lab:

Thông tin để login vào lab:

+ Địa chỉ eve: 192.168.3.10

+ User login: tenho, (default password: lab123)

+ Folder để tạo topology lab của mỗi người : mọi người tạo lab đúng vị trí, và ko sử dụng bài lab của người khác, do có thể dẫn đến conflict.

![](image/73318753c977268a84441c403888e33a)

+ Hướng dẫn để install các Junos mới vào eve: (đã có sẵn một số OS anh em đã install vào từ trước: vMX 14, vMX 19.3, ….).

[Juniper vMX 16.X, 17.X (eve-ng.net)](https://www.eve-ng.net/index.php/documentation/howtos/howto-add-juniper-vmx-16-x-17-x/%20%5Ct%20_blank)

Hướng dẫn sử dụng tool gen cấu hình lab:

Nhân tiện có server mới, em giới thiệu thêm 1 tool nữa nhé:

+ Tên tool: gen\_eve\_lab\_conf

+ Công dụng: Tạo cấu hình tự động khi tạo lab eve (LDP, IGP, IP đấu nối, loopback, …)

+ Cách sử dụng:

1. / Tạo topology lab:

- Đặt tên các thiết bị: string+number: R1, r1, abc1, …

Loopback và các ip đấu nối sẽ được tạo dựa trên number trên tên.

Ex: R1: loopback 10.210.1.1, ip đấu nối: 10.10.x.1/24

R2: loopback 10.210.1.2, ip đấu nối: 10.10.x.2/24

- Đấu nối các thiết bị với nhau.

- Nếu xử dụng VCP + VFB, thì topo tạo VFB trước, đấu nối các VFB theo mô hình. Ko thêm VCP lúc này.

![](image/622fecab0dab3d279a9de7d78c46f273)

2. / Out lab và export file topo:

![](image/10a4b07ff218afb2cad9d97671a0eadd)

3. / Sau khi download về, giải nén ra sẽ được file .unl

![](image/de246a70507b6513d71321a611aae8d8)

4. / Đăng nhập vào website 192.168.3.188, chọn option GEN CONF và upload file lên:

![](image/86cd3dc9164ca77d12180eea8ecce0d6)

![](image/f7ab066396681be64efe196e0de25755)

5. / Chọn NEXT để upload file đi tới trang Advance option

![](image/cd286493ac238c67faffadbffad2f3e0)

6. / Chọn igp protocol: ospf or isis. Thêm vào các cấu hình mặc định.

Note: user đã có sẵn: root/lab123, lab/lab123

Sau đó click Generate configuration

![](image/1660baace798624a0706cf34ca05087c)

7. / Các file cấu hình đã được tạo ra theo file topology đã upload

![](image/5a7bfbe0bc1e107cf73761fb176e8337)

Em cập nhật thêm xíu nhé.

Sau khi tool generate xong conf sẽ có kèm theo 1 file new\_topo. New\_topo sẽ là topo cũ và note vào subnet các link để dễ hơn trong việc lab. Mọi người có thể upload ngược lên eve để sử dụng.

![](image/4224752076f614af16c5bab2d098672c)

Topo mới sau khi upload:

![](image/17a1afca34e5d0817dd8c52462160f86)

Regards
