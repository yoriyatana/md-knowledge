# LACP Troubleshooting and Diagnostics (Juniper)

> Generated deterministically from the approved grouping manifest.


## Source: `formatted/TS_notes/LACP check-list commands.md`

# LACP check-list commands

Phía MX:

1. Apply traceoptions LACP và PPM trên cả 4 thiết bị QFX & MX.

2. Thu thập thông tin và enable event-options để MX tự động thu thập log khi có trigger liên quan đến event lacpd\_timeout và lacp\_intf\_down.

3. Thu thập thông tin dưới shell mode và kernel

[ Thursday, January 13, 2022 11:13 AM ] ⁨SVT.Thái.NĐ⁩: 1. Enable cli timestamp

```text
set cli timestamp
```
2. Enable lacp traceoptions and reproduce the issue

```text
set protocols lacp traceoptions file lacpd.log size 1g world-readable
set protocols lacp traceoptions flag all
set routing-options ppm traceoptions flag al
set routing-options ppm traceoptions file ppmd.log size 1g
```
3. Take multiple output of below commands in RE.

```text
show lacp interfaces extensive
show lacp statistics interfaces
show interfaces ae | match flap
show lacp timeouts (multiple times)
show ppm adjacencies protocol lacp detail
show ppm transmissions protocol lacp detail
show ppm adjacencies protocol lacp
show ppm transmissions protocol lacp
```
4. Go to PFE shell using any of the below-mentioned methods

a. While at the CLI prompt

start shell pfe network fpc

OR

b. While at the FreeBSD prompt of RE

vty fpc

```text
clear ppm statistics first before collecting any data.
set ppm utrace protocol lacp
set ppm utrace protocol lacp
set ppm utrace tcpdump
```
debug ppm protocol lacp level 3

```text
set ppm utrace proto
set ppm utrace protocol lacp
set ppm utrace all
```
debug ppm protocol lacp level 3

```text
show ukern\_trace handles <<<<
```
search for PPM handle <<<<

```text
set ukern\_trace  level extensive
set ukern\_trace  logging enable
set ukern\_trace  buffer 100000000
set ukern\_trace  printf enable
```
Above debugs will be coming continuously. keep separate console and collect the above debugs running on both DUT and PEER device through out the logs collection.

Take multiple output of below commands in while in PFE shell?. Take these commands without timedelay

Collect these clis using cprod.

at the start of the logs collection on both sides on PFEs. >> clear ppm statistics

```text
show ppm statistics protocol lacp
show ppm adjacencies protocol lacp
show ppm transmits protocol lacp
show ppm statistics detail
```
freebsd promt:

copy paste the clis continuously for few times.

date

cprod -A fpc -c "show sched"

cprod -A fpc -c "show threads cpu"

cprod -A fpc -c "show ttp statistics"

cprod -A fpc -c " show ppm statistics"

PFE BCM commands to Collect.

HW( "show c cpu" & "show c") -> ("show halp-pkt pkt-stats") ->  "show ttp statistics" -> use tcp-dump etc.

Below are the commands.

VTY: Both Device.

```text
show halp-pkt asic-queues
show dcbcm ifd all
show halp-pkt hostpath-cfgs
show halp-pkt pkt-stats    << Multiple outputs.
```
If drop is seen on PFE-SHIM/HALP, there are commands to enable debug. "debug halp-pkt tx/rx".

Output of "debug halp tx/rx" can be seen in as below

FPC0(PE-3 vty)# show ukern\_trace handles

FPC0(PE-3 vty)# show ukern\_trace 13

[Tue Oct 13 10:42:24.314] [9430] brcm\_rx\_init:408 (init) rx init done

[Tue Oct 13 10:42:24.314] [9431] brcm\_tx\_init:441 (init) tx init done

[Tue Oct 13 10:42:24.317] [9432] brcm\_pkt\_fastpath\_init:754 (init) pkt fp thread started

[Fri Oct 23 04:04:02.702] [13917] brcm\_pkt\_debug\_tx:1827 (tx\_api\_entry) pkt 0xaf5f0178  ifd  idx 656 len 74

proto 0 ifl\_inp 0 hint 40009001 msec 840115082

18 2a d3 9c d8 35 78 4f 9b eb fc d1 08 00 45 c0 00 3c d2 51 00 00 01 2e 8e 61 ab 0a 01 06 ab 0a

01 07 11 14 bc 3d 01 00 00 28 00 0c 16 01 1b d7 9c 5e e6 ab 73 68 00 0c 83 01 00 00 00 00 00 00

[Fri Oct 23 04:04:02.867] [13918] brcm\_pkt\_debug\_tx:1827 (tx\_api\_entry) pkt 0xaf5f0178  ifd  idx 656 len 85

