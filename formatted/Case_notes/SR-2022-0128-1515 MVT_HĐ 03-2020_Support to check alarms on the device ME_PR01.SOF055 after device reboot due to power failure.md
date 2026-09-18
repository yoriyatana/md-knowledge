# SR-2022-0128-1515 MVT/HĐ 03-2020/Support to check alarms on the device ME_PR01.SOF055 after device reboot due to power failure

```text
TEST SCB VÀ MPC
```

### Hướng dẫn này giả định RE1 đang ở trạng thái backup

### Thu thập các thông tin liên quan trước khi thực hiện

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
> show system switchover /\* Show on Backup RE – GRES Readiness Check\*/
```

```text
> show task replication  /\* Show on Master RE – RPD Synchronization Check\*/
```

```text
> show database-replication summary /\* Show on Master RE – For BNG only \*/
```

### Kiểm tra trạng thái RE1

###### Đảm bảo RE1 đang ở trạng thái Backup vì mình sẽ tác động vào SCB slot 1, dẫn tới tác  động trên RE1.

{master}

```text
> show chassis routing-engine | match "Slot|State|Start"
```

Dec 15 00:47:05

Slot 0:

```text
Current state                  Master
```

Start time                     2020-09-11 23:31:07 CAT

Slot 1:

```text
Current state                  Backup
```

Start time                     2020-09-11 23:20:51 CAT

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

Start time                     2020-09-11 23:31:07 CAT

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
> show chassis fabric summary extended
```

0      Online     NO     NO        NO/  NO         459 days, 1 hour, 17 minutes, 20 seconds

1      Online     NO     NO        NO/  NO         459 days, 1 hour, 17 minutes, 20 seconds

2      Online     NO     NO        NO/  NO         459 days, 1 hour, 17 minutes, 20 seconds

3      Online     NO     NO        NO/  NO         459 days, 1 hour, 17 minutes, 20 seconds

4      Offline

5      Offline

6      Offline

7      Offline

### Tháo SCB1 ra khỏi chassis và gắn SCB cần test vào vị trí CB1.

### Gắn card MPC cần test vào vị trí vị FPC slot trống.

### Đợi 10 phút và thực hiện các lệnh show để kiểm tra

```text
> show chassis hardware models | no-more
```

```text
> show chassis hardware | no-more
```

```text
> show log inventory | no-more
```

```text
> show log chassisd | no-more
```

### Chụp hình tình trạng đèn trên CB và FPC lỗi

### Thu thập thông tin RSI, varlog

```text
request support information | no-more | save /var/log/RSI\_ME\_PR01.SOF055\_20220316
```

```text
file archive source /var/log/\* destination /var/tmp/LOG\_ME\_PR01.SOF055\_20220316
```

### Rollback lại trạng thái cũ

- --

{master}

vietpn@ME\_PR01.SOF055\_RE1> show chassis hardware models

Hardware inventory:

Item             Version  Part number  Serial number     FRU model number

Midplane         REV 09   750-047862   ACRE3969          CHAS-BP3-MX480-S

FPM Board        REV 02   710-017254   CAEA1444          CRAFT-MX480-S

PEM 0            Rev 05   740-027736   QCS1451T0AB       PWR-MX480-2400-DC-S

PEM 1            Rev 05   740-027736   QCS1451T0MP       PWR-MX480-2400-DC-S

PEM 2            Rev 05   740-027736   QCS1451T0H2       PWR-MX480-2400-DC-S

PEM 3            Rev 05   740-027736   QCS1451T0FU       PWR-MX480-2400-DC-S

Routing Engine 1 REV 10   740-031116   9009225243        RE-S-1800X4-16G-S

CB 1             REV 24   750-031391   CAEA9516          SCBE-MX-S

FPC 0            REV 20   750-038489   CAEA0973          MX-MPC1E-3D

MIC 0          REV 25   750-028380   CAEJ3555          MIC-3D-2XGE-XFP

MIC 1          REV 25   750-028380   CAEJ3651          MIC-3D-2XGE-XFP

FPC 2            REV 07   750-063747   CANB5244          MX-MPC1E-3D

MIC 0          REV 29   750-028380   CAJA2537          MIC-3D-2XGE-XFP

FPC 3            REV 20   750-063184   CAPW3043          MPC2E-3D-NG

MIC 0          REV 34   750-028387   CAPS0860          MIC-3D-4XGE-XFP

