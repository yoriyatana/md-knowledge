# RR for VNPT-NET

Về mặt support thì:

- ---------------------

- 17.3, EOE  25-Aug-2021 & EOS 25-Feb-2022.

- 18.4 EOE 22-Dec-2021 &  EoS 22-Jun-2022.

- 19.3 EoS Mar-2023 & 19.4 EoS Jun-2023.

JTac recommend:

- -------------------

Junos 17.3R3-S10

Junos 18.4R2-S5

Junos 19.3R3

Junos 19.4R3

Các tính năng bổ sung quan trọng & có liên quan đến BGP của NET:

===================================

Junos 18

- add-path cho inet-vpn & inet6-vpn <<< NET ko cần cái này

- Multipath optimization to improve RIB learning rate (performance)

Junos 19.1/19.2/19.3

- None

Junos 19.4:

- Bgp rib sharding (performance) <<< Split bgp process into different threads <<< Architecture change

- Bgp io thread enhancements (performance) <<< New thread

- Bgp pic-edge for LU

- Bgp neighbor re-establishment optimization (performance)

Sơ bộ:

- -------

- Do 19.4 có cải thiện performance của bgp bằng cách thay đổi kiến trúc nên cần xem xét kỹ các PR có thể xảy ra.

- 19 không có bổ sung tính năng BGP gì quan trọng cho đến 19.4

- 18 thì 1 năm nữa EoS

>>>>  Do vậy anh tạm đề nghị:

- Option 1: sử dụng 2 bản 19.3 & 19.4 <<< Prefered

- Option 2: sử dụng 2 bản 19.3 & 18.4 <<< Nếu có PR nghiem trong o 19.4

- Chờ kết quả PR từ @⁨Hung Le⁩ rồi chốt

Add-path họ chỉ yêu cầu cho IPv4 & IPv6 quốc tế thôi anh ah

1> The BGP process is split into different threads so that they can run concurrently on a multicore routing engine through RIB sharding which results in reduced convergance time and faster performance.

2> BGP update thread is disabled by default. If you configure update-threading on a routing engine, RPD creates update threads.

This topic discusses using route reflectors to simplify configuration and aid in scaling. A further way to reduce the workload on a route reflector that is not in the traffic-forwarding path is to use the no-install statement at the [edit protocols bgp family family-name] hierarchy level. Starting in Junos OS Release 15.1, the no-install statement eliminates interaction between the routing protocols daemon (rpd) and other components in the Junos system such as the kernel or the distributed firewall daemon (dfwd). This interaction is eliminated by prohibiting any routes in the associated rpd routing information bases (RIBs), also known as routing tables, from being published to those components.
