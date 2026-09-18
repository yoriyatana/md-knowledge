# SR-2021-1225-2235 - MVT/HĐ SLA 03/Xử lý case cảnh báo trên thiết bị ME_AR03.GAZ080

- --

Phát sinh: alarm RE0 trên ME\_AR03.GAZ080

- --

Ghi nhận ban đầu

- Trên ME\_AR03.GAZ080 phát sinh các cảnh báo lỗi:

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show chassis alarms

Dec 25 12:30:03

2 alarms currently active

Alarm time               Class  Description

2021-12-15 07:06:32 CAT  Minor  Loss of communication with Backup RE

2021-12-15 07:06:32 CAT  Minor  Backup RE Active

- Thiết bị chỉ chạy trên RE1:

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show chassis routing-engine | match "slot|state|start"

Dec 25 12:31:12

Slot 0:

Current state                 Present

Slot 1:

Current state                  Master

Start time                     2020-09-14 21:57:52 CAT

- --

Các bước xử lý

- --

Kiểm tra sơ bộ

- IP MNS thiết bị 10.250.0.23
- Check S/N thiết bị

- >>> chưa check

- Health check thiết bị dựa trên RSI

- >>> Chưa check

- Process chiếm CPU >>> chưa check

- Health check show system storage no-forwarding  <<< chưa check

- show version detail no-forwarding

{master}

[vietpn@PR02.TET](mailto:vietpn@PR02.TET)040\_RE0> show version invoke-on all-routing-engines | match "re0|re1|junos:"

re0:

- -------------------------------------------------------------------------

Hostname: PR02.TET040\_RE0

Junos: 17.3R3-S8.1

re1:

- -------------------------------------------------------------------------

Hostname: PR02.TET040\_RE1

Junos: 17.3R3-S8.1

- Không phát sinh core-dump

- Show chasssis fpc detail <<< chưa check

- show route summary <<< chưa check

- Log messages bị trôi, log cuối cùng 13:00 15/12
- Log interactive-commands <<< không có tác động vào thời điểm phát sinh
- Log chassisd <<< chưa check

Thu thập các thông tin liên quan

request support information | no-more | save /var/log/RSI\_ME\_AR03.GAZ080\_20211225

file archive source /var/log/\* destination /var/log/LOG\_ME\_AR03.GAZ080\_20211225

> show version invoke-on all-routing-engines | match "re0|re1|Junos:"

> show chassis alarms

> show system alarms

> show system core-dumps

> show chassis routing-engine | no-more

> show chassis routing-engine | match "Slot|State|Start"

show chassis environment cb | no-more

show chassis environment cb | match "CB|State"

## Regarding to FPC

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

Kiểm tra các case cũ, google với alarm phát sinh

- Chưa kiểm tra

Xử lý trên thiết bị

- Thu thập baseline <<< không thu thập baseline

/\* Lưu thông tin cấu hình và RSI \*/

> set cli timestamp

> show configuration | no-more

> request support information | no-more

/\* Lưu thông tin alarm/core \*/

> show system alarms

> show chassis alarms

> show system core-dumps

/\* Lưu thông tin về IGP \*/

> show ospf interface | no-more

> show ospf interface | count

> show ospf neighbor instance all | no-more

> show ospf3 interface | no-more

> show ospf3 interface | count

> show ospf3 neighbor instance all | no-more

/\* Lưu thông tin về MPLS/LDP/RSVP \*/

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

/\* Lưu thông tin về BGP \*/

> shwo bgp sum | no-more

show bgp summary | match Establ | count

> show bgp neighbor | no-more

> show route summary | no-more

> show bfd session detail | no-more

/\* Lưu thông tin VRRP/L2VPN/VPLS/LLDP/BFD \*/

> show vrrp | no-more

> show l2circuit connections | no-more

> show vpls connections | no-more

> show vpls mac-table | no-more

> show lldp neighbors | no-more

> show bfd session detail | no-more

/\* Lưu thông tin hardware/fabric/fpc \*/

> show chassis hardware | no-more

> show chassis fabric fpcs | no-more

> show chassis fabric summary extended | no-more

> show chassis fabric plane | no-more

/\* Lưu thông tin đồng bộ GRES and NSR - KB32931  \*/

> show system switchover /\* Show on Backup RE – GRES Readiness Check \*/

> show task replication  /\* Show on Master RE – RPD Synchronization Check \*/

> show database-replication summary /\* Show on Master RE – For BNG only \*/

> show system subscriber-management summary

- Tiến hành manual power-on RE0 bằng lệnh

### Thực hiện manual power-on lại RE0

request system power-on other-routing-engine

### Sau khi manual power-on RE0 thì RE0 online trở lại, không phát sinh ngoài kế hoạch

Kết quả xử lý trên thiết bị

- Xử lý ngày 25/12:

