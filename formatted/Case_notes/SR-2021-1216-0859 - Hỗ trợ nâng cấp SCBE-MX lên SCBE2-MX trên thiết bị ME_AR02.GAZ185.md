# SR-2021-1216-0859 - Hỗ trợ nâng cấp SCBE-MX lên SCBE2-MX trên thiết bị ME_AR02.GAZ185

- --

Phát sinh: nâng cấp SCBE-MX lên SCBE2-MX trên thiết bị ME\_AR02.GAZ185

- --

Ghi nhận ban đầu

- Thiết bị ME\_AR02.GAZ185 đang chạy CB0 và RE0 do hôm trước thu hồi CB1 + RE1 ứng cứu cho thiết bị ME\_PR01.GAZ020 (case ID SR-2021-1201-0922).

- Hiện kho đã hết card MX-SCBE nên thực hiện nâng cấp lên MX-SCBE2.

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show chassis hardware

Hardware inventory:

Item             Version  Part number  Serial number     Description

Chassis                                JN1242EB7AFB      MX480

Midplane         REV 04   750-047862   ACRD1717          Enhanced MX480 Midplane

Routing Engine 0 REV 10   740-031116   9009199844        RE-S-1800x4

CB 0             REV 24   750-031391   CAEA9005          Enhanced MX SCB

- --

Các bước xử lý

- --

Kiểm tra sơ bộ

- IP MNS thiết bị 10.250.0.22
- Health check thiết bị

- CPU (1%), MEM(8%), TEMP (29C) không có bất thường, system boot (462 ngày)

vietpn@ME\_AR02.GAZ185\_RE0> show chassis routing-engine

Routing Engine status:

Slot 0:

```text
Current state                  Master
```

Election priority              Master

Temperature                 29 degrees C / 84 degrees F

CPU temperature             27 degrees C / 80 degrees F

DRAM                      16329 MB (16384 MB installed)

Memory utilization           8 percent

5 sec CPU utilization:

User                       0 percent

Background                 0 percent

Kernel                     1 percent

Interrupt                  0 percent

Idle                      99 percent

1 min CPU utilization:

User                       0 percent

Background                 0 percent

Kernel                     1 percent

Interrupt                  0 percent

Idle                      98 percent

5 min CPU utilization:

User                       0 percent

Background                 0 percent

Kernel                     1 percent

Interrupt                  0 percent

Idle                      98 percent

15 min CPU utilization:

User                       0 percent

Background                 0 percent

Kernel                     1 percent

Interrupt                  0 percent

Idle                      98 percent

Model                          RE-S-1800x4

Serial ID                      9009199844

Start time                     2020-09-09 23:40:16 CAT

Uptime                         462 days, 16 minutes, 20 seconds

Last reboot reason             Router rebooted after a normal shutdown.

```text
Load averages:                 1 minute   5 minute  15 minute
```

0. 02       0.11       0.14

- Không có process chiếm CPU

vietpn@ME\_AR02.GAZ185\_RE0> show system processes extensive

Dec 15 23:57:09

last pid: 37030;  load averages:  0.07,  0.11,  0.14  up 462+00:16:53    23:57:09

232 processes: 5 running, 197 sleeping, 30 waiting

```text
Mem: 57M Active, 2379M Inact, 909M Wired, 1687M Buf, 12G Free
```

```text
Swap: 8192M Total, 8192M Free
```

```text
PID USERNAME PRI NICE   SIZE    RES STATE   C   TIME    WCPU COMMAND
```

10 root     155 ki31     0K    64K RUN     1    ??? 100.00% idle{idle: cpu1}

10 root     155 ki31     0K    64K CPU3    3    ??? 100.00% idle{idle: cpu3}

10 root     155 ki31     0K    64K CPU2    2    ??? 100.00% idle{idle: cpu2}

10 root     155 ki31     0K    64K CPU0    0    ??? 100.00% idle{idle: cpu0}

