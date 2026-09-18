# - MVT/ HĐ 03-2020/ Hỗ trợ xử lý lỗi box PR02.TET040

---

**Phát sinh 1: alarm CB1 trên�**�**PR02.TET040**

---

**Ghi nhận ban đầu**

- Trên PR02.TET040 phát sinh các cảnh báo lỗi:

```
icinga@PR02.TET040_RE0> show chassis alarms       
1 alarms currently active
Alarm time               Class  Description
2020-11-28 10:09:11 CAT  Major  FPC 1 Major Errors - HSL2 Error code: 0x200001
```

---

**Các bước xử lý**

---

**Kiểm tra sơ bộ**

- IP MNS thiết bị <span style="background-color: #ffaaaa">**10.250.28.36**</span>
- Check S/N thiết bị
    - <span style="background-color: #ffaaaa">**>>> Tất cả các S/N hết services**</span>
- Health check thiết bị dựa trên RSI
    - CPU (2%), MEM(8%), TEMP (35C) không có bất thường, system boot (93 ngày)

```
{master}
vietpn@PR02.TET040_RE0> show chassis routing-engine
Routing Engine status:
  Slot 0:
    Current state                  Master
    Election priority              Master
    Temperature                 43 degrees C / 109 degrees F
    CPU temperature             40 degrees C / 104 degrees F
    DRAM                      16329 MB (16384 MB installed)
    Memory utilization           8 percent
    5 sec CPU utilization:
      User                       0 percent
      Background                 0 percent
      Kernel                     2 percent
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
    Serial ID                      9009219380
    Start time                     2020-09-09 01:20:08 CAT
    Uptime                         468 days, 22 hours, 53 minutes, 46 seconds
    Last reboot reason             Router rebooted after a normal shutdown.
    Load averages:                 1 minute   5 minute  15 minute
                                       0.17       0.20       0.21
Routing Engine status:
  Slot 1:
    Current state                  Backup
    Election priority              Backup
    Temperature                 42 degrees C / 107 degrees F
    CPU temperature             39 degrees C / 102 degrees F
    DRAM                      16329 MB (16384 MB installed)
    Memory utilization           7 percent
    5 sec CPU utilization:
      User                       0 percent
      Background                 0 percent
      Kernel                     0 percent
      Interrupt                  0 percent
      Idle                     100 percent
    Model                          RE-S-1800x4
    Serial ID                      9013084966
    Start time                     2020-09-09 01:09:57 CAT
    Uptime                         468 days, 23 hours, 3 minutes, 43 seconds
    Last reboot reason             Router rebooted after a normal shutdown.
    Load averages:                 1 minute   5 minute  15 minute
                                       0.20       0.20       0.17
```

    - Không có process chiếm CPU

```
vietpn@PR02.TET040_RE0> show system processes extensive
Dec 22 00:15:23
last pid: 20561;  load averages:  0.31,  0.23,  0.22  up 468+22:55:15    00:15:23
233 processes: 5 running, 198 sleeping, 30 waiting

Mem: 68M Active, 2350M Inact, 911M Wired, 1674M Buf, 12G Free
Swap: 8192M Total, 8192M Free

  PID USERNAME PRI NICE   SIZE    RES STATE   C   TIME    WCPU COMMAND
   10 root     155 ki31     0K    64K CPU1    1    ??? 100.00% idle{idle: cpu1}
   10 root     155 ki31     0K    64K CPU3    3    ??? 100.00% idle{idle: cpu3}
   10 root     155 ki31     0K    64K CPU2    2    ??? 100.00% idle{idle: cpu2}
   10 root     155 ki31     0K    64K RUN     0    ??? 100.00% idle{idle: cpu0}
13511 root      21    0   825M 48092K select  3 509.8H   3.66% chassisd{chassisd}
   11 root     -72    -     0K   480K WAIT    2  27.3H   0.00% intr{swi1: netisr 0}
14214 root      20    0  1191M   253M kqread  0  23.8H   0.00% rpd{rpd}
13549 root      20    0   725M 11064K select  0  21.9H   0.00% clksyncd
14468 root      20    0   767M 15712K select  2  17.8H   0.00% repd{repd}
   11 root     -60    -     0K   480K WAIT    0 928:38   0.00% intr{swi4: clock}
14460 root      20    0   793M 43576K select  1 881:42   0.00% mib2d
```