- Sau khi thực hiện power-on lại RE0 thì cảnh báo đã được clear, RE0 đã online ở trạng thái Backup >>> Tiếp tục theo dõi tình trạng RE0
- Do máy remote full ổ cứng nên không lưu được log session

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show chassis routing-engine

Dec 25 12:39:29

Slot 0:

Current state                  Backup

Start time                     2021-12-25 12:32:49 CAT

Slot 1:

Current state                  Master

Start time                     2020-09-14 21:57:52 CAT

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show chassis alarms

Dec 25 12:40:03

1 alarms currently active

Alarm time               Class  Description

2021-12-15 07:06:32 CAT  Minor  Backup RE Active

- --

ae1 GAZ009  ---><--- ae11 GAZ080

vietpn@ME\_AR03.GAZ080\_RE1> show configuration interfaces ae11

description "To GAZ009 AE0 - Left ring";

aggregated-ether-options {

link-speed 1g;

lacp {

active;

}

}

unit 0 {

family inet {

address 10.248.35.42/30;

}

family mpls;

}

- --

vietpn@ME\_GAZ009SRT01> show configuration interfaces ae1

description "To AR03.GAZ080 AE21 - Right ring";

aggregated-ether-options {

lacp {

active;

}

}

unit 0 {

family inet {

address 10.248.35.41/30;

}

family mpls;

}

vietpn@ME\_GAZ009SRT01>

- -

vietpn@ME\_AR03.GAZ080\_RE1> show interfaces ge-1/2/1

Physical interface: ge-1/2/1, Administratively down, Physical link is Down

Interface index: 229, SNMP ifIndex: 524

Description: Connect to GAZ009SRT AE1 - Right ring

Link-level type: Ethernet, MTU: 9000, MRU: 9008, LAN-PHY mode, Speed: 1000mbps, BPDU Error: None, Loop Detect PDU Error: None,

Ethernet-Switching Error: None, MAC-REWRITE Error: None, Loopback: Disabled, Source filtering: Disabled, Flow control: Disabled,

Auto-negotiation: Enabled, Remote fault: Online

Pad to minimum frame size: Disabled

Device flags   : Present Running Down

Interface flags: Hardware-Down Down SNMP-Traps Internal: 0x4000

Link flags     : None

CoS queues     : 8 supported, 8 maximum usable queues

Current address: cc:e1:7f:08:ef:c6, Hardware address: cc:e1:7f:08:e9:ef

Last flapped   : 2021-12-25 10:13:34 CAT (00:48:05 ago)

Input rate     : 0 bps (0 pps)

Output rate    : 0 bps (0 pps)

Active alarms  : LINK

Active defects : LINK

PCS statistics                      Seconds

Bit errors                             0

Errored blocks                         0

Ethernet FEC statistics              Errors

FEC Corrected Errors                    0

FEC Uncorrected Errors                  0

FEC Corrected Errors Rate               0

FEC Uncorrected Errors Rate             0

Interface transmit statistics: Disabled

Logical interface ge-1/2/1.0 (Index 411) (SNMP ifIndex 545)

Flags: Device-Down SNMP-Traps 0x4004000 Encapsulation: ENET2

Input packets : 896122

Output packets: 899425

Protocol aenet, AE bundle: ae11.0

- -

vietpn@ME\_GAZ009SRT01> show interfaces ge-1/2/1

Physical interface: ge-1/2/1, Enabled, Physical link is Up

Interface index: 167, SNMP ifIndex: 526

Description: Connect to AR.GAZ080 - Right ring

Link-level type: Ethernet, Media type: Fiber, MTU: 9000, LAN-PHY mode, Speed: 1000mbps, BPDU Error: None, Loop Detect PDU Error: None,

Ethernet-Switching Error: None, MAC-REWRITE Error: None, Loopback: Disabled, Source filtering: Disabled, Flow control: Disabled,

Auto-negotiation: Enabled, Remote fault: Online

Device flags   : Present Running

Interface flags: SNMP-Traps Internal: 0x0

Link flags     : None

CoS queues     : 8 supported, 8 maximum usable queues

Current address: 28:8a:1c:7c:f4:71, Hardware address: 28:8a:1c:7c:f4:55

Last flapped   : 2021-12-25 09:55:03 CAT (01:08:24 ago)

Input rate     : 1008 bps (0 pps)

Output rate    : 1008 bps (0 pps)

Active alarms  : None

Active defects : None

PCS statistics                      Seconds

Bit errors                             0

Errored blocks                         0

Ethernet FEC statistics              Errors

FEC Corrected Errors                    0

FEC Uncorrected Errors                  0

FEC Corrected Errors Rate               0

FEC Uncorrected Errors Rate             0

Interface transmit statistics: Disabled

Logical interface ge-1/2/1.0 (Index 369) (SNMP ifIndex 586)