13511 root      21    0   825M 47000K select  0 490.4H   2.59% chassisd{chassisd}

11 root     -72    -     0K   480K WAIT    2  47.9H   0.00% intr{swi1: netisr 0}

14218 root      20    0  1271M   333M kqread  0  38.2H   0.00% rpd{rpd}

13536 root      20    0   728M 12772K select  2  26.7H   0.00% ppmd

- Health check show system storage no-forwarding  <<< còn trống 8.8G

vietpn@ME\_AR02.GAZ185\_RE0> show system storage

Dec 15 23:57:25

Filesystem              Size       Used      Avail  Capacity   Mounted on

/dev/md0.uzip            21M        21M         0B      100%  /

devfs                   1.0K       1.0K         0B      100%  /dev

/dev/gpt/junos           19G       8.9G       8.8G       50%  /.mount

```text
show version detail no-forwarding
```

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show version invoke-on all-routing-engines | match "re0|re1|Junos:"

Dec 16 00:03:58

re0:

- -------------------------------------------------------------------------

Hostname: ME\_AR02.GAZ185\_RE0

```text
Junos: 17.3R3-S8.1
```

- Không phát sinh core-dump

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show system core-dumps

Dec 15 23:58:00

/var/crash/\*core\*: No such file or directory

/var/tmp/\*core\*: No such file or directory

/var/tmp/pics/\*core\*: No such file or directory

/var/crash/kernel.\*: No such file or directory

/var/jails/rest-api/tmp/\*core\*: No such file or directory

/tftpboot/corefiles/\*core\*: No such file or directory

```text
Show system resource-monitor fpc <<< không bất tường
```

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show system resource-monitor fpc

FPC Resource Usage Summary

Free Heap Mem Watermark         : 20  %

Free NH Mem Watermark           : 20  %

Free Filter Mem Watermark       : 20  %

\* - Watermark reached

Heap            Avg                   ENCAP mem       NH mem          FW mem

Slot #         % Free       RTT  RTT        PFE #        % Free       % Free          % Free

0             90       --     --(--)      0            NA          73              99

1             89       --     --(--)      0            NA          73              99

```text
show route summary <<< route không nhiều
```

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show route summary | no-more

Dec 16 00:02:45

Autonomous system number: 37342

Router ID: 10.250.64.22

```text
inet.0: 2308 destinations, 2629 routes (2305 active, 0 holddown, 3 hidden)
```

```text
Direct:     17 routes,     16 active
```

```text
Local:     15 routes,     15 active
```

```text
OSPF:   1914 routes,   1914 active
```

```text
BGP:    680 routes,    359 active
```

```text
RSVP:      2 routes,      0 active
```

```text
LDP:      1 routes,      1 active
```

- Log messages <<< không có log lạ
- Log interactive-commands <<< chưa check
- Log chassisd <<< chưa check

Thu thập các thông tin liên quan

```text
> request support information | no-more | save /var/log/RSI\_ME\_PR01.GAZ185\_20211216
```

```text
> file archive source /var/log/\* destination /var/log/LOG\_ME\_PR01.GAZ185\_20211216
```

```text
> show configuration | no-more | save /var/log/CONFIG\_ME\_AR02.GAZ185\_20211216
```

```text
> show version invoke-on all-routing-engines | match "re0|re1|Junos:"
```

```text
> show chassis alarms
```

```text
> show system alarms
```

```text
> show system core-dumps
```

```text
> show chassis routing-engine | no-more
```

```text
> show chassis routing-engine | match "Slot|State|Start"
```

```text
show chassis environment cb | no-more
```

```text
show chassis environment cb | match "CB|State"
```

```text
> show chassis fabric summary | no-more
```

/\* Lưu thông tin hardware/fabric/fpc \*/

```text
> show chassis hardware | no-more
```

```text
> show chassis fabric fpcs | no-more
```

