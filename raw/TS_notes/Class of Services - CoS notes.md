# Class of Services - CoS notes

set cli timestamp

###1/ Kiểm tra cấu hình forwarding class cấu hình:

show class-of-service forwarding-class

###2/ Kiểm tra các BA classifier đã cấu hình:

show class-of-service classifier name CL\_DSCP

show class-of-service classifier name CL\_802.1p

show class-of-service classifier name CL\_EXP

###3/ Kiểm tra các re-write rule cấu hình:

show class-of-service rewrite-rule name RW\_DSCP

show class-of-service rewrite-rule name RW\_EXP

show class-of-service rewrite-rule name RW\_802.1p

###4/ Kiểm tra scheduler-map đã cấu hình:

show class-of-service scheduler-map SCH-MAP

###5/ Kiểm tra các interface đã cấu hình CoS:

show class-of-service interface ae9

###6/Kiểm tra egress traffic queue tương ứng mỗi forwarding class:

show interfaces queue ae9 egress forwarding-class FTTX

###7/ Kiểm tra classifier mức PFE (apply xuống line card)

show class-of-service classifier name CL-DSCP

start shell pfe network fpc7

show cos classifier 25562

###8/ Check forwarding class ở PFE:

show class-of-service forwarding-class

start shell pfe network fpc7

show cos forwarding-class table

###9/ Kiểm tra rewrite rule ở PFE:

show cos rewrite 60698    ###giá trị này nằm ở lệnh show mục 3

###10/Kiểm tra scheduler trên linecard:

show class-of-service scheduler-hierarchy fpc slot 7

start shell pfe network fpc7

show cos scheduler-hierarchy

###

show interfaces ge-3/2/1 extensive | find queue counters

show interfaces queue ge-3/2/1 | find queue

CLI

show class-of-service interface ge-2/2/1 comprehensive (2 times)

show class-of-service interface ge-2/2/1 detail

show class-of-service scheduler-map

FPC shell

show cos halp ifl

show cos halp ifd

show cos scheduling-policy

show interfaces queue egress ae13 | match \"Queue|Tail-\"

---

Here are my findings:

When interface is not congested then traffic will be scheduled based on Priority Queuing and Packet based Round Robin (PQ-RR).

Therefore, in this case all queues will be scheduled in the following way:

- Packets in strict-high and high queues are transmitted first

- Packets in medium-high and medium-low queues are transmitted next

- Packets in low queue are transmitted in the end

So, as per below scheduler configuration and for in-profile traffic, queues that map to the same hardware priority are given equal priority.

Even if they are configured with different transmit-rates, the queues are processed in a packet based round robin manner.

However buffer size defines the number of packets that can be queued or buffered and hence due to less buffer space available in queue 0 and high traffic rate then other low priority queues tail drops areexpected in case of burst.

Note: Burst will not reflect on SNMP traffic graph as it has polling rate is around 1 sec and burst is measured in milliseconds.

---

Can you give

CLI config (TCP, shaper and queues)

show cos halp ifl X

show qx N tail-rule Y 0 0

show qx N q Z queue-length

With two different temporal values in queues.

Remember that you must configure guaranteed-rate for shaping to work in QX as

accustomed to DPCE and MQ. Otherwise all your queues are in excess region.

---

Hi Saku,

Requested outputs below (this is not a finished policy, for now I'm just

playing with buffers mainly).

