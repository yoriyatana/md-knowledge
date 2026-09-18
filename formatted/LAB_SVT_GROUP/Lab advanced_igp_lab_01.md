# Lab advanced_igp_lab_01

- --

LAB IGP

- --

Task 1:

- R1:

- R2:

Using isis L2 authentication-type md5, does not meet the requirements of the task

~~~> set protocols isis level 2 authentication-type simple

Mar  8 08:14:42.429283 OSPF packet ignored: authentication failure (bad cksum).

Mar  8 08:14:42.429351 OSPF packet ignored: authentication failure from 10.10.4.2

~~~> set protocols ospf area 0.0.0.0 interface ge-0/0/1.0 authentication md5 1 key "$9$RkASK8db2JUHM87VbYZGTz36/t0OR"

Missing enable interface ge-0/0/5.0 in protocol isis

~~~> set protocols isis interface ge-0/0/5.0 point-to-point

- R3:

root@R3# run show log debug\_isis | match err

Mar  8 04:14:16.058491 ERROR: ISIS ignored a bad packet: IIH with duplicate sysid on interface ge-0/0/3.0

~~~>

Missing ISIS authentication ~~~>

set protocols isis level 1 authentication-key "$9$A8mf0RSM87bYohSeW8xwsik.Pfzn6A"

set protocols isis level 1 authentication-type simple

set protocols isis level 2 authentication-key "$9$A8mf0RSM87bYohSeW8xwsik.Pfzn6A"

set protocols isis level 2 authentication-type simple

- --

Missing OSPF authentication

~~~> set protocols ospf area 0.0.0.1 interface ge-0/0/5.0 authentication md5 1 key "$9$hGjrMXbs4Gjq8X-wsgUDz369CuB1h"

- R4:

Missing change interface type p2p on interface ge-0/0/5.0

~~~> set protocols isis interface ge-0/0/5.0 point-to-point

- R5:

Mar  8 04:01:00.011648 ERROR: IIH authentication information with bad length 10

Mar  8 04:01:00.011750 ERROR: IIH from R4 on ge-0/0/5.0 failed authentication

Mar  8 04:01:00.011758 ERROR: previous error from L1, source R4 on ge-0/0/5.0

Wrong authentication-key on isis L1

~~~> set protocols isis level 1 authentication-key "$9$A8mf0RSM87bYohSeW8xwsik.Pfzn6A"

- R6:

Missing ISIS L1 authentication

~~~>

set protocols isis level 1 authentication-key "$9$A8mf0RSM87bYohSeW8xwsik.Pfzn6A"

set protocols isis level 1 authentication-type simple

- R7:

Missing ISIS L1 authentication

~~~>

set protocols isis level 1 authentication-key "$9$A8mf0RSM87bYohSeW8xwsik.Pfzn6A"

set protocols isis level 1 authentication-type simple

- R8:

Task 2:

- R2:

set protocols ospf spf-options rapid-runs 5

set protocols isis overload timeout 300

Task 3:

- R1:

set protocols ospf area 0.0.0.0 interface ge-0/0/5.0 interface-type p2mp

~~~> set protocols ospf area 0.0.0.0 interface ge-0/0/5.0 interface-type p2p

- --

set interfaces ge-0/0/2 mtu 1700

~~~> delete interfaces ge-0/0/2 mtu

- R2:

set routing-options router-id 10.210.1.5

~~~> delete routing-options router-id

- R3:

- R4:

Missing OSPF configurations

set protocols ospf area 0.0.0.11 nssa

set protocols ospf area 0.0.0.11 interface ge-0/0/6.0 interface-type p2p

- R5:

- R6:

Interface ge-0/0/1 is in disable state

~~~> set interfaces ge-0/0/3 disable ~~~> delete interfaces ge-0/0/3 disable

- R7:

- R8:

Missing OSPF configurations

set protocols ospf area 0.0.0.10 interface ge-0/0/6.0

Task 4:

- R1:

[edit]

lab@R1# show protocols isis | display inheritance

##

## 'traffic-engineering' was inherited from group 'no-traffic'

## 'disable' was inherited from group 'no-traffic'

##

traffic-engineering disable;

level 1 {

wide-metrics-only;

}