```text
> show chassis fabric summary extended | no-more
```

```text
> show chassis fabric plane | no-more
```

/\* Lưu thông tin đồng bộ GRES and NSR - KB32931  \*/

```text
> show system switchover /\* Show on Backup RE – GRES Readiness Check\*/
```

```text
> show task replication  /\* Show on Master RE – RPD Synchronization Check\*/
```

```text
> show database-replication summary /\* Show on Master RE – For BNG only \*/
```

Kiểm tra các case cũ, google hướng dẫn thực hiện

- Hướng dẫn nâng cấp MX-SCBE2 trên trang chủ Juniper:

- Upgrading an MX960 to Use the SCBE2-MX

- <https://www.juniper.net/documentation/us/en/hardware/mx960/topics/task/scb2-mxseries-mx960-upgrading-operational.html>

- Quy trình thay thế Routing-Engine Juniper MX

- Quy trình thay thế Routing-Engine Juniper MX.doc

Yêu cầu khách hàng chuẩn bị

- Máy tính:

- Có sẵn driver dây console
- Có kết nối internet
- Phần mềm cho phép điều khiển từ xa

- Dây console + dây mạng RJ45
- JunOS Phiên bản 17.3R3-S8.1

- Bản cài trực tiếp

- Có thể dùng lại bản lưu trên RE0 cho nhanh

- Bản cài bằng USB

- Dùng trong trường hợp không cài được bằng bản cài trực tiếp

- 1 USB dung lượng 8G, hỗ trợ USB 3.0 càng tốt

Xử lý trên thiết bị

- Thu thập baseline

/\* Lưu thông tin cấu hình và RSI \*/

```text
> set cli timestamp
```

```text
> show configuration | no-more
```

```text
> request support information | no-more
```

/\* Lưu thông tin alarm/core \*/

```text
> show system alarms
```

```text
> show chassis alarms
```

```text
> show system core-dumps
```

/\* Lưu thông tin về IGP \*/

```text
> show ospf interface | no-more
```

```text
> show ospf interface | count
```

```text
> show ospf neighbor instance all | no-more
```

```text
> show ospf3 interface | no-more
```

```text
> show ospf3 interface | count
```

```text
> show ospf3 neighbor instance all | no-more
```

/\* Lưu thông tin về MPLS/LDP/RSVP \*/

```text
> show mpls interface | no-more
```

```text
> show mpls interface | count
```

```text
> show ldp interface | no-more
```

```text
> show ldp interface | count
```

```text
> show rsvp interface | no-more
```

```text
> show rsvp interface | count
```

```text
> show ldp neighbor | no-more
```

```text
> show ldp neighbor | count
```

```text
> show ldp session | no-more
```

```text
> show ldp session | count
```

```text
> show rsvp session | no-more
```

```text
> show rsvp session | count
```

```text
> show mpls lsp | no-more
```

/\* Lưu thông tin về BGP \*/

```text
> shwo bgp sum | no-more
```

```text
show bgp summary | match Establ | count
```

```text
> show bgp neighbor | no-more
```

```text
> show route summary | no-more
```

```text
> show bfd session detail | no-more
```

/\* Lưu thông tin VRRP/L2VPN/VPLS/LLDP/BFD \*/

```text
> show vrrp | no-more
```

```text
> show l2circuit connections | no-more
```

```text
> show vpls connections | no-more
```

```text
> show vpls mac-table | no-more
```

```text
> show lldp neighbors | no-more
```

```text
> show bfd session detail | no-more
```

/\* Lưu thông tin hardware/fabric/fpc \*/

```text
> show chassis hardware | no-more
```

```text
> show chassis fabric fpcs | no-more
```

```text
> show chassis fabric summary extended | no-more
```

```text
> show chassis fabric plane | no-more
```

/\* Lưu thông tin đồng bộ GRES and NSR - KB32931  \*/

