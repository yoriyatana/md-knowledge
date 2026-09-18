# SR-2021-1125-1639 - MVT/ HĐ SLA 03/2020/ Hỗ trợ kiểm tra cảnh báo lỗi FPC1 trên MAN057

---

**Phát sinh 1: alarm FPC1 trên MAN057**

---

**Ghi nhận ban đầu**

- Trên ME_PR02.MAN057 phát sinh cảnh báo lỗi FPC1:
    - <span style="background-color: #ffaaaa">2021-08-28 16:31:19 CAT  Major  FPC 1 Major Errors - MQ Chip Error code: 0x3000b</span>

---

**Các bước xử lý**

---

**Kiểm tra sơ bộ**

- IP MNS thiết bị <span style="background-color: #ffaaaa">10.250.28.38</span>
- Check S/N thiết bị

|CAEA0988|N/A|MX-MPC1E-3D|12-May-2016|0068213416|01-Sep-2020|04-Mar-2022| Active|PAR-RTF-MX-MPC1-3D|
|--------|---|-----------|-----------|----------|-----------|-----------|-------|------------------|

- Check S/N thiết bị
    - Health check thiết bị dựa trên RSI
        - CPU (12%), MEM(8%), TEMP (45C) không có bất thường, system boot (441 ngày)

```
Mem: 117M Active, 2503M Inact, 829M Wired, 1634M Buf, 12G Free
```

```
PID USERNAME PRI NICE   SIZE    RES STATE   C   TIME    WCPU COMMAND
   10 root     155 ki31     0K    64K CPU3    3    ??? 100.00% idle{idle: cpu3}
   10 root     155 ki31     0K    64K CPU2    2    ??? 100.00% idle{idle: cpu2}
   10 root     155 ki31     0K    64K CPU1    1    ???  99.37% idle{idle: cpu1}
   10 root     155 ki31     0K    64K RUN     0    ???  98.00% idle{idle: cpu0}
12965 root      23    0   825M 49288K select  0 491.1H   5.37% chassisd{chassisd}
43820 root      25    0   769M 51736K select  0   0:00   1.76% cli
13683 root      21    0  1287M   341M kqread  3  83.8H   1.56% rpd{rsvp-io}
43821 root      52    0   752M 33236K select  1   0:00   0.98% mgd
```

        - show pfe statistics error: có couter khác 0

```
Slot 1

HSL2 Errors:
------------
  *****  No errors on this PFE  *****
LU Chip 0
LUCHIP(0) ISTAT PIO Errors:
    None recorded.
MQ Chip 0

WI Error Counters:
  xge traffic overflow           : 0
  wrong pkt dlmtr in dq pipeline : 0

FI Error Counters:
  stream counters(mask 0 match 0):
    cell_timeout             : 0
    err_cell                 : 7
    late_cell                : 0
    chunk_empty              : 0
    ptuse_drops              : 0
    eng_underflow            : 0
    pt_pkt_errors            : 7
  misc counters:
    input_port_0_overflow    : 0
    input_port_1_overflow    : 0
    input_port_2_overflow    : 0
    input_port_3_overflow    : 0
    input_port_0_rg_overflow : 0
    input_port_1_rg_overflow : 0
    input_port_2_rg_overflow : 0
    input_port_3_rg_overflow : 0
    l1_empty                 : 0
    l2_empty                 : 0
    cp_empty                 : 0
IXCHIP 0 Ingress Buffer Mgr Errors:

               Counter Name            Total           Rate      Peak Rate
   ------------------------ ---------------- -------------- --------------
          Tail Drop Pkt Cnt                0              0              0
       Pkt LinkRAM PERR Cnt                0              0              0
       Ctl DataRAM PERR Cnt                0              0              0
      Cell LinkRAM PERR Cnt                0              0              0
      ENQ PERR Drop Pkt Cnt                0              0              0

IXCHIP 2 Ingress Buffer Mgr Errors:

               Counter Name            Total           Rate      Peak Rate
   ------------------------ ---------------- -------------- --------------
          Tail Drop Pkt Cnt                0              0              0
       Pkt LinkRAM PERR Cnt                0              0              0
       Ctl DataRAM PERR Cnt                0              0              0
      Cell LinkRAM PERR Cnt                0              0              0
      ENQ PERR Drop Pkt Cnt                0              0              0

IXCHIP 0 Egress Buffer Mgr Errors:

               Counter Name            Total           Rate      Peak Rate
   ------------------------ ---------------- -------------- --------------
          Tail Drop Pkt Cnt                0              0              0
          EOPE Drop Pkt Cnt             6969              0             14
       Ctl DataRAM PERR Cnt                0              0              0
      Cell LinkRAM PERR Cnt                0              0              0
      ENQ PERR Drop Pkt Cnt                0              0              0

IXCHIP 2 Egress Buffer Mgr Errors:

               Counter Name            Total           Rate      Peak Rate
   ------------------------ ---------------- -------------- --------------
          Tail Drop Pkt Cnt                0              0              0
          EOPE Drop Pkt Cnt             3117              0            737
       Ctl DataRAM PERR Cnt                0              0              0
      Cell LinkRAM PERR Cnt                0              0              0
      ENQ PERR Drop Pkt Cnt                0              0              0
```

        - Health check show pfe statistics traffic

