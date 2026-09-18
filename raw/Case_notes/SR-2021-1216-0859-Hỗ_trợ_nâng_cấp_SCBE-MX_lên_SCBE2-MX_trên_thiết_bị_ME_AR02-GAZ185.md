# SR-2021-1216-0859 - Hỗ trợ nâng cấp SCBE-MX lên SCBE2-MX trên thiết bị ME_AR02.GAZ185

---

**Phát sinh:�**�**nâng cấp SCBE-MX lên SCBE2-MX trên thiết bị ME_AR02.GAZ185**

---

**Ghi nhận ban đầu**

- Thiết bị ME_AR02.GAZ185 đang chạy CB0 và RE0 do hôm trước thu hồi CB1 + RE1 ứng cứu cho thiết bị ME_PR01.GAZ020 (case ID SR-2021-1201-0922).
    - Hiện kho đã hết card MX-SCBE nên thực hiện nâng cấp lên MX-SCBE2.

{master}

vietpn@ME_AR02.GAZ185_RE0> show chassis hardware

Hardware inventory:

Item             Version  Part number  Serial number     Description

Chassis                                JN1242EB7AFB      MX480

Midplane         REV 04   750-047862   ACRD1717          Enhanced MX480 Midplane

<span style="background-color: #ffaaaa">Routing Engine 0 REV 10   740-031116   9009199844        RE-S-1800x4</span>

<span style="background-color: #ffaaaa">CB 0             REV 24   750-031391   CAEA9005          Enhanced MX SCB</span>

---

**Các bước xử lý**

---

**Kiểm tra sơ bộ**

- IP MNS thiết bị <span style="background-color: #ffaaaa">**10.250.0.22**</span>
- Health check thiết bị
    - CPU (1%), MEM(8%), TEMP (29C) không có bất thường, system boot (462 ngày)

vietpn@ME_AR02.GAZ185_RE0> show chassis routing-engine         

Routing Engine status:

  Slot 0:

    Current state                  Master

    Election priority              Master

    <span style="background-color: #ffaaaa">Temperature                 29 degrees C / 84 degrees F</span>

    CPU temperature             27 degrees C / 80 degrees F

    DRAM                      16329 MB (16384 MB installed)

    <span style="background-color: #ffaaaa">Memory utilization           8 percent</span>

    5 sec CPU utilization:

      User                       0 percent

      Background                 0 percent

      Kernel                     1 percent

      Interrupt                  0 percent

      <span style="background-color: #ffaaaa">Idle                      99 percent</span>

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

    <span style="background-color: #ffaaaa">Uptime                         462 days, 16 minutes, 20 seconds</span>

    Last reboot reason             Router rebooted after a normal shutdown.

    Load averages:                 1 minute   5 minute  15 minute

                                       0.02       0.11       0.14

    - Không có process chiếm CPU

vietpn@ME_AR02.GAZ185_RE0> show system processes extensive      

Dec 15 23:57:09

last pid: 37030;  <span style="background-color: #ffaaaa">load averages:  0.07,  0.11,  0.14</span>  up 462+00:16:53    23:57:09

232 processes: 5 running, 197 sleeping, 30 waiting

<span style="background-color: #ffaaaa">Mem: 57M Active, 2379M Inact, 909M Wired, 1687M Buf, 12G Free</span>

Swap: 8192M Total, 8192M Free

  PID USERNAME PRI NICE   SIZE    RES STATE   C   TIME    WCPU COMMAND

   10 root     155 ki31     0K    64K RUN     1    ??? 100.00% idle{idle: cpu1}

   10 root     155 ki31     0K    64K CPU3    3    ??? 100.00% idle{idle: cpu3}

   10 root     155 ki31     0K    64K CPU2    2    ??? 100.00% idle{idle: cpu2}

   10 root     155 ki31     0K    64K CPU0    0    ??? 100.00% idle{idle: cpu0}

13511 root      21    0   825M 47000K select  0 490.4H   2.59% chassisd{chassisd}

   11 root     -72    -     0K   480K WAIT    2  47.9H   0.00% intr{swi1: netisr 0}

14218 root      20    0  1271M   333M kqread  0  38.2H   0.00% rpd{rpd}

13536 root      20    0   728M 12772K select  2  26.7H   0.00% ppmd

- Health check show system storage no-forwarding  <<< còn trống 8.8G