- Health check show system storage no-forwarding  <<< còn trống 6,9G

```
vietpn@PR02.TET040_RE0> show system storage
Dec 22 00:16:05
Filesystem              Size       Used      Avail  Capacity   Mounted on
/dev/md0.uzip            21M        21M         0B      100%  /
devfs                   1.0K       1.0K         0B      100%  /dev
/dev/gpt/junos           19G       8.9G       8.7G       51%  /.mount
```

        - show version detail no-forwarding

```
{master}
vietpn@PR02.TET040_RE0> show version invoke-on all-routing-engines | match "re0|re1|junos:"   
re0:
--------------------------------------------------------------------------
Hostname: PR02.TET040_RE0
Junos: 17.3R3-S8.1
re1:
--------------------------------------------------------------------------
Hostname: PR02.TET040_RE1
Junos: 17.3R3-S8.1
```

- Không phát sinh core-dump

```
{master}
vietpn@PR02.TET040_RE0> show system core-dumps
Dec 22 00:18:07
-rw-r--r--  1 root  wheel   48444566 Nov 28  2020 /var/crash/core-NPC0.gz.core.0
-rw-------  1 root  wheel    3254579 Dec 25  2017 /var/tmp/chassisd.core.0.gz
/var/tmp/pics/*core*: No such file or directory
/var/crash/kernel.*: No such file or directory
/var/jails/rest-api/tmp/*core*: No such file or directory
/tftpboot/corefiles/*core*: No such file or directory
total files: 2
```

- Show chasssis fpc detail <<< không bất tường

```
root@ME_PR01.GAZ020_RE0> show chassis fpc detail

Slot 0 information:
  State                               Online
  Temperature                      32 degrees C / 89 degrees F
  Total CPU DRAM                 2048 MB
  Total RLDRAM                    331 MB
  Total DDR DRAM                 1536 MB
  Start time                          2021-10-29 01:06:18 CAT
  Uptime                              33 days, 3 hours, 28 minutes, 37 seconds
  Max power consumption            227 Watts
Slot 1 information:
  State                               Online
  Temperature                      31 degrees C / 87 degrees F
  Total CPU DRAM                 2048 MB
  Total RLDRAM                    331 MB
  Total DDR DRAM                 1536 MB
  Start time                          2021-10-29 01:06:09 CAT
  Uptime                              33 days, 3 hours, 28 minutes, 46 seconds
  Max power consumption            227 Watts
Slot 2 information:
  State                               Online
  Temperature                      31 degrees C / 87 degrees F
  Total CPU DRAM                 2048 MB
  Total RLDRAM                    331 MB
  Total DDR DRAM                 1536 MB
  Start time                          2021-10-29 01:06:12 CAT
  Uptime                              33 days, 3 hours, 28 minutes, 43 seconds
  Max power consumption            227 Watts
Slot 3 information:
  State                               Online
  Temperature                      31 degrees C / 87 degrees F
  Total CPU DRAM                 2048 MB
  Total RLDRAM                    331 MB
  Total DDR DRAM                 1536 MB
  Start time                          2021-10-29 01:06:16 CAT
  Uptime                              33 days, 3 hours, 28 minutes, 39 seconds
  Max power consumption            227 Watts
Slot 4 information:
  State                               Online
  Temperature                      31 degrees C / 87 degrees F
  Total CPU DRAM                 2048 MB
  Total RLDRAM                    331 MB
  Total DDR DRAM                 1536 MB
  Start time                          2021-10-29 01:06:06 CAT
  Uptime                              33 days, 3 hours, 28 minutes, 49 seconds
  Max power consumption            227 Watts
```

- show route summary <<< route không nhiều

```
root@ME_PR01.GAZ020_RE0> show route summary

Autonomous system number: 37342
Router ID: 10.250.64.5

inet.0: 2245 destinations, 2566 routes (2238 active, 0 holddown, 7 hidden)
              Direct:     24 routes,     24 active
               Local:     24 routes,     24 active
                OSPF:   1835 routes,   1831 active
                 BGP:    674 routes,    357 active
                RSVP:      8 routes,      1 active
                 LDP:      1 routes,      1 active
```

