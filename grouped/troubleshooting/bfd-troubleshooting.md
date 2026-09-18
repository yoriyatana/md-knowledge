# BFD Troubleshooting

> Generated deterministically from the approved grouping manifest.


## Source: `formatted/TS_notes/BFD anchorship PFE.md`

# BFD anchorship PFE

Như đã trao đổi qua phone:

- Theo anh hiểu khi thiết kế anchor BFD thì Juniper đã không xét đến trường hợp PFE bị disable, chỉ xét đến trường hợp MPC bị offline

- Mình có thể cân nhắc 2 giải pháp:

1. dùng (micro-bfd + dynamic routing) thay vì multihop-bfd cho bgp. Lúc này không cần quan tâm đến vụ anchor nữa vì BFD chạy trên từng AE member. Nếu mất cả 2 AE thì BGP sẽ down ngay vì không còn route nữa (hy vọng ko có 0/0).

2. sửa lại pfe\_disable\_script thành ra là offline cả mpc thay vì chỉ disable PFE (number 0)

Còn việc yêu cầu ER (Enhanced Request) thì sẽ cần:

- giải thích chi tiết scenario sử dụng, tốt nhất là dạng ppt. Bao gồm cả platform, hardware yêu cầu.

- việc này sẽ mất nhiều thời gian để thực hiện, Thái có thể làm rõ thêm với Cương nhé.

- --

Hi Tân, case nhiều session BFD đều ăn theo duy nhất 1 Anchor PFE lúc trước. sau thời gian JTAC verify behavior và hỏi thông tin từ engineering.

JTAC nói không có câu lệnh manual nào để ép các BFD sessions ăn theo các Anchor PFE khác nhau nhé.

Here are the final comments from Engineering on this matter.

(1)     BFD anchorship will not change when PFE disable action is taken on any of the instance of anchor FPC.

(2)     When PFE disable action is taken, Non-Inline BFD session (e.g. multihop) may go down and come up again if there is another PFE instance on the anchor FPC and the peer router is still reachable.

(3)     Inline BFD session may remain down if the anchor PFE instance is disabled.

Is there other way to force 4 BFD sessions distributed to 2 FPC equally, no need to reboot the FPC?

JTAC : There is no way to delegate anchor ship manually

Chào a.Đăng, a.Hưng, a.Cương Juniper và anh em SVTech,

Gần đây trên mạng Viettel có case như sau:

- Trên thiết bị có 4 phiên Inline-BFD và cả 4 phiên này đang được xử lý in-line trên cùng 1 FPC.
- Thời điểm lỗi thiết bị xuất hiện Major Alarm trên FPC làm disable PFE, dẫn đến cả 4 phiên inline-BFD này stuck ở trạng thái Init/Down làm ảnh hưởng dịch vụ.

SVTech có test các action disable PFE/reboot FPC (bằng câu lệnh request lẫn trigger major alarm) thì ghi nhận các behavior BFD tóm gọn ở một số ý như sau: *(**Chi tiết test case xem luồng email bên dưới**)*

- Từ TC10 có thể thấy, việc xóa đi tạo lại cấu hình session BFD thì Junos vẫn hành xử ăn theo 1 FPC đã được dedicated từ trước. Chỉ có việc reboot FPC thì session BFD mới ăn theo 1 FPC khác.
- Từ TC5 & TC6 có thể thấy, khi reboot chassis, card FPC nào online trước thì BFD session sẽ ăn theo FPC đó. *Note: ghi nhận trên lab thì FPC8 online trước FPC7 khoảng 1 phút 30 giây đến 2 phút.*
- *Note: test với junos* *17.4R3-S2 và 18.4R3-S7 đều có behavior tương tự.*

Do đó, SVTech có mở case với JTAC làm rõ cách các phiên inline-BFD lựa chọn Anchor FPC nào để xử lý in-line, cũng như hỏi JTAC/engineering xem có cách nào để ép các BFD sessions ăn theo các Anchor PFE khác nhau hay không?

* Case ID: 2021-1007-335833*

Câu trả lời của JTAC như sau:

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

(2)     When PFE disable action is taken, **Non-Inline** BFD session (e.g. multihop) may go down and come up again if there is another PFE instance on the anchor FPC and the peer router is still reachable.

(3)     Inline BFD session may remain down if the anchor **PFE instance** is disabled.

- JTAC : There is no way to delegate anchor ship manually

* *[SVTech]:**

As per your JTAC & engineering comment:

1. May I know this kind of behavior is as per design or not ?
2. Juniper has any plan to change this behavior on any upcoming release ? That’s because of point (3): Inline BFD session may remain down if the anchor **PFE instance** is disabled.

* *[JTAC]:**

Hello Thai

I too have tested in different release then only we went to engineering .

As I mentioned this behaviour is as per design , I am not aware of any plan to change this behaviour .

If you have any requirement you can try raising ER through accounts team.

Nhờ các anh Juniper xem giúp SVTech behavior BFD này và có cân nhắc hay escalate nội bộ để thay đổi behavior không mong muốn như point (3) được không ạ?

Em xin cảm ơn.

Hi Nirosh,

![](../assets/bfd-troubleshooting/9be26875e1-2fee46b7af4f6bc48075ca075fac4571.png)

(3)  **Inline BFD** session may remain down if the anchor **PFE instance** is disabled.

I am discussing with Juniper SE about the point (3) regarding to Inline BFD.

Meanwhile, I performed some test cases regarding to point (2) – Try to configure Non-Inline BFD. Below are my observations:

1. / TC 1: Configure “set routing-options ppm no-inline-processing” . That means BFD sessions is still distributed to FPC but No-Inline BFD.