```
Packet Forwarding Engine traffic statistics:
    Input  packets:       70428609268567              2906017 pps
    Output packets:       70431739233169              2913732 pps
    Fabric Input  :       22292081509363              1908271 pps
    Fabric Output :       22292081468778              1899527 pps
Packet Forwarding Engine local traffic statistics:
    Local packets input                 :           2784096569
    Local packets output                :           4938487014
    Software input control plane drops  :                    0
    Software input high drops           :                    0
    Software input medium drops         :                    0
    Software input low drops            :                    0
    Software output drops               :                    0
    Hardware input drops                :                 4862
Packet Forwarding Engine local protocol statistics:
    HDLC keepalives            :                    0
    ATM OAM                    :                    0
    Frame Relay LMI            :                    0
    PPP LCP/NCP                :                    0
    OSPF hello                 :             16654638
    OSPF3 hello                :                    0
    RSVP hello                 :             58183658
    LDP hello                  :             59585528
    BFD                        :             14335979
    IS-IS IIH                  :                    0
    LACP                       :            207627563
    ARP                        :               133079
    ETHER OAM                  :                    0
    Unknown                    :                  184
Packet Forwarding Engine hardware discard statistics:
    Timeout                    :                    0
    Truncated key              :                    0
    Bits to test               :                    0
    Data error                 :                    0
    TCP header length error    :                    0
    Stack underflow            :                    0
    Stack overflow             :                    0
    Normal discard             :           2935930690
    Extended discard           :                    0
    Invalid interface          :                    0
    Info cell drops            :                    0
    Fabric drops               :                    0
Packet Forwarding Engine Input IPv4 Header Checksum Error and Output MTU Error statistics:
    Input Checksum             :                    0
    Output MTU                 :                    0
```

        - Health check show system storage no-forwarding  <<< còn trống 6,7G

```
Filesystem              Size       Used      Avail  Capacity   Mounted on
/dev/md0.uzip            21M        21M         0B      100%  /
devfs                   1.0K       1.0K         0B      100%  /dev
/dev/gpt/junos           19G        11G       6.7G       62%  /.mount
```

        - show version detail no-forwarding

```
Hostname: ME_PR02.MAN057_RE0
Model: mx480
Junos: 17.3R3-S8.1
```

        - Không phát sinh core-dump
        - Show chasssis fpc detail

```
Slot 1 information:
  State                               Online
  Temperature                      40 degrees C / 104 degrees F
  Total CPU DRAM                 2048 MB
  Total RLDRAM                    331 MB
  Total DDR DRAM                 1536 MB
  Start time                          2020-09-09 22:51:24 CAT
  Uptime                              441 days, 11 hours, 58 minutes, 45 seconds
  Max power consumption            227 Watts
```

        - Thiết bị route ít

```
show route summary

Autonomous system number: 37342
Router ID: 10.250.92.38

inet.0: 2118 destinations, 2435 routes (2114 active, 0 holddown, 4 hidden)
              Direct:      8 routes,      7 active
               Local:      6 routes,      6 active
                OSPF:   1774 routes,   1774 active
                 BGP:    642 routes,    325 active
                RSVP:      4 routes,      1 active
                 LDP:      1 routes,      1 active
```

        - Log chassisd ngày phát sinh alarm