```text
> show system switchover /\* Show on Backup RE – GRES Readiness Check \*/
```

```text
> show task replication  /\* Show on Master RE – RPD Synchronization Check \*/
```

```text
> show database-replication summary /\* Show on Master RE – For BNG only \*/
```

```text
> show system subscriber-management summary
```

- Kiểm tra điều kiện bắt buộc để sử dụng được MX-SCBE2

- NOTE: The SCBE2-MX is supported only on:

- Junos OS Release 13.3 or later
- Network Services Mode: Enhanced-IP

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show version invoke-on all-routing-engines | match "re0|re1|Junos:"

Dec 16 00:03:58

re0:

- -------------------------------------------------------------------------

Hostname: ME\_AR02.GAZ185\_RE0

```text
Junos: 17.3R3-S8.1
```

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show chassis network-services

Dec 16 00:04:31

Network Services Mode: Enhanced-IP

```text
>>> Thiết bị đã đủ điều kiện để nâng cấp MX-SCBE2
```

- Tiến hành Power-off thiết bị bằng lệnh "request system halt both-routing-engines" để tắt RE một cách an toàn.

{master}

vietpn@ME\_AR02.GAZ185\_RE0> request system halt both-routing-engines

Dec 16 00:15:11

warning: Other routing-engine not present

Halt the system ? [yes,no] (no) yes

Dec 16 00:15:20

\*\*\* FINAL System shutdown message from SP@ME\_AR02.GAZ185\_RE0 \*\*\*

System going down IMMEDIATELY

Shutdown NOW!

[pid 37975]

- Thao tác vật lý tháo SCBE-MX và thay thế bằng SCBE2-MX vào thiết bị.
- Gắn lại RE0 (RE đang dùng trên thiết bị) vào CB0.

- Do RE1 là RE mới nên chưa thực hiện gắn vào CB1 ở bước này

- Mở nguồn lại cho thiết bị và kiểm tra

- Các dịch vụ trên box vẫn hoạt động bình thường
- box không có alarm
- log message không có bất thường.

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show chassis hardware

Hardware inventory:

Item             Version  Part number  Serial number     Description

Chassis                                JN1242EB7AFB      MX480

Routing Engine 0 REV 10   740-031116   9009199844        RE-S-1800x4

CB 0             REV 13   750-062572   CAPR1217          Enhanced MX SCB 2

CB 1             REV 13   750-062572   CAPM6835          Enhanced MX SCB 2

- -------

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show chassis fpc

Temp  CPU Utilization (%)   CPU Utilization (%)  Memory    Utilization (%)

```text
Slot State            (C)  Total  Interrupt      1min   5min   15min  DRAM (MB) Heap     Buffer
```

0  Online            23      8          0        8      3      1    2048        8         20

1  Online            23     13          0       16      7      3    2048       10         21

2  Empty

3  Empty

4  Empty

5  Empty

- -------

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show version

Hostname: ME\_AR02.GAZ185\_RE0

Model: mx480

```text
Junos: 17.3R3-S8.1
```

- -------

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show route summary

Autonomous system number: 37342

Router ID: 10.250.64.22

```text
inet.0: 2308 destinations, 2629 routes (2305 active, 0 holddown, 3 hidden)
```

```text
Direct:     17 routes,     16 active
```

```text
Local:     15 routes,     15 active
```

```text
OSPF:   1914 routes,   1914 active
```

```text
BGP:    680 routes,    359 active
```

```text
RSVP:      2 routes,      0 active
```

```text
LDP:      1 routes,      1 active
```

- -------

vietpn@ME\_AR02.GAZ185\_RE0> show system processes extensive | except 0.00

263 processes: 5 running, 228 sleeping, 30 waiting

```text
Mem: 716M Active, 1484M Inact, 648M Wired, 1643M Buf, 13G Free
```

```text
Swap: 8192M Total, 8192M Free
```