Flags: Up SNMP-Traps 0x0 Encapsulation: ENET2

Input packets : 1303058

Output packets: 549988

Protocol aenet, AE bundle: ae1.0

- --

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show chassis routing-engine

Dec 25 12:39:29

Routing Engine status:

Slot 0:

Current state                  Backup

Election priority              Master

Temperature                 27 degrees C / 80 degrees F

CPU temperature             24 degrees C / 75 degrees F

DRAM                      16329 MB (16384 MB installed)

Memory utilization          12 percent

5 sec CPU utilization:

User                       0 percent

Background                 0 percent

Kernel                     0 percent

Interrupt                  0 percent

Idle                      99 percent

Model                          RE-S-1800x4

Serial ID                      9009200633

Start time                     2021-12-25 12:32:49 CAT

Uptime                         6 minutes, 25 seconds

Last reboot reason             0x1:power cycle/failure

Load averages:                 1 minute   5 minute  15 minute

0. 04       0.27       0.17

Routing Engine status:

Slot 1:

Current state                  Master

Election priority              Backup

Temperature                 26 degrees C / 78 degrees F

CPU temperature             25 degrees C / 77 degrees F

DRAM                      16329 MB (16384 MB installed)

Memory utilization          10 percent

5 sec CPU utilization:

User                       0 percent

Background                 0 percent

Kernel                     2 percent

Interrupt                  0 percent

Idle                      98 percent

1 min CPU utilization:

User                       0 percent

Background                 0 percent

Kernel                     2 percent

Interrupt                  0 percent

Idle                      98 percent

5 min CPU utilization:

User                       0 percent

Background                 0 percent

Kernel                     2 percent

Interrupt                  0 percent

Idle                      97 percent

15 min CPU utilization:

User                       1 percent

Background                 0 percent

Kernel                     2 percent

Interrupt                  0 percent

Idle                      97 percent

Model                          RE-S-1800x4

Serial ID                      9013084900

Start time                     2020-09-14 21:57:52 CAT

Uptime                         466 days, 14 hours, 41 minutes, 34 seconds

Last reboot reason             Router rebooted after a normal shutdown.

Load averages:                 1 minute   5 minute  15 minute

0. 24       0.22       0.17

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show chassis routing-engine | match "slot|state|start"

Slot 0:

Current state                 Present

Slot 1:

Current state                  Master

Start time                     2020-09-14 21:57:52 CAT

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show chassis alarms

Dec 25 12:40:03

2 alarms currently active

Alarm time               Class  Description

2021-12-15 07:06:32 CAT  Minor  Loss of communication with Backup RE

2021-12-15 07:06:32 CAT  Minor  Backup RE Active

vietpn@ME\_AR03.GAZ080\_RE1> show chassis hardware

Hardware inventory:

Item             Version  Part number  Serial number     Description

Chassis                                JN1242EA1AFB      MX480

Midplane         REV 04   750-047862   ACRD1729          Enhanced MX480 Midplane

FPM Board        REV 02   710-017254   CADF7683          Front Panel Display

PEM 0            Rev 05   740-027736   QCS1416T0V3       DC 2.4kW Power Entry Module

PEM 1            Rev 02   740-063045   QCS2033T01L       DC 2.4kW Power Entry Module

PEM 2            Rev 05   740-027736   QCS1416T0SD       DC 2.4kW Power Entry Module

PEM 3            Rev 05   740-027736   QCS1416T090       DC 2.4kW Power Entry Module

Routing Engine 0 REV 10   740-031116   9009200633        RE-S-1800x4

Routing Engine 1 REV 10   740-031116   9013084900        RE-S-1800x4

CB 0             REV 24   750-031391   CAEA9044          Enhanced MX SCB

CB 1             REV 24   750-031391   CAEA9302          Enhanced MX SCB

FPC 0            REV 18   750-038489   CACZ0351          MPCE Type 1 3D

CPU            REV 06   711-038484   CACZ0826          MPCE PMB 2G

MIC 0          REV 25   750-028380   CADE7929          3D 2x 10GE XFP

PIC 0                 BUILTIN      BUILTIN           1x 10GE XFP

Xcvr 0              NON-JNPR     FB082799005C      UNKNOWN

PIC 1                 BUILTIN      BUILTIN           1x 10GE XFP

Xcvr 0     REV 01   740-031833   45T749101106      XFP-10G-LW

MIC 1          REV 25   750-028380   CADD2570          3D 2x 10GE XFP

PIC 2                 BUILTIN      BUILTIN           1x 10GE XFP

Xcvr 0     REV 01   740-031834   3XT390100704      XFP-10G-ER

PIC 3                 BUILTIN      BUILTIN           1x 10GE XFP

Xcvr 0              NON-JNPR     030LRTD0B7000210  XFP-10G-ER

FPC 1            REV 20   750-038489   CAEA0971          MPCE Type 1 3D