level 2 {

wide-metrics-only;

}

Apply both traffic-engineering disable and wide-metrics-only under protocols ISIS will result in the total loss of ISIS routing information

~~~> delete apply-groups no-traffic

- --

set groups int\_inet6 interfaces  unit <\*> family inet6

set apply-groups int\_inet6

- R2:

set groups int\_inet6 interfaces  unit <\*> family inet6

set apply-groups int\_inet6

- --

Missing local sysid

~~~> set interfaces lo0 unit 0 family iso address 49.1111.1111.0102.1000.1002.00

~~~> set protocols isis no-ipv4-routing

- R3:

set groups int\_inet6 interfaces  unit <\*> family inet6

set apply-groups int\_inet6

- --

set protocols isis no-ipv4-routing

Missing enable interface ge-0/0/3.0, ge-0/0/5.0 in protocol isis   ~~~>

set protocols isis interface ge-0/0/3.0 point-to-point level 1 disable

set protocols isis interface ge-0/0/5.0 point-to-point level 2 disable

- R4:

set groups int\_inet6 interfaces  unit <\*> family inet6

set apply-groups int\_inet6

- --

R4-R8 setup L3 adjacency

~~~> set protocols isis level 2 disable

- R5:

set groups int\_inet6 interfaces  unit <\*> family inet6

set apply-groups int\_inet6

- --

Missing change interface type p2p on interface ge-0/0/5.0

~~~> set protocols isis interface ge-0/0/5.0 point-to-point

duplicate sysid to R3:

set interfaces lo0 unit 0 family iso address 49.1111.1111.0102.1000.1003.00

~~~>

delete interfaces lo0 unit 0 family iso address 49.1111.1111.0102.1000.1003.00

set interfaces lo0 unit 0 family iso address 49.1111.1111.0102.1000.1005.00

- R6:

set groups int\_inet6 interfaces  unit <\*> family inet6

set apply-groups int\_inet6

- --

set protocols isis no-ipv4-routing

Missing change interface type p2p on interface ge-0/0/1.0

~~~> set protocols isis interface ge-0/0/1.0 point-to-point level 1 disable

Interface ge-0/0/1 is missing family iso

~~~> set interfaces ge-0/0/3 unit 0 family iso

- R7:

set groups int\_inet6 interfaces  unit <\*> family inet6

set apply-groups int\_inet6

- --

set protocols isis no-ipv4-routing

- R8:

set groups int\_inet6 interfaces  unit <\*> family inet6

set apply-groups int\_inet6

- --

Disabled protocol ISIS

~~~> delete protocols isis disable

R4-R8 setup L3 adjacency

~~~> set protocols isis level 2 disable

Task 5:

- R3:

~~~>

set protocols ospf area 0.0.0.1 network-summary-export OSPF\_FILTER\_AREA0\_TO\_AREA1

set protocols ospf area 0.0.0.1 network-summary-import OSPF\_FILTER\_AREA1\_TO\_AREA0

set policy-options policy-statement OSPF\_FILTER\_AREA0\_TO\_AREA1 term ABR\_LOOPBACK from route-filter 10.210.1.3/32 exact

set policy-options policy-statement OSPF\_FILTER\_AREA0\_TO\_AREA1 term ABR\_LOOPBACK then accept

set policy-options policy-statement OSPF\_FILTER\_AREA0\_TO\_AREA1 term REJECT\_ALL then reject

set policy-options policy-statement OSPF\_FILTER\_AREA1\_TO\_AREA0 term REJECT\_ALL then reject

- R6:

~~~>

set protocols ospf area 0.0.0.1 network-summary-export OSPF\_FILTER\_AREA0\_TO\_AREA1

set protocols ospf area 0.0.0.1 network-summary-import OSPF\_FILTER\_AREA1\_TO\_AREA0

set policy-options policy-statement OSPF\_FILTER\_AREA0\_TO\_AREA1 term ABR\_LOOPBACK from route-filter 10.210.1.6/32 exact

set policy-options policy-statement OSPF\_FILTER\_AREA0\_TO\_AREA1 term ABR\_LOOPBACK then accept

set policy-options policy-statement OSPF\_FILTER\_AREA0\_TO\_AREA1 term REJECT\_ALL then reject