proto 0 ifl\_inp 0 hint 9001 msec 840115247

However if drop is in HW/BCM then need to check why HW is dropping.

BCM(sad)Both Device)

```text
Show c
Show c cpu
tcpdump -ni
```
Lấy giúp em các output dưới đây (ở mức shell) vào giờ thấp điểm, và chạy từng lệnh một:

```text
set cli screen-length 0
```
## Check linecard shell-mode

```text
request pfe execute command "show syslog messages" target fpc2
request pfe execute command "show nvram" target fpc2
request pfe execute command "show cmerror module" target fpc2
request pfe execute command "show hsl2 statistics" target fpc2
request pfe execute command "show hsl2 statistics crc" target fpc2
request pfe execute command "show threads cpu" target fpc2
request pfe execute command "show sched" target fpc2
>>>> take this output 3 times in the interval of 30secs
request pfe execute command "show ppm transmits protocol lacp" target fpc2
request pfe execute command "show ppm adjacencies protocol lacp" target fpc2
request pfe execute command "show ppm statistics protocol lacp" target fpc2
```
## Check linecard shell-mode

```text
request pfe execute command "show syslog messages" target fpc4
request pfe execute command "show nvram" target fpc4
request pfe execute command "show cmerror module" target fpc4
request pfe execute command "show hsl2 statistics" target fpc4
request pfe execute command "show hsl2 statistics crc" target fpc4
request pfe execute command "show threads cpu" target fpc4
request pfe execute command "show sched" target fpc4
>>>> take this output 3 times in the interval of 30secs
request pfe execute command "show ppm transmits protocol lacp" target fpc4
request pfe execute command "show ppm adjacencies protocol lacp" target fpc4
request pfe execute command "show ppm statistics protocol lacp" target fpc4
```
# ------------------------

```text
set cli screen-length 30
```

## Source: `formatted/TS_notes/MPC11E - LACP không up_join.md`

# MPC11E - LACP không up/join

0x7

00000111

11100000

1 Active

1 SHORT timeout

1 WILL aggregate

0 Not in sync

0 Mux is NOT Collecting

0 Mux is NOT Distributing

0 LACP PDU

0 No expired

0x46

01000110

01100010

0 Passive

0 Mux is Distributing

1 default

0x47

01000111

11100010

- --

# LACP Port State

```text
The LACP port state (also known as the actor state) field is a single byte, each bit of which is a flag indicating a particular status. In this table, mux (i.e. a multiplexer) refers to the logical unit which aggregates the links into a single logical transmitter/receiver.
```
The meaning of each bit is as follows:

|  |  |  |
| --- | --- | --- |
| Bit | Name | Meaning |
| 0 | LACP\_Activity | Device intends to transmit periodically in order to find potential members for the aggregate. This is toggled by mode active in the channel-group configuration on the member interfaces.  1 = Active, 0 = Passive. |
| 1 | LACP\_Timeout | Length of the LACP timeout.  1 = Short Timeout, 0 = Long Timeout |
| 2 | Aggregation | Will allow the link to be aggregated.  1 = Yes, 0 = No (individual link) |
| 3 | Synchronization | Indicates that the mux on the transmitting machine is in sync with what’s being advertised in the LACP frames.  1 = In sync, 0 = Not in sync |
| 4 | Collecting | Mux is accepting traffic received on this port  1 = Yes, 0 = No |
| 5 | Distributing | Mux is sending traffic using this port  1 = Yes, 0 = No |
| 6 | Defaulted | Whether the receiving mux is using default (administratively defined) parameters, if the information was received in an LACP PDU.  1 = default settings, 0 = via LACP PDU |
| 7 | Expired | In an expired state  1 = Yes, 0 = No |

# Junos OS and NXOS

Junos OS users are probably smiling right now, as this should look very familiar:

```text
john@switch> show lacp interfaces ae1
```
Aggregated interface: ae1

```text
LACP state: Role Exp Def Dist Col Syn Aggr Timeout Activity
```
xe-1/0/0 Actor No No Yes Yes Yes Yes Fast Active

xe-1/0/0 Partner No No Yes Yes Yes Yes Fast Passive

xe-2/0/0 Actor No No No No No Yes Fast Active

xe-2/0/0 Partner No No No Yes Yes Yes Fast Passive

Cisco users on the other hand may be weeping quietly when viewing a port-channel summary:

us-atl01-z1fa07a# show lacp neighbor interface port-channel 101

Flags: S - Device is sending Slow LACPDUs F - Device is sending Fast LACPDUs

A - Device is in Active mode P - Device is in Passive mode

port-channel101 neighbors

Partner's information

Partner Partner Partner

Port System ID Port Number Age Flags

Eth1/6 127,39-0d-12-c2-2b-40 0x3 427434 SA

LACP Partner Partner Partner