CPU            REV 06   711-038484   CAEK8793          MPCE PMB 2G

MIC 0          REV 25   750-028380   CAEJ3765          3D 2x 10GE XFP

PIC 0                 BUILTIN      BUILTIN           1x 10GE XFP

Xcvr 0     REV 01   740-031834   3YT390100139      XFP-10G-EW

PIC 1                 BUILTIN      BUILTIN           1x 10GE XFP

Xcvr 0     REV 01   740-031833   46T749100487      XFP-10G-LW

MIC 1          REV 31   750-028392   CAEL8143          3D 20x 1GE(LAN) SFP

PIC 2                 BUILTIN      BUILTIN           10x 1GE(LAN) SFP

Xcvr 0     REV 01   740-017726   AX14300006308     SFP-EX

Xcvr 1     REV 01   740-011783   AX14300009472     SFP-LX10

Xcvr 2     REV 01   740-011783   AX14300009509     SFP-LX10

Xcvr 3     REV 01   740-017726   AX18470005261     SFP-EX

Xcvr 4     REV 01   740-011612   FC2005140129      SFP-LH

Xcvr 9     REV 01   740-011783   AX14300006729     SFP-LX10

PIC 3                 BUILTIN      BUILTIN           10x 1GE(LAN) SFP

Xcvr 0     REV 01   740-011783   AX14300009238     SFP-LX10

Xcvr 1     REV 01   740-011783   AX14300006740     SFP-LX10

Xcvr 2     REV 01   740-011783   AX14300009239     SFP-LX10

Xcvr 3     REV 01   740-011783   AX14300009242     SFP-LX10

Xcvr 5     REV 01   740-011783   AX14300009233     SFP-LX10

Fan Tray                                                 Enhanced Left Fan Tray

{master}

- --

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show interfaces descriptions

Interface       Admin Link Description

xe-0/0/0        up    up   TO\_AR.GAZ027\_xe-0/0/0

e1-0/0/2:50                2G\_INH010\_Link\_3

e1-0/0/2:51                2G\_INH010\_Link\_4

xe-0/1/0        up    up   Connect to PR01.GAZ020\_Xe-0/1/0

xe-1/0/0        up    up   ME\_AR02.GAZ185\_XE-1/0/0\_old-GAZ006

xe-1/1/0        up    up   ME\_AR02.INH080\_XE-0/0/0

ge-1/2/0        up    up   Connect to GAZ100SRT AE1 - Right ring

ge-1/2/1        up    up   Connect to GAZ009SRT AE1 - Right ring

ge-1/2/2        up    up   Connect to  GAZ080SRT AE1 - Right ring

ge-1/2/3        up    up   TO\_ME\_GAZ102SRT01

ge-1/2/4        up    up   TO\_GAZ016SRT02\_BACKUP\_UNDERGROUND

ge-1/2/9        down  down TO\_RRMP02\_GE-8/2/5\_Via\_SDH\_XDM300/I13/port8

ge-1/3/0        up    up   TO\_XDM300/I13/port4\_For\_Hub\_SWITCH

ge-1/3/1        up    up   TO\_GAZ092SRT01

ge-1/3/2        up    down TO\_SWITCH\_GAZ080\_P27\_shutdown

ge-1/3/5        up    up   TO GAZ088:Via\_TSS\_Cable

ae0             up    up   ME\_AR02.GAZ185\_AE1\_old-GAZ006

ae0.121         up    up   Interface run OSPF area 121-AR02.GAZ006-AR03.GAZ080

ae0.122         up    up   Interface run OSPF area 122-AR02.GAZ006-AR03.GAZ080

ae0.123         up    up   Interface run OSPF area 123-AR02.GAZ006-AR03.GAZ080

ae1             up    up   ME\_AR02.INH080\_XE-0/0/0

ae1.126         up    up   Interface run OSPF area 126-AR03.GAZ080-AR02.INH080

ae2             up    up   Connect to PR01.GAZ020-XE-1/0/0

ae4             up    up   To\_GAZ080SRT01

ae5             up    up   TO\_AR.GAZ027

ae5.0           up    up   ME\_AR.GAZ027\_AE0

ae5.127         up    up   Interface run OSPF area 127-AR03.GAZ080-AR.GAZ027

ae10            up    up   To GAZ100 AE1 - Left ring

ae11            up    up   To GAZ009 AE0 - Left ring

ae12            up    up   To GAZ080 AE1 - Right Ring

ae13            up    up   To\_GAZ092SRT01

ae15            up    up   TO\_ME\_GAZ102SRT01

ae16            up    up   TO\_ME\_GAZ016SRT02

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show interfaces di

^

'di' is ambiguous.

Possible completions:

Name of physical or logical interface

diagnostics          Show interface diagnostics information