|  |
| --- |
| {master}[edit groups test-BFD routing-options]  lab@test# show  ppm {  no-inline-processing;  }  static {  route 125.235.249.1/32 {  next-hop 10.20.41.29;  qualified-next-hop 10.20.41.31 {  bfd-liveness-detection {  minimum-interval 300;  neighbor 10.20.41.31;  local-address 10.20.41.30;  }  }  bfd-liveness-detection {  minimum-interval 300;  neighbor 10.20.41.29;  local-address 10.20.41.28;  }  }  route 125.235.251.185/32 {  next-hop 10.20.41.33;  qualified-next-hop 10.20.41.35 {  bfd-liveness-detection {  minimum-interval 300;  neighbor 10.20.41.35;  local-address 10.20.41.34;  }  }  bfd-liveness-detection {  minimum-interval 300;  neighbor 10.20.41.33;  local-address 10.20.41.32;  }  }  }  autonomous-system 7552;  lab@test# run show bfd session  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.29              Up        ae1.1          0.900     0.300        3  10.20.41.31              Up        ae2.1          0.900     0.300        3  10.20.41.33              Up        ae1.2          0.900     0.300        3  10.20.41.35              Up        ae2.2          0.900     0.300        3  4 sessions, 4 clients  Cumulative transmit rate 13.3 pps, cumulative receive rate 13.3 pps  {master}[edit]  lab@test# run show bfd session detail  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.29              Up        ae1.1          0.900     0.300        3  Client Static, TX interval 0.300, RX interval 0.300  Session up time 00:03:08, previous down time 00:00:03  Local diagnostic None, remote diagnostic None  Remote state Up, version 1  Replicated  Session type: Single hop BFD  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.31              Up        ae2.1          0.900     0.300        3  Client Static, TX interval 0.300, RX interval 0.300  Session up time 00:03:08, previous down time 00:00:03  Local diagnostic None, remote diagnostic None  Remote state Up, version 1  Replicated  Session type: Single hop BFD  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.33              Up        ae1.2          0.900     0.300        3  Client Static, TX interval 0.300, RX interval 0.300  Session up time 00:03:08, previous down time 00:00:03  Local diagnostic None, remote diagnostic None  Remote state Up, version 1  Replicated  Session type: Single hop BFD  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.35              Up        ae2.2          0.900     0.300        3  Client Static, TX interval 0.300, RX interval 0.300  Session up time 00:03:08, previous down time 00:00:03  Local diagnostic None, remote diagnostic None  Remote state Up, version 1  Replicated  Session type: Single hop BFD  4 sessions, 4 clients  Cumulative transmit rate 13.3 pps, cumulative receive rate 13.3 pps  {master}[edit]  lab@test# run show ppm adjacencies protocol bfd detail  Protocol: BFD, Hold time: 900, IFL-index: 329  Distributed: TRUE  Replicated  BFD discriminator: 28, BFD routing table index: 0  Redirection Type: DYNAMIC\_FILTER, Rule Term Src: 10.20.41.29, Rule Term Port: 3784, Rule Term Action: 605  Num Packets: 16, Absorbed Packets: 0, Rx Packet: 20 C8 03 18 00 00 00 36 00 00 00 1C 00 04 93 E0 00 04 93 E0 00 00 00 00  Distribution handle: 99, Distribution address: fpc7  Protocol: BFD, Hold time: 900, IFL-index: 330  Distributed: TRUE  Replicated  BFD discriminator: 29, BFD routing table index: 0  Redirection Type: DYNAMIC\_FILTER, Rule Term Src: 10.20.41.33, Rule Term Port: 3784, Rule Term Action: 605  Num Packets: 16, Absorbed Packets: 0, Rx Packet: 20 C8 03 18 00 00 00 34 00 00 00 1D 00 04 93 E0 00 04 93 E0 00 00 00 00  Distribution handle: 97, Distribution address: fpc7  Protocol: BFD, Hold time: 900, IFL-index: 333  Distributed: TRUE  Replicated  BFD discriminator: 32, BFD routing table index: 0  Redirection Type: DYNAMIC\_FILTER, Rule Term Src: 10.20.41.35, Rule Term Port: 3784, Rule Term Action: 605  Num Packets: 15, Absorbed Packets: 0, Rx Packet: 20 C8 03 18 00 00 00 39 00 00 00 20 00 04 93 E0 00 04 93 E0 00 00 00 00  Distribution handle: 95, Distribution address: fpc7  Protocol: BFD, Hold time: 900, IFL-index: 332  Distributed: TRUE  Replicated  BFD discriminator: 33, BFD routing table index: 0  Redirection Type: DYNAMIC\_FILTER, Rule Term Src: 10.20.41.31, Rule Term Port: 3784, Rule Term Action: 605  Num Packets: 16, Absorbed Packets: 0, Rx Packet: 20 C8 03 18 00 00 00 38 00 00 00 21 00 04 93 E0 00 04 93 E0 00 00 00 00  Distribution handle: 96, Distribution address: fpc7  Adjacencies: 4, Remote adjacencies: 4  lab@test# run request pfe execute command "show ppm adjacencies protocol bfd" target fpc7  SENT: Ukern command: show ppm adjacencies protocol bfd  PPM Adjacency information for BFD  IFL-index  Holdtime  PPM handle   Discr  Absorbed   Packets   Length  Dist  Do-dist HadExpired  ExpCount  LargeDiff  LastRx Leaked Leak timer Inline Session State  Rx-Packet  329        900       14              28  811        826       24      no-dist no-do-dist FALSE      0     320        300    0      FALSE       NO     UP  20 C8 03 18 00 00 00 36 00 00 00 1C 00 04 93 E0 00 04 93 E0 00 00 00 00  330        900       12              29  811        826       24      no-dist no-do-dist FALSE      0     320        300    0      FALSE       NO     UP  20 C8 03 18 00 00 00 34 00 00 00 1D 00 04 93 E0 00 04 93 E0 00 00 00 00  333        900       10              32  811        826       24      no-dist no-do-dist FALSE      0     320        300    0      FALSE       NO     UP  20 C8 03 18 00 00 00 39 00 00 00 20 00 04 93 E0 00 04 93 E0 00 00 00 00  332        900       11              33  811        827       24      no-dist no-do-dist FALSE      0     320        300    0      FALSE       NO     UP  20 C8 03 18 00 00 00 38 00 00 00 21 00 04 93 E0 00 04 93 E0 00 00 00 00  lab@test# run show chassis hardware | match fpc  FPC 2            REV 20   750-038489   CAEA0979          MPCE Type 1 3D  FPC 7            REV 06   750-063744   CAGZ6743          MPCE Type 2 3D  FPC 8            REV 06   750-063747   CAJW8640          MPCE Type 1 3D  {master}[edit]  lab@test# run show chassis fabric fpcs  Fabric management FPC state:  FPC 2  PFE #0  Plane 0: Plane enabled  Plane 1: Plane enabled  Plane 2: Plane enabled  Plane 3: Plane enabled  Plane 4: Links ok  Plane 5: Links ok  FPC 7  PFE #0  Plane 0: Plane enabled  Plane 1: Plane enabled  Plane 2: Plane enabled  Plane 3: Plane enabled  Plane 4: Links ok  Plane 5: Links ok  PFE #1  Plane 0: Plane enabled  Plane 1: Plane enabled  Plane 2: Plane enabled  Plane 3: Plane enabled  Plane 4: Links ok  Plane 5: Links ok  FPC 8  PFE #0  Plane 0: Plane enabled  Plane 1: Plane enabled  Plane 2: Plane enabled  Plane 3: Plane enabled  Plane 4: Links ok  Plane 5: Links ok |