- <span style="background-color: #ffaaaa">Log messages bị trôi</span>
- <span style="background-color: #ffaaaa">Log interactive-commands <<< chưa check</span>
- <span style="background-color: #ffaaaa">Log chassisd <<< chưa check</span>

**Thu thập các thông tin liên quan**

```
request support information | no-more | save /var/log/RSI_PR02.TET040_20211222
file archive source /var/log/* destination /var/log/LOG_PR02.TET040_20211222
```

```
> show version invoke-on all-routing-engines | match "re0|re1|Junos:"

> show chassis alarms
> show system alarms
> show system core-dumps

> show chassis routing-engine | no-more
> show chassis routing-engine | match "Slot|State|Start"

show chassis environment cb | no-more
show chassis environment cb | match "CB|State"

show log messages | no-more
show log messages.0.gz  | no-more
show log messages.1.gz | no-more
show log messages.2.gz | no-more
show log messages.3.gz | no-more

show log chassisd | no-more
show log chassisd .0.gz | no-more
show log chassisd.1.gz | no-more
show log chassisd.2.gz | no-more
show log chassisd.3.gz | no-more

##Regarding to FPC
show chassis hardware | no-more
show chassis alarm
show version
show chassis fpc | no-more
show chassis fpc pic-status | no-more
show chassis fpc errors | no-more
show chassis fabric fpcs  | no-more
show chassis fabric plane  | no-more
show chassis fabric summary  | no-more
show chassis fabric map | no-more
show chassis fabric plane-location | no-more
show chassis fabric destinations | no-more
show system resource-monitor fpc
show pfe statistics traffic  | no-more
show pfe statistics traffic detail  | no-more
show pfe statistics error | no-more

###PFE level information
request pfe execute command "show syslog messages" target fpc1   | no-more
request pfe execute command "show nvram" target fpc1   | no-more
request pfe execute command "show ttp statistics" target fpc1  | no-more
request pfe execute command "show hsl2 statistics" target fpc1  | no-more
request pfe execute command "show hsl2 statistics crc" target fpc1  | no-more
request pfe execute command "show cmerror module" target fpc1  | no-more
request pfe execute command "show sched" target fpc1  | no-more
request pfe execute command "show threads cpu" target fpc1  | no-more
request pfe execute command "show jnh 0 exceptions" target fpc1  | no-more

### show hsl2 statistics
request pfe execute command "show cmerror level" target fpc1  | no-more
request pfe execute command "show cmerror module brief" target fpc1  | no-more
request pfe execute command "show cmerror module <id>" target fpc1 <<<< replace with the id collected from above command where you see the errors
request pfe execute command "show cmerror statistics" target fpc1 | no-more

```

**Kiểm tra các case cũ, google với alarm phát sinh**

- Ghi nhận giống alarm trên dòng EX có case ID <span style="background-color: #ffaaaa">2021-0401-0787</span>
    - <span style="background-color: #ffaaaa">Hướng xử lý:</span>
        - <span style="background-color: #ffaaaa">restart lại FPC có cảnh báo</span>
        - <span style="background-color: #ffaaaa">reseat lại FPC có cảnh báo</span>
        - <span style="background-color: #ffaaaa">Thay thế vật tư dự phòng</span>

**Xử lý trên thiết bị**

- Thu thập baseline

```
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
```

- Tiến hành reseat FPC1

```
### Thực hiện restart lại FPC1
request chassis fpc slot 1 restart

### Sau khi FPC1 restart và online trở lại thì dịch vụ đã phục hồi, không phát sinh ngoài kế hoạch
```

**Kết quả xử lý trên thiết bị**

- Xử lý ngày 22/12:
    - Sau khi thực hiện restart lại FPC1 thì cảnh báo đã được clear >>> Tiếp tục theo dõi xem cảnh báo còn phát sinh trở lại không?
    - Quá trình thực hiện ghi nhận Weathermap theo dõi phát sinh không thu thập đúng thông tin về port, BW trên mạng lưới.