Fan Tray                                                 FFANTRAY-MX480-HC-S

{master}

vietpn@ME\_PR01.SOF055\_RE1> show configuration interfaces | display set | match "[geax][et]-1"

```text
set interfaces xe-1/0/0 apply-groups-except MTU
```

```text
set interfaces xe-1/0/0 description TO\_AR01.INH085\_Xe-1/0/0
```

```text
set interfaces xe-1/0/0 hold-time up 2000
```

```text
set interfaces xe-1/0/0 hold-time down 300
```

```text
set interfaces xe-1/0/0 framing wan-phy
```

```text
set interfaces xe-1/0/0 gigether-options 802.3ad ae3
```

```text
set interfaces xe-1/1/0 apply-groups-except MTU
```

```text
set interfaces xe-1/1/0 description To\_ME\_PR01\_ZAM034\_XE-0/2/0\_NEW\_LINK
```

```text
set interfaces xe-1/1/0 framing wan-phy
```

```text
set interfaces xe-1/1/0 gigether-options 802.3ad ae4
```

```text
set interfaces ge-1/2/0 description 3G\_HUB:TO\_OSN3500:\_SL14/P1
```

```text
set interfaces ge-1/2/0 flexible-vlan-tagging
```

```text
set interfaces ge-1/2/0 speed 1g
```

```text
set interfaces ge-1/2/0 mtu 9000
```

```text
set interfaces ge-1/2/0 link-mode full-duplex
```

```text
set interfaces ge-1/2/0 encapsulation flexible-ethernet-services
```

```text
set interfaces ge-1/2/0 gigether-options no-auto-negotiation
```

```text
set interfaces ge-1/2/1 description 3G\_HUB:TO\_OSN3500:\_SL14/P2
```

```text
set interfaces ge-1/2/1 flexible-vlan-tagging
```

```text
set interfaces ge-1/2/1 speed 1g
```

```text
set interfaces ge-1/2/1 mtu 9000
```

```text
set interfaces ge-1/2/1 link-mode full-duplex
```

```text
set interfaces ge-1/2/1 encapsulation flexible-ethernet-services
```

```text
set interfaces ge-1/2/1 gigether-options no-auto-negotiation
```

```text
set interfaces ge-1/2/2 description 3G\_HUB:TO\_OSN3500:\_SL14/P3
```

```text
set interfaces ge-1/2/2 flexible-vlan-tagging
```

```text
set interfaces ge-1/2/2 speed 1g
```

```text
set interfaces ge-1/2/2 mtu 9000
```

```text
set interfaces ge-1/2/2 link-mode full-duplex
```

```text
set interfaces ge-1/2/2 encapsulation flexible-ethernet-services
```

```text
set interfaces ge-1/2/2 gigether-options no-auto-negotiation
```

```text
set interfaces ge-1/2/3 description 3G\_HUB:TO\_OSN3500:\_SL14/P4
```

```text
set interfaces ge-1/2/3 flexible-vlan-tagging
```

```text
set interfaces ge-1/2/3 speed 1g
```

```text
set interfaces ge-1/2/3 mtu 9000
```

```text
set interfaces ge-1/2/3 link-mode full-duplex
```

```text
set interfaces ge-1/2/3 encapsulation flexible-ethernet-services
```

```text
set interfaces ge-1/2/3 gigether-options no-auto-negotiation
```

```text
set interfaces ge-1/3/0 description FOR\_SWITCH\_SOF055
```

```text
set interfaces ge-1/3/0 flexible-vlan-tagging
```

```text
set interfaces ge-1/3/0 speed 100m
```

```text
set interfaces ge-1/3/0 link-mode full-duplex
```

```text
set interfaces ge-1/3/0 encapsulation flexible-ethernet-services
```

```text
set interfaces ge-1/3/0 unit 0 encapsulation vlan-vpls
```

```text
set interfaces ge-1/3/0 unit 0 vlan-id-list 10-4000
```

```text
set interfaces ge-1/3/0 unit 0 input-vlan-map push
```

```text
set interfaces ge-1/3/0 unit 0 input-vlan-map vlan-id 2557
```

```text
set interfaces ge-1/3/0 unit 0 output-vlan-map pop
```

```text
set interfaces ge-1/3/1 apply-groups-except MTU
```

