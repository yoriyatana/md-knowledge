# SR-2021-1215-1001 - Hỗ trợ xử lý case cảnh báo trên thiết bị AR01.NIA088 copy

- --

Phát sinh: alarm CB1 trên AR01.NIA088

- --

Ghi nhận ban đầu

- Trên AR01.NIA088 phát sinh các cảnh báo lỗi:

{master}

vietpn@AR01.NIA088\_RE0> show chassis alarms

2 alarms currently active

Alarm time               Class  Description

2021-01-28 13:06:39 CAT  Minor  CB 1 Fabric Chip 1 Not Online

2021-01-28 13:06:38 CAT  Minor  CB 1 Fabric Chip 0 Not Online

- --

Các bước xử lý

- --

Kiểm tra sơ bộ

- IP MNS thiết bị 10.250.28.41
- Cảnh báo phát sinh giống lỗi trên thiết bị ME\_PR01.GAZ020 (case ID SR-2021-1201-0922).
- Health check thiết bị

- CPU (2%), MEM(8%), TEMP (35C) không có bất thường, system boot (466 ngày)

{master}

[vietpn@AR01.NIA](mailto:vietpn@AR01.NIA)088\_RE0> show chassis routing-engine no-forwarding

Routing Engine status:

Slot 0:

```text
Current state                  Master
```

Election priority              Master

Temperature                 33 degrees C / 91 degrees F

CPU temperature             30 degrees C / 86 degrees F

DRAM                      32713 MB (32768 MB installed)

Memory utilization           8 percent

5 sec CPU utilization:

User                       0 percent

Background                 0 percent

Kernel                     1 percent

Interrupt                  0 percent

Idle                      98 percent

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

Serial ID                      9016065507

Start time                     2020-09-04 23:25:59 CAT

Uptime                         466 days, 43 minutes

Last reboot reason             Router rebooted after a normal shutdown.

```text
Load averages:                 1 minute   5 minute  15 minute
```

0. 31       0.28       0.25

Routing Engine status:

Slot 1:

```text
Current state                  Backup
```

Election priority              Backup

Temperature                 32 degrees C / 89 degrees F

CPU temperature             30 degrees C / 86 degrees F

DRAM                      32713 MB (32768 MB installed)

Memory utilization           9 percent

5 sec CPU utilization:

User                       0 percent

Background                 0 percent

Kernel                     0 percent

Interrupt                  0 percent

Idle                     100 percent

Model                          RE-S-1800x4

Serial ID                      9016065286

Start time                     2020-09-04 23:15:28 CAT

Uptime                         466 days, 53 minutes, 20 seconds

Last reboot reason             Router rebooted after a normal shutdown.

```text
Load averages:                 1 minute   5 minute  15 minute
```

0. 16       0.19       0.16

- Không có process chiếm CPU

{master}

[vietpn@AR01.NIA](mailto:vietpn@AR01.NIA)088\_RE0> show system processes extensive no-forwarding

last pid: 88761;  load averages:  0.26,  0.27,  0.25  up 466+00:43:31    00:09:30

237 processes: 5 running, 202 sleeping, 30 waiting

```text
Mem: 94M Active, 6567M Inact, 1684M Wired, 1675M Buf, 23G Free
```

```text
Swap: 8192M Total, 8192M Free
```

```text
PID USERNAME PRI NICE   SIZE    RES STATE   C   TIME    WCPU COMMAND
```

10 root     155 ki31     0K    64K CPU1    1    ??? 100.00% idle{idle: cpu1}

10 root     155 ki31     0K    64K CPU3    3    ??? 100.00% idle{idle: cpu3}

10 root     155 ki31     0K    64K CPU2    2    ??? 100.00% idle{idle: cpu2}

10 root     155 ki31     0K    64K RUN     0    ??? 100.00% idle{idle: cpu0}

16705 root       4    0   825M 48640K select  3 467.9H   3.96% chassisd{chassisd}

