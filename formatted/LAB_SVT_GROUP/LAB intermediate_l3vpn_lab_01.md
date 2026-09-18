# LAB intermediate_l3vpn_lab_01

- --

LAB L3VPN

- --

Task 1:

- R1:

[edit]

+ routing-options {

+ autonomous-system 123;

+ }

[edit protocols]

+ bgp {

```text
group RR {
```

+ type internal;

+ local-address 10.210.1.1;

+ family inet-vpn {

+ unicast;

+ }

+ family inet6-vpn {

+ unicast;

+ }

+ neighbor 10.210.1.10;

+ }

+ }

[edit protocols]

+ mpls {

+ interface all;

+ }

+ ldp {

+ interface all;

+ }

- R2:

[edit]

+ routing-options {

+ autonomous-system 123;

+ }

[edit protocols]

+ bgp {

```text
group RR {
```

+ type internal;

+ local-address 10.210.1.2;

+ family inet-vpn {

+ unicast;

+ }

+ family inet6-vpn {

+ unicast;

+ }

+ neighbor 10.210.1.10;

+ }

+ }

[edit protocols]

+ mpls {

+ interface all;

+ }

+ ldp {

+ interface all;

+ }

- R3:

z[edit]

+ routing-options {

+ autonomous-system 123;

+ }

[edit protocols]

+ bgp {

```text
group RR {
```

+ type internal;

+ local-address 10.210.1.4;

+ family inet-vpn {

+ unicast;

+ }

+ family inet6-vpn {

+ unicast;

+ }

+ neighbor 10.210.1.10;

+ }

+ }

[edit protocols]

+ mpls {

+ interface all;

+ }

+ ldp {

+ interface all;

+ }

- R4:

[edit]

+ routing-options {

+ autonomous-system 123;

+ }

[edit protocols]

+ bgp {

```text
group RR {
```

+ type internal;

+ local-address 10.210.1.4;

+ family inet-vpn {

+ unicast;

+ }

+ family inet6-vpn {

+ unicast;

+ }

+ neighbor 10.210.1.10;

+ }

+ }

[edit protocols ospf area 0.0.0.0]

interface ge-0/0/2.0 { ... }

+ interface lo0.0;

[edit protocols]

+ mpls {

+ interface all;

+ }

+ ldp {

+ interface all;

+ }

- R5:

[edit]

+ routing-options {

+ autonomous-system 123;

+ }

[edit protocols]

+ bgp {

```text
group RR {
```

+ type internal;

+ local-address 10.210.1.5;

+ family inet-vpn {

+ unicast;

+ }

+ family inet6-vpn {

+ unicast;

+ }

+ neighbor 10.210.1.10;

+ }

+ }

[edit protocols]

+ mpls {

+ interface all;

+ }

+ ldp {

+ interface all;

+ }

- R6:

[edit]

+ routing-options {

+ autonomous-system 123;

+ }

[edit protocols]

+ bgp {

```text
group RR {
```

+ type internal;

+ local-address 10.210.1.6;

+ family inet-vpn {

+ unicast;

+ }

+ family inet6-vpn {

+ unicast;

+ }

+ neighbor 10.210.1.10;

+ }

+ }

[edit protocols]

+ mpls {

+ interface all;

+ }

+ ldp {

+ interface all;

+ }

- RR:

[edit routing-options]

+ rib inet.3 {

+ static {

+ route 0.0.0.0/0 discard;

+ }

+ }

+ rib inet6.3 {

+ static {

+ route ::/0 discard;

+ }

+ }

[edit protocols]

+ bgp {

```text
group PE {
```

+ type internal;

+ local-address 10.210.1.10;

+ family inet-vpn {

+ unicast;

+ }

+ family inet6-vpn {

+ unicast;

+ }

+ cluster 10.210.1.10;

+ neighbor 10.210.1.1;

+ neighbor 10.210.1.2;

+ neighbor 10.210.1.3;

+ neighbor 10.210.1.4;

+ neighbor 10.210.1.5;

+ neighbor 10.210.1.6;

+ }

+ }

Task 2:

- R1:

[edit interfaces]

+ ge-0/0/5 {

+ apply-groups-except interface-family;

+ flexible-vlan-tagging;

+ encapsulation flexible-ethernet-services;

+ unit 11 {

+ vlan-id 11;

+ family inet {

+ address 10.100.1.1/30;

+ }

+ }

+ }

