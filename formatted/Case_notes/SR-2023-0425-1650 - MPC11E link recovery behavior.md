# SR-2023-0425-1650 - MPC11E link recovery behavior

SR-2023-0425-1650

\* Qua quá trình phối hợp thực hiện các test cases:

\* Đấu nối trực tiếp giữa MPC11E và các MPC khác;

\* Đấu nối qua truyền dẫn DWDM (OTN) giữa MPC11E và MX204, MPC9E và MX204;

\* Cũng như các thông tin từ JTAC, SVTECH xin thông tin:

\* Việc thời gian chuyển trang thái từ Down --> Up lại của MPC11E sẽ rơi vào khoảng 25s--35s.

\* Đây là hành xử do thiết kế của dòng card MPC11E (sử dụng dòng chip ZT) mới.

\* Với Junos OS từ 21.3R1 về sau, có thể cải thiện thời gian re-up lại port của MPC11E giảm đi 10 seconds, nghĩa là rơi vào khoảng 15s--25s.

\* Đối với các dòng card này, việc cấu hình hình Hold-time Down được khuyến nghị ở mức Seconds, và phải lớn hơn 25s (không hoạt động được ở mức sub-seconds (ms))

\* Vì đây là hành xử của card MPC11E, nên xin gửi đến các Anh thông tin, rất mong FTEL sẽ thiết kế & triển khai cards trong các LACP AE interfaces và có dự phòng đủ để tránh đuợc hiện tượng mất traffic dịch vụ của thiết bị tại Tỉnh/TP.

Ngoài ra, như thông tin đã trao đổi, việc port detect down dựa vào tín hiệu LF từ hệ thống DWDM (Mac Fault Change. Mac LF (0 -> 1) Mac RF (0 -> 0)) khi sử dụng truyền dẫn DWDM (OTN | PSM).

\* Hành xử này được thấy trên cả MPC11E và MPC9E, nên port et- interface lập tức chuyển trạng thái sang down.

\* Vậy nhờ Thọ trao đổi cùng các Anh truyền dẫn FTEL xem có tinh chỉnh Optional trên hệ thống DWDM để không gửi thông tin LF này cho các đầu Local hoặc far end CE (Router) được không? Việc này có thể giúp cho port et- trên card MPC11E không chuyển trạng thái sang “down”.

However, as described in AT#292-B, the hold-down time on MPC11 is still not perfect if tested via toggling laser OFF/ON. For Rx LOS clear, the actual link up recovery time is longer due to a lengthy DFE tune time caused by Inphi gear box. Hold-down time shorter than 25 seconds won't work as expected.