17094 root      20    0   806M 17020K select  0 857:11   0.20% repd{repd}

16738 root      20    0  1467M   532M kqread  3  46.7H   0.00% rpd{rpd}

- Health check show system storage no-forwarding  <<< còn trống 7.8G

{master}

[vietpn@AR01.NIA](mailto:vietpn@AR01.NIA)088\_RE0> show system storage no-forwarding

Filesystem              Size       Used      Avail  Capacity   Mounted on

/dev/md0.uzip            21M        21M         0B      100%  /

devfs                   1.0K       1.0K         0B      100%  /dev

/dev/gpt/junos           19G       9.8G       7.8G       56%  /.mount

```text
show version detail no-forwarding
```

{master}

[vietpn@AR01.NIA](mailto:vietpn@AR01.NIA)088\_RE0> show version invoke-on all-routing-engines | match "re0|re1|Junos:"

re0:

- -------------------------------------------------------------------------

Hostname: AR01.NIA088\_RE0

```text
Junos: 17.3R3-S8.1
```

re1:

- -------------------------------------------------------------------------

Hostname: AR01.NIA088\_RE1

```text
Junos: 17.3R3-S8.1
```

- Không phát sinh core-dump

{master}

[vietpn@AR01.NIA](mailto:vietpn@AR01.NIA)088\_RE0> show system core-dumps

- rw-r--r--  1 root  wheel   50787532 Aug 25  2020 /var/crash/core-NPC0.gz.core.0

/var/tmp/\*core\*: No such file or directory

/var/tmp/pics/\*core\*: No such file or directory

/var/crash/kernel.\*: No such file or directory

/var/jails/rest-api/tmp/\*core\*: No such file or directory

/tftpboot/corefiles/\*core\*: No such file or directory

total files: 1

```text
Show system resource-monitor fpc <<< không bất tường
```

{master}

[vietpn@AR01.NIA](mailto:vietpn@AR01.NIA)088\_RE0> show system resource-monitor fpc

FPC Resource Usage Summary

Free Heap Mem Watermark         : 20  %

Free NH Mem Watermark           : 20  %

Free Filter Mem Watermark       : 20  %

\* - Watermark reached

Heap            Avg                   ENCAP mem       NH mem          FW mem

Slot #         % Free       RTT  RTT        PFE #        % Free       % Free          % Free

0             90       --     --(--)      0            NA          88              99

1             89       --     --(--)      0            NA          88              99

```text
show route summary <<< route không nhiều
```

{master}

[vietpn@AR01.NIA](mailto:vietpn@AR01.NIA)088\_RE0> show route summary

Autonomous system number: 37342

Router ID: 10.250.92.41

```text
inet.0: 2945 destinations, 3949 routes (2940 active, 0 holddown, 5 hidden)
```

```text
Direct:     13 routes,     12 active
```

```text
Local:     14 routes,     14 active
```

```text
OSPF:   1885 routes,   1885 active
```

```text
BGP:   2032 routes,   1028 active
```

```text
RSVP:      4 routes,      0 active
```

```text
LDP:      1 routes,      1 active
```

- Log messages <<< không có log lạ
- Log interactive-commands <<< chưa check
- Log chassisd <<< chưa check

Thu thập các thông tin liên quan

```text
request support information | no-more | save /var/log/RSI\_AR01.NIA088\_20211215
```

