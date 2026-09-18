# Link Flap and Physical Layer

> Generated deterministically from the approved grouping manifest.


## Source: `formatted/TS_notes/BUG Hold-time down không hoạt động được nếu cấu hình nhỏ hơn 1s trên interface chạy WANPHY.md`

# BUG Hold-time down không hoạt động được nếu cấu hình nhỏ hơn 1s trên interface chạy WANPHY

Hi Team,

Junos từ 18 đến 20.4R3-S4 đang có bug với các interface đang bật WANPHY đồng thời cấu hình hold-time down với thời gian nhỏ hơn 1 giây thì sẽ gây flap interface nếu nháy truyền dẫn, tức là hold-time down không hoạt động đúng mong đợi. Hiện tại, lỗi này chưa biết được trigger nên chưa có kế hoạch để có thể fix trên Junos.

Hiện tại ghi nhận được bug không gặp trong các trường hợp sau:

- Ở Junos 17.x

- Interface chạy mode LANPHY

- Chạy WANPHY nhưng không cấu hình hold-time down hoặc có cấu hình nhưng thời gian tầm 2 giây trở lên.

Workaround cho lỗi này thì có thể cân nhắc 2 option bên dưới:

1/. Thay đổi thành interface từ mode WANPHY -> LANPHY. giải pháp này cần kiểm tra thêm đầu truyền dẫn xem có hỗ trợ mode này hay không

2/. Tăng hold-time down lên khoảng 2s: giải pháp này thì có thể sẽ gây blackhole traffic trong khoảng thời gian hold-time down. (thực tế test ở lab, theo Hoàng NWHNI kiểm tra thì khi set hold-time down tầm 1,5 giây thì vẫn gây flap).

Chi tiết về case này, Hoàng NWHNI có làm việc với JTAC qua case 2022-0731-520372 - đồng thời thực hiện test Lab với kết quả rất chi tiết ở mail dưới. AE xem thêm để nắm bug của lỗi này để tránh/hạn chế gặp trên các Junos hiện tại.

## Source: `formatted/TS_notes/Delay thời gian up time của CE interfaces.md`

# Delay thời gian up time của CE interfaces

để optimize down time do bi core isolation: sẽ delay thời gian up time của CE interfaces:

lab@mx480-re0# show protocols network-isolation

group hoo {

detection {

hold-time up 60000;

service-tracking {

core-isolation;

}

service-tracking-action link-down;

lab@mx480-re0# show interfaces ae0

flexible-vlan-tagging;

mtu 9216;

encapsulation flexible-ethernet-services;

network-isolation-profile hoo;

## Source: `formatted/TS_notes/Lệnh off laser mode shell _ dùng flap link.md`

# Lệnh off laser mode shell <<< dùng flap link

xe-1/0/1 {

description looped-2;

hold-time up 2000 down 300 alternative;

framing {

wan-phy;

sonet-options {

trigger {

ber-sd {

hold-time up 3000 down 1000;

[ February 24, 2023 16:56 ] ⁨Hung Le⁩: test ifd xe-1/0/0 laser off 50

Dec  4 20:35:06.652 LOG: Debug] xe-1/0/0: turn off laser for 50 msec, then turn on laser

RMPC1(jtac-mx240-r2036-re0 vty)#  test ifd xe-1/0/0 laser off 50

Kết quả test trên lab

SMPC platform (1750Mhz Intel(R) Atom(TM) CPU processor, 3168MB memory, 8192KB flash)

SMPC4(MX960-01\_RE1 vty)# test ifd xe-4/1/1 laser off 5000

[Jul  5 08:58:36.115 LOG: Debug] xe-4/1/1: turn off laser for 5000 msec, then turn on laser

[Jul  5 08:58:36.619 LOG: Info] ifp xe-4/1/1 ifd\_mdown: 186954054 ms

[Jul  5 08:58:40.955 LOG: Notice] SMIC(4/1) link 1 SFP laser bias current low  alarm set

[Jul  5 08:58:40.955 LOG: Notice] SMIC(4/1) link 1 SFP output power low  alarm set

[Jul  5 08:58:40.955 LOG: Notice] SMIC(4/1) link 1 SFP laser bias current low  warning set

[Jul  5 08:58:40.955 LOG: Notice] SMIC(4/1) link 1 SFP output power low  warning set

[Jul  5 08:58:47.014 LOG: Notice] SMIC(4/1) link 1 SFP laser bias current low  alarm cleared

[Jul  5 08:58:47.014 LOG: Notice] SMIC(4/1) link 1 SFP output power low  alarm cleared

[Jul  5 08:58:47.014 LOG: Notice] SMIC(4/1) link 1 SFP laser bias current low  warning cleared

[Jul  5 08:58:47.014 LOG: Notice] SMIC(4/1) link 1 SFP output power low  warning cleared

test cfp  laser  off

test cfp  laser  on

[ July 5, 2023 16:01 ] ⁨SVT.Anh.VT⁩: lệnh để up down cổng ngay lập tức dưới shell anh em nhé

ifconfig ge-0/0/3 down

ifconfig ge-0/0/3 up