set policy-options policy-statement OSPF\_FILTER\_AREA1\_TO\_AREA0 term REJECT\_ALL then reject

Task 6:

- R3:

~~~>

set protocols isis interface ge-0/0/3.0 bfd-liveness-detection minimum-interval 100

set protocols isis interface ge-0/0/3.0 bfd-liveness-detection multiplier 5

~~~>

set protocols ospf area 0.0.0.0 interface ge-0/0/3.0 bfd-liveness-detection minimum-interval 100

set protocols ospf area 0.0.0.0 interface ge-0/0/3.0 bfd-liveness-detection multiplier 5

- R5:

~~~>

set protocols isis interface ge-0/0/3.0 bfd-liveness-detection minimum-interval 100

set protocols isis interface ge-0/0/3.0 bfd-liveness-detection multiplier 5

~~~>

set protocols ospf area 0.0.0.0 interface ge-0/0/3.0 bfd-liveness-detection minimum-interval 100

set protocols ospf area 0.0.0.0 interface ge-0/0/3.0 bfd-liveness-detection multiplier 5

Task 7:

- R3:

set protocols ospf3 area 0.0.0.10 interface ge-0/0/6.0

~~~>

set protocols ospf3 realm ipv4-unicast area 0.0.0.10 interface ge-0/0/6.0 interface-type p2p

set protocols ospf3 area 0.0.0.10 interface ge-0/0/6.0 interface-type p2p

- R4:

~~~>

set protocols ospf area 0.0.0.11 nssa

set protocols ospf area 0.0.0.11 interface ge-0/0/6.0 interface-type p2p

~~~> set protocols ripng group ripng neighbor ge-0/0/6.0

- R7:

set protocols ospf3 area 0.0.0.50 interface ge-0/0/6.0 interface-type p2p

~~~>

delete protocols ospf3 area 0.0.0.50

set protocols ospf3 area 0.0.0.10 interface ge-0/0/6.0 interface-type p2p

set protocols ospf3 realm ipv4-unicast area 0.0.0.10 interface ge-0/0/6.0 interface-type p2p

- R8:

set protocols ospf area 0.0.0.10 interface ge-0/0/6.0 interface-type p2p

~~~> delete protocols ospf area 0.0.0.10 interface ge-0/0/6.0 interface-type

~~~> set protocols ripng group ripng neighbor ge-0/0/6.0

Task 8:

- R3:

set protocols ospf3 realm ipv4-unicast import IMPORT\_OSPF3

set protocols ospf3 import IMPORT\_OSPF3

set policy-options policy-statement IMPORT\_OSPF3 term REJECT from route-filter 172.16.76.0/24 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT from route-filter 172.16.70.0/24 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT from route-filter 172.16.79.0/24 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT from route-filter 172.16.80.0/24 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT then reject

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_IPv6 from route-filter 2022:c:2:6::/64 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_IPv6 from route-filter 2022:c:2:7::/64 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_IPv6 from route-filter 2022:c:2:8::/64 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_IPv6 from route-filter 2022:c:2:9::/64 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_IPv6 from route-filter 2022:c:2:10::/64 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_IPv6 then reject

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_R7\_EXPORT\_ROUTES from protocol ospf3

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_R7\_EXPORT\_ROUTES from tag 18

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_R7\_EXPORT\_ROUTES then reject

- R4:

set protocols ospf import IMPORT\_OSPF

set protocols ripng import IMPORT\_RIPNG

set policy-options policy-statement IMPORT\_OSPF term REJECT from route-filter 172.16.0.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT from route-filter 172.16.1.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT from route-filter 172.16.2.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT from route-filter 172.16.3.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT from route-filter 172.16.4.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT from route-filter 172.16.5.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT from route-filter 172.16.6.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT from route-filter 172.16.7.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT then reject

set policy-options policy-statement IMPORT\_OSPF term REJECT\_R8\_EXPORT\_ROUTES from tag 48

set policy-options policy-statement IMPORT\_OSPF term REJECT\_R8\_EXPORT\_ROUTES then reject

set policy-options policy-statement IMPORT\_RIPNG term reject from route-filter 2022:c:1:0::/64 exact

set policy-options policy-statement IMPORT\_RIPNG term reject then reject