```text
file archive source /var/log/\* destination /var/log/LOG\_AR01.NIA088\_20211215
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

{master}

```text
[vietpn@AR01.NIA](mailto:vietpn@AR01.NIA)088\_RE0> show chassis environment cb | match "CB|State"
```

CB 0 status:

```text
State                      Online Master
```

CB 1 status:

```text
State                      Online Standby
```

{master}

[vietpn@AR01.NIA](mailto:vietpn@AR01.NIA)088\_RE0> show chassis fabric summary | no-more

```text
Plane   State    Uptime
```

0      Online   465 days, 23 hours, 45 minutes, 37 seconds

1      Online   465 days, 23 hours, 45 minutes, 37 seconds

2      Online   465 days, 23 hours, 45 minutes, 37 seconds

3      Online   465 days, 23 hours, 45 minutes, 37 seconds

4      Offline

5      Offline

6      Offline

7      Offline

Note: For extended summary, use

```text
show chassis fabric summary extended
```

{master}

[vietpn@AR01.NIA](mailto:vietpn@AR01.NIA)088\_RE0> show chassis alarms

2 alarms currently active

Alarm time               Class  Description

2021-01-28 13:06:39 CAT  Minor  CB 1 Fabric Chip 1 Not Online

2021-01-28 13:06:38 CAT  Minor  CB 1 Fabric Chip 0 Not Online

Kiểm tra các case cũ, google với alarm phát sinh

- Ghi nhận giống case SR-2021-1201-0922

- Hướng xử lý: restart lại CB1

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

- Tiến hành reseat CB1 >>> KB <https://kb.juniper.net/InfoCenter/index?page=content&id=KB23067&actp=METADATA>

### Kiểm tra trạng thái RE1

###### Đảm bảo RE1 đang ở trạng thái Backup vì mình sẽ tác động vào SCB slot 1, dẫn tới tác  động trên RE1.

{master}

```text
[vietpn@AR01.NIA](mailto:vietpn@AR01.NIA)088\_RE0> show chassis routing-engine | match "Slot|State|Start"
```

Dec 15 00:26:27

Slot 0:

```text
Current state                  Master
```

Start time                     2020-09-04 23:25:59 CAT

Slot 1:

```text
Current state                  Backup
```

Start time                     2020-09-04 23:15:28 CAT

### Thực hiện offline RE1

###### Đứng trên RE0, offline RE1 bằng lệnh:

```text
> request system power-off other-routing-engine
```

###### Kiểm tra RE1 đã offline

```text
> show chassis routing-engine | match "Slot|State|Start"
```

Slot 0:

```text
Current state                  Master
```

Start time                     2020-09-04 23:25:59 CAT

Slot 1:

```text
Current state                  Present
```

### Thực hiện offline CB1

###### Offline CB1 bằng lệnh:

```text
> request chassis cb offline slot 1
```

###### Xác nhận CB1 ở trạng thái offline

```text
> show chassis environment cb | match "CB|State"
```

CB 0 status:

```text
State                      Online Master
```

CB 1 status:

```text
State                      Offline
```

###### Kiểm tra trạng thái các fabric plane

```text
> show chassis fabric summary extended
```

0      Online     NO     NO        NO/  NO         465 days, 23 hours, 47 minutes, 47 seconds

1      Online     NO     NO        NO/  NO         465 days, 23 hours, 47 minutes, 47 seconds

2      Online     NO     NO        NO/  NO         465 days, 23 hours, 47 minutes, 47 seconds

3      Online     NO     NO        NO/  NO         465 days, 23 hours, 47 minutes, 47 seconds

4      Offline

5      Offline

6      Offline

7      Offline

```text
>>> Sau khi Offline CB1 và RE1 thì cảnh báo vẫn chưa clear.
```

### Thực hiện online CB1 bằng lệnh

```text
> request chassis cb online slot 1
```

```text
>>> Sau khi CB1 online trở lại thì cảnh báo liên quan CB1 đã được clear
```

[vietpn@AR01.NIA](mailto:vietpn@AR01.NIA)088\_RE0> show system alarms

Dec 15 00:32:19

No alarms currently active

### Kiểm tra trạng thái đồng bộ trên RE1 đã được đồng bộ, quá trình thực hiện không ghi nhận phát sinh ngoài dự kiến

Kết quả xử lý trên thiết bị

- Xử lý ngày 15/12:

- Sau khi thực hiện OFF/ON lại CB1 thì cảnh báo đã được clear