```text
Port Priority Oper Key Port State
```
127 0x2 0x3f

Eth2/6 127,39-0d-12-c2-2b-40 0x1 112 SA

```text
The partner port state is 0x3f, which is not very helpful. The good news is that looking at individual members does reveal the information in a more human-friendly format:
```
us-atl01-z1fa07a# show lacp interface eth 1/6

Interface Ethernet1/6 is up

[...]

Local Port: Eth1/6 MAC Address= 0-de-fb-11-32-a6

System Identifier=0x8000, Port Identifier=0x8000,0x106

Operational key=100

LACP\_Activity=active

LACP\_Timeout=Long Timeout (30s)

Synchronization=IN\_SYNC

Collecting=true

Distributing=true

Partner information refresh timeout=Short Timeout (3s)

```text
Actor Admin State=(Ac-1:To-1:Ag-1:Sy-0:Co-0:Di-0:De-0:Ex-0)
Actor Oper State=(Ac-1:To-0:Ag-1:Sy-1:Co-1:Di-1:De-0:Ex-0)
Neighbor: 0x3
```
MAC Address= 39-0d-12-c2-2b-40

System Identifier=0x7f, Port Identifier=0x7f,0x3

Operational key=2

LACP\_Timeout=short Timeout (1s)

```text
Partner Admin State=(Ac-0:To-1:Ag-0:Sy-0:Co-0:Di-0:De-0:Ex-0)
Partner Oper State=(Ac-1:To-1:Ag-1:Sy-1:Co-1:Di-1:De-0:Ex-0)
```
Aggregate or Individual(True=1)= 1

However, for the sake of anybody who has been sent output from show lacp neighbor interface port-channel X and wants to understand the hex value that’s displayed (0x3F in this case), it’s pretty simple.

# Decode-o-matic

- Convert hexadecimal to binary. Hexadecimal 0x3F is 00111111 in binary.
- Flip the bits around. 00111111 becomes 11111100
- Map the bits in this order to the table above:

1 -> ACTIVE mode

1 -> SHORT timeout

1 -> WILL aggregate

1 -> In SYNC

1 -> Mux is Collecting

1 -> Mux is Distributing

0 -> NOT running administratively configured settings

0 -> NOT expired

Alternatively, I suppose, flip the table so that the entries run from 7 to 0 instead of 0 to 7, then you don’t have to flip the bits; either way works. In this case 0x3F indicates a link which is an active part of the aggregated interface.

Clearly what we want from a link is that bit 7 is 0 (not expired) and bits 2-5 are 1 (will aggregate, in sync, collecting, distributing).

```text
A recent port I had trouble with was reported as partner port state 0xC7, which in binary is 11000111, which when flipped to 11100011 means:
```
1 -> ACTIVE mode

0 -> NOT In Sync

0 -> Mux is NOT Collecting

0 -> Mux is NOT Distributing

1 -> Running administratively configured settings

1 -> EXPIRED!

Clearly this link was not happy, but thankfully a shut / no shut sequence was enough to revive the patient.

Happy aggregating!

## Source: `formatted/TS_notes/lacp flap khi dung VC mix-mode.md`

# lacp flap khi dung VC mix-mode

như trao đổi với anh Đính, mình có một số lưu ý sau:

1. Virtual chassis đang config là Mix-mode, Mix-mode chỉ nên cấu hình khi chủng loại thiết bị Switch là khác nhau. trong trường hợp của bên mình thì member Switch đang đều là dòng Switch EX4300 nên khuyến nghị cấu hình Virtual Chassis tiêu chuẩn (non mix)

2. Nhờ anh hỏi bên đối tác FTP xem switch Huawei họ đang dùng là thực sự chỉ 1 Switch vật lý hay nhiều Switch gom lại thành Virtual chassis

3. Bên em sẽ anydesk để kiểm tra trạng thái lacp interface để xem các member link trên VC-EX4300 đang ở trạng thái cùng Active/Active hay ở trạng thái Active/Standby ? có thể monitor traffic interface để kiểm tra Arp Request/ Arp Reply khi thực hiện Ping

"truong hop LACP neu 2 port gan tren 2 member thi bi loi ping á, a chuyển qua 2 port lên 1 member thi ok" , anh @⁨SVT.Thái.NĐ⁩ hỗ trợ giúp em về cơ chế này của VC nhé anh

Em chỉ nhớ case CMC bị y chang hiện tượng : flap bgp 90s, queue bgp bị tăng lên do ko gửi được => lỗi MTU ko đồng nhất trên các phân đoạn.

Case này cấu hình mtu-discovery rồi mà ko giải quyết được, phải nhờ ae CMC trace từng phân đoạn rồi chỉnh lại MTU ở mấy con ở giữa mới OK.