distribution-list    Show distribution list information of a bundle

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show interfaces diagnostics optics ge-1/2/1

Physical interface: ge-1/2/1

Laser bias current                        :  19.368 mA

Laser output power                        :  0.2170 mW / -6.64 dBm

Module temperature                        :  32 degrees C / 90 degrees F

Module voltage                            :  3.2840 V

Laser receiver power                      :  0.1824 mW / -7.39 dBm

Laser bias current high alarm             :  Off

Laser bias current low alarm              :  Off

Laser bias current high warning           :  Off

Laser bias current low warning            :  Off

Laser output power high alarm             :  Off

Laser output power low alarm              :  Off

Laser output power high warning           :  Off

Laser output power low warning            :  Off

Module temperature high alarm             :  Off

Module temperature low alarm              :  Off

Module temperature high warning           :  Off

Module temperature low warning            :  Off

Module voltage high alarm                 :  Off

Module voltage low alarm                  :  Off

Module voltage high warning               :  Off

Module voltage low warning                :  Off

Laser rx power high alarm                 :  Off

Laser rx power low alarm                  :  Off

Laser rx power high warning               :  Off

Laser rx power low warning                :  Off

Laser bias current high alarm threshold   :  60.000 mA

Laser bias current low alarm threshold    :  3.000 mA

Laser bias current high warning threshold :  50.000 mA

Laser bias current low warning threshold  :  5.000 mA

Laser output power high alarm threshold   :  0.6300 mW / -2.01 dBm

Laser output power low alarm threshold    :  0.0890 mW / -10.51 dBm

Laser output power high warning threshold :  0.5010 mW / -3.00 dBm

Laser output power low warning threshold  :  0.1120 mW / -9.51 dBm

Module temperature high alarm threshold   :  75 degrees C / 167 degrees F

Module temperature low alarm threshold    :  -5 degrees C / 23 degrees F

Module temperature high warning threshold :  70 degrees C / 158 degrees F

Module temperature low warning threshold  :  0 degrees C / 32 degrees F

Module voltage high alarm threshold       :  3.600 V

Module voltage low alarm threshold        :  3.000 V

Module voltage high warning threshold     :  3.500 V

Module voltage low warning threshold      :  3.100 V

Laser rx power high alarm threshold       :  0.6309 mW / -2.00 dBm

Laser rx power low alarm threshold        :  0.0079 mW / -21.02 dBm

Laser rx power high warning threshold     :  0.5011 mW / -3.00 dBm

Laser rx power low warning threshold      :  0.0100 mW / -20.00 dBm

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show lacp interfaces ae1

Aggregated interface: ae1

LACP state:       Role   Exp   Def  Dist  Col  Syn  Aggr  Timeout  Activity

xe-1/1/0       Actor    No    No   Yes  Yes  Yes   Yes     Fast    Active

xe-1/1/0     Partner    No    No   Yes  Yes  Yes   Yes     Fast    Active

LACP protocol:        Receive State  Transmit State          Mux State

xe-1/1/0                  Current   Fast periodic Collecting distributing

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show lldp neighbors

Local Interface    Parent Interface    Chassis Id          Port info          System Name

ge-1/2/2           ae4                 1c:9c:8c:d3:66:70   ge-1/2/0           ME\_GAZ080SRT01

ge-1/2/1           ae11                28:8a:1c:7c:f4:70   ge-1/2/1           ME\_GAZ009SRT01

ge-1/2/0           ae10                28:8a:1c:7d:09:70   ge-1/2/1           ME\_GAZ100SRT01

ge-1/3/5           ae12                28:8a:1c:7d:3a:f0   ge-1/1/0           ME\_GAZ088SRT01

ge-1/2/3           ae15                3c:8c:93:b8:fc:f0   ge-1/2/0           ME\_GAZ102SRT01

ge-1/3/1           ae13                44:ec:ce:20:c1:70   ge-1/2/0           ME\_GAZ092SRT01

xe-1/1/0           ae1                 7c:e2:ca:be:17:cc   xe-0/0/0           ME\_AR02.INH080

xe-0/0/0           ae5                 b8:c2:53:18:37:c0   xe-0/0/0           AR.GAZ027

xe-0/1/0           ae2                 cc:e1:7f:08:e7:c0   xe-1/1/0           ME\_PR01.GAZ020\_RE0

xe-1/0/0           ae0                 cc:e1:7f:09:27:c0   xe-1/0/0           ME\_AR02.GAZ185\_RE0

ge-1/2/4           ae16                f4:bf:a8:a1:68:f0   ge-1/2/0           ME\_GAZ016SRT02

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show log messages | match "ae11|ge-1/2/1"

Dec 27 07:17:05.822 2021  ME\_AR03.GAZ080\_RE1 mib2d[22376]: %DAEMON-4-SNMP\_TRAP\_LINK\_DOWN: ifIndex 524, ifAdminStatus up(1), ifOperStatus down(2), ifName ge-1/2/1

