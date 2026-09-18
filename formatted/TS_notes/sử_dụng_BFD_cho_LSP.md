# sử dụng BFD cho LSP

Như trao đổi sáng nay, để tránh trường hợp traffic bị blackhole do stuck tunnel (đang nghi ngờ lỗi trên HK04 hoặc PE04), anh đề xuất việc sử dụng BFD cho LSP để như một giải pháp phòng ngừa. Khi sử dụng BFD cho LSP có một số lưu ý như sau

- BFD cho LSP sử dụng tài nguyên của Routing Engine, do vậy không khuyến nghị khai báo quá nhiều, cũng như thời gian interval gửi BFD Hello không nên để mức millisecond.
- Cơ chế hoạt động của BFD cho LSP đó là từ Ingress sẽ gửi bản tin BFD Hello theo LSP mà mình muốn bảo vệ, bản tin này sẽ đi theo LSP đến Egress, và Egress sẽ ACK lại theo routing IGP, với bản tin UDP port 3784 àTrên RE Protect của Ingress PE cần mở thêm term này để BFD Up được.

Anh gửi cấu hình cho 01 LSP mẫu nhé

|Oct 19 13:58:46

to 150.10.10.1;

bandwidth 1g;

oam {

    bfd-liveness-detection {

        minimum-interval 1000;

        multiplier 3;

    }

}

no-cspf;

link-protection;

primary p_PATH;
root@PE-04> show configuration protocols mpls label-switched-path TO_PE_01|
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

Sử dụng câu lệnh dưới đây để verify trạng thái BFD

|Oct 19 13:59:54

                                                  Detect   Transmit

Address                  State     Interface      Time     Interval  Multiplier

127. 0.0.1                Up        xe-0/0/4.0     3.000     1.000        3

 Client RSVP-OAM, TX interval 1.000, RX interval 1.000

Session up time 00:04:39

Local diagnostic None, remote diagnostic None

Remote state Up, version 1

Session type: Multi hop BFD

Min async interval 1.000, min slow interval 1.000

Adaptive async TX interval 1.000, RX interval 1.000

Local min TX interval 1.000, minimum RX interval 1.000, multiplier 3

Remote min TX interval 0.050, min RX interval 0.050, multiplier 3

Local discriminator 17, remote discriminator 17

Echo TX interval 0.000, echo detection interval 0.000

Echo mode disabled/inactive

* *LSP-Name TO_PE_01**

* *Path-Name p_PATH**

  Session ID: 0x0

1 sessions, 1 clients

Cumulative transmit rate 1.0 pps, cumulative receive rate 1.0 pps
root@PE-04> show bfd session extensive|
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

HoaND

Thanks