```text
PID USERNAME PRI NICE   SIZE    RES STATE   C   TIME    WCPU COMMAND
```

4754 root      23    0   825M 47360K nanslp  0   0:34   4.79% chassisd{chassisd}

4768 root      20    0  1239M   292M kqread  2   0:13   0.59% rpd{rpd}

11 root     -72    -     0K   480K WAIT    2   0:04   0.10% intr{swi1: netisr 0}

- -------

{master}

```text
vietpn@ME\_AR02.GAZ185\_RE0> show chassis environment cb | match "CB|state"
```

CB 0 status:

```text
State                      Online Master
```

CB 1 status:

```text
State                      Online
```

- -------

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show chassis fabric summary

```text
Plane   State    Uptime
```

0      Online   7 minutes, 24 seconds

1      Online   7 minutes, 24 seconds

2      Online   7 minutes, 18 seconds

3      Online   7 minutes, 18 seconds

4      Spare    7 minutes, 12 seconds

5      Spare    7 minutes, 12 seconds

6      Spare    7 minutes, 6 seconds

7      Spare    7 minutes, 6 seconds

Note: For extended summary, use

```text
show chassis fabric summary extended
```

- -------

vietpn@ME\_AR02.GAZ185\_RE0> show chassis fabric fpcs

Dec 16 00:40:47

```text
Fabric management FPC state:
```

FPC 0

PFE #0

Plane 0: Plane enabled

Plane 1: Plane enabled

Plane 2: Plane enabled

Plane 3: Plane enabled

Plane 4: Links ok

Plane 5: Links ok

Plane 6: Links ok

Plane 7: Links ok

FPC 1

PFE #0

Plane 0: Plane enabled

Plane 1: Plane enabled

Plane 2: Plane enabled

Plane 3: Plane enabled

Plane 4: Links ok

Plane 5: Links ok

Plane 6: Links ok

Plane 7: Links ok

- -------

vietpn@ME\_AR02.GAZ185\_RE0> show chassis fabric summary extended

Dec 16 00:41:03

```text
Plane   State      Link   Link  Destination errors  Uptime
```

```text
Error  TF    Local / Remote
```

0      Online     NO     NO        NO/  NO         8 minutes, 42 seconds

1      Online     NO     NO        NO/  NO         8 minutes, 42 seconds

2      Online     NO     NO        NO/  NO         8 minutes, 36 seconds

3      Online     NO     NO        NO/  NO         8 minutes, 36 seconds

4      Spare      NO     NO        NO/  NO         8 minutes, 30 seconds

5      Spare      NO     NO        NO/  NO         8 minutes, 30 seconds

6      Spare      NO     NO        NO/  NO         8 minutes, 24 seconds

7      Spare      NO     NO        NO/  NO         8 minutes, 24 seconds

=> Hoàn tất việc nâng cấp SCBE2-MX.

Công việc tiếp theo liên quan đến việc gắn RE mới vào slot 1.

- Tắt tính năng Graceful-switchover và NSR

{master}

```text
> configure private
```

# deactivate chassis redundancy graceful-switchover

# deactivate routing-options nonstop-routing

# deactivate system commit synchronize

# deactivate system switchover-on-routing-crash

# deactivate routing-options nsr-phantom-holdtime

{master}[edit]

vietpn@ME\_AR02.GAZ185\_RE0# show | compare

Dec 16 00:43:58

[edit system]

!   inactive: switchover-on-routing-crash;

[edit system commit]

!    inactive: synchronize;

[edit chassis redundancy]

!     inactive: graceful-switchover { ... }

[edit routing-options]

!   inactive: nonstop-routing;

# commit

- Gắn RE1 vào CB1, thực hiện nâng cấp JunOS lên phiên bản giống với RE0
- Đồng bộ cấu hình, các script file.

[edit]

vietpn@ME\_AR02.GAZ185\_RE0# commit synchronize scripts