```text
set interfaces ge-1/3/1 description TO\_AR04.SOF089\_Ge-0/2/0\_Via:XDM\_I13/P1\_BACKUP
```

```text
set interfaces ge-1/3/1 speed 1g
```

```text
set interfaces ge-1/3/1 link-mode full-duplex
```

```text
set interfaces ge-1/3/1 gigether-options no-auto-negotiation
```

```text
set interfaces ge-1/3/1 gigether-options 802.3ad ae11
```

```text
set interfaces ge-1/3/2 apply-groups-except MTU
```

```text
set interfaces ge-1/3/2 description TO\_AR04.SOF089\_Ge-0/2/1\_Via:XDM\_I13/P2\_BACKUP
```

```text
set interfaces ge-1/3/2 speed 1g
```

```text
set interfaces ge-1/3/2 link-mode full-duplex
```

```text
set interfaces ge-1/3/2 gigether-options no-auto-negotiation
```

```text
set interfaces ge-1/3/2 gigether-options 802.3ad ae11
```

```text
set interfaces ge-1/3/4 apply-groups-except MTU
```

```text
set interfaces ge-1/3/4 description TO\_ME\_SOF055SRT01
```

```text
set interfaces ge-1/3/4 gigether-options 802.3ad ae10
```

```text
set interfaces ge-1/3/5 apply-groups-except MTU
```

```text
set interfaces ge-1/3/5 description TO\_ME\_SOF086SRT01
```

```text
set interfaces ge-1/3/5 gigether-options 802.3ad ae13
```

replace pattern xe-1/0/0 with xe-3/0/0

replace pattern xe-1/1/0 with xe-1/1/0

replace pattern ge-0/0/0 with ge-0/1/0

replace pattern ge-0/0/0 with ge-0/1/0

replace pattern ge-0/0/0 with ge-0/1/0

replace pattern ge-0/0/0 with ge-0/1/0

replace pattern ge-0/0/0 with ge-0/1/0

replace pattern ge-0/0/0 with ge-0/1/0

replace pattern ge-0/0/0 with ge-0/1/0

Sep 16 23:05:23 CB - part number 750-031391, serial number CAEA9516

Sep 16 23:05:24 MX480 Midplane chassis, serial number JN1251F42AFB\x08

Sep 16 23:05:24 mx480 chassis, serial number JN1251F42AFB

Sep 16 23:05:24 FPC 0 - part number 750-038489, serial number CAEA0973

Sep 16 23:05:24 FPC 1 - part number 750-063747, serial number CAHW3177

Sep 16 23:05:24 FPC 2 - part number 750-063747, serial number CANB5244

Sep 16 23:05:25 CB 1 - part number 750-031391, serial number CAEA9516

Sep 16 23:05:25 CB 0 - part number 750-031391, serial number CAEA9135

Sep 16 23:05:29 FPM - part number 710-017254, serial number CAEA1444

Sep 16 23:05:30 FPC 0 - part number 750-038489, serial number CAEA0973

Sep 16 23:05:30 FPC 1 - part number 750-063747, serial number CAHW3177

Sep 16 23:05:30 FPC 2 - part number 750-063747, serial number CANB5244

Sep 16 23:05:34 PEM 0 - part number 740-027736, serial number QCS1451T0AB

Sep 16 23:05:34 PEM 1 - part number 740-027736, serial number QCS1451T0MP

Sep 16 23:05:34 PEM 2 - part number 740-027736, serial number QCS1451T0H2

Sep 16 23:05:34 PEM 3 - part number 740-027736, serial number QCS1451T0FU

Sep 16 23:06:45 FPC 0 CPU - part number 711-038484, serial number CAEK8484

Sep 16 23:06:52 FPC 1 CPU - part number 711-063749, serial number CAHW0286

Sep 16 23:06:58 FPC 2 CPU - part number 711-063749, serial number CANC1195

Sep 16 23:07:03 FPC 0 PIC 0 - part number 750-028380, serial number CAEJ3555

Sep 16 23:07:03 FPC 0 MIC 0 - part number 750-028380, serial number CAEJ3555

Sep 16 23:07:04 FPC 0 PIC 1 - part number 750-028380, serial number CAEJ3555

Sep 16 23:07:04 FPC 0 MIC 0 - part number 750-028380, serial number CAEJ3555

Sep 16 23:07:08 FPC 0 PIC 2 - part number 750-028380, serial number CAEJ3651