IFD is in PIR mode as only PIR is configured (interface could be

oversubscribed so configuring guaranteed rate doesn't make sense). As I

understand it, queues are therefore always in excess (apart from

rate-limited queue) with weight proportional to the transmit-rate (correct

me if I am wrong).

Thanks,

Dan

--

class-of-service {

traffic-control-profiles {

10M {

scheduler-map 10M\_COS;

shaping-rate 10m;

}

}

interfaces {

xe-0/0/1 {

unit 2000 {

output-traffic-control-profile 10M;

}

}

}

scheduler-maps {

10M\_COS {

forwarding-class Q5 scheduler RT;

forwarding-class Q2 scheduler SIG;

forwarding-class Q1 scheduler PRI;

forwarding-class Q3 scheduler NC;

forwarding-class Q0 scheduler BE;

}

}

schedulers {

NC {

transmit-rate percent 1;

buffer-size temporal 500k;

priority medium-high;

excess-priority high;

}

RT {

transmit-rate {

percent 24;

rate-limit;

}

buffer-size temporal 20k;

priority high;

}

SIG {

transmit-rate percent 2;

buffer-size temporal 500k;

}

PRI {

transmit-rate percent 24;

buffer-size temporal 165k;

}

BE {

transmit-rate percent 24;

buffer-size temporal 165k;

}

}

}

NPC0(pe1-RE0 vty)# show cos halp ifl 329

IFL type: Basic

--------------------------------------------------------------------------------

IFL name: (xe-0/0/1.2000, xe-0/0/1)   (Index 329, IFD Index 164)

QX chip id: 0

QX chip dummy L2 index: 4

QX chip Scheduler: 4

QX chip L3 index: 4

QX chip base Q index: 32

Number of queues: 8

Queue    State        Max       Guaranteed   Burst  Weight Priorities

Drop-Rules

Index                 rate         rate      size            G    E   Wred

Tail

------ ----------- ----------- ------------ ------- ------ ----------

----------

32  Configured    10000000            0  131072    320   GL   EL    4

0

33  Configured    10000000            0  131072    320   GL   EL    4

0

34  Configured    10000000            0  131072     26   GL   EL    4

0

35  Configured    10000000            0  131072     13   GM   EH    4

127

36  Configured    10000000            0  131072      1   GL   EL    0

255

37  Configured    10000000      2400000  131072    320   GH   EH    4

193

38  Configured    10000000            0  131072      1   GL   EL    0

255

39  Configured    10000000            0  131072      1   GL   EL    0

255

Rate limit info:

Q 5: Bandwidth = 2400000, Burst size = 73536. Policer NH:

0x3077afaa0003b000

Index NH: 0xda4be18980801006

NPC0(pe1-RE0 vty)# show qxchip 0 tail-rule 33 0 0

Tail drop rule configuration   : 33

ref\_count    : 0

Drop Engine 0   :

Tail drop rule ram address   : 00000840

threshold    : 2686976 bytes

shift   : 14

mantissa   : 164

Drop Engine 1   :

Tail drop rule ram address   : 00000840

threshold    : 2686976 bytes

shift   : 14

mantissa   : 164

NPC0(pe1-RE0 vty)# show qxchip 0 tail-rule 34 0 0

Tail drop rule configuration   : 34

ref\_count    : 0

Drop Engine 0   :

Tail drop rule ram address   : 00000880

threshold    : 2801664 bytes

shift   : 14

mantissa   : 171

Drop Engine 1   :

Tail drop rule ram address   : 00000880

threshold    : 2801664 bytes

shift   : 14

mantissa   : 171

NPC0(pe1-RE0 vty)# show qxchip 0 q 32 queue-length

QX Queue Index: 32

Current instantaneous queue depth : 0 bytes

WRED TAQL queue depth             : 0 bytes

Configured queue depth:

region   color   queue-depth

------   -----   -----------

0       0         4096

0       1         4096

0       2         4096

0       3         4096

1       0         3264

1       1         3264

1       2         3264

1       3         3264

2       0         512

2       1         512

2       2         512

2       3         512

3       0         0

3       1         0

3       2         0

3       3         0

---

admin@router-re0> show class-of-service scheduler-hierarchy interface pp0.5020

---

NGMPC3(jtac-mx480-r2046 vty)# show xqchip 0 drop tail-drop-rule rule 9

Tail drop rule configuration   : 9

ref\_count    : 0

region color threshold\_bytes     tail-ram-addr   mantissa shift

------ ----- ---------------     -------------   -------- -----

0     0             4736           1152           148      5

0     1             4736           1184           148      5

0     2             4736           1216           148      5

0     3             4736           1248           148      5

1     0             4736           1156           148      5

1     1             4736           1188           148      5

1     2             4736           1220           148      5

1     3             4736           1252           148      5

2     0             4736           1160           148      5

---

NGMPC3(jtac-mx480-r2046 vty)# show xqchip 0 drop info

Tail drop rule configuration:

----------------------------

Rule Map: 1 rules 1024 regions 8 colors 4

Number of rules: allocated 799  free 225

---

In this example, FPC 3 is MPC3E NG HQoS, which is an XQ-based card.

labroot@jtac-mx480-r2046# run show interfaces queue xe-3/2/0.100

labroot@jtac-mx480-r2046# run show class-of-service interface xe-3/2/0.100 comprehensive

<https://supportportal.juniper.net/s/article/MX-Example-Queue-depth-calculation-on-QX-based-cards>

<https://supportportal.juniper.net/s/article/MX-Example-Queue-depth-calculation-on-Next-Generation-XQ-based-cards?language=en_US>

---

sho cos scheduler-hierarchy

sho cos halp ifl 171

--

ftelsuper@HCMM005402620MX48-re1> show configuration | match ae8 | display set

set interfaces xe-0/2/3 description "PORT-HCMM005402620MX48[xe-0/2/3](ae8)-TPBank[Port](Eth)"

set interfaces xe-0/2/3 gigether-options 802.3ad ae8

---

NPC0(HCMM005402620MX48-re1 vty)# show cos scheduler-hierarchy

class-of-service egress scheduler hierarchy - rates in kbps

-------------------------------------------------------------------------------------

shaping guarntd delaybf  excess

interface name                   index    rate    rate    rate    rate      other

---------------------------- ---------  ------- ------- ------- ------- -------------

xe-0/0/0                           158        0       0       0       0

xe-0/0/1                           159        0       0       0       0

xe-0/0/2                           160        0       0       0       0

xe-0/0/3                           161        0       0       0       0

xe-0/0/4                           162        0       0       0       0

xe-0/0/5                           163        0       0       0       0

xe-0/0/6                           164        0       0       0       0

xe-0/0/7                           165        0       0       0       0

xe-0/0/8                           166        0       0       0       0

q 0 - pri 1/0                  31478        0     15%     15%       0

q 1 - pri 1/0                  31478        0     30%     30%       0

q 2 - pri 2/0                  31478        0     10%     10%       0

q 3 - pri 4/0                  31478        0      5%      5%       0

q 4 - pri 3/0                  31478        0     15%     15%       0

q 5 - pri 3/0                  31478        0     20%     10%       0

q 6 - pri 3/0                  31478        0      5%      5%       0

xe-0/0/9                           167        0       0       0       0

q 0 - pri 1/0                  31479        0     15%     15%       0

q 1 - pri 1/0                  31479        0     30%     30%       0

q 2 - pri 2/0                  31479        0     10%     10%       0

q 3 - pri 4/0                  31479        0      5%      5%       0

q 4 - pri 3/0                  31479        0     15%     15%       0

q 5 - pri 3/0                  31479        0     20%     10%       0

q 6 - pri 3/0                  31479        0      5%      5%       0

xe-0/2/0                           168        0       0       0       0

xe-0/2/1                           169        0       0       0       0

xe-0/2/2                           170        0       0       0       0

q 0 - pri 1/0                   7936        0     15%     15%       0

q 1 - pri 1/0                   7936        0     30%     30%       0

q 2 - pri 2/0                   7936        0     10%     10%       0

q 3 - pri 4/0                   7936        0      5%      5%       0

q 4 - pri 3/0                   7936        0     15%     15%       0

q 5 - pri 3/0                   7936        0     20%     10%       0

q 6 - pri 3/0                   7936        0      5%      5%       0

xe-0/2/3                           171        0       0       0       0

xe-0/2/4                           172        0       0       0       0

xe-0/2/5                           173        0       0       0       0

xe-0/2/6                           174        0       0       0       0

xe-0/2/7                           175        0       0       0       0

xe-0/2/8                           176        0       0       0       0

q 0 - pri 1/0                  29430        0     15%     15%       0

q 1 - pri 1/0                  29430        0     30%     30%       0

q 2 - pri 2/0                  29430        0     10%     10%       0

q 3 - pri 4/0                  29430        0      5%      5%       0

q 4 - pri 3/0                  29430        0     15%     15%       0

q 5 - pri 3/0                  29430        0     20%     10%       0

q 6 - pri 3/0                  29430        0      5%      5%       0

xe-0/2/9                           177        0       0       0       0

q 0 - pri 1/0                  29431        0     15%     15%       0

q 1 - pri 1/0                  29431        0     30%     30%       0

q 2 - pri 2/0                  29431        0     10%     10%       0

q 3 - pri 4/0                  29431        0      5%      5%       0

q 4 - pri 3/0                  29431        0     15%     15%       0

q 5 - pri 3/0                  29431        0     20%     10%       0

q 6 - pri 3/0                  29431        0      5%      5%       0

--

Logical interface ae5.922

Flags: Up SNMP-Traps 0x4000 VLAN-Tag [ 0x8100.922 ]  Encapsulation: ENET2

inet  42.112.145.113/29

42.112.145.114/29

inet6 fe80::e6fc:8203:9aa5:2fc4/64

multiservice

Interface       Admin Link Proto Input Filter         Output Filter

ae5.922         up    up   inet                       FTI-Direct-SGLD50048-Toyota-1-OUT-ae5.922-o

inet6                      IPv6-FTI-Direct-SGLD50048-Toyota-1-OUT-ae5.922-o

multiservice

Interface       Admin Link Proto Input Policer         Output Policer

ae5.922         up    up

inet

inet6

multiservice \_\_default\_arp\_policer\_\_

Logical interface: ae5.922, Index: 572

Object                  Name                   Type                    Index

Classifier              dscp-ipv6-compatibility dscp-ipv6                  9

Classifier              ipprec-compatibility   ip                         13

---

syntax error, expecting .

ftelsuper@HCMM005402620MX48-re1> start shell pfe network fpc0

NPC platform (1067Mhz MPC 8548 processor, 2048MB memory, 512KB flash)

NPC0(HCMM005402620MX48-re1 vty)# show cos halp ifl 572

IFL type: Aggregate

IFL name: (ae5.922)   (Index 572)

--------------------------------------------------------------------------------

IFL name: (xe-0/2/4.922, xe-0/2/4)   (Index 798, IFD Index 172) egress information

Not found

NPC0(HCMM005402620MX48-re1 vty)#

NPC0(HCMM005402620MX48-re1 vty)#

NPC0(HCMM005402620MX48-re1 vty)# show cos halp ifl 132

Not Found

NPC0(HCMM005402620MX48-re1 vty)# show cos halp ifd 132

IFD name: ae5   (Index 132) ingress information

Not found

NPC0(HCMM005402620MX48-re1 vty)# show cos halp ifd 172

--------------------------------------------------------------------------------

rich queueing enabled: 1

Q chip present: 0

IFD name: xe-0/2/4   (Index 172) egress information

XM chip id: 0

XM chip Scheduler: 0

XM chip L1 index: 69

XM chip dummy L2 index: 138

XM chip base Q index: 552

Number of queues: 8

Rich queuing support: 1 (ifl queued:0)

--------------------------------------------------------------------------------------------

Queue  State        Max           Guaranteed    Burst       Weight  G-Pri  E-Pri  WRED  TAIL

Index               Rate          Rate          Size                              Rule  Rule

--------------------------------------------------------------------------------------------

552    Configured   10000000000   9500000000    131064      118     GL     EL     4     148

553    Configured   10000000000   0             131064      1       GL     EL     0     1

554    Configured   10000000000   0             131064      1       GL     EL     0     1

555    Configured   10000000000   500000000     131064      6       GL     EL     4     72

556    Configured   10000000000   0             131064      1       GL     EL     0     1

557    Configured   10000000000   0             131064      1       GL     EL     0     1

558    Configured   10000000000   0             131064      1       GL     EL     0     1

559    Configured   10000000000   0             131064      1       GL     EL     0     1

--------------------------------------------------------------------------------------------

NPC0(HCMM005402620MX48-re1 vty)# show cos halp ifl 798

IFL type: Basic

--------------------------------------------------------------------------------

IFL name: (xe-0/2/4.922, xe-0/2/4)   (Index 798, IFD Index 172) egress information

Not found

NPC0(HCMM005402620MX48-re1 vty)# exit

--

Could you please configure "per-unit-scheduler" on the IFD since we are applying the scheduler-map on the IFL.

Below document for reference:

<https://www.juniper.net/documentation/us/en/software/junos/interfaces-adaptive-services/topics/ref/statement/per-unit-scheduler-edit-interfaces.html>

<https://supportportal.juniper.net/s/article/MX-Using-per-unit-scheduler-with-rate-limit-or-exact>

Since this is a new implementation, I would suggest you to check with your accounts team who can help you with the exact configuration needed as per your network design and the traffic flow.

<https://supportportal.juniper.net/s/article/MX-CoS-Drops-in-network-control-queue-because-of-a-configuration-issue-it-had-1-percent-of-transmit-rate-and-buffer-size>
