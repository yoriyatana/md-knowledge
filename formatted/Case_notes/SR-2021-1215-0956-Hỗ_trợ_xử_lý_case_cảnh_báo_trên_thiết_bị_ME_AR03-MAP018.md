# SR-2021-1215-0956 - Hỗ trợ xử lý case cảnh báo trên thiết bị ME_AR03.MAP018

- --

* *Phát sinh: alarm CB1 trên�**�**ME_AR03.MAP018**

- --

* *Ghi nhận ban đầu**

- Trên ME_AR03.MAP018 phát sinh các cảnh báo lỗi:

{master}

vietpn@ME_AR03.MAP018_RE0> show chassis alarms

2 alarms currently active

Alarm time               Class  Description

<span style="background-color: #ffaaaa">2021-03-18 17:38:45 CAT  Minor  CB 1 Fabric Chip 1 Not Online</span>

<span style="background-color: #ffaaaa">2021-03-18 17:38:44 CAT  Minor  CB 1 Fabric Chip 0 Not Online</span>

- --

* *Các bước xử lý**

- --

* *Kiểm tra sơ bộ**

- IP MNS thiết bị <span style="background-color: #ffaaaa">**10.250.0.17**</span>
- Cảnh báo phát sinh giống lỗi trên thiết bị ME_PR01.GAZ020 (case ID SR-2021-1201-0922).
- Health check thiết bị
    - CPU (2%), MEM(8%), TEMP (31C) không có bất thường, system boot (459 ngày)

{master}

vietpn@ME_AR03.MAP018_RE0> show chassis routing-engine | no-more

Dec 15 00:46:49

Routing Engine status:

  Slot 0:

    Current state                  Master

    Election priority              Master

    <span style="background-color: #ffaaaa">Temperature                 32 degrees C / 89 degrees F</span>

    CPU temperature             27 degrees C / 80 degrees F

    DRAM                      16329 MB (16384 MB installed)

    <span style="background-color: #ffaaaa">Memory utilization           8 percent</span>

    5 sec CPU utilization:

      User                       0 percent

      Background                 0 percent

      Kernel                     1 percent

      Interrupt                  0 percent

      <span style="background-color: #ffaaaa">Idle                      98 percent</span>

    1 min CPU utilization:

      User                       1 percent

      Background                 0 percent

      Kernel                     2 percent

      Interrupt                  0 percent

      Idle                      98 percent

    5 min CPU utilization:

      User                       0 percent

      Background                 0 percent

      Kernel                     2 percent

      Interrupt                  0 percent

      Idle                      98 percent

    15 min CPU utilization:

      User                       0 percent

      Background                 0 percent

      Kernel                     1 percent

      Interrupt                  0 percent

      Idle                      98 percent

    Model                          RE-S-1800x4

    Serial ID                      9009199833

    Start time                     2020-09-11 23:31:07 CAT

    <span style="background-color: #ffaaaa">Uptime                         459 days, 1 hour, 15 minutes, 39 seconds</span>

    Last reboot reason             Router rebooted after a normal shutdown.

    Load averages:                 1 minute   5 minute  15 minute

                                       0. 32       0.24       0.22

Routing Engine status:

  Slot 1:

    Current state                  Backup

    Election priority              Backup

    <span style="background-color: #ffaaaa">Temperature                 32 degrees C / 89 degrees F</span>

    CPU temperature             28 degrees C / 82 degrees F

    DRAM                      16329 MB (16384 MB installed)

    <span style="background-color: #ffaaaa">Memory utilization           8 percent</span>

    5 sec CPU utilization:

      User                       0 percent

      Background                 0 percent

      Kernel                     0 percent

      Interrupt                  0 percent

      <span style="background-color: #ffaaaa">Idle                      99 percent</span>

    Model                          RE-S-1800x4

    Serial ID                      9009199857

    Start time                     2020-09-11 23:20:51 CAT

    <span style="background-color: #ffaaaa">Uptime                         459 days, 1 hour, 25 minutes, 51 seconds</span>

    Last reboot reason             Router rebooted after a normal shutdown.

    Load averages:                 1 minute   5 minute  15 minute

                                       0. 15       0.16       0.15

    - Không có process chiếm CPU

{master}

vietpn@ME_AR03.MAP018_RE0> show system processes extensive no-forwarding

Dec 15 00:44:46

last pid: 68608;  <span style="background-color: #ffaaaa">load averages:  0.15,  0.18,  0.21</span>  up 459+01:13:39    00:44:46

230 processes: 6 running, 194 sleeping, 30 waiting

<span style="background-color: #ffaaaa">Mem: 80M Active, 2440M Inact, 932M Wired, 1622M Buf, 12G Free</span>