Sep 16 23:07:08 FPC 0 MIC 1 - part number 750-028380, serial number CAEJ3651

Sep 16 23:07:08 FPC 0 PIC 3 - part number 750-028380, serial number CAEJ3651

Sep 16 23:07:08 FPC 0 MIC 1 - part number 750-028380, serial number CAEJ3651

Sep 16 23:07:13 FPC 1 PIC 0 - part number 750-028380, serial number CAJA2841

Sep 16 23:07:13 FPC 1 MIC 0 - part number 750-028380, serial number CAJA2841

Sep 16 23:07:13 FPC 1 PIC 1 - part number 750-028380, serial number CAJA2841

Sep 16 23:07:13 FPC 1 MIC 0 - part number 750-028380, serial number CAJA2841

Sep 16 23:07:17 FPC 1 PIC 2 - part number 750-028392, serial number CADA2837

Sep 16 23:07:17 FPC 1 MIC 1 - part number 750-028392, serial number CADA2837

Sep 16 23:07:17 FPC 1 PIC 3 - part number 750-028392, serial number CADA2837

Sep 16 23:07:17 FPC 1 MIC 1 - part number 750-028392, serial number CADA2837

Sep 16 23:07:23 FPC 2 PIC 0 - part number 750-028380, serial number CAJA2537

Sep 16 23:07:23 FPC 2 MIC 0 - part number 750-028380, serial number CAJA2537

Sep 16 23:07:23 FPC 2 PIC 1 - part number 750-028380, serial number CAJA2537

Sep 16 23:07:23 FPC 2 MIC 0 - part number 750-028380, serial number CAJA2537

Sep 16 23:19:59 CHASSISD release 17.3R3-S8.1 built by builder on 2020-05-20 16:31:01 UTC

Sep 16 23:20:01 Routing Engine 1 - part number 740-031116, serial number 9009225243

Sep 16 23:20:09 Routing Engine 0 - part number 740-031116, serial number 9009227835

Jun  3 06:33:29 CHASSISD release 17.3R3-S8.1 built by builder on 2020-05-20 16:31:01 UTC

Jun  3 06:33:35 Routing Engine 1 - part number 740-031116, serial number 9009225243

Jun  3 06:33:57 Routing Engine 0 - part number 740-031116, serial number 9009227835

Jul 16 06:39:35 CHASSISD release 17.3R3-S8.1 built by builder on 2020-05-20 16:31:01 UTC

Jul 16 06:39:29 Routing Engine 1 - part number 740-031116, serial number 9009225243

Jul 16 06:39:56 Routing Engine 0 - part number 740-031116, serial number 9009227835

RE0

```text
request support information | no-more | save /var/log/RSI\_ME\_PR01.SOF055\_20220128
```

```text
file archive source /var/log/\* destination /var/tmp/LOG\_ME\_PR01.SOF055\_20220128
```

\* Mở case liên quan alarm - 2021-1201-372793

Movitel | MX480 | PR01.SOF055 | 17.3R3-S8.1 | CB0 and MPC1E (FPC slot 1) not online after device reboot due to power failure

- --

S/N to open case

CAHW3177

- --

Hi JTAC,

Our customer observed many alarms raised and CB0 nad FPC1 can not online after device reboot due to power failure.

{master}

vietpn@ME\_PR01.SOF055\_RE1> show chassis alarms

6 alarms currently active

Alarm time               Class  Description

2022-01-27 16:36:23 CAT  Minor  CB 0 Temp Sensor Fail

2022-01-27 16:35:18 CAT  Major  CB 0 Failure

2022-01-27 16:35:18 CAT  Minor  Backup RE Active

2022-01-27 16:35:18 CAT  Minor  Loss of communication with Backup RE

2022-01-27 16:35:18 CAT  Minor  CB 0 Fabric Chip 0 Not Online

2022-01-27 16:35:18 CAT  Minor  CB 0 Fabric Chip 1 Not Online

{master}

vietpn@ME\_PR01.SOF055\_RE1> show chassis hardware

Hardware inventory:

Item             Version  Part number  Serial number     Description

Chassis                                JN1251F42AFB      MX480

Midplane         REV 09   750-047862   ACRE3969          Enhanced MX480 Midplane

FPM Board        REV 02   710-017254   CAEA1444          Front Panel Display

