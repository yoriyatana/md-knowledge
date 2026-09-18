# Cơ chế điều chỉnh tốc độ quạt MX

Dear a.Hạ, a.Khoa,

Sáng nay em có phối hợp với a.Khoa kiểm tra qua, hiện tại các thiết bị mà FAN bị điều chỉnh tốc độ quạt sau khi gắn card MPC3E-NG vào mà mình đã báo thì các thiết bị này đang chạy version Junos OS 15.1R7. Với Junos OS version này, khi gắn card MPC3E-NG vào thì sẽ gây ra việc quạt bị điều chỉnh tốc độ quạt liên tục như đã đề cập ở PR1316192 mà năm ngoái em có làm việc với bên mình ở case "SR#23220001/VNPT-NET3/MAN-E 10TTP 2017/Kiểm tra cảnh báo nhiệt độ cao, Fan high speed thiết bị GLI08PKU" như thông tin bên dưới:

------------------------------------

Cơ chế điều chỉnh tốc độ quạt ở trên version 15.1 là dựa vào hardcoded values theo từng dòng chipset ASIC. Trên các dòng card NG mới như MPC3E-3D-NG thì kiến trúc card đã thay đổi hoàn toàn nên việc dùng cơ chế này để thay đổi tốc độ quạt không còn được tối ưu. Do đó, trên các OS bị ảnh hưởng bởi PR này, khi gắn các card này vào thì tốc độ quạt sẽ thay đổi thường xuyên.

Ở các bản fixed releases (17.3R3-S7) thì Juniper đã thay đổi lại cơ chế điều chỉnh tốc độ quạt theo từng loại linecard khác nhau, chứ không chỉ dựa vào loại chipset ASIC, nên khi đó, quạt sẽ không còn thay đổi tốc độ thường xuyên như đã gặp trên các version 15.1.

------------------------------------

Như đã trao đổi với anh Hạ, trước mắt nhờ các anh INOC3 xem có thể cải thiện được nhiệt độ phòng máy tại điểm hút gió vào của thiết bị không - đồng thời vệ sinh thêm airfilter của thiết bị. Nếu bên mình đã thực hiện rồi mà việc điều chỉnh tốc độ quạt vẫn xảy ra liên tục thì có thể cân nhắc để nâng cấp lên fixed release ạ.

Regards,

NgocND

+84.90.886.0884

---