1. 1/ TC 1.1: FPC slot 7 has 2 PFE instances (PFE #0 and PFE #1). I bring down PFE #0 on FPC7 (PFE #1 is still available).

* However, BFD sessions got stuck to Init/Down state, they did not* *come up again if there is another PFE instance on the anchor FPC and the peer router is still reachable.*

|  |
| --- |
| lab@test# run **request chassis fabric pfe 0 fpc 7 offline**  PFE Fabric offline initiated, use "show chassis fabric fpcs/plane" to verify  lab@test# run show chassis fabric fpcs  Fabric management FPC state:  FPC 2  PFE #0  Plane 0: Plane enabled  Plane 1: Plane enabled  Plane 2: Plane enabled  Plane 3: Plane enabled  Plane 4: Links ok  Plane 5: Links ok  **FPC 7**  **PFE #0**  **: Fabric Disabled**  PFE #1  Plane 0: Plane enabled  Plane 1: Plane enabled  Plane 2: Plane enabled  Plane 3: Plane enabled  Plane 4: Links ok  Plane 5: Links ok  FPC 8  PFE #0  Plane 0: Plane enabled  Plane 1: Plane enabled  Plane 2: Plane enabled  Plane 3: Plane enabled  Plane 4: Links ok  lab@test# run show bfd session  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.29              **Init**      ae1.1          6.000     2.000        3  10.20.41.31              **Init**      ae2.1          6.000     2.000        3  10.20.41.33              **Init**      ae1.2          6.000     2.000        3  10.20.41.35              **Init**      ae2.2          6.000     2.000        3  4 sessions, 4 clients  Cumulative transmit rate 2.0 pps, cumulative receive rate 2.0 pps  {master}[edit]  lab@test# run show bgp summary  Groups: 1 Peers: 2 Down peers: 2  Table          Tot Paths  Act Paths Suppressed    History Damp State    Pending  inet.0  0          0          0          0          0          0  Peer                     AS      InPkt     OutPkt    OutQ   Flaps Last Up/Dwn State|#Active/Received/Accepted/Damped...  125.235.249.1          7552          0          0       0       1        5:22 Connect  125.235.251.185        7552          0          0       0       1        5:41 Active  lab@test# run show ppm adjacencies protocol bfd detail  Protocol: BFD, Hold time: 6000, IFL-index: 329  **No-absorb, No-refresh, Do-not-age, Distributed: TRUE**  Replicated  BFD discriminator: 28, BFD routing table index: 0  Redirection Type: DYNAMIC\_FILTER, Rule Term Src: 10.20.41.29, Rule Term Port: 3784, Rule Term Action: 605  Num Packets: 16, Absorbed Packets: 0, Rx Packet: 20 C8 03 18 00 00 00 36 00 00 00 1C 00 04 93 E0 00 04 93 E0 00 00 00 00  Distribution handle: 99, Distribution address: fpc7  Protocol: BFD, Hold time: 6000, IFL-index: 330  No-absorb, No-refresh, Do-not-age, Distributed: TRUE  Replicated  BFD discriminator: 29, BFD routing table index: 0  Redirection Type: DYNAMIC\_FILTER, Rule Term Src: 10.20.41.33, Rule Term Port: 3784, Rule Term Action: 605  Num Packets: 16, Absorbed Packets: 0, Rx Packet: 20 C8 03 18 00 00 00 34 00 00 00 1D 00 04 93 E0 00 04 93 E0 00 00 00 00  Distribution handle: 97, Distribution address: fpc7  Protocol: BFD, Hold time: 6000, IFL-index: 333  No-absorb, No-refresh, Do-not-age, Distributed: TRUE  Replicated  BFD discriminator: 32, BFD routing table index: 0  Redirection Type: DYNAMIC\_FILTER, Rule Term Src: 10.20.41.35, Rule Term Port: 3784, Rule Term Action: 605  Num Packets: 15, Absorbed Packets: 0, Rx Packet: 20 C8 03 18 00 00 00 39 00 00 00 20 00 04 93 E0 00 04 93 E0 00 00 00 00  Distribution handle: 95, Distribution address: fpc7  Protocol: BFD, Hold time: 6000, IFL-index: 332  No-absorb, No-refresh, Do-not-age, Distributed: TRUE  Replicated  BFD discriminator: 33, BFD routing table index: 0  Redirection Type: DYNAMIC\_FILTER, Rule Term Src: 10.20.41.31, Rule Term Port: 3784, Rule Term Action: 605  Num Packets: 16, Absorbed Packets: 0, Rx Packet: 20 C8 03 18 00 00 00 38 00 00 00 21 00 04 93 E0 00 04 93 E0 00 00 00 00  Distribution handle: 96, Distribution address: fpc7  Adjacencies: 4, Remote adjacencies: 4  lab@test# run request pfe execute command "show ppm adjacencies protocol bfd" target fpc7  SENT: Ukern command: show ppm adjacencies protocol bfd  PPM Adjacency information for BFD  IFL-index  Holdtime  PPM handle   Discr  Absorbed   Packets   Length  Dist  Do-dist HadExpired  ExpCount  LargeDiff  LastRx Leaked Leak timer Inline Session State  Rx-Packet  329        6000      14              28  2468       2483      24      no-dist no-do-dist FALSE      0     320        300    0      FALSE       NO     DOWN  20 C8 03 18 00 00 00 36 00 00 00 1C 00 04 93 E0 00 04 93 E0 00 00 00 00  330        6000      12              29  2468       2483      24      no-dist no-do-dist FALSE      0     320        300    0      FALSE       NO     DOWN  20 C8 03 18 00 00 00 34 00 00 00 1D 00 04 93 E0 00 04 93 E0 00 00 00 00  333        6000      10              32  2468       2483      24      no-dist no-do-dist FALSE      0     320        300    0      FALSE       NO     DOWN  20 C8 03 18 00 00 00 39 00 00 00 20 00 04 93 E0 00 04 93 E0 00 00 00 00  332        6000      11              33  2467       2483      24      no-dist no-do-dist FALSE      0     320        300    0      FALSE       NO     DOWN   20. 8 03 18 00 00 00 38 00 00 00 21 00 04 93 E0 00 04 93 E0 00 00 00 00 |

1. 2/ TC 1.2: FPC slot 7 has 2 PFE instances (PFE #0 and PFE #1). I bring down PFE #1 on FPC7 (PFE #0 is still available). BFD session still remain Up.

* Note: I tried to bring down PFE #1 many times and can see there is no affected when shutting down PFE#1.*

|  |
| --- |
| lab@test# run show bfd session  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.29              Up        ae1.1          0.900     0.300        3  10.20.41.31              Up        ae2.1          0.900     0.300        3  10.20.41.33              Up        ae1.2          0.900     0.300        3  10.20.41.35              Up        ae2.2          0.900     0.300        3  4 sessions, 4 clients  Cumulative transmit rate 13.3 pps, cumulative receive rate 13.3 pps  {master}[edit]  lab@test# run show ppm adjacencies protocol bfd detail  Protocol: BFD, Hold time: 900, IFL-index: 329  Distributed: TRUE  Replicated  BFD discriminator: 28, BFD routing table index: 0  Redirection Type: DYNAMIC\_FILTER, Rule Term Src: 10.20.41.29, Rule Term Port: 3784, Rule Term Action: 605  Num Packets: 28, Absorbed Packets: 0, Rx Packet: 20 C8 03 18 00 00 00 36 00 00 00 1C 00 04 93 E0 00 04 93 E0 00 00 00 00  Distribution handle: 139, Distribution address: fpc7  Protocol: BFD, Hold time: 900, IFL-index: 330  Distributed: TRUE  Replicated  BFD discriminator: 29, BFD routing table index: 0  Redirection Type: DYNAMIC\_FILTER, Rule Term Src: 10.20.41.33, Rule Term Port: 3784, Rule Term Action: 605  Num Packets: 27, Absorbed Packets: 0, Rx Packet: 20 C8 03 18 00 00 00 34 00 00 00 1D 00 04 93 E0 00 04 93 E0 00 00 00 00  Distribution handle: 138, Distribution address: fpc7  Protocol: BFD, Hold time: 900, IFL-index: 333  Distributed: TRUE  Replicated  BFD discriminator: 32, BFD routing table index: 0  Redirection Type: DYNAMIC\_FILTER, Rule Term Src: 10.20.41.35, Rule Term Port: 3784, Rule Term Action: 605  Num Packets: 27, Absorbed Packets: 0, Rx Packet: 20 C8 03 18 00 00 00 39 00 00 00 20 00 04 93 E0 00 04 93 E0 00 00 00 00  Distribution handle: 136, Distribution address: fpc7  Protocol: BFD, Hold time: 900, IFL-index: 332  Distributed: TRUE  Replicated  BFD discriminator: 33, BFD routing table index: 0  Redirection Type: DYNAMIC\_FILTER, Rule Term Src: 10.20.41.31, Rule Term Port: 3784, Rule Term Action: 605  Num Packets: 27, Absorbed Packets: 0, Rx Packet: 20 C8 03 18 00 00 00 38 00 00 00 21 00 04 93 E0 00 04 93 E0 00 00 00 00  Distribution handle: 137, Distribution address: fpc7  Adjacencies: 4, Remote adjacencies: 4  lab@test# run **request chassis fabric pfe 1 fpc 7 offline**  PFE Fabric offline initiated, use "show chassis fabric fpcs/plane" to verify  {master}[edit]  lab@test# run show chassis fabric fpcs  Fabric management FPC state:  FPC 2  PFE #0  Plane 0: Plane enabled  Plane 1: Plane enabled  Plane 2: Plane enabled  Plane 3: Plane enabled  Plane 4: Links ok  Plane 5: Links ok  FPC 7  PFE #0  Plane 0: Plane enabled  Plane 1: Plane enabled  Plane 2: Plane enabled  Plane 3: Plane enabled  Plane 4: Links ok  Plane 5: Links ok  PFE #1  : Fabric Disabled  FPC 8  PFE #0  Plane 0: Plane enabled  Plane 1: Plane enabled  Plane 2: Plane enabled  Plane 3: Plane enabled  Plane 4: Links ok  Plane 5: Links ok  lab@test# run show bfd session  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.29              Up        ae1.1          0.900     0.300        3  10.20.41.31              Up        ae2.1          0.900     0.300        3  10.20.41.33              Up        ae1.2          0.900     0.300        3  10.20.41.35              Up        ae2.2          0.900     0.300        3 |

2. / TC 2: Configure “set routing-options ppm no-inline-processing” and configure “no-delegate-processing” .

That means BFD sessions is processed in centralized mode – Routing Engine based. No distribution to FPC anymore. In case of one of PFE/FPC disabled/offline, BFD sessions still remain UP.

|  |
| --- |
| {master}[edit groups test-BFD routing-options]  lab@test# show  ppm {  no-delegate-processing;  no-inline-processing;  }  static {  route 125.235.249.1/32 {  next-hop 10.20.41.29;  qualified-next-hop 10.20.41.31 {  bfd-liveness-detection {  minimum-interval 300;  neighbor 10.20.41.31;  local-address 10.20.41.30;  }  }  bfd-liveness-detection {  minimum-interval 300;  neighbor 10.20.41.29;  local-address 10.20.41.28;  }  }  route 125.235.251.185/32 {  next-hop 10.20.41.33;  qualified-next-hop 10.20.41.35 {  bfd-liveness-detection {  minimum-interval 300;  neighbor 10.20.41.35;  local-address 10.20.41.34;  }  }  bfd-liveness-detection {  minimum-interval 300;  neighbor 10.20.41.33;  local-address 10.20.41.32;  }  }  }  autonomous-system 7552;  lab@test# run show bfd session  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.29              Up        ae1.1          0.900     0.300        3  10.20.41.31              Up        ae2.1          0.900     0.300        3  10.20.41.33              Up        ae1.2          0.900     0.300        3  10.20.41.35              Up        ae2.2          0.900     0.300        3  4 sessions, 4 clients  Cumulative transmit rate 13.3 pps, cumulative receive rate 13.3 pps  {master}[edit]  lab@test# run show bfd session detail  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.29              Up        ae1.1          0.900     0.300        3  Client Static, TX interval 0.300, RX interval 0.300  Session up time 00:07:32, previous down time 00:00:03  Local diagnostic None, remote diagnostic None  Remote state Up, version 1  Replicated  Session type: Single hop BFD  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.31              Up        ae2.1          0.900     0.300        3  Client Static, TX interval 0.300, RX interval 0.300  Session up time 00:07:32, previous down time 00:00:03  Local diagnostic None, remote diagnostic None  Remote state Up, version 1  Replicated  Session type: Single hop BFD  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.33              Up        ae1.2          0.900     0.300        3  Client Static, TX interval 0.300, RX interval 0.300  Session up time 00:07:32, previous down time 00:00:03  Local diagnostic None, remote diagnostic None  Remote state Up, version 1  Replicated  Session type: Single hop BFD  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.35              Up        ae2.2          0.900     0.300        3  Client Static, TX interval 0.300, RX interval 0.300  Session up time 00:07:32, previous down time 00:00:03  Local diagnostic None, remote diagnostic None  Remote state Up, version 1  Replicated  Session type: Single hop BFD  4 sessions, 4 clients  lab@test# run show ppm adjacencies protocol bfd detail  Protocol: BFD, Hold time: 900, IFL-index: 329  Distributed: FALSE  Replicated  In Do-Dist thread:  BFD discriminator: 28, BFD routing table index: 0  HadExpired: FALSE, Expired-Count: 0, Largest-Interval: 326, Last Rx Interval: 300, Num Packets: 1572, Absorbed Packets: 1568, Rx Packet: 20 C8 03 18 00 00 00 36 00 00 00 1C 00 04 93 E0 00 04 93 E0 00 00 00 00  Protocol: BFD, Hold time: 900, IFL-index: 330  Distributed: FALSE  Replicated  In Do-Dist thread:  BFD discriminator: 29, BFD routing table index: 0  HadExpired: FALSE, Expired-Count: 0, Largest-Interval: 349, Last Rx Interval: 299, Num Packets: 1573, Absorbed Packets: 1568, Rx Packet: 20 C8 03 18 00 00 00 34 00 00 00 1D 00 04 93 E0 00 04 93 E0 00 00 00 00  Protocol: BFD, Hold time: 900, IFL-index: 333  Distributed: FALSE  Replicated  In Do-Dist thread:  BFD discriminator: 32, BFD routing table index: 0  HadExpired: FALSE, Expired-Count: 0, Largest-Interval: 349, Last Rx Interval: 299, Num Packets: 1574, Absorbed Packets: 1568, Rx Packet: 20 C8 03 18 00 00 00 39 00 00 00 20 00 04 93 E0 00 04 93 E0 00 00 00 00  Protocol: BFD, Hold time: 900, IFL-index: 332  Distributed: FALSE  Replicated  In Do-Dist thread:  BFD discriminator: 33, BFD routing table index: 0  HadExpired: FALSE, Expired-Count: 0, Largest-Interval: 326, Last Rx Interval: 299, Num Packets: 1573, Absorbed Packets: 1568, Rx Packet: 20 C8 03 18 00 00 00 38 00 00 00 21 00 04 93 E0 00 04 93 E0 00 00 00 00  Adjacencies: 4, Remote adjacencies: 0  ### BFD sessions based Routing Engine ###  lab@test# show interfaces lo0 | display inheritance no-comments  **unit 0 {**  **family inet {**  **filter {**  **output protect-re;**  }  address 125.235.249.147/32 {  primary;  lab@test# show firewall family inet filter protect-re | display inheritance no-comments  term 1 {  **from {**  **protocol udp;**  **destination-port 3784;**  **}**  **then {**  **count Singlehop-BFD-based-RE;**  accept;  }  }  term final {  then accept;  }  lab@test# run show bfd session  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  10.20.41.29              Up        ae1.1          0.900     0.300        3  10.20.41.31              Up        ae2.1          0.900     0.300        3  10.20.41.33              Up        ae1.2          0.900     0.300        3  10.20.41.35              Up        ae2.2          0.900     0.300        3  4 sessions, 4 clients  Cumulative transmit rate 13.3 pps, cumulative receive rate 13.3 pps  {master}[edit]  lab@test# run show firewall filter protect-re  Filter: protect-re  Counters:  Name                                                Bytes              Packets  Singlehop-BFD-based-RE                             100204                 1927 |

As per JTAC/Engineering comments so far:

Can you clarify and answer observations from test case 1.1 and 1.2:

- From the test case TC1.1, I can see BFD session did not come up when shutting down PFE #0 while PFE#1 is available.
- From the test case TC1.2, I can see shutting down PFE #1 not affecting BFD sessions anymore. It seems like BFD sessions is associated with PFE#0.

## Source: `formatted/TS_notes/command list to collect the bfd data from the respective fpc.md`

# command list to collect the bfd data from the respective fpc

start shell pfe network fpcx

# show ddos policer bfd stats

# show ppm statistics detail

# show ppm adjacencies

# show ppm statistics protocol bfd

# show ppm transmits protocol bfd

## Source: `formatted/TS_notes/commands need to collect to check BFD (MPC10_11) - From TAC.md`

# commands need to collect to check BFD (MPC10/11) - From TAC

JTAC : Please share the below outputs.

show ddos-protection protocols arp parameters

show configuration system ddos-protection protocols | display set

show ddos-protection protocols arp statistics terse

show route forwarding-table destination 10.113.255.3  | match "Destination|ucst"

show route forwarding-table destination 10.113.255.4  | match "Destination|ucst"

show pfe statistics traffic | match drop

show policer | match arp

show class-of-service fabric statistics |  no-more

show class-of-service fabric statistics summary | no-more

show system connection |no-more

show system connection extensive |no-more

start shell pfe network fpc < FPC no> --collect for fpc 0 and 5

show interfaces

show class-of-service interface queue-stats index  interface index based on the above output.

show ddos policer violations arp

show ddos policer arp configuration

show system info

show jnh exceptions level inst 0

show jnh exceptions level inst 1

show jnh exception-qdrops inst 0

show jnh exception-qdrops inst 1

show class-of-service interface scheduler brief

show ppm adjacencies

show ppm adjacencies protocol bfd detail

show ppm statistics protocol bfd

show ppm interfaces detail | no-more

show ppm transmissions detail | no-more

show ppm transmissions protocol bfd detail

show pfe statistics traffic | no-more

show ppm distribution-statistics

show ppm dfw-statistics

show ppm packet-snapshot

show ppm request-queue

show ppm rpc-statistics

show ppm info

show ppm objects

show ppm statistics detail

show ttp statistics

show system queue

show threads

show sched

show host-path ports

show host-path ports fp0

show host-path ports fp1

show host-path ports cp0

show host-path ports punts

show host-path ports io reassembly fp0

show host-path ports io reassembly fp1

show host-path ports punts fp0

show host-path ports punts fp1

show host-path packet-type

show host-path network

show host-path packets

show host-path ports ppm0

show filter pkt-log

show firewall stats

show host-path ddos all-policers nzero

show ddos all-policers nzero

show jnh ddos scfd global

show jnh ddos policer statistics

show jnh ddos policer configuration

show pfe statistics reroute

show pfe statistics traffic

show pfe statistics error

show pfe statistics notification

show cda xqss statistics server api

show host-path network layer2 ethernet

show host-path app wedge-detect pfe-status

show host-path app wedge-detect state

show host-path app wedge-detect sm-stats

show host-path app hw-notif statistics

show host-path app icmp statistics

show host-path app mlp statistics

show host-path app ppm

show host-path app resolve state

show host-path app resolve statistics

show host-path app rpc-statistics

show host-path app twamp statistics

show host-path app vxlanpkt statistics

show jnh ucode-vars All inst 0

show jnh ucode-vars All inst 1

show jnh ucode-vars GeHost inst 0

show jnh ucode-vars GeHost inst 1

show interfaces statistics .punt

## Source: `formatted/TS_notes/sử dụng BFD cho LSP.md`

# sử dụng BFD cho LSP

Như trao đổi sáng nay, để tránh trường hợp traffic bị blackhole do stuck tunnel (đang nghi ngờ lỗi trên HK04 hoặc PE04), anh đề xuất việc sử dụng BFD cho LSP để như một giải pháp phòng ngừa. Khi sử dụng BFD cho LSP có một số lưu ý như sau

- BFD cho LSP sử dụng tài nguyên của Routing Engine, do vậy không khuyến nghị khai báo quá nhiều, cũng như thời gian interval gửi BFD Hello không nên để mức millisecond.
- Cơ chế hoạt động của BFD cho LSP đó là từ Ingress sẽ gửi bản tin BFD Hello theo LSP mà mình muốn bảo vệ, bản tin này sẽ đi theo LSP đến Egress, và Egress sẽ ACK lại theo routing IGP, với bản tin UDP port 3784 àTrên RE Protect của Ingress PE cần mở thêm term này để BFD Up được.

Anh gửi cấu hình cho 01 LSP mẫu nhé

|  |
| --- |
| root@PE-04> show configuration protocols mpls label-switched-path TO\_PE\_01  Oct 19 13:58:46  to 150.10.10.1;  bandwidth 1g;  oam {  bfd-liveness-detection {  minimum-interval 1000;  multiplier 3;  }  }  no-cspf;  link-protection;  primary p\_PATH; |

Sử dụng câu lệnh dưới đây để verify trạng thái BFD

|  |
| --- |
| root@PE-04> show bfd session extensive  Oct 19 13:59:54  Detect   Transmit  Address                  State     Interface      Time     Interval  Multiplier  127.0.0.1                Up        xe-0/0/4.0     3.000     1.000        3  Client RSVP-OAM, TX interval 1.000, RX interval 1.000  Session up time 00:04:39  Local diagnostic None, remote diagnostic None  Remote state Up, version 1  Session type: Multi hop BFD  Min async interval 1.000, min slow interval 1.000  Adaptive async TX interval 1.000, RX interval 1.000  Local min TX interval 1.000, minimum RX interval 1.000, multiplier 3  Remote min TX interval 0.050, min RX interval 0.050, multiplier 3  Local discriminator 17, remote discriminator 17  Echo TX interval 0.000, echo detection interval 0.000  Echo mode disabled/inactive  LSP-Name TO\_PE\_01  Path-Name p\_PATH  Session ID: 0x0    1 sessions, 1 clients  Cumulative transmit rate 1.0 pps, cumulative receive rate 1.0 pps |

HoaND

Thanks

## Source: `formatted/TS_notes/BFD.md`

# BFD

run show bfd session

run show bfd session detail

run show ppm adjacencies protocol bfd detail

run request pfe execute command "show ppm adjacencies protocol bfd" target fpc7

run show chassis fabric fpcs

run request chassis fabric pfe 0 fpc 7 offline

PFE:

show syslog messages

show ppm adjacencies protocol bfd

show ppm transmits protocol bfd

show pfe statistics errors

show pfe manager session statistics

show pfe manager queue

clear threads max-time

show threads verbose

show pfe bfdsession all

show pfe bfdsession id  extensive

show filter

show filter index  program

show packet

###### #####################

### RPD

set cli timestamp

show chassis hardware

show chassis routing-engine

show system processes extensive no-forwarding | except 0.00

show system processes memory

show system virtual-memory | no-more

show task memory detail | no-more

show log messages | no-more

show log messages | match RPD\_SCHED\_SLIP

show task accounting

show krt queue

show krt state

show task io

show task jobs

show task accounting detail

show task summary

show chassis fpc

show chassis fpc details

show system resource-monitor fpc

- -----

request pfe execute command "show heap 0" target fpc0

request pfe execute command "show nhdb summary detail" target fpc0

request pfe execute command "show nhdb sizes" target fpc0

request pfe execute command "show heap 0 sanity" target fpc0

request pfe execute command "show jnh 0 pool summary" target fpc0

request pfe execute command "show jnh 0 pool" target fpc0

request pfe execute command "show jnh 0 pool usage" target fpc0

request pfe execute command "show jnh 0 pool detail" target fpc0

request pfe execute command "show jnh 0 pool layout" target fpc0

request pfe execute command "show jnh 0 pool layout verbose" target fpc0

request pfe execute command "show jnh 0 pool composition" target fpc0

request pfe execute command "show jnh 0 pool stats nh" target fpc0

request pfe execute command "show jnh 0 pool stats fw" target fpc0

request pfe execute command "show jnh 0 pool stats cnt" target fpc0

request pfe execute command "show cassis\_alloc" target fpc0

request pfe execute command "show sample-rr summary" target fpc0

request pfe execute command "show resmon summary" target fpc0

## Source: `formatted/TS_notes/BFD ISSUE VIETTEL KV3_BRAS28.md`

# BFD ISSUE VIETTEL KV3/BRAS28

có 4 BFD session được phân phối xuống 2 FPC 7 & FPC8 để xử lý

1. / TH1: 8-8-7-7

- Disble FPE trên FPC8 bằng câu lệnh request => BFD session (8-8) Init và bị stuck trạng thái, không tự chuyển qua FPC7 còn lại

2. / TH2: 8-8-7-7

- Reboot FPC8 => 2 BFD session trên FPC8 sẽ revert qua FPC7.

3. / TH3: 7-7-7-7

- Disable PFE trên FPC7 bằng câu lệnh request => 4 BFD session stuck ở trạng thái INIT => BGP session DOWN.

4. / TH4: 7-7-7-7

- Reboot FPC7 => 4 BFD session chuyển qua FPC8

5. / TH5: 8-8-8-8

- Reboot nguyên chassis => FPC8 online trước, FPC7 online sau => 4 phiên BFD session ăn theo FPC8.

6. / TH6: 8-8-7-7

7. / TH7: 8-8-8-8

- Rút hết các member links ra khỏi FPC8 => 4 BFD sessions vẫn ăn theo FPC8, không đổi.

8. / TH8: 7-7-8-8

- Disable PFE trên FPC7 bằng scripts (scripts đánh down PFE khi có major alarm) => BFD (7-7) stuck ở INIT, không tự chuyển qua FPC8. BGP không flap do còn 2 phiên còn lại

9. /TH9: 7-7-7-7

- Disable PFE trên FPC7 bằng scripts (scripts đánh down PFE khi có major alarm) => BFD (7-7-7-7) stuck ở INIT, không tự chuyển qua FPC8. BGP session Down.

10. / TC10: 8-8-8-8. Tạm gọi các session là: 8a-8b-8c-8d. Mục tiêu cuối cùng là làm cách nào để 4 BFD trở thành 7-7-8-8 ?

10a./ TC10a: 8a-8b-8c-8d:

- xóa cấu hình lần lượt từng session và cấu hình lại từng phiên BFD => vẫn ghi nhận BFD ăn theo FPC cũ (8-8-8-8).

10b./ TC10b: 8a-8b-8c-8d:

- xóa cấu hình BFD session 8a & 8b. => lúc này chỉ còn lại session 8c & 8d.

- Restart lại FPC7, sau đó cấu hình lại 2 session đã xóa trước đó. => vẫn ghi nhận 2 session mới ăn theo FPC8 (8a-8b-8c-8d)

10c./ TC10c: 8a-8b-8c-8d:

- Restart lại FPC8, sau đó cấu hình lại 2 session đã xóa trước đó. => vẫn ghi nhận 2 session mới ăn theo FPC8 (8a-8b). tuy nhiên 2 session cũ (8c-8d) do đã restart lại FPC8 nên đã trở thành (7c-7d)

Từ TC10 có thể thấy, việc xóa đi tạo lại cấu hình session BFD thì Junos vẫn hành xử ăn theo 1 FPC đã được dedicate từ trước. Chỉ có việc reboot FPC thì session BFD mới ăn theo 1 FPC khác.

Từ TC5 & TC6 có thể thấy, khi reboot chassis, card FPC nào online trước thì BFD session sẽ ăn theo FPC đó.

## Source: `formatted/TS_notes/_M_MX_T_ Troubleshooting Checklist - BFD.md`

# [M/MX/T] Troubleshooting Checklist - BFD

SYMPTOMS:

- BFD session is not coming up or it went down
- BFD flapping

### BFD Session Not UP:

Perform the following steps to troubleshoot a BFD session that is not in the UP state:

Step 1: Verify the configuration of the BFD.

> Refer to the technical documentation here:
>
> - [Configuring BFD for Static Routes for Faster Network Failure Detection](https://www.juniper.net/documentation//en_US/junos/topics/example/policy-static-routes-bfd.html)
> - [Configuring BFD on Internal BGP Peer Sessions](https://www.juniper.net/documentation//en_US/junos/topics/example/bgp-bfd-ibgp.html)
> - [Configuring PIM and the Bidirectional Forwarding Detection (BFD) Protocol](http://www.juniper.net/techpubs/en_US/junos/topics/topic-map/mcast-pim-bfd.html)
> - [Configuring BFD for MPLS IPv4 LSPs](http://www.juniper.net/techpubs/en_US/junos/topics/usage-guidelines/mpls-configuring-bfd-for-mpls-ipv4-lsps.html)
>
> Important:  Verify that the configuration settings on both ends match, and verify that both are interoperable for BFD.

Step 2: Check if the interface through which BFD is sending packets is in the UP state; use the command

show interfaces interface-name extensive

> This output also gives error statistics that might indicate if packet drops are seen on the interface.
>
> For more information on troubleshooting Ethernet interfaces, refer to [KB26486 - Troubleshooting Checklist - Ethernet Physical Interfaces](https://kb.juniper.net/KB26486)

Step 3: Verify that the next-hop IP route is available on the local router to which the router is sending BFD hello packets; use the command

show route x.x.x.x

> Note: For a single-hop BFD, even though the next hop is directly connected and the route is always there on the local router, in some corner cases if this is not the case then the above output gives information related to the next hop.

Step 4: Check if there is an issue with any intermediate media/device to the other end router.

> The physical path of a network data circuit sometimes consists of a number of segments interconnected by devices that repeat and regenerate the transmission signal. An issue with any intermediate circuit may lead to packet loss. Hence, to verify or troubleshoot, perform a loopback test and a BERT test.
>
> For more information, refer to [KB26486 - Troubleshooting Checklist - Ethernet Physical Interfaces](https://kb.juniper.net/KB26486).

Step 5: Configure bfd and ppmd traceoptions, and review the traceoptions output.

user@Router# show protocols bfd

traceoptions {

file bfd-log size 10m files 10;

flag all;

}

user@Router# show routing-options ppm

file ppm-log size 10m files 10;

For help on how to configure traceoptions and view debug output, refer to [KB16108 - Configuring Traceoptions for Debugging and Trimming Output](https://kb.juniper.net/KB16108).

Step 6:  Configure a specific firewall filter term under the lo0 interface to check if the first two packets are being processed by routing engine. Look for any BFD policer that might be dropping the session

to come up.

> In addition to checking whether packets are being reached at the routing engine, an FW can be configured to count the BFD packets to confirm the same quantity is being sent and received. It can also be correlated with the filter configured under lo0.
>
> Example of the firewall filter that can be used:
>
> set firewall filter family inet BFD interface-specific
>
> set firewall filter family inet BFD term In from protocol udp
>
> set firewall filter family inet BFD term In from port [4784 3784 3785]
>
> set firewall filter family inet BFD term In from source-address <>
>
> set firewall filter family inet BFD term In from destination-address <>
>
> set firewall filter family inet BFD term In then accept
>
> set firewall filter family inet BFD term In then count BFD-In
>
> set firewall filter family inet BFD term In then log
>
> set firewall filter family inet BFD term Out from protocol udp
>
> set firewall filter family inet BFD term Out from port  [4784 3784 3785]
>
> set firewall filter family inet BFD term Out from destination-address <>
>
> set firewall filter family inet BFD term Out from source-address <>
>
> set firewall filter family inet BFD term Out then accept
>
> set firewall filter family inet BFD term Out then count BFD-OUT
>
> set firewall filter family inet BFD term Out then log
>
> set firewall filter family inet BFD term anything then accept
>
> This FW should apply in/out direction in the outgoing interface along with lo0, so make sure first packets are handled by the RE, then moving to the pfed/ppmd.

### BFD Flapping:

BFD flapping can be verified with repeated syslog messages indicating BFD session churning UP and DOWN states, as shown below:

bfdd[711]: BFDD\_TRAP\_STATE\_DOWN: local discriminator: 3, new state: down rpd[819]: RPD\_OSPF\_NBRDOWN: OSPF neighbor 208.108.231.66 (realm ospf-v2 vlan.1933 area 0.0.0.0) state changed from Full to Down due to InActiveTimer (event reason: BFD session timed out and neighbor was declared dead)

bfdd[711]: BFDD\_TRAP\_STATE\_DOWN: local discriminator: 3, new state: down rpd[819]: RPD\_OSPF\_NBRDOWN: OSPF neighbor 208.108.231.66 (realm ospf-v2 vlan.1933 area 0.0.0.0) state changed from Full to Init due to 1WayRcvd (event reason: neighbor is in one-way mode)

Also, the current status of the BFD session may be down:

User@Router> show bfd session

Detect   Transmit Address    State     Interface      Time     Interval  Multiplier

1. 1.100.1     Down         4.000     0.900                        1

To fix BFD flapping issues, perform the following steps:

CAUTION: Some of the command outputs in the following steps are not officially supported by Juniper Networks; nevertheless, they are helpful in troubleshooting. It is not recommended to run these commands in a 'live' production network.  A maintenance window is recommended.

Note: The default operational mode of BFD for all protocols is distributed mode (runs on PFE), one exception being OSPFv3 which runs on the Routing Engine by default (centralized mode).

1. Identify the current affected BFD session, whether belonging to single hop or multihops.

Single-hop BFD control packets use UPD port 3784, and multihop BFD control packets use UDP port 4784. The single-hop BFD may or may not use distributed ppmd, but the multihop BFD is always Routing Engine-based, with no relation to the ppman on the PFE.

Note: Multihop BFD can be deployed by distributed ppmd  through RLI 13271- Distributed BFD for multi-hop protocols (BGP, static routes, and so on) .

Starting with Junos Release 12.3, multihop BFD is not Routing Engine-based.
2. If it is a non-distributed (Routing Engine-based) BFD, then verify if any process is hogging the CPU and hence missing the processing of BFD packets.

Verify the CPU utilization on the Routing Engine with show chassis routing-engine or show system process extensive commands.  If the CPU is high, refer to [KB26261 - Troubleshooting Checklist - Routing Engine High CPU](https://kb.juniper.net/KB26261) to troubleshoot the high CPU. One way to mitigate BFD flapping due to high Routing Engine CPU is to increase the minimum interval of BFD keepalives; for more information, see Step 8 below.
3. Monitor the interface on which the affected BFD session is running and verify if the BFD control traffic is hitting the local interface.

If there are no inbound packets or if some of them are dropping somewhere in between, then the issue is external (with the asymmetric traffic path or the intermediate device suffered from a hardware or transmission issue).
4. Check the Ethernet switch errors between the CB/FPC/RE.

To do this, review the output of the following commands:

show chassis ethernet-switch statistics

show chassis ethernet-switch error
5. If it is distributed, then check PPM stats.

Delegate the BFD processing job to the PFE (also called distributed mode, which is the default). BFD sessions are very lightweight, hence flaps generally do not occur when sessions are distributed. If they do, then it could be a PFE issue.

To check PPM stats, first login to the corresponding PFE using >start shell pfe network fpcX, then use the show ppm statistics protocol bfd command:

ADPC5( vty)# show ppm statistics protocol bfd

BFD input errors:

No interface            : 0

No family               : 0

Not IPv4                : 0

Bad IP checksum         : 0

Bad IP options          : 0

Bad IP len              : 0

Bad UDP checksum        : 0

Bad UDP len             : 0

Unknown UDP ports       : 0

Local ifl failures      : 0

Prefix len mismatch     : 0

Authentication failure  : 0

RX Queue overflow       : 0

Packet get failed       : 0

Total BFD Packets       : 0

Absorbed BFD Packets    : 0

Packet send drops       : 0

Refresh stats:

Adjacencies : Refreshed     0    Not-refreshed     0

Transmits   : Refreshed     0    Not-refreshed     0

Interfaces  : Refreshed     0    Not-refreshed     0

Stats Groups: Refreshed     0    Not-refreshed     0

Verify that no error counters are incrementing.
6. Check if any packet drops are reported on the Packet Forwarding Engine.

To do this, use the show pfe statistics traffic command:

lab# run show pfe statistics traffic

Packet Forwarding Engine traffic statistics:

Input packets: 2004354 0 pps

Output packets: 2008275 0 pps

Packet Forwarding Engine local traffic statistics:

Local packets input : 870715

Local packets output : 923411

Software input control plane drops : 0

Software input high drops : 0

Software input medium drops : 0

Software input low drops : 0

Software output drops : 0

Hardware input drops : 0

Packet Forwarding Engine local protocol statistics:

HDLC keepalives : 0

ATM OAM : 0

Frame Relay LMI : 0

PPP LCP/NCP : 0

OSPF hello : 224323

OSPF3 hello : 0

RSVP hello : 0

LDP hello : 0

BFD : 0

IS-IS IIH : 0

LACP : 0

ARP : 39370

ETHER OAM : 0

Unknown : 42774

Packet Forwarding Engine hardware discard statistics:

Timeout : 0

Truncated key : 0

Bits to test : 0

Data error : 0

Stack underflow : 0

Stack overflow : 0

Normal discard : 51395

Extended discard : 0

Invalid interface : 0

Info cell drops : 0

Fabric drops : 0

Packet Forwarding Engine Input IPv4 Header Checksum Error and Output MTU Error statistics:

Input Checksum : 0

Output MTU

If packet drops are seen, then the packets that are being dropped randomly could be BFD packets. All BFD packets are treated as data packets, so it could be possible that they are being dropped randomly.

Verify if packets are getting dropped by issuing the following commands:

show system queues

show ttp statistics  (you need to log in to the corresponding FPC, as shown in Step 5)
7. Check which threads are consuming the CPU.

Usually D-BFD flaps are seen when an ukernel thread hogs the CPU.  To check, issue the show threads command at the corresponding PFE.

ADPC5( vty)# show threads

PID PR State Name Stack Use Time (Last/Max/Total)

- -- -- ------- --------------------- --------- ---------------------

1 H asleep Maintenance 296/2048 0/0/0 ms

2 L ready Idle 280/2056 5/5/327341520 ms

3 H asleep Timer Services 288/2056 0/0/0 ms

5 L asleep Sheaf Background 376/2048 5/5/5 ms

6 H asleep IPv4 PFE Control Background 296/8200 0/0/0 ms

7 M asleep DCC Background 280/4104 0/0/0 ms

8 M asleep OTN 360/4104 0/0/0 ms

This should give us an indication about which threads hog the CPU. If a flap is seen when a link is disabled or enabled, then it could be an issue with a CPU hog and should be investigated.

If you doubt that BFD packets are being dropped, then first make it centralized with the command set routing-option ppm no-delegate-ppm, followed by clear bfd session.

Increase the timer of the BFD session; minimum on the RE should be 100 ms.

Start monitoring the interface; if there is a lag in packets received, then you know there is an issue with the PFE.
8. Check the minimum-interval.

When configuring BFD, care should be taken when choosing minimum-interval under bfd-liveness-detection. If you choose a very low minimum-interval, then BFD will send hello packets very aggressively, which in some cases might lead to BFD flap.

For a recommendation on the optimal values to choose for  minimum-interval, refer to the technical documentation on [Configuring BFD for Static Routes for Faster Network Failure Detection](https://www.juniper.net/documentation//en_US/junos/topics/example/policy-static-routes-bfd.html).
9. Capture the BFD packets using ip-filter in order to identify if packets are hitting from the issued BFD interface.

User@Router# show firewall filter test-in

term 10 {

from {

protocol udp;

destination-port 4784;

then {

count bfd-in;

syslog;

accept;

term 20 {

then accept;

[edit]

User@Router# show firewall filter test-out

count bfd-out;

User@Router# show system syslog

file bfd-log {

firewall any;

User@Router# show configuration interfaces

ge-0/0/4 {

unit 100 {

vlan-id 100;

family inet {

filter {

input bfd-in;

output bfd-out;

address 172.1.0.1/30;

If the filter is applied to the incoming interface, and you don't see packets coming in, investigate where the packets are getting dropped.

If the filter is applied to the outgoing interface, and you're not seeing packets going out, check the configuration (this is a local issue).