Dec 27 07:28:43.334 2021  ME\_AR03.GAZ080\_RE1 kernel: %KERN-4: lag\_bundlestate\_ifd\_change: bundle ae11 is now Up. uplinks 1 >= min\_links 1

Dec 27 07:28:43.405 2021  ME\_AR03.GAZ080\_RE1 rpd[15392]: %DAEMON-4-RPD\_RSVP\_NBRUP: RSVP neighbor 10.248.35.41 up on interface ae11.0 nbr-type Direct

{master}

vietpn@ME\_AR03.GAZ080\_RE1> show log interactive-commands | match "ae11|ge-1/2/1" | match "Dec 27 0"

Dec 27 06:39:09.932 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'delete interfaces ae11 disable '

Dec 27 06:39:27.322 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'run show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:18.898 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'run show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:39.299 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:42.886 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:43.747 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:44.396 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:45.004 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:45.758 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:47.599 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:48.610 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:49.301 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:52.510 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:55.150 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:56.430 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:41:59.845 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:42:01.355 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:43:48.641 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'run show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:43:52.289 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'run show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:44:07.005 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'run show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:44:11.489 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'run show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:44:13.992 2021  ME\_AR03.GAZ080\_RE1 mgd[30510]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'run show interfaces diagnostics optics ge-1/2/1 '

Dec 27 06:47:33.331 2021  ME\_AR03.GAZ080\_RE1 mgd[30746]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'run show interfaces diagnostics optics ge-1/2/1 '

Dec 27 07:19:42.435 2021  ME\_AR03.GAZ080\_RE1 mgd[30746]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'set interfaces ge-1/2/1 disable '

Dec 27 07:20:02.791 2021  ME\_AR03.GAZ080\_RE1 mgd[30746]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'run show interfaces diagnostics optics ge-1/2/1 '

Dec 27 07:28:43.931 2021  ME\_AR03.GAZ080\_RE1 mgd[31417]: UI\_JUNOSCRIPT\_CMD: User 'root' used JUNOScript client to run command 'get-interface-information interface-name=ae11'

Dec 27 07:30:21.841 2021  ME\_AR03.GAZ080\_RE1 mgd[30746]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces ae11 '

Dec 27 07:30:41.419 2021  ME\_AR03.GAZ080\_RE1 mgd[30746]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces ae11 '

Dec 27 07:30:48.245 2021  ME\_AR03.GAZ080\_RE1 mgd[30746]: UI\_CMDLINE\_READ\_LINE: User 'longnh', command 'show interfaces ae11 '

Dec 27 07:33:38.468 2021  ME\_AR03.GAZ080\_RE1 mgd[20015]: UI\_CMDLINE\_READ\_LINE: User 'antoniosd', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 07:33:43.958 2021  ME\_AR03.GAZ080\_RE1 mgd[31417]: UI\_JUNOSCRIPT\_CMD: User 'root' used JUNOScript client to run command 'get-interface-information interface-name=ae11'

Dec 27 07:33:44.301 2021  ME\_AR03.GAZ080\_RE1 mgd[31417]: UI\_CMDLINE\_READ\_LINE: User 'root', command 'rpc get-ospf-neighbor-information area 0.0.0.0 area get-ospf-neighbor-information rpc rpc get-interface-information interface-name ae11 interface-name get-interface-information rpc rpc get-interface-information interface-name ae11 interface-name get-interface-information rpc rpc command show interface lo0 terse '

Dec 27 07:33:49.780 2021  ME\_AR03.GAZ080\_RE1 mgd[20015]: UI\_CMDLINE\_READ\_LINE: User 'antoniosd', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 09:09:31.510 2021  ME\_AR03.GAZ080\_RE1 mgd[32736]: UI\_CMDLINE\_READ\_LINE: User 'icinga', command 'show log messages | match ae11 '

Dec 27 09:09:50.532 2021  ME\_AR03.GAZ080\_RE1 mgd[32736]: UI\_CMDLINE\_READ\_LINE: User 'icinga', command 'show log interactive-commands | match ae11 '

Dec 27 09:27:19.138 2021  ME\_AR03.GAZ080\_RE1 mgd[32974]: UI\_CMDLINE\_READ\_LINE: User 'vietpn', command 'show interfaces diagnostics optics ge-1/2/1 '

Dec 27 09:31:36.603 2021  ME\_AR03.GAZ080\_RE1 mgd[32974]: UI\_CMDLINE\_READ\_LINE: User 'vietpn', command 'show log interactive-commands | match ae11 '

Dec 27 09:32:40.153 2021  ME\_AR03.GAZ080\_RE1 mgd[32974]: UI\_CMDLINE\_READ\_LINE: User 'vietpn', command '"interface-name=ae11'Dec1017:30:33.3452021ME\_AR03.GAZ080\_RE1mgd[76737]:UI\_JUNOSCRIPT\_CMD:User'root'usedJUNOScriptclienttoruncommand'get-interface-information" '