vietpn@ME_AR02.GAZ185_RE0> show system storage

Dec 15 23:57:25

Filesystem              Size       Used      Avail  Capacity   Mounted on

/dev/md0.uzip            21M        21M         0B      100%  /

devfs                   1.0K       1.0K         0B      100%  /dev

<span style="background-color: #ffaaaa">/dev/gpt/junos           19G       8.9G       8.8G       50%  /.mount</span>

        - show version detail no-forwarding

{master}

vietpn@ME_AR02.GAZ185_RE0> show version invoke-on all-routing-engines | match "re0|re1|Junos:"

Dec 16 00:03:58

re0:

--------------------------------------------------------------------------

Hostname: ME_AR02.GAZ185_RE0

<span style="background-color: #ffaaaa">Junos: 17.3R3-S8.1</span>

- Không phát sinh core-dump

{master}

vietpn@ME_AR02.GAZ185_RE0> show system core-dumps

Dec 15 23:58:00

/var/crash/*core*: No such file or directory

/var/tmp/*core*: No such file or directory

/var/tmp/pics/*core*: No such file or directory

/var/crash/kernel.*: No such file or directory

/var/jails/rest-api/tmp/*core*: No such file or directory

/tftpboot/corefiles/*core*: No such file or directory

- Show system resource-monitor fpc <<< không bất tường

{master}

vietpn@ME_AR02.GAZ185_RE0> show system resource-monitor fpc

FPC Resource Usage Summary

Free Heap Mem Watermark         : 20  %

Free NH Mem Watermark           : 20  %

Free Filter Mem Watermark       : 20  %       

* - Watermark reached

                    Heap            Avg                   ENCAP mem       NH mem          FW mem  

   Slot #         % Free       RTT  RTT        PFE #        % Free       % Free          % Free         

<span style="background-color: #ffaaaa">        0             90       --     --(--)      0            NA          73              99</span>

<span style="background-color: #ffaaaa">        1             89       --     --(--)      0            NA          73              99</span>

- show route summary <<< route không nhiều

{master}

vietpn@ME_AR02.GAZ185_RE0> show route summary | no-more

Dec 16 00:02:45

Autonomous system number: 37342

Router ID: 10.250.64.22

<span style="background-color: #ffaaaa">inet.0: 2308 destinations, 2629 routes</span> (2305 active, 0 holddown, 3 hidden)

              Direct:     17 routes,     16 active

               Local:     15 routes,     15 active

                OSPF:   1914 routes,   1914 active

                 BGP:    680 routes,    359 active

                RSVP:      2 routes,      0 active

                 LDP:      1 routes,      1 active

- <span style="background-color: #ffaaaa">Log messages <<< không có log lạ</span>
- <span style="background-color: #ffaaaa">Log interactive-commands <<< chưa check</span>
- <span style="background-color: #ffaaaa">Log chassisd <<< chưa check</span>

**Thu thập các thông tin liên quan**

> request support information | no-more | save /var/log/RSI_ME_PR01.GAZ185_20211216

> file archive source /var/log/* destination /var/log/LOG_ME_PR01.GAZ185_20211216

> show configuration | no-more | save /var/log/CONFIG_ME_AR02.GAZ185_20211216

> show version invoke-on all-routing-engines | match "re0|re1|Junos:"

> show chassis alarms

> show system alarms

> show system core-dumps

> show chassis routing-engine | no-more

> show chassis routing-engine | match "Slot|State|Start"

show chassis environment cb | no-more

show chassis environment cb | match "CB|State"

> show chassis fabric summary | no-more

/* Lưu thông tin hardware/fabric/fpc */

> show chassis hardware | no-more

> show chassis fabric fpcs | no-more

> show chassis fabric summary extended | no-more

> show chassis fabric plane | no-more

/* Lưu thông tin đồng bộ GRES and NSR - KB32931  */

> show system switchover /* Show on <span style="background-color: #ffaaaa">Backup RE</span> – GRES Readiness Check*/

> show task replication  /* Show on <span style="background-color: #ffaaaa">Master RE</span> – RPD Synchronization Check*/

> show database-replication summary /* Show on <span style="background-color: #ffaaaa">Master RE</span> – For BNG only */

**Kiểm tra các case cũ, google hướng dẫn thực hiện**

