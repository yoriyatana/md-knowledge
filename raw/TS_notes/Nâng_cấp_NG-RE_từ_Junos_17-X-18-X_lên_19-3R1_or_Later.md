# Nâng cấp NG-RE từ Junos 17.X-18.X lên 19.3R1 or Later

Dear anh em.

 

Hôm nay anh có task cần nâng cấp Junos OS cho Next-Generation Routing Engine từ bản 18.4R3 lên 19.3R2 (dự án RR-VNPT-2020), nhận thấy có một số thay đổi quan trọng, dẫn đến cần phải update lại quy trình cũng như total thời gian nâng cấp cho khách hàng cũng tăng lên. Email này anh ko đề cập chi tiết quy trình nâng cấp, mà chỉ highlight các thay đổi để anh em lưu ý khi recommend hay trao đổi thông tin với khách hàng nhé.

1. **Tổng quan**: Bắt đầu từ phiên bản Junos 19.3R1, Junos OS yêu cầu vmhost cần phải hỗ trợ phần firmware tương ứng phải là version 6.0.1, trong khi các Junos trở về trước chỉ yêu cầu **version là 4.02**. Để xác định firmware version, anh em có thể dùng lệnh này (lưu ý chỉ thực hiện được lệnh này trê Master RE)

|Jun 01 16:33:44

**Routing Engine 0 RE  i40e-NVM       7    4.26       0          OK               �**� 

Routing Engine  1                    0   0.53.1     0         OK  
juniper@HNI-RR-ALL-RE0>  show system firmware |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

èNhư vậy, việc đầu tiên mình cần làm đó là nâng cấp firmware của box hiện tại lên đúng version 6.01 trước (cho cả 02 NG-RE). Nếu mình vẫn cố nâng cấp, sẽ gặp các log kiểu như này

|--- JUNOS 18.4R3-S4.2 Kernel  64-bit  JNPR-11.0-20200618.2bc7e35_buil

root@RR-VNPT-LAB_RE0:~ # cli

NVM_version: 04.26

DRV_version: 1.1.23

ERROR: i40e NVM firmware is  not compatible ,please upgrade i40e NVM before installing this package

ERROR: Aborting the  installation

1

ERROR: Upgrade failed
Last login: Tue Jun  1  06:56:49 2021 from re1|
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

1. **Junos OS hỗ trợ firmware 6.01**

Không phải tất cả các Junos OS đều hỗ trợ và tương thích với firmware 6.01, nói cách khác nếu Junos OS của khách hàng hiện tại không nằm trong list dưới đây, thì mình cần phải downgrade/upgrade lên 01 bản OS tương ứng để có thể nâng cấp được firemware. List chi tiết anh em tham khảo dưới đây

[https://www.juniper.net/documentation/us/en/software/junos/junos-install-upgrade/topics/task/vmhost-nvm-upgrade.html](https://www.juniper.net/documentation/us/en/software/junos/junos-install-upgrade/topics/task/vmhost-nvm-upgrade.html) ==>Table 1

Ví dụ: Box của khách hàng đang dùng là MX240/MX480/MX960 thì mình cần phải đảm bảo OS đang dùng phải là 17.1R3 hoặc 17.2R3/17.3R3 hoặc 18.1R1. Như hôm nay anh đang dùng 18.4R3-S4, vậy là phải downgrade về bản 17.3R3-S8 trước khi thực hiện các bước còn lại.

1. **Nâng cấp firmware**

Download bản firmware tương ứng từ link dưới đây. Lưu ý: Nếu ở bước  2 mình đã về bản 17.X thì sử dụng bản jfirmware 17, nếu mình lên bản 19 thì sử dụng jfirmware 19

[https://drive.google.com/drive/folders/1trobaxb3ykO9fzxHBKrn1ZglRc0bl-lp?usp=sharing](https://drive.google.com/drive/folders/1trobaxb3ykO9fzxHBKrn1ZglRc0bl-lp?usp=sharing)

**Lưu ý quan trọng:** Việc nâng cấp firmware này có 1 yêu cầu bắt buộc đó là  phải có người onsite để hỗ trợ kết nối với box qua dây console( để quan sát output tương ứng trong quá trình booting của RE). Ngoài ra, việc này cần thực hiện cho cả 02 NG-RE, do vậy đây là khoảng thời gian phát sinh thêm (total khoảng 45p đến 60p).

1. **Nâng cấp lên Junos 19.3R1**

Sau khi cả 02 RE đã được nâng cấp lên firmware 6.01, có thể thực hiện upgrade lên 19.3R1 như quy trình trước đây anh em vẫn làm.

|**Routing Engine 0 RE  i40e-NVM       7    6.1                    6.01                   OK**                 
root@RR-VNPT-LAB_RE0> show  system firmware | match i40 |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|

Sau này khi có case study cụ thể của khách hàng, anh sẽ xây dựng lại quy trình chi tiết và đầy đủ hơn nhé.