Dec 16 01:10:53

re0:

configuration check succeeds

re1:

[edit]

'chassis'

warning: Chassis configuration for network services has been changed. A system reboot is mandatory.  Please reboot \*ALL\* routing engines NOW. Continuing without a reboot might result in unexpected system behavior.

Generating RSA key /etc/ssh/ssh\_host\_key

Generating DSA key /etc/ssh/ssh\_host\_dsa\_key

Generating RSA2 key /etc/ssh/ssh\_host\_rsa\_key

Generating ECDSA key /etc/ssh/ssh\_host\_ecdsa\_key

Generating ED25519 key /etc/ssh/ssh\_host\_ed25519\_key

```text
commit complete
```

re0:

```text
commit complete
```

- Thực hiện Reboot lại RE1 để đồng bộ network-services enhanced-ip
- Bật lại tính năng Graceful-switchover và NSR

```text
> configure
```

# activate chassis redundancy graceful-switchover

# activate routing-options nonstop-routing

# activate system commit synchronize

# activate system switchover-on-routing-crash

# activate routing-options nsr-phantom-holdtime

[edit]

vietpn@ME\_AR02.GAZ185\_RE0# show | compare

Dec 16 01:23:13

[edit system]

!   active: switchover-on-routing-crash;

[edit system commit]

!    active: synchronize;

[edit chassis redundancy]

!     active: graceful-switchover { ... }

[edit routing-options]

!   active: nonstop-routing;

[edit]

vietpn@ME\_AR02.GAZ185\_RE0# commit

- Thực hiện switch master RE 2 lần RE0 ->RE1 và RE1-> RE0 ghi nhận thiết bị hoạt động đúng mong đợi.

- Thực hiện bước này sau khoảng 10-15 phút để cho RE mới đồng bộ xong trạng thái với RE master.
- Kiểm tra trạng thái đồng bộ giữa 2 RE đã sẵn sang để việc switchover không gây ảnh hưởng dịch vụ/hoặc gây ảnh hưởng dịch vụ là nhỏ nhất.

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show task replication

Dec 16 01:33:44

Stateful Replication: Enabled

RE mode: Master

Protocol                Synchronization Status

OSPF                    Complete

BGP                     Complete

MPLS                    Complete

RSVP                    Complete

LDP                     Complete

{master}

vietpn@ME\_AR02.GAZ185\_RE0> show database-replication summary

Dec 16 01:33:56

General:

Graceful Restart           Enabled

Mastership                 Master

Connection                 Up

Database                   Synchronized

Message Queue              Ready

{master}

vietpn@ME\_AR02.GAZ185\_RE0> request chassis routing-engine master switch check

Dec 16 01:34:26

Switchover Ready

{master}

vietpn@ME\_AR02.GAZ185\_RE0> request routing-engine login other-routing-engine

Dec 16 01:34:52

- -- JUNOS 17.3R3-S8.1 Kernel 64-bit  JNPR-10.3-20200425.36498d6\_buil

{backup}

vietpn@ME\_AR02.GAZ185\_RE1> show system switchover

Graceful switchover: On

Configuration database: Ready

Kernel database: Ready

Switchover Status: Ready

{backup}

vietpn@ME\_AR02.GAZ185\_RE1> show task replication

Stateful Replication: Enabled

RE mode: Backup

{backup}

vietpn@ME\_AR02.GAZ185\_RE1> exit

rlogin: connection closed

{master}

vietpn@ME\_AR02.GAZ185\_RE0> request chassis routing-engine master switch

Dec 16 01:36:53

Toggle mastership between routing engines ? [yes,no] (no) yes

Dec 16 01:36:57

Kết quả xử lý trên thiết bị

- Xử lý ngày 16/12:

- Hoàn tất nâng cấp MX-SCBE lên MX-SCBE2
- Quá trình thực hiện không phát sinh ngoài kế hoạch dự kiến.