- Hướng dẫn nâng cấp MX-SCBE2 trên trang chủ Juniper:
    - Upgrading an MX960 to Use the SCBE2-MX
        - [https://www.juniper.net/documentation/us/en/hardware/mx960/topics/task/scb2-mxseries-mx960-upgrading-operational.html](https://www.juniper.net/documentation/us/en/hardware/mx960/topics/task/scb2-mxseries-mx960-upgrading-operational.html)
- Quy trình thay thế Routing-Engine Juniper MX
    - Quy trình thay thế Routing-Engine Juniper MX.doc

**Yêu cầu khách hàng chuẩn bị**

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

**Xử lý trên thiết bị**

- Thu thập baseline

/* Lưu thông tin cấu hình và RSI */

> set cli timestamp

> show configuration | no-more

> request support information | no-more

/* Lưu thông tin alarm/core */

> show system alarms

> show chassis alarms

> show system core-dumps

/* Lưu thông tin về IGP */

> show ospf interface | no-more

> show ospf interface | count

> show ospf neighbor instance all | no-more

> show ospf3 interface | no-more

> show ospf3 interface | count

> show ospf3 neighbor instance all | no-more

/* Lưu thông tin về MPLS/LDP/RSVP */

> show mpls interface | no-more

> show mpls interface | count

> show ldp interface | no-more

> show ldp interface | count

> show rsvp interface | no-more

> show rsvp interface | count

> show ldp neighbor | no-more

> show ldp neighbor | count

> show ldp session | no-more

> show ldp session | count

> show rsvp session | no-more

> show rsvp session | count

> show mpls lsp | no-more

/* Lưu thông tin về BGP */

> shwo bgp sum | no-more

show bgp summary | match Establ | count

> show bgp neighbor | no-more

> show route summary | no-more

> show bfd session detail | no-more

/* Lưu thông tin VRRP/L2VPN/VPLS/LLDP/BFD */

> show vrrp | no-more

> show l2circuit connections | no-more

> show vpls connections | no-more

> show vpls mac-table | no-more

> show lldp neighbors | no-more

> show bfd session detail | no-more

/* Lưu thông tin hardware/fabric/fpc */

> show chassis hardware | no-more

> show chassis fabric fpcs | no-more

> show chassis fabric summary extended | no-more

> show chassis fabric plane | no-more

/* Lưu thông tin đồng bộ GRES and NSR - KB32931  */

> show system switchover /* Show on Backup RE – GRES Readiness Check */

> show task replication  /* Show on Master RE – RPD Synchronization Check */

> show database-replication summary /* Show on Master RE – For BNG only */

> show system subscriber-management summary

- Kiểm tra điều kiện bắt buộc để sử dụng được MX-SCBE2
    - <span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">NOTE: The SCBE2-MX is supported only on:</span></span>
        - <span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">Junos OS Release 13.3 or later</span></span>
        - <span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">Network Services Mode: Enhanced-IP</span></span>

```
{master}
vietpn@ME_AR02.GAZ185_RE0> show version invoke-on all-routing-engines | match "re0|re1|Junos:"
Dec 16 00:03:58
re0:
--------------------------------------------------------------------------
Hostname: ME_AR02.GAZ185_RE0
Junos: 17.3R3-S8.1

{master}
vietpn@ME_AR02.GAZ185_RE0> show chassis network-services
Dec 16 00:04:31
Network Services Mode: Enhanced-IP
```

>>> Thiết bị đã đủ điều kiện để nâng cấp MX-SCBE2

- Tiến hành Power-off thiết bị bằng lệnh "request system halt both-routing-engines" để tắt RE một cách an toàn.

{master}

vietpn@ME_AR02.GAZ185_RE0> request system halt both-routing-engines

Dec 16 00:15:11

warning: Other routing-engine not present

Halt the system ? [yes,no] (no) yes

Dec 16 00:15:20

                                                                               

*** FINAL System shutdown message from SP@ME_AR02.GAZ185_RE0 ***             

System going down IMMEDIATELY                                                  

                                                                               

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">Shutdown NOW!</span></span>

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">[pid 37975]</span></span>

- Thao tác vật lý tháo SCBE-MX và thay thế bằng SCBE2-MX vào thiết bị.
- Gắn lại RE0 (RE đang dùng trên thiết bị) vào CB0.
    - <span style="background-color: #ffaaaa">Do RE1 là RE mới nên chưa thực hiện gắn vào CB1 ở bước này</span>
- Mở nguồn lại cho thiết bị và kiểm tra
    - Các dịch vụ trên box vẫn hoạt động bình thường
    - box không có alarm
    - log message không có bất thường.

```
{master}
vietpn@ME_AR02.GAZ185_RE0> show chassis hardware
Hardware inventory:
Item             Version  Part number  Serial number     Description
Chassis                                JN1242EB7AFB      MX480
Routing Engine 0 REV 10   740-031116   9009199844        RE-S-1800x4
CB 0             REV 13   750-062572   CAPR1217          Enhanced MX SCB 2
CB 1             REV 13   750-062572   CAPM6835          Enhanced MX SCB 2

--------
{master}
vietpn@ME_AR02.GAZ185_RE0> show chassis fpc
                     Temp  CPU Utilization (%)   CPU Utilization (%)  Memory    Utilization (%)
Slot State            (C)  Total  Interrupt      1min   5min   15min  DRAM (MB) Heap     Buffer
  0  Online            23      8          0        8      3      1    2048        8         20
  1  Online            23     13          0       16      7      3    2048       10         21
  2  Empty           
  3  Empty           
  4  Empty           
  5  Empty     

--------
{master}
vietpn@ME_AR02.GAZ185_RE0> show version
Hostname: ME_AR02.GAZ185_RE0
Model: mx480
Junos: 17.3R3-S8.1

--------
{master}
vietpn@ME_AR02.GAZ185_RE0> show route summary
Autonomous system number: 37342
Router ID: 10.250.64.22

inet.0: 2308 destinations, 2629 routes (2305 active, 0 holddown, 3 hidden)
              Direct:     17 routes,     16 active
               Local:     15 routes,     15 active
                OSPF:   1914 routes,   1914 active
                 BGP:    680 routes,    359 active
                RSVP:      2 routes,      0 active
                 LDP:      1 routes,      1 active

--------
vietpn@ME_AR02.GAZ185_RE0> show system processes extensive | except 0.00
263 processes: 5 running, 228 sleeping, 30 waiting

Mem: 716M Active, 1484M Inact, 648M Wired, 1643M Buf, 13G Free
Swap: 8192M Total, 8192M Free

  PID USERNAME PRI NICE   SIZE    RES STATE   C   TIME    WCPU COMMAND
4754 root      23    0   825M 47360K nanslp  0   0:34   4.79% chassisd{chassisd}
4768 root      20    0  1239M   292M kqread  2   0:13   0.59% rpd{rpd}
   11 root     -72    -     0K   480K WAIT    2   0:04   0.10% intr{swi1: netisr 0}

--------
{master}
vietpn@ME_AR02.GAZ185_RE0> show chassis environment cb | match "CB|state"
CB 0 status:
  State                      Online Master
CB 1 status:
  State                      Online

--------
{master}
vietpn@ME_AR02.GAZ185_RE0> show chassis fabric summary
Plane   State    Uptime
0      Online   7 minutes, 24 seconds
1      Online   7 minutes, 24 seconds
2      Online   7 minutes, 18 seconds
3      Online   7 minutes, 18 seconds
4      Spare    7 minutes, 12 seconds
5      Spare    7 minutes, 12 seconds
6      Spare    7 minutes, 6 seconds
7      Spare    7 minutes, 6 seconds
  
Note: For extended summary, use
       show chassis fabric summary extended

--------
vietpn@ME_AR02.GAZ185_RE0> show chassis fabric fpcs
Dec 16 00:40:47
Fabric management FPC state:
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

--------
vietpn@ME_AR02.GAZ185_RE0> show chassis fabric summary extended
Dec 16 00:41:03
Plane   State      Link   Link  Destination errors  Uptime
                   Error  TF    Local / Remote
0      Online     NO     NO        NO/  NO         8 minutes, 42 seconds
1      Online     NO     NO        NO/  NO         8 minutes, 42 seconds
2      Online     NO     NO        NO/  NO         8 minutes, 36 seconds
3      Online     NO     NO        NO/  NO         8 minutes, 36 seconds
4      Spare      NO     NO        NO/  NO         8 minutes, 30 seconds
5      Spare      NO     NO        NO/  NO         8 minutes, 30 seconds
6      Spare      NO     NO        NO/  NO         8 minutes, 24 seconds
7      Spare      NO     NO        NO/  NO         8 minutes, 24 seconds
```

<span style="background-color: #ffaaaa">=> Hoàn tất việc nâng cấp </span><span style="background-color: #ffaaaa">SCBE2-MX.</span>

Công việc tiếp theo liên quan đến việc gắn RE mới vào slot 1.

- Tắt tính năng Graceful-switchover và NSR

```
{master}
> configure private
# deactivate chassis redundancy graceful-switchover
# deactivate routing-options nonstop-routing
# deactivate system commit synchronize
# deactivate system switchover-on-routing-crash
# deactivate routing-options nsr-phantom-holdtime

{master}[edit]
vietpn@ME_AR02.GAZ185_RE0# show | compare
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
```

- Gắn RE1 vào CB1, thực hiện nâng cấp JunOS lên phiên bản giống với RE0
- Đồng bộ cấu hình, các script file.

```
[edit]
vietpn@ME_AR02.GAZ185_RE0# commit synchronize scripts
Dec 16 01:10:53
re0:
configuration check succeeds
re1:
[edit]
  'chassis'
    warning: Chassis configuration for network services has been changed. A system reboot is mandatory.  Please reboot *ALL* routing engines NOW. Continuing without a reboot might result in unexpected system behavior.
Generating RSA key /etc/ssh/ssh_host_key
Generating DSA key /etc/ssh/ssh_host_dsa_key
Generating RSA2 key /etc/ssh/ssh_host_rsa_key
Generating ECDSA key /etc/ssh/ssh_host_ecdsa_key
Generating ED25519 key /etc/ssh/ssh_host_ed25519_key
commit complete
re0:
commit complete
```

- Thực hiện Reboot lại RE1 để đồng bộ network-services enhanced-ip
- Bật lại tính năng Graceful-switchover và NSR

```
> configure
# activate chassis redundancy graceful-switchover
# activate routing-options nonstop-routing
# activate system commit synchronize
# activate system switchover-on-routing-crash
# activate routing-options nsr-phantom-holdtime

[edit]
vietpn@ME_AR02.GAZ185_RE0# show | compare
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
vietpn@ME_AR02.GAZ185_RE0# commit
```

- Thực hiện switch master RE 2 lần RE0 ->RE1 và RE1-> RE0 ghi nhận thiết bị hoạt động đúng mong đợi.
    - Thực hiện bước này sau khoảng 10-15 phút để cho RE mới đồng bộ xong trạng thái với RE master.
    - Kiểm tra trạng thái đồng bộ giữa 2 RE đã sẵn sang để việc switchover không gây ảnh hưởng dịch vụ/hoặc gây ảnh hưởng dịch vụ là nhỏ nhất.

```
{master}
vietpn@ME_AR02.GAZ185_RE0> show task replication
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
vietpn@ME_AR02.GAZ185_RE0> show database-replication summary
Dec 16 01:33:56

General:
    Graceful Restart           Enabled
    Mastership                 Master
    Connection                 Up
    Database                   Synchronized
    Message Queue              Ready

{master}
vietpn@ME_AR02.GAZ185_RE0> request chassis routing-engine master switch check     
Dec 16 01:34:26
Switchover Ready

{master}
vietpn@ME_AR02.GAZ185_RE0> request routing-engine login other-routing-engine
Dec 16 01:34:52

--- JUNOS 17.3R3-S8.1 Kernel 64-bit  JNPR-10.3-20200425.36498d6_buil
{backup}
vietpn@ME_AR02.GAZ185_RE1> show system switchover
Graceful switchover: On
Configuration database: Ready
Kernel database: Ready
Switchover Status: Ready

{backup}
vietpn@ME_AR02.GAZ185_RE1> show task replication
        Stateful Replication: Enabled
        RE mode: Backup

{backup}
vietpn@ME_AR02.GAZ185_RE1> exit    

rlogin: connection closed

{master}
vietpn@ME_AR02.GAZ185_RE0> request chassis routing-engine master switch
Dec 16 01:36:53
Toggle mastership between routing engines ? [yes,no] (no) yes
Dec 16 01:36:57

```

**Kết quả xử lý trên thiết bị**

- Xử lý ngày 16/12:
    - <span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">Hoàn tất nâng cấp MX-SCBE lên MX-SCBE2</span></span>
    - <span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">Quá trình thực hiện không phát sinh ngoài kế hoạch dự kiến.</span></span>