[edit]

+ policy-options {

+ policy-statement EXPORT\_OSPF {

+ term src\_BGP {

+ from protocol bgp;

+ then accept;

+ }

+ }

+ }

+ routing-instances {

+ C1 {

+ instance-type vrf;

+ interface ge-0/0/5.11;

+ route-distinguisher 10.210.1.1:1;

+ vrf-target target:123:1;

+ vrf-table-label;

+ protocols {

+ ospf {

+ export EXPORT\_OSPF;

+ area 0.0.0.1 {

+ interface ge-0/0/5.11 {

+ interface-type p2p;

+ }

+ }

+ }

+ }

+ }

+ }

- R2:

[edit interfaces]

+ ge-0/0/5 {

+ apply-groups-except interface-family;

+ flexible-vlan-tagging;

+ encapsulation flexible-ethernet-services;

+ unit 13 {

+ vlan-id 13;

+ family inet {

+ address 10.100.1.9/30;

+ }

+ }

+ }

[edit]

+ policy-options {

+ policy-statement EXPORT\_OSPF {

+ term src\_BGP {

+ from protocol bgp;

+ then accept;

+ }

+ }

+ }

+ routing-instances {

+ C1 {

+ instance-type vrf;

+ interface ge-0/0/5.13;

+ route-distinguisher 10.210.1.2:1;

+ vrf-target target:123:1;

+ vrf-table-label;

+ protocols {

+ ospf {

+ export EXPORT\_OSPF;

+ area 0.0.0.3 {

+ interface ge-0/0/5.13 {

+ interface-type p2p;

+ }

+ }

+ }

+ }

+ }

+ }

- R6:

[edit interfaces]

+ ge-0/0/5 {

+ apply-groups-except interface-family;

+ flexible-vlan-tagging;

+ encapsulation flexible-ethernet-services;

+ unit 13 {

+ vlan-id 13;

+ family inet {

+ address 10.100.1.9/30;

+ }

+ }

+ }

[edit]

+ policy-options {

+ policy-statement EXPORT\_OSPF {

+ term src\_BGP {

+ from protocol bgp;

+ then accept;

+ }

+ }

+ }

+ routing-instances {

+ C1 {

+ instance-type vrf;

+ interface ge-0/0/5.12;

+ route-distinguisher 10.210.1.6:1;

+ vrf-target target:123:1;

+ vrf-table-label;

+ protocols {

+ ospf {

+ export EXPORT\_OSPF;

+ area 0.0.0.2 {

+ interface ge-0/0/5.12 {

+ interface-type p2p;

+ }

+ }

+ }

+ }

+ }

+ }

Task 3:

- R1:

[edit interfaces ge-0/0/5]

+ unit 21 {

+ vlan-id 21;

+ family inet {

+ address 10.100.2.1/30;

+ }

+ family inet6 {

+ address ::10:100:2:1/126;

+ }

+ }

[edit policy-options]

+ policy-statement VRF\_EXPORT\_C2 {

+ term src\_BGP {

+ then {

+ community add target:123:222;

+ accept;

+ }

+ }

+ }

+ policy-statement VRF\_IMPORT\_C2 {

+ term src\_BGP {

+ from community target:123:111;

+ then accept;

+ }

+ }

[edit policy-options]

+ community target:123:111 members target:123:111;

+ community target:123:222 members target:123:222;

[edit routing-instances]

+ C2 {

+ instance-type vrf;

+ interface ge-0/0/5.21;

+ route-distinguisher 10.210.1.1:2;

+ vrf-import VRF\_IMPORT\_C2;

+ vrf-export VRF\_EXPORT\_C2;

+ vrf-table-label;

+ protocols {

+ bgp {

```text
group S1 {
```

+ type external;

+ family inet {

+ unicast;

+ }

+ family inet6 {

+ unicast;

+ }

+ peer-as 20;

+ as-override;

+ neighbor 10.100.2.2;

+ }

+ }

+ }

+ }

- R6:

[edit interfaces ge-0/0/5]

+ unit 22 {

+ vlan-id 22;

+ family inet {

+ address 10.100.2.5/30;

+ }

+ family inet6 {

+ address ::10:100:2:5/126;

+ }

+ }

[edit policy-options]

+ policy-statement VRF\_EXPORT\_C2 {

+ term src\_BGP {

+ then {

+ community add target:123:111;

+ accept;

+ }

+ }

+ }

+ policy-statement VRF\_IMPORT\_C2 {

+ term src\_BGP {

+ from community target:123:222;

+ then accept;

+ }

+ }

[edit policy-options]

+ community target:123:111 members target:123:111;

+ community target:123:222 members target:123:222;

[edit routing-instances]

+ C2 {

+ instance-type vrf;

+ interface ge-0/0/5.22;

+ route-distinguisher 10.210.1.6:2;

+ vrf-import VRF\_IMPORT\_C2;

+ vrf-export VRF\_EXPORT\_C2;

+ vrf-table-label;

+ protocols {

+ bgp {

```text
group S2 {
```

+ type external;

+ family inet {

+ unicast;

+ }

+ family inet6 {

+ unicast;

+ }

+ peer-as 20;

+ as-override;

+ neighbor 10.100.2.6;

+ }

+ }

+ }

+ }

Task 4:

- R1:

[edit protocols mpls]

+ ipv6-tunneling;

[edit policy-options]

+ policy-statement EXPORT\_BGP\_S1 {

+ term reset\_v6\_NH {

+ from {

+ protocol bgp;

+ rib C2.inet6.0;

+ }

+ then {

+ next-hop ::10:100:2:1;

+ accept;

+ }

+ }

+ }

+ policy-statement IMPORT\_BGP\_S1 {

+ term reset\_v6\_NH {

+ from {

+ rib inet6.0;

+ next-hop ::ffff:10.100.2.2;

+ }

+ then {

+ next-hop ::10.100.2.2;

+ accept;

+ }

+ }

+ }

[edit routing-instances C2 protocols bgp group S1 neighbor 10.100.2.2]

+ import IMPORT\_BGP\_S1;

+ export EXPORT\_BGP\_S1;

- R2:

[edit protocols mpls]

+ ipv6-tunneling;

- R3:

[edit protocols mpls]

+ ipv6-tunneling;

- R4:

[edit protocols mpls]

+ ipv6-tunneling;

- R5:

[edit protocols mpls]

+ ipv6-tunneling;

- R6:

[edit protocols mpls]

+ ipv6-tunneling;

[edit policy-options]

+ policy-statement EXPORT\_BGP\_S2 {

+ term reset\_v6\_NH {

+ from {

+ protocol bgp;

+ rib C2.inet6.0;

+ }

+ then {

+ next-hop ::10:100:2:5;

+ accept;

+ }

+ }

+ }

+ policy-statement IMPORT\_BGP\_S2 {

+ term reset\_v6\_NH {

+ from {

+ rib inet6.0;

+ next-hop ::ffff:10.100.2.6;

+ }

+ then {

+ next-hop ::10.100.2.6;

+ accept;

+ }

+ }

+ }

[edit routing-instances C2 protocols bgp group S2 neighbor 10.100.2.6]

+ import IMPORT\_BGP\_S2;

+ export EXPORT\_BGP\_S2;

Task 5:

- R3:

[edit interfaces ge-0/0/5]

+ apply-groups-except interface-family;

+ flexible-vlan-tagging;

+ encapsulation flexible-ethernet-services;

+ unit 32 {

+ vlan-id 32;

+ family inet {

+ address 10.100.3.5/30;

+ }

+ }

+ unit 33 {

+ vlan-id 33;

+ family inet {

+ address 10.100.3.9/30;

+ }

+ }

[edit]

+ policy-options {

+ policy-statement EXPORT\_BGP\_S3 {

+ term redis\_ospf {

+ from protocol ospf;

+ then accept;

+ }

+ }

+ policy-statement EXPORT\_OSPF {

+ term src\_BGP {

+ from protocol bgp;

+ then accept;

+ }

+ }

+ }

+ routing-instances {

+ C3 {

+ instance-type vrf;

+ interface ge-0/0/5.32;

+ interface ge-0/0/5.33;

+ route-distinguisher 10.210.1.3:3;

+ vrf-target target:123:3;

+ vrf-table-label;

+ protocols {

+ bgp {

```text
group S3 {
```

+ type external;

+ peer-as 321;

+ neighbor 10.100.3.10 {

+ export EXPORT\_BGP\_S3;

+ }

+ }

+ }

+ ospf {

+ export EXPORT\_OSPF;

+ area 0.0.0.0 {

+ interface ge-0/0/5.32 {

+ interface-type p2p;

+ }

+ }

+ }

+ }

+ }

+ }

- R4:

[edit interfaces]

+ ge-0/0/5 {

+ apply-groups-except interface-family;

+ flexible-vlan-tagging;

+ encapsulation flexible-ethernet-services;

+ unit 31 {

+ vlan-id 31;

+ family inet {

+ address 10.100.3.1/30;

+ }

+ }

+ }

[edit]

+ policy-options {

+ policy-statement EXPORT\_OSPF {

+ term src\_BGP {

+ from protocol bgp;

+ then accept;

+ }

+ }

+ }

+ routing-instances {

+ C3 {

+ instance-type vrf;

+ interface ge-0/0/5.31;

+ route-distinguisher 10.210.1.4:3;

+ vrf-target target:123:3;

+ vrf-table-label;

+ routing-options {

+ router-id 10.100.3.2;

+ }

+ protocols {

+ ospf {

+ export EXPORT\_OSPF;

+ area 0.0.0.0 {

+ interface ge-0/0/5.31 {

+ interface-type p2p;

+ }

+ }

+ }

+ }

+ }

+ }

Task 6:

- R3:

~

- R5:

~

Task 7:

- R5:

[edit interfaces ge-0/0/5]

+ unit 100 {

+ vlan-id 100;

+ family inet {

+ address 10.100.100.1/30;

+ }

+ }

[edit routing-options]

+ static {

+ route 0.0.0.0/0 next-hop 10.100.100.2;

+ }

[edit protocols bgp group RR]

+ family inet {

+ unicast;

+ }

+ export EXPORT\_RR;

[edit]

+ policy-options {

+ policy-statement EXPORT\_RR {

+ term export\_default {

+ from {

+ rib inet.0;

+ route-filter 0.0.0.0/0 exact;

+ }

+ then {

+ next-hop self;

+ accept;

+ }

+ }

+ }

+ }

- R4:

[edit routing-options]

+ rib-groups {

+ LEAK\_C3\_S1\_TO\_INET0 {

+ import-rib [ C3.inet.0 inet.0 ];

+ import-policy LEAK\_C3\_S1\_TO\_INET0;

+ }

+ }

[edit protocols bgp group RR]

+ family inet {

+ unicast;

+ }

+ export EXPORT\_RR;

[edit policy-options policy-statement EXPORT\_OSPF term src\_BGP from]

- protocol bgp;

+ protocol [ bgp static ];

[edit policy-options]

+ policy-statement EXPORT\_RR {

+ term 1 {

+ from community C3\_S1;

+ then {

+ next-hop self;

+ accept;

+ }

+ }

+ }

+ policy-statement EXPORT\_VRF\_C3\_S1 {

+ term 1 {

+ from protocol [ ospf direct ];

+ then {

+ community add target:123:3;

+ accept;

+ }

+ }

+ term FINAL {

+ then reject;

+ }

+ }

+ policy-statement IMPORT\_VRF\_C3\_S1 {

+ term 1 {

+ from community target:123:3;

+ then accept;

+ }

+ term FINAL {

+ then reject;

+ }

+ }

+ policy-statement LEAK\_C3\_S1\_TO\_INET0 {

+ term 1 {

+ then {

+ tag 321;

+ community add C3\_S1;

+ }

+ }

+ }

[edit policy-options]

+ community C3\_S1 members 123:3;

+ community target:123:3 members target:123:3;

[edit routing-instances C3]

+ vrf-import IMPORT\_VRF\_C3\_S1;

+ vrf-export EXPORT\_VRF\_C3\_S1;

- vrf-target target:123:3;

[edit routing-instances C3 routing-options]

+ interface-routes {

+ rib-group inet LEAK\_C3\_S1\_TO\_INET0;

+ }

+ static {

+ route 0.0.0.0/0 next-table inet.0;

+ }

[edit routing-instances C3 protocols ospf]

+ rib-group LEAK\_C3\_S1\_TO\_INET0;