Swap: 8192M Total, 8192M Free

  PID USERNAME PRI NICE   SIZE    RES STATE   C   TIME    WCPU COMMAND

   10 root     155 ki31     0K    64K RUN     3    ??? 100.00% idle{idle: cpu3}

   10 root     155 ki31     0K    64K CPU2    2    ??? 100.00% idle{idle: cpu2}

   10 root     155 ki31     0K    64K CPU0    0    ???  98.19% idle{idle: cpu0}

   10 root     155 ki31     0K    64K RUN     1    ???  97.17% idle{idle: cpu1}

12495 root      22    0   829M 48244K CPU1    1 438.7H   3.56% chassisd{chassisd}

13483 root      20    0   798M 47080K select  2  30.2H   0.68% mib2d

   11 root     -72    -     0K   480K WAIT    3  65.7H   0.10% intr{swi1: netisr 0}

13235 root      20    0  1319M   384M kqread  2  56.0H   0.00% rpd{rpd}

- Health check show system storage no-forwarding  <<< còn trống11G

{master}

vietpn@ME_AR03.MAP018_RE0> show system storage no-forwarding

Dec 15 00:45:00

Filesystem              Size       Used      Avail  Capacity   Mounted on

/dev/md0.uzip            21M        21M         0B      100%  /

devfs                   1.0K       1.0K         0B      100%  /dev

<span style="background-color: #ffaaaa">/dev/gpt/junos           19G       6.5G        11G       37%  /.mount</span>

        - show version detail no-forwarding

{master}

vietpn@ME_AR03.MAP018_RE0> show version invoke-on all-routing-engines | match "re0|re1|Junos:"

Dec 15 00:46:34

re0:

- -------------------------------------------------------------------------

Hostname: ME_AR03.MAP018_RE0

Junos: 17.3R3-S8.1

re1:

- -------------------------------------------------------------------------

Hostname: ME_AR03.MAP018_RE1

Junos: 17.3R3-S8.1

- Không phát sinh core-dump

{master}

vietpn@ME_AR03.MAP018_RE0> show system core-dumps no-forwarding

Dec 15 00:45:16