```
{master}
icinga@ME_PR02.MAN057_RE0> show log chassisd.1.gz | find "Aug 28"
Aug 28 15:47:25  ch_gencfg_chassis_startup_time_blob_set: Adding blob for chassis startup time for key aaaaaaaa keylen 4 , 1599684267.207564, blob pointer a172d50
Aug 28 15:47:25  ch_gencfg_update_startup_time_blob: Updated hw.chassis.startup_time to 1599684267.207564 (RE)
Aug 28 15:47:25  ch_gencfg_chassis_startup_time_handler: master_re: true, GENCFG_CHASSIS_STARTUP_TIME, minor_type: 8
Aug 28 16:31:19  send: red alarm set, device FPC 1, reason FPC 1 Major Errors - MQ Chip Error code: 0x3000b
Aug 28 16:47:24  ch_gencfg_chassis_startup_time_blob_set: chassis startup time set in kernel 1599684267.207560
Aug 28 16:47:24  ch_gencfg_chassis_startup_time_blob_set: Adding blob for chassis startup time for key aaaaaaaa keylen 4 , 1599684267.207560, blob pointer a172d50
Aug 28 16:47:24  ch_gencfg_update_startup_time_blob: Updated hw.chassis.startup_time to 1599684267.207560 (RE)
Aug 28 16:47:25  ch_gencfg_chassis_startup_time_handler: master_re: true, GENCFG_CHASSIS_STARTUP_TIME, minor_type: 8
```

        - <span style="background-color: #ffaaaa">Log messages bị trôi</span>
        - <span style="background-color: #ffaaaa">Log interactive-commands bị trôi</span>
        - <span style="background-color: #ffaaaa">log messages trên FPC1 cũng bị trôi</span>

**Kiểm tra các case cũ, google với alarm phát sinh**

- Tìm theo alarm phát sinh thì có KB gần giống:
    - [https://kb.juniper.net/InfoCenter/index?page=content&id=KB35989&actp=METADATA](https://kb.juniper.net/InfoCenter/index?page=content&id=KB35989&actp=METADATA)
- Tìm trên case cũ thì không có case tương tự

**Mở case với TAC**

```
Movitel | MX480 |  ME_PR02.MAN057 | 17.3R3-S8.1 | Major  FPC 1 Major Errors - MQ Chip Error code: 0x3000b
----
S/N to open case
CAEA0988
----
Hi JTAC,

Our customer observed the "FPC 1 Major Errors - MQ Chip Error code: 0x3000b" alarm raised long time ago.

root@ME_PR02.MAN057_RE0> show chassis alarms no-forwarding

2 alarms currently active
Alarm time               Class  Description
2021-10-30 01:03:21 CAT  Minor  PEM 2 Fan Failed
2021-08-28 16:31:19 CAT  Major  FPC 1 Major Errors - MQ Chip Error code: 0x3000b

We found a KB with symtoms is similar to this alarm. https://kb.juniper.net/InfoCenter/index?page=content&id=KB35989&actp=METADATA&act=login

Please help us check if KB matching to this case and guide us to clear it.

I uploaded the varlog, rsi and some command outputs as below:

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
request pfe execute command "show syslog messages" target fpc1
request pfe execute command "show nvram" target fpc1
request pfe execute command "show ttp statistics" target fpc1
request pfe execute command "show hsl2 statistics" target fpc1
request pfe execute command "show hsl2 statistics crc" target fpc1
request pfe execute command "show cmerror module" target fpc1
request pfe execute command "show sched" target fpc1
request pfe execute command "show threads cpu" target fpc1
request pfe execute command "show jnh 0 exceptions" target fpc1

request pfe execute command "show hsl2 statistics" target fpc1
request pfe execute command "show cmerror level" target fpc1
request pfe execute command "show cmerror module brief" target fpc1
request pfe execute command "show cmerror module 6 " target fpc1
request pfe execute command "show cmerror statistics" target fpc1
request pfe execute command "show syslog messages" target fpc1
request pfe execute command "show nvram" target fpc1

```

- TAC xác nhận case matching mô tả lỗi trong  [KB35989](https://kb.juniper.net/InfoCenter/index?page=content&id=KB35989&actp=METADATA&act=login)
    - Phương án xử lý dùng lệnh ẩn để clear lỗi
    - Nếu vẫn phát sinh thì thực hiện restart lại FPC

**Cập nhật kết quả xử lý cho khách hàng**

- Phản hồi kết quả xử lý cho khách hàng

**Xử lý trên thiết bị**

- khách hàng đã thực hiện action (1) dùng lệnh ẩn để clear lỗi và cảnh báo đã mất (30/11) -> theo dõi hết tuần