PEM 0            Rev 05   740-027736   QCS1451T0AB       DC 2.4kW Power Entry Module

PEM 1            Rev 05   740-027736   QCS1451T0MP       DC 2.4kW Power Entry Module

PEM 2            Rev 05   740-027736   QCS1451T0H2       DC 2.4kW Power Entry Module

PEM 3            Rev 05   740-027736   QCS1451T0FU       DC 2.4kW Power Entry Module

Routing Engine 1 REV 10   740-031116   9009225243        RE-S-1800x4

CB 0

CB 1             REV 24   750-031391   CAEA9516          Enhanced MX SCB

FPC 0            REV 20   750-038489   CAEA0973          MPCE Type 1 3D

CPU            REV 06   711-038484   CAEK8484          MPCE PMB 2G

MIC 0          REV 25   750-028380   CAEJ3555          3D 2x 10GE XFP

PIC 0                 BUILTIN      BUILTIN           1x 10GE XFP

Xcvr 0     REV 01   740-031833   UTB1G6V           XFP-10G-LW

PIC 1                 BUILTIN      BUILTIN           1x 10GE XFP

Xcvr 0     REV 01   740-031833   UTB1LNE           XFP-10G-LW

MIC 1          REV 25   750-028380   CAEJ3651          3D 2x 10GE XFP

PIC 2                 BUILTIN      BUILTIN           1x 10GE XFP

Xcvr 0     REV 01   740-031833   UTB1K9L           XFP-10G-LW

PIC 3                 BUILTIN      BUILTIN           1x 10GE XFP

Xcvr 0              NON-JNPR     AXJ1LBW           XFP-10G-LW

FPC 1

CPU

FPC 2            REV 07   750-063747   CANB5244          MPCE Type 1 3D

CPU            REV 04   711-063749   CANC1195          MPCE PMB 2G

MIC 0          REV 29   750-028380   CAJA2537          3D 2x 10GE XFP

PIC 0                 BUILTIN      BUILTIN           1x 10GE XFP

Xcvr 0     REV 01   740-011607   FC1909169103      XFP-10G-LW

PIC 1                 BUILTIN      BUILTIN           1x 10GE XFP

Xcvr 0     REV 01   740-011607   FC1909169102      XFP-10G-LW

FPC 3            REV 20   750-063184   CAPW3043          MPC2E NG PQ & Flex Q

CPU            REV 13   711-045719   CAPW1182          RMPC PMB

MIC 0          REV 34   750-028387   CAPS0860          3D 4x 10GE  XFP

PIC 0                 BUILTIN      BUILTIN           2x 10GE  XFP

Xcvr 0              NON-JNPR     AXK15NM           XFP-10G-LW

Xcvr 1              NON-JNPR     AXJ0PVM           XFP-10G-LW

PIC 1                 BUILTIN      BUILTIN           2x 10GE  XFP

Xcvr 0     REV 01   740-011607   FC2010071934      XFP-10G-LW

Xcvr 1     REV 01   740-011607   FC2010071935      XFP-10G-LW

Fan Tray                                                 Enhanced Left Fan Tray

```text
When we replace CB0 with the new SCB, the CB0 was up, RE0 online and the alarms were cleared. The FPC1 still failed because we didn't have the spare MPC1E.
```

Please help us RCA for CB0 and FPC1.

- -

{master}

longnh@ME\_AR02.SOF033\_RE0> show chassis hardware | no-more

Hardware inventory:

Item             Version  Part number  Serial number     Description

Chassis                                JN1242D3FAFB      MX480

Midplane         REV 04   750-047862   ACRD1708          Enhanced MX480 Midplane

FPM Board        REV 02   710-017254   CADF7600          Front Panel Display

PEM 0            Rev 05   740-027736   QCS1416T109       DC 2.4kW Power Entry Module

PEM 1            Rev 05   740-027736   QCS1416T0SN       DC 2.4kW Power Entry Module

PEM 2            Rev 05   740-027736   QCS1416T0VJ       DC 2.4kW Power Entry Module

PEM 3            Rev 02   740-063045   QCS1705T0JH       DC 2.4kW Power Entry Module

Routing Engine 0 REV 10   740-031116   9009198800        RE-S-1800x4

CB 0             REV 23   750-031391   CACZ3569          Enhanced MX SCB

CB 1

FPC 2

CPU

Fan Tray                                                 Enhanced Left Fan Tray