/var/crash/*core*: No such file or directory

/var/tmp/*core*: No such file or directory

/var/tmp/pics/*core*: No such file or directory

/var/crash/kernel.*: No such file or directory

/var/jails/rest-api/tmp/*core*: No such file or directory

/tftpboot/corefiles/*core*: No such file or directory

- Show system resource-monitor fpc <<< không bất tường

{master}

vietpn@ME_AR03.MAP018_RE0> show system resource-monitor fpc

Dec 15 01:03:28

FPC Resource Usage Summary

Free Heap Mem Watermark         : 20  %

Free NH Mem Watermark           : 20  %

Free Filter Mem Watermark       : 20  %

* - Watermark reached

                    Heap            Avg                   ENCAP mem       NH mem          FW mem

   Slot #         % Free       RTT  RTT        PFE #        % Free       % Free          % Free

<span style="background-color: #ffaaaa">        0             90       --     --(--)      0            NA          88              99</span>

<span style="background-color: #ffaaaa">        1             89       --     --(--)      0            NA          87              99</span>

- show route summary <<< route không nhiều

{master}

vietpn@ME_AR03.MAP018_RE0> show route summary

Dec 15 00:45:31

Autonomous system number: 37342

Router ID: 10.250.64.17

<span style="background-color: #ffaaaa">inet.0: 2491 destinations, 2811 routes</span> (2484 active, 0 holddown, 7 hidden)

              Direct:     30 routes,     29 active

               Local:     29 routes,     29 active

                OSPF:   2031 routes,   2031 active

                 BGP:    714 routes,    394 active

                RSVP:      6 routes,      0 active

                 LDP:      1 routes,      1 active

- <span style="background-color: #ffaaaa">Log messages <<< không có log lạ</span>
- <span style="background-color: #ffaaaa">Log interactive-commands <<< chưa check</span>
- <span style="background-color: #ffaaaa">Log chassisd <<< chưa check</span>

* *Thu thập các thông tin liên quan**

request support information | no-more | save /var/log/RSI_ME_AR03.MAP018_20211215

file archive source /var/log/* destination /var/log/LOG_ME_AR03.MAP018_20211215

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

{master}

vietpn@ME_AR03.MAP018_RE0> show chassis environment cb | match "CB|State"

Dec 15 00:55:49

CB 0 status:

  State                      Online Master

<span style="background-color: #ffaaaa">CB 1 status:</span>

<span style="background-color: #ffaaaa">  State                      Online Standby</span>

{master}

vietpn@ME_AR03.MAP018_RE0> show chassis fabric summary

Dec 15 00:55:58

Plane   State    Uptime

0      Online   459 days, 1 hour, 15 minutes, 44 seconds

1      Online   459 days, 1 hour, 15 minutes, 44 seconds

2      Online   459 days, 1 hour, 15 minutes, 44 seconds

3      Online   459 days, 1 hour, 15 minutes, 44 seconds

<span style="background-color: #ffaaaa">4      Offline  </span>

<span style="background-color: #ffaaaa">5      Offline  </span>

<span style="background-color: #ffaaaa">6      Offline  </span>

<span style="background-color: #ffaaaa">7      Offline  </span>

Note: For extended summary, use

       show chassis fabric summary extended

{master}

vietpn@ME_AR03.MAP018_RE0> show chassis alarms

2 alarms currently active

Alarm time               Class  Description

<span style="background-color: #ffaaaa">2021-03-18 17:38:45 CAT  Minor  CB 1 Fabric Chip 1 Not Online</span>

<span style="background-color: #ffaaaa">2021-03-18 17:38:44 CAT  Minor  CB 1 Fabric Chip 0 Not Online</span>

* *Kiểm tra các case cũ, google với alarm phát sinh**

- Ghi nhận <span style="background-color: #ffaaaa">giống case </span><span style="background-color: #ffaaaa">SR-2021-1201-0922</span>
    - <span style="background-color: #ffaaaa">Hướng xử lý: restart lại CB1</span>

* *Xử lý trên thiết bị**

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

- Tiến hành reseat CB1 >>> KB [https://kb.juniper.net/InfoCenter/index?page=content&id=KB23067&actp=METADATA](https://kb.juniper.net/InfoCenter/index?page=content&id=KB23067&actp=METADATA)

### Kiểm tra trạng thái RE1

###### Đảm bảo RE1 đang ở trạng thái Backup vì mình sẽ tác động vào SCB slot 1, dẫn tới tác  động trên RE1.

{master}

> <span style="background-color: #ffaaaa">show chassis routing-engine | match "Slot|State|Start"</span>

Dec 15 00:47:05

  Slot 0:

    Current state                  Master

    Start time                     2020-09-11 23:31:07 CAT

<span style="background-color: #ffaaaa">  Slot 1:</span>

<span style="background-color: #ffaaaa">    Current state                  Backup</span>

<span style="background-color: #ffaaaa">    Start time                     2020-09-11 23:20:51 CAT</span>

### Thực hiện offline RE1

###### Đứng trên RE0, offline RE1 bằng lệnh:

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">> request system power-off other-routing-engine</span></span>

###### Kiểm tra RE1 đã offline

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">> show chassis routing-engine | match "Slot|State|Start"</span></span>

  Slot 0:

    Current state                  Master

    Start time                     2020-09-11 23:31:07 CAT

<span style="background-color: #ffaaaa">  Slot 1:</span>

<span style="background-color: #ffaaaa">    Current state                  Present</span>

### Thực hiện offline CB1

###### Offline CB1 bằng lệnh:

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">> request chassis cb offline slot 1</span></span>

###### Xác nhận CB1 ở trạng thái offline

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">> show chassis environment cb | match "CB|State"</span></span>

CB 0 status:

  State                      Online Master

CB 1 status:

  State                      Offline

###### Kiểm tra trạng thái các fabric plane

<span style="background-color: #ffaaaa">> show chassis fabric summary </span><span style="background-color: #ffaaaa">extended</span>

0      Online     NO     NO        NO/  NO         459 days, 1 hour, 17 minutes, 20 seconds

1      Online     NO     NO        NO/  NO         459 days, 1 hour, 17 minutes, 20 seconds

2      Online     NO     NO        NO/  NO         459 days, 1 hour, 17 minutes, 20 seconds

3      Online     NO     NO        NO/  NO         459 days, 1 hour, 17 minutes, 20 seconds

4      Offline

5      Offline

6      Offline

7      Offline

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">>>> Sau khi Offline CB1 và RE1 thì cảnh báo vẫn chưa clear.</span></span>

### Thực hiện online CB1 bằng lệnh

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">> request chassis cb online slot 1</span></span>

<span style="background-color: #ffaaaa">**>>> Sau khi CB1 online trở lại thì cảnh báo liên quan CB1 đã được clear**</span>

vietpn@ME_AR03.MAP018_RE0> show chassis alarms

Dec 15 01:01:15

No alarms currently active

<span style="background-color: #ffaaaa">**### Kiểm tra trạng thái đồng bộ trên RE1 đã được đồng bộ, quá trình thực hiện không ghi nhận phát sinh ngoài dự kiến**</span>

* *Kết quả xử lý trên thiết bị**

- Xử lý ngày 15/12:
    - Sau khi thực hiện OFF/ON lại CB1 thì cảnh báo đã được clear
