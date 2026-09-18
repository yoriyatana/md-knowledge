# L2VPN, VPLS, and CCC Configuration

> Generated deterministically from the approved grouping manifest.


## Source: `formatted/TS_notes/L2circuit.md`

# L2circuit

show l2circuit connections history

show l2circuit connections instance-history

## Source: `formatted/TS_notes/Configure connection CCC example.md`

# Configure connection CCC example

lab@MX204-01> show configuration | compare

[edit interfaces xe-0/1/5]

+ unit 2000 {

+ encapsulation vlan-ccc;

+ vlan-id-list [ 2000-2100 4000 ];

+ }

[edit interfaces ae100]

[edit protocols]

+ mpls {

+ interface xe-0/1/5.2000;

+ interface ae100.2000;

+ connections {

+ interface-switch EndUser\_to\_SRT {

[edit interfaces xe-0/1/0]

+ description To-MX104\_01-ge-0/0/3;

+ mtu 9192;

+ encapsulation ethernet-ccc;

+ unit 0 {

+ family ccc;

[edit interfaces xe-0/1/1]

+ description To-MX104\_01-ge-0/0/4;

[edit protocols mpls]

+ interface xe-0/1/0.0;

+ interface xe-0/1/1.0;

[edit protocols connections]

+ interface-switch LOOP\_MX960\_02 {

## Source: `formatted/Learning_Notes/EoMPLS VC Type.md`

# EoMPLS VC Type

Are you talking about EoMPLS VC Type? If Yes so

VC Type 4 is used for Ethernet VLAN mode.

VC Type 5 is used for Ethernet Port mode.

- --

you are referring to EoMPLS Pseudowire Types (which are better defined in rfc4446 and not 4448) and indeed there are 2 ways to handle tags.

VC Type 4 : The original 802.1Q tag is inserted in the EoMPLS payload (along with the MPLS label) before forwarding it to the MPLS core. At the ingress of the remote end or receiving PE the 802.1Q tag is stripped off before its transmission to the internal bus. If a packet is received from the MPLS core without a tag (ether type of the packet is other than 0x8100) the packet is dropped.

VC Type 5 : In EoMPLS VLAN mode configuration, only the MPLS label is added to the packet transmitted to the MPLS core. On the ingress of the remote end or receiving PE the MPLS label stack is popped out before the transmission on the internal bus. If Port mode is configured instead, the 802.1Q tag is also carried along with the MPLS label

The actions taken by the PE interfaces facing the CE are solely determined by the specific interface configuration. If such configuration requires 802.1Q tagging, the egress frame is tagged; otherwise the egress frame is sent untagged. EoMPLS VC type 5 is the default configuration mode on the platforms supporting it. Meaning that the PEs will try to first negotiate and use VC 5, if one of them (or both) does not support it they will reverse to VC 4. EoMPLS type VLAN offers backward compatibility in case the remote peer does not support VC type Ethernet.

VC type 4 or VC type 5 is not a configurable option and is platform dependent, the capability is instead auto

sensed at control plane level"

## Source: `formatted/TS_notes/Qui tắc về forwarding traffic với VPLS mesh-group.md`

# Qui tắc về forwarding traffic với VPLS mesh-group

Qui tắc về forwarding traffic với VPLS mesh-group:

● CE mesh-group (group mặc định)

○ Tất cả các interface nối đến CE sẽ nằm trong group này

○ Local-switching ON (default), có thể OFF bằng cách dùng no-local-switching ở mức [routing-instance ].

○ Lưu ý, traffic multicast không bị ảnh hưởng bởi lệnh no-local-switching.

○ Flood traffic đến VE mesh-group và tất cả các mesh-group định nghĩa thêm

● VE mesh-group (group mặc định)

○ Tất cả các neighbor (pw) nếu không nằm trong mesh-group nào thì sẽ nằm trong

mesh-group này

○ mặc định là no-local-switching, không thể thay đổi.

○ Floods tới CE mesh-group và tất cả mesh-group được định nghĩa thêm

● mesh-group định nghĩa thêm:

- mặc định no-local-switching, có thể thay đổi bằng lệnh local-switching ở mức

[routing-instance  protocols vpls mess-group ]

- Floods tới CE meshgroup và tất cả mesh-group khác

Cấu hình core-facing:

- Tại [interfaces  unit  family vpls]

- Config này chuyển CE interface từ CE meshgroup tới VE mesh-group (default mesh-group).

Lệnh này sẽ cách ly hoàn toàn traffic giữa các port CE, kể cả traffic multicast.
