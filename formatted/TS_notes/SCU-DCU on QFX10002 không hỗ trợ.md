# SCU-DCU on QFX10002 không hỗ trợ

Hi Thảo, Lực,

Qua phối hợp kiểm tra cùng Lực, thiết bị có apply policy classify SCU-DCU vào forwarding table, do thiết bị QFX10002 không hỗ trợ tính năng này, khi apply gây ảnh hưởng đến việc forward bản tin qua link ngang giữa 2 CDN. Điều này lý giải nguyên nhân vì sao lo0.0 trên 2 thiết bị CDN không thể ping được từ các thiets bị phía SMC khi shutdown uplink. Sau khi kĩ sư Ftel tìm hiểu và thử bỏ apply SCU-DCU, thiết bị đã có thể hoạt động đúng yêu cầu (dự phòng được qua link ngang giữa 2 thiết bị).

Case này sau khi thực hiện action kể trên, thiết bị đã hoạt động bình thường khoảng 2 tuần nay, vậy nếu không còn yêu cầu gì thêm mình xin phép đóng case nhé.

Mình cảm ơn