- R7:

set protocols ospf3 realm ipv4-unicast import IMPORT\_OSPF3

set protocols ospf3 import IMPORT\_OSPF3

set policy-options policy-statement IMPORT\_OSPF3 term REJECT from route-filter 172.16.76.0/24 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT from route-filter 172.16.70.0/24 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT from route-filter 172.16.79.0/24 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT from route-filter 172.16.80.0/24 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT then reject

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_IPv6 from route-filter 2022:c:2:6::/64 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_IPv6 from route-filter 2022:c:2:7::/64 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_IPv6 from route-filter 2022:c:2:8::/64 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_IPv6 from route-filter 2022:c:2:9::/64 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_IPv6 from route-filter 2022:c:2:10::/64 exact

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_IPv6 then reject

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_R7\_EXPORT\_ROUTES from protocol ospf3

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_R7\_EXPORT\_ROUTES from tag 18

set policy-options policy-statement IMPORT\_OSPF3 term REJECT\_R7\_EXPORT\_ROUTES then reject

- R8:

set protocols ospf import IMPORT\_OSPF

set protocols ripng import IMPORT\_RIPNG

set policy-options policy-statement IMPORT\_OSPF term REJECT\_UNACCEPT\_ROUTES from route-filter 172.16.0.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT\_UNACCEPT\_ROUTES from route-filter 172.16.1.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT\_UNACCEPT\_ROUTES from route-filter 172.16.2.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT\_UNACCEPT\_ROUTES from route-filter 172.16.3.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT\_UNACCEPT\_ROUTES from route-filter 172.16.4.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT\_UNACCEPT\_ROUTES from route-filter 172.16.5.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT\_UNACCEPT\_ROUTES from route-filter 172.16.6.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT\_UNACCEPT\_ROUTES from route-filter 172.16.7.0/24 exact

set policy-options policy-statement IMPORT\_OSPF term REJECT\_UNACCEPT\_ROUTES then reject

set policy-options policy-statement IMPORT\_OSPF term REJECT\_R4\_EXPORT\_ROUTES from tag 48

set policy-options policy-statement IMPORT\_OSPF term REJECT\_R4\_EXPORT\_ROUTES then reject

set policy-options policy-statement IMPORT\_RIPNG term reject from route-filter 2022:c:1:0::/64 exact

set policy-options policy-statement IMPORT\_RIPNG term reject then reject

Task 9:

- R1:

set routing-options rib inet6.0 aggregate route 2022:c:1::/61

set routing-options aggregate route 172.16.0.0/19

set protocols isis export EXPORT\_ISIS

set protocols ospf export EXPORT\_OSPF

set policy-options policy-statement EXPORT\_ISIS term EXTERNAL\_L1\_SUMMARY from protocol aggregate

set policy-options policy-statement EXPORT\_ISIS term EXTERNAL\_L1\_SUMMARY from route-filter 2022:c:1::/61 exact

set policy-options policy-statement EXPORT\_ISIS term EXTERNAL\_L1\_SUMMARY to level 2

set policy-options policy-statement EXPORT\_ISIS term EXTERNAL\_L1\_SUMMARY then accept

set policy-options policy-statement EXPORT\_OSPF term SRC\_AGGREGATE from protocol aggregate

set policy-options policy-statement EXPORT\_OSPF term SRC\_AGGREGATE from route-filter 172.16.0.0/19 exact

set policy-options policy-statement EXPORT\_OSPF term SRC\_AGGREGATE then accept

- R3:

- R5:

- R6:

Task 10:

- R1:

- R2:

- R3:

- R4:

- R5:

- R6:

- R7:

- R8:

Task 11:

- R1:

- R2:

- R3:

- R4:

- R5:

- R6:

- R7:

- R8:

Task 12:

- R1:

- R2:

- R3:

- R4:

- R5:

- R6:

- R7:

- R8:

Task 13:

- R1:

- R2:

- R3:

- R4:

- R5:

- R6:

- R7:

- R8:

Task 14:

- R1:

- R2:

- R3:

- R4:

- R5:

- R6:

- R7:

- R8:

Task 15:

- R1:

- R2:

- R3:

- R4:

- R5:

- R6:

- R7:

- R8:
