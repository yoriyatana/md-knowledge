# Untitled Note

Liên quan đến case này anh summarize lại như sau

1. Viettel có plan đổ tải hơn 27K thuê bao vào MPC7E (slot 2 và slot 3) và đang sử dụng Junos OS 17.3R3-S6. Với version này, cùng với việc sử dụng logical-interface-policer trong các gói cước, dẫn đến hit scaling và có hiện tượng xuất hiện Segment 4 trong phần allocate memory trên linecard (tương tự như log dưới đây)
2. Khi xuất hiện Segment 4 này, các thuê bao online sau sẽ không được cấp phát tài nguyên, dẫn đển ảnh hưởng dịch vụ àLiên quan đến lỗi này, bên anh đã có công văn khuyến nghị cần phải upgrade lên OS 18.4R3-S7 để fix được lỗi này, nhờ Phóng cùng anh em Viettel follow để nắm thông tin.
3. Cùng thời điểm xuất hiện log Segment 4 này, trên thiết bị còn xuất hiện các log và file **ppe như dưới đây (trên FPC3)**

|<163>1  2021-06-25T08:45:00.261+07:00 NAN8101BRA01_RE0 - - - - fpc3 EA[0:0].disp[3]  SECONDARY_TIMEOUT (PPE 0 Zone 3). 

<163>1  2021-06-25T08:45:00.261+07:00 NAN8101BRA01_RE0 - - - - fpc3 EA[0:0]_PPE 48  Errors thread timeout error 

<163>1  2021-06-25T08:45:00.261+07:00 NAN8101BRA01_RE0 - - - - fpc3 EA[0:0].disp[2]  SECONDARY_TIMEOUT (PPE 0 Zone 29). 

<163>1  2021-06-25T08:45:01.262+07:00 NAN8101BRA01_RE0 - - - - fpc3 EA[0:0]_PPE 72  Errors thread timeout error 

<163>1  2021-06-25T08:45:01.263+07:00 NAN8101BRA01_RE0 - - - - fpc3 EA[0:0].disp[3]  SECONDARY_TIMEOUT (PPE 0 Zone 3). 

<163>1  2021-06-25T08:45:01.264+07:00 NAN8101BRA01_RE0 - - - - fpc3 EA[0:0]_PPE 48  Errors thread timeout error 

<163>1  2021-06-25T08:45:01.265+07:00 NAN8101BRA01_RE0 - - - - fpc3 EA[0:0].disp[2]  SECONDARY_TIMEOUT (PPE 0 Zone 29).
<163>1  2021-06-25T08:45:00.261+07:00 NAN8101BRA01_RE0 - - - - fpc3 EA[0:0]_PPE 72  Errors thread timeout error |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

1. SVT + Juniper đã decode các file ppe xuất hiện trên thiết bị và ghi nhận gói tin malformed liên quan đến DNS,  cụ thể khi bóc tách gói tin upstream, FPC3 nhận thấy không đúng định dạng và sinh ra file ppe nói trên (PPE là 01 thành phần của khối LUSS trên MPC7E, có trách nhiệm tìm đường đi của gói tin)

èDưới đây là nội dung decode của file ppe trên thiết bị

|   8534003000024412

   2000018d003d01**81**

**   00**0000000000031d

   000000a000020000

   **45**00001c739d2171

   3b1184de**cb718302**

   7468a3083030313a

   3530303a36303a3a

//obmit  output

Với gói tin bình thường trong mô hình BRAS, từ giá tri 8100 đến  giá trị 45 chỉ cách nhau 04 byte (8 giá trị hexa)
   1ad8809005f40000|
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

1. Về việc xuất hiện malformed, SVT+Juniper cũng đã test và tìm cách replicate trong lab tuy nhiên chưa tạo ra được dạng file này, các file ppe này cũng không còn xuất hiện thêm kể từ thời điểm card FPC2/FPC3 được rebooted (Từ ngày 26/06)

Vậy bên anh báo lại để Phóng nắm thông tin, đồng thời có thêm câu hỏi gì nữa để bên anh làm rõ thêm nhé.