Dec 27 09:32:43.008 2021  ME\_AR03.GAZ080\_RE1 mgd[32974]: UI\_CMDLINE\_READ\_LINE: User 'vietpn', command '"interface-name=ae11'Dec1017:35:33.3642021ME\_AR03.GAZ080\_RE1mgd[76737]:UI\_JUNOSCRIPT\_CMD:User'root'usedJUNOScriptclienttoruncommand'get-interface-information" '

Dec 27 09:36:00.306 2021  ME\_AR03.GAZ080\_RE1 mgd[32974]: UI\_CMDLINE\_READ\_LINE: User 'vietpn', command 'show log messages | match "ae11|ge-1/2/1" '

Dec 27 09:42:35.696 2021  ME\_AR03.GAZ080\_RE1 mgd[32974]: UI\_CMDLINE\_READ\_LINE: User 'vietpn', command 'show log messages | match "ae11|ge-1/2/1" '

Dec 27 09:44:57.923 2021  ME\_AR03.GAZ080\_RE1 mgd[32974]: UI\_CMDLINE\_READ\_LINE: User 'vietpn', command 'show log interactive-commands | match "ae11|ge-1/2/1" '

Dec 27 09:45:51.656 2021  ME\_AR03.GAZ080\_RE1 mgd[32974]: UI\_CMDLINE\_READ\_LINE: User 'vietpn', command 'show log messages | match "ae11|ge-1/2/1" '

Dec 27 09:46:17.627 2021  ME\_AR03.GAZ080\_RE1 mgd[32974]: UI\_CMDLINE\_READ\_LINE: User 'vietpn', command 'show log interactive-commands | match "ae11|ge-1/2/1" | match "Dec 27 0" '

- --

vietpn@ME\_GAZ009SRT01> show interfaces ge-1/2/1

Physical interface: ge-1/2/1, Enabled, Physical link is Up

Interface index: 167, SNMP ifIndex: 526

Description: Connect to AR.GAZ080 - Right ring

Link-level type: Ethernet, Media type: Fiber, MTU: 9000, LAN-PHY mode, Speed: 1000mbps, BPDU Error: None, Loop Detect PDU Error: None,

Ethernet-Switching Error: None, MAC-REWRITE Error: None, Loopback: Disabled, Source filtering: Disabled, Flow control: Disabled,

Auto-negotiation: Enabled, Remote fault: Online

Device flags   : Present Running

Interface flags: SNMP-Traps Internal: 0x0

Link flags     : None

CoS queues     : 8 supported, 8 maximum usable queues

Current address: 28:8a:1c:7c:f4:71, Hardware address: 28:8a:1c:7c:f4:55

Last flapped   : 2021-12-27 07:28:40 CAT (02:22:37 ago)

Input rate     : 81450096 bps (18979 pps)

Output rate    : 33000944 bps (24294 pps)

Active alarms  : None

Active defects : None

PCS statistics                      Seconds

Bit errors                             0

Errored blocks                         0

Ethernet FEC statistics              Errors

FEC Corrected Errors                    0

FEC Uncorrected Errors                  0

FEC Corrected Errors Rate               0

FEC Uncorrected Errors Rate             0

Interface transmit statistics: Disabled

Logical interface ge-1/2/1.0 (Index 369) (SNMP ifIndex 586)

Flags: Up SNMP-Traps 0x0 Encapsulation: ENET2

Input packets : 169739

Output packets: 78124

Protocol aenet, AE bundle: ae1.0

vietpn@ME\_GAZ009SRT01> show interfaces des

^

'des' is ambiguous.

Possible completions:

Name of physical or logical interface

descriptions         Display interface description strings

destination-class    Show statistics for destination class

vietpn@ME\_GAZ009SRT01> show interfaces descriptions

Interface       Admin Link Description

e1-0/0/0        up    up   BTS\_2G\_GAZ009\_Link\_0

e1-0/0/1        up    down BTS\_2G\_GAZ009\_Link\_1

ge-1/0/0        up    up   NodeB\_UGAZ009

ge-1/0/3        up    up   PTP for 2G

ge-1/1/0        up    up   LGAZ009

ge-1/1/0.20     up    up   LGAZ009\_CPUP

ge-1/1/0.21     up    up   LGAZ009\_CPUP\_OAM

ge-1/1/1        up    up   TO GAZ171 Via:TSS\_Backup

ge-1/1/2        up    down FTTH\_3909010116364\_Cruz\_Vermelha\_De\_Mocambique\_Delegacao\_De\_Gaza

ge-1/1/2.1010   up    down FTTH

ge-1/1/3        up    up   SWT\_GAZ009\_33.206;

ge-1/1/3.1010   up    up   FTTH

ge-1/1/3.1062   up    up   OAM

ge-1/1/3.1163   up    up   PLC\_FIPAG\_GAZ

ge-1/1/3.1286   up    up   PLC\_DCPOWER\_MONITORING

ge-1/1/3.2644   up    up   L3LL\_RED\_CROSS

ge-1/1/3.2645   up    up   L3LL\_STAE

ge-1/2/0        up    up   Connect to GAZ058 - Left ring

ge-1/2/1        up    up   Connect to AR.GAZ080 - Right ring

ae0             up    up   To GAZ058 AE1 - Right ring

ae1             up    up   To AR03.GAZ080 AE21 - Right ring

vietpn@ME\_GAZ009SRT01> show lldp neighbors

Local Interface    Parent Interface    Chassis Id          Port info          System Name

ge-1/0/3           -                   28:8a:1c:7c:f4:70   ge-1/0/3           ME\_GAZ009SRT01

ge-1/2/0           ae0                 28:8a:1c:7d:a6:70   ge-1/2/1           ME\_GAZ058SRT01

ge-1/1/1           -                   28:8a:1c:7d:b5:70   ge-1/1/1           ME\_GAZ171SRT01

ge-1/2/1           ae1                 cc:e1:7f:08:ef:c0   ge-1/2/1           ME\_AR03.GAZ080\_RE1

vietpn@ME\_GAZ009SRT01> show winte

^

syntax error, expecting .

vietpn@ME\_GAZ009SRT01> show wintedi

^

syntax error, expecting .

vietpn@ME\_GAZ009SRT01> show interfaces diagnostics optics ge-1/2/1

Physical interface: ge-1/2/1

Laser bias current                        :  35.000 mA

Laser output power                        :  1.3440 mW / 1.28 dBm

Module temperature                        :  53 degrees C / 127 degrees F

Module voltage                            :  3.2040 V

Laser receiver power                      :  0.0330 mW / -14.81 dBm

Laser bias current high alarm             :  Off

Laser bias current low alarm              :  Off

Laser bias current high warning           :  Off

Laser bias current low warning            :  Off

Laser output power high alarm             :  Off

Laser output power low alarm              :  Off

Laser output power high warning           :  Off

Laser output power low warning            :  Off

Module temperature high alarm             :  Off

Module temperature low alarm              :  Off

Module temperature high warning           :  Off

Module temperature low warning            :  Off

Module voltage high alarm                 :  Off

Module voltage low alarm                  :  Off

Module voltage high warning               :  Off

Module voltage low warning                :  Off

Laser rx power high alarm                 :  Off

Laser rx power low alarm                  :  Off

Laser rx power high warning               :  Off

Laser rx power low warning                :  Off

Laser bias current high alarm threshold   :  85.000 mA

Laser bias current low alarm threshold    :  5.000 mA

Laser bias current high warning threshold :  80.000 mA

Laser bias current low warning threshold  :  7.000 mA

Laser output power high alarm threshold   :  3.1620 mW / 5.00 dBm

Laser output power low alarm threshold    :  0.4460 mW / -3.51 dBm

Laser output power high warning threshold :  2.5110 mW / 4.00 dBm

Laser output power low warning threshold  :  0.6300 mW / -2.01 dBm

Module temperature high alarm threshold   :  90 degrees C / 194 degrees F

Module temperature low alarm threshold    :  -40 degrees C / -40 degrees F

Module temperature high warning threshold :  85 degrees C / 185 degrees F

Module temperature low warning threshold  :  -35 degrees C / -31 degrees F

Module voltage high alarm threshold       :  3.799 V

Module voltage low alarm threshold        :  2.799 V

Module voltage high warning threshold     :  3.700 V

Module voltage low warning threshold      :  2.900 V

Laser rx power high alarm threshold       :  1.2589 mW / 1.00 dBm

Laser rx power low alarm threshold        :  0.0039 mW / -24.09 dBm

Laser rx power high warning threshold     :  1.0000 mW / 0.00 dBm

Laser rx power low warning threshold      :  0.0050 mW / -23.01 dBm

vietpn@ME\_GAZ009SRT01> show lacp interfaces ae11

error: device ae11 not found

vietpn@ME\_GAZ009SRT01> show lacp interfaces ae1

Aggregated interface: ae1

LACP state:       Role   Exp   Def  Dist  Col  Syn  Aggr  Timeout  Activity

ge-1/2/1       Actor    No    No   Yes  Yes  Yes   Yes     Fast    Active

ge-1/2/1     Partner    No    No   Yes  Yes  Yes   Yes     Fast    Active

LACP protocol:        Receive State  Transmit State          Mux State

ge-1/2/1                  Current   Fast periodic Collecting distributing

vietpn@ME\_GAZ009SRT01>
