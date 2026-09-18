# CSPF to secondary loopback

<https://lists.archive.carbon60.com/nsp/juniper/8098>

<https://kb.juniper.net/InfoCenter/index?page=content&id=KB32447&cat=PTX9000&actp=LIST>

* *SUMMARY:**

This article provides a discussion of how ISIS distributed information is used to populate the TED (Traffic Engineering Database) on a Juniper router. It references the industry well-known topic **RFC5305 “IS-IS Extensions for Traffic Engineering”.**

There is a specific part related to the Juniper implementation (starting with Junos OS 13.3) resulting in additional IP addresses possibly found in the TED and as such used for MPLS LSPs tunnel destinations. In particular, besides MPLS LSP tail-end's TE RID (ISIS LSP's TLV  type 134), other /32 IP addresses configured on it can find their way (by the means of ISIS TLV type 132) to the TED on other Juniper routers in the ISIS domain.

Note: This discussion is specific to ISIS, as OSPF does not exhibit the same behavior.

* *SOLUTION:**

### **References**

As per [RFC5305 “IS-IS Extensions for Traffic Engineering”](https://tools.ietf.org/html/rfc5305)**,**the ISIS TLVs (Sub-TLVs) that are used to populate the MPLS TED with LSP's tail-end destination IP addresses are:

* *1: TLV type 134:  The Traffic Engineering router ID TLV**

* The router ID TLV contains the 4-octet router ID of the router originating the ISIS LSP.  For traffic engineering, it guarantees that we have a single stable address that can always be referenced in a path that will be reachable from multiple hops away, regardless of the state of the node's interfaces.*

* *2: TLV type 22:  The Extended IS Reachability TLV**

* *Sub-TLV 6: IPv4 Interface Address sub-TLV**

* This sub-TLV contains a 4-octet IPv4 address for the interface described by the (main) TLV.*

* *Sub-TLV 8: IPv4 Neighbor Address sub-TLV**

This sub-TLV contains a single IPv4 address for a neighbouring router on*this link.*

Although not mentioned in RFC5305, also note ISIS TLV type 132. In Junos OS 13.3, TLV type 132 started to play a role with TED “population”. A good reference for ISIS TLV type 132 is the famous **JNCIS study guide**: <https://www.juniper.net/assets/us/en/local/pdf/study-guide/study-guide-jncis.pdf>

* *IP Interface Address TLV**

Each IPv4 address configured on an IS-IS router may be advertised in the IP interface address TLV (type code 132). While a minimum of one address must be included, an individual implementation may include all of the local router’s addresses. The JUNOS software default is to advertise just the address configured on the loopback interface within the TLV.

- --

###

### Topology

* *lo0: [47.47.3.3] lo0: [47.47.1.1/47.47.2.2]**

+ ----------+ +------------+ | |-[xe-2/0/1.0]------------[xe-3/0/3.0]-| GRANADA |-[ge-4/1/3.0]-- | BERGEN | |------------| | | |-[xe-2/0/1.2]------------[xe-3/0/3.2]-| GRANADA-LS |-[ge-4/1/4.0]-- +----------+ +------------+

* *lo0: [47.47.11.11]**

#### Router Roles

BERGEN:      MPLS LSP head-end (ingress) router

GRANADA:   MPLS LSP tail-end (egress) router

- --

###

### Pre Junos OS 13.3 Behavior

First, in this article the behavior of pre Junos OS 13.3 behavior will be demonstrated. For that, it is enough to have just the MPLS LSP tail-end router on pre 13.3 Junos OS release. In summary, the IP addresses "imported" in the TED are from ISIS TLV type 134 and sub-TLVs (6 and 8) of the TLV type 22.

#### MPLS LSP Head-end Router

user@bergen-re0> show version

Hostname: bergen-re0

Model: mx104

Junos: 15.1F6-S5.6

<….>

user@bergen-re0> show isis overview

Instance: master

Router ID: 47.47.3.3

Hostname: bergen-re0

Sysid: 0047.0047.0303

Areaid: 49.0001

<…>

user@bergen-re0> show isis adjacency

Interface             System         L State        Hold (secs) SNPA

xe-2/0/1.0            granada-re0    2  Up                   20

xe-2/0/1.2            granada-re0-milan 2 Up                 19

#### MPLS LSP Tail-end Router

user@granada-re0> show version

Hostname: granada-re0

Model: mx480

* *JUNOS Base OS boot [12.3R9.4]**

<…>

user@granada-re0> show isis overview

Instance: master

Router ID: 47.47.1.1

<…>

user@granada-re0> show isis adjacency

Interface System L State Hold (secs) SNPA

ge-4/1/3.0 granada-re0-milan 2 Up 26

xe-3/0/3.0 bergen-re0 2 Up 20

####

#### Auxiliary Router (Logical-System on the MPLS LSP tail-end node)

user@granada-re0> show isis overview logical-system milan

Instance: master

Router ID: 47.47.11.11

<…>

user@granada-re0> show isis adjacency logical-system milan

Interface System L State Hold (secs) SNPA

ge-4/1/4.0 granada-re0 2 Up 24

xe-3/0/3.2 bergen-re0 2 Up 26

The focus is on having more than one IP addresses configured on the MPLS LSP tail-end's (egress) lo0 interface and attempting to establish CSPF routed MPLS LSP towards each of those, in particular to non TE RID IP address. For sake of simplicity, only two (2)  Lo0 addresses are configured.

As well, the Router ID (RID) is explicitly configured to correspond to one of those two (2) IP addresses:

####

#### MPLS LSP Tail-end Router

user@granada-re0> show configuration interfaces lo0

unit 0 {

family inet {

address 47.47.1.1/32;

address **47.47.2.2/32**;

}

family iso {

address 49.0001.0047.0047.0101.00;

}

}

user@granada-re0> show configuration routing-options router-id

router-id 47.47.1.1;

#### MPLS LSP Head-end Router

On the MPLS LSP  head-end (ingress) router two MPLS LSPs are configured, one to each of those 2 tail-end’s Lo0 IP addresses.

user@bergen-re0> show configuration protocols mpls

label-switched-path to-granadas-RID {

to 47.47.1.1;

primary path\_granada;

}

label-switched-path to-granadas-sec\_lo0 {

to **47.47.2.2**;

primary path\_granada;

}

path path\_granada;

interface xe-2/0/1.0;

interface xe-2/0/1.2;

Note that only of the MPLS LSP’s is established using the CSFP (TED). The one which is up is towards the RID (47.47.1.1) of the MPLS LSP tail-end (egress) node.

user@bergen-re0> show mpls lsp

Ingress LSP: 2 sessions

To              From            State Rt P     ActivePath       LSPname

47. 47.1.1       47.47.3.3       **Up**     0 \*     path\_granada     to-granadas-RID

47. 47.2.2       0.0.0.0         **Dn**    0       -                to-granadas-sec\_lo0

Total 2 displayed, Up 1, Down 1

<...>

user@bergen-re0> show mpls lsp extensive

Ingress LSP: 2 session

47. 47.1.1

From: 47.47.3.3, State: Up, ActiveRoute: 0, LSPname: to-granadas-RID

ActivePath: path\_granada (primary)

LSPtype: Static Configured, Penultimate hop popping

LoadBalance: Random

Encoding type: Packet, Switching type: Packet, GPID: IPv4

\*Primary   path\_granada     State: Up

Priorities: 7 0

SmartOptimizeTimer: 180

Computed ERO (S [L] denotes strict [loose] hops): (CSPF metric: 10)

47. 47.13.1 S

Received RRO (ProtectionFlag 1=Available 2=InUse 4=B/W 8=Node 10=SoftPreempt 20=Node-ID):

47. 47.13.1

10 Jan 23 13:46:51.326 Record Route:  47.47.13.1

9 Jan 23 13:46:51.326 Up

8 Jan 23 13:46:51.320 Originate Call

7 Jan 23 13:46:51.320 CSPF: computation result accepted  47.47.13.1

6 Jan 23 13:46:51.317 Clear Call

5 Jan 23 13:44:27.245 Selected as active path

4 Jan 23 13:44:27.241 Record Route:  47.47.13.1

3 Jan 23 13:44:27.240 Up

2 Jan 23 13:44:27.233 Originate Call

1 Jan 23 13:44:27.233 CSPF: computation result accepted  47.47.13.1

Created: Tue Jan 23 13:44:26 2018

* *47.47.2.2**

From: 0.0.0.0, **State: Dn**, ActiveRoute: 0, LSPname: to-granadas-sec\_lo0

ActivePath: (none)

LSPtype: Static Configured, Penultimate hop popping

LoadBalance: Random

Encoding type: Packet, Switching type: Packet, GPID: IPv4

Primary   path\_granada     State: Dn

Priorities: 7 0

SmartOptimizeTimer: 180

Will be enqueued for recomputation in 11 second(s).

1 Jan 23 13:59:31.476 **CSPF failed: no route toward 47.47.2.2**[32 times]

Created: Tue Jan 23 13:44:26 2018

Total 2 displayed, Up 1, Down 1

<...>

The non-established LSP (towards the MPLS LSP tail-end node’s secondary Lo0 IP addresses) is failing with a reason:

* *CSPF failed: no route toward 47.47.2.2**

That failure reason suggests us to take a look at the MPLS TED.

user@bergen-re0> show ted database

TED database: 3 ISIS nodes 3 INET nodes

ID                            Type Age(s) LnkIn LnkOut Protocol

granada-re0.00(47.47.1.1)     Rtr      27     2      2 IS-IS(2)

To: bergen-re0.00(47.47.3.3), Local: 47.47.13.1, Remote: 47.47.13.2

Local interface index: 364, Remote interface index: 367

To: granada-re0-milan.00(47.47.11.11), Local: 111.111.111.1, Remote: 111.111.111.2

Local interface index: 360, Remote interface index: 327

ID                            Type Age(s) LnkIn LnkOut Protocol

<...>

user@bergen-re0> show ted database 47.47.1.1 extensive

TED database: 3 ISIS nodes 3 INET nodes

* *NodeID: granada-re0.00(47.47.1.1)**

Type: Rtr, Age: 11 secs, LinkIn: 2, LinkOut: 2

Protocol: IS-IS(2)

* *47.47.1.1**

To: bergen-re0.00(47.47.3.3),**Local: 47.47.13.1, Remote: 47.47.13.2**

Local interface index: 364, Remote interface index: 367

<...>

To: granada-re0-milan.00(47.47.11.11), **Local: 111.111.111.1, Remote: 111.111.111.2**

Local interface index: 360, Remote interface index: 327

<...>

And indeed, there is not any (TED) reference to IP address **47.47.2.2**; hence the informative failure reason.

Next, it is helpful to check what is in the ISIS LSP from the tail-end router, particularly ISIS TLV  type 134 and Sub-TLVs (6 and 8) of TLV type 22.

Also, note ISIS TLV  type 132, as that plays a role starting with Junos OS 13.3.

user@bergen-re0> show isis adjacency

Interface             System         L State        Hold (secs) SNPA

xe-2/0/1.0            granada-re0    2  Up                   26

xe-2/0/1.2            granada-re0-milan 2 Up                 22

user@bergen-re0> monitor traffic interface xe-2/0/1.0 matching "(ether src host 40:b4:f0:ec:0b:e1) and iso" layer2-headers no-resolve detail

Address resolution is OFF.

Listening on xe-2/0/1.0, capture size 1514 bytes

<…>

14:36:29.016073  In 40:b4:f0:ec:0b:e1 > 09:00:2b:00:00:05, ethertype 802.1Q (0x8100), length 415: vlan 10, p 6, LLC, dsap OSI (0xfe) Individual, ssap OSI (0xfe) Command, ctrl 0x03: OSI NLPID IS-IS (0x83): length 394

L2 LSP, hlen: 27, v: 1, pdu-v: 1, sys-id-len: 6 (0), max-area: 3 (0)

lsp-id: 0047.0047.0101.00-00, seq: 0x00000ee6, lifetime:   348s

<...>

Protocols supported TLV #129, length: 2

NLPID(s): IPv4 (0xcc), IPv6 (0x8e)

* *Traffic Engineering Router ID TLV #134, length: 4**

* *Traffic Engineering Router ID: 47.47.1.1**

* *IPv4 Interface address(es) TLV #132, length: 4**

* *IPv4 interface address: 47.47.1.1**

Hostname TLV #137, length: 11

Hostname: granada-re0

* *Extended IS Reachability TLV #22, length: 170**

* *IS Neighbor: 0047.0047.1111.00, Metric: 10, sub-TLVs present (74)**

* *IPv4 interface address subTLV #6, length: 4, 111.111.111.1**

* *IPv4 neighbor address subTLV #8, length: 4, 111.111.111.2**

Link Local/Remote Identifier subTLV #4, length: 8, 0x00000168, 0x00000147

<...>

I**S Neighbor: 0047.0047.0303.00, Metric: 50000, sub-TLVs present (74)**

* *IPv4 interface address subTLV #6, length: 4, 47.47.13.1**

* *IPv4 neighbor address subTLV #8, length: 4, 47.47.13.2**

Link Local/Remote Identifier subTLV #4, length: 8, 0x0000016c, 0x0000016f

<...>

Extended IPv4 Reachability TLV #135, length: 36

<...>

IPv6 reachability TLV #236, length: 80

<...>

Extended IPv4 Reachability TLV #135, length: 34

<...>

Note that the only IP address encoded in the ISIS TLV type 132 is the RID (router-id).

Cross checking with the info (related to the IP addresses) in the TED makes a clear correlation:

user@bergen-re0> show ted database 47.47.1.1 extensive

TED database: 3 ISIS nodes 3 INET nodes

NodeID: granada-re0.00(47.47.1.1)

Type: Rtr, Age: 13 secs, LinkIn: 2, LinkOut: 2

* *Protocol: IS-IS(2)**

* *47.47.1.1**  **<<<<**

To: bergen-re0.00(47.47.3.3), **Local: 47.47.13.1, Remote: 47.47.13.2**

Local interface index: 364, Remote interface index: 367

<…>

To: granada-re0-milan.00(47.47.11.11), Local: **111.111.111.1, Remote: 111.111.111.2**

Local interface index: 360, Remote interface index: 327

<…>

Note the following section of the output as a reference with respect to the post Junos OS 13.3 release, discussed below.

* *<…>**

* *Protocol: IS-IS(2)**

* *47.47.1.1**

* *<…>**

- --

### **Junos OS 13.3 and above Behavior**

In summary, starting with Junos OS 13.3, all /32 IP addresses configured are included on the lo0 interface in ISIS LSPs and they are encoded in TLV type 132. On the "receiving" (MPLS LSP ingress router) side, in the TED, the information found in ISIS TLV type 132 is imported as well. It is not that important but for the completeness, this change was introduced as a mechanism to support the following feature: <https://www.juniper.net/documentation/en_US/junos/topics/concept/mpls-egress-protection-layer3-vpn-overview.html>

In order to demonstrate this change the only difference to the previously described setup is the upgrade of GRANADA router to Junos OS 13.3R9:

user@granada-re0> show version

Hostname: granada-re0

Model: mx480

Junos: 13.3R9.13

<..>

user@granada-re0> show isis overview

Instance: master

Router ID: 47.47.1.1

<...>

Checking the state of our two MPLS LSPs shows that both of them are UP:

user@bergen-re0> show mpls lsp ingress

Ingress LSP: 2 sessions

To              From            State Rt P     ActivePath       LSPname

47. 47.1.1       47.47.3.3       **Up**     0 \*     path\_granada     to-granadas-RID

47. 47.2.2       47.47.3.3       **Up**     0 \*     path\_granada     to-granadas-sec\_lo0

Total 2 displayed, Up 2, Down 0

user@bergen-re0> show mpls lsp ingress extensive

Ingress LSP: 2 session

47. 47.1.1

From: 47.47.3.3, State: Up, ActiveRoute: 0, LSPname: to-granadas-RID

ActivePath: path\_granada (primary)

LSPtype: Static Configured, Penultimate hop popping

LoadBalance: Random

Encoding type: Packet, Switching type: Packet, GPID: IPv4

\*Primary   path\_granada     State: Up

Priorities: 7 0

SmartOptimizeTimer: 180

Computed ERO (S [L] denotes strict [loose] hops): (CSPF metric: 10)

47. 47.13.1 S

Received RRO (ProtectionFlag 1=Available 2=InUse 4=B/W 8=Node 10=SoftPreempt 20=Node-ID):

47. 47.13.1

5 Jan 24 18:11:33.380 Selected as active path

4 Jan 24 18:11:33.379 Record Route:  47.47.13.1

3 Jan 24 18:11:33.379 Up

2 Jan 24 18:11:33.372 Originate Call

1 Jan 24 18:11:33.372 CSPF: computation result accepted  47.47.13.1

Created: Wed Jan 24 18:11:32 2018

47. 47.2.2

From: 47.47.3.3, State: Up, ActiveRoute: 0, LSPname: to-granadas-sec\_lo0

ActivePath: path\_granada (primary)

LSPtype: Static Configured, Penultimate hop popping

LoadBalance: Random

Encoding type: Packet, Switching type: Packet, GPID: IPv4

\*Primary   path\_granada     State: Up

Priorities: 7 0

SmartOptimizeTimer: 180

Computed ERO (S [L] denotes strict [loose] hops): (CSPF metric: 10)

47. 47.13.1 S

Received RRO (ProtectionFlag 1=Available 2=InUse 4=B/W 8=Node 10=SoftPreempt 20=Node-ID):

47. 47.13.1

5 Jan 24 18:11:33.481 Selected as active path

4 Jan 24 18:11:33.480 Record Route:  47.47.13.1

3 Jan 24 18:11:33.480 Up

2 Jan 24 18:11:33.376 Originate Call

1 Jan 24 18:11:33.376 CSPF: computation result accepted  47.47.13.1

Created: Wed Jan 24 18:11:32 2018

Total 2 displayed, Up 2, Down 0

user@bergen-re0>

The reason is because now both (including 47.47.2.2 which was missing before) of the MPLS LSP egress router's Lo0 interface IP addresses are found (imported) in the TED on the ingress router:

user@bergen-re0> show ted database 47.47.1.1 extensive

TED database: 3 ISIS nodes 3 INET nodes

NodeID: granada-re0.00(47.47.1.1)

Type: Rtr, Age: 17 secs, LinkIn: 2, LinkOut: 2

* *Protocol: IS-IS(2)**

* *47.47.1.1, 47.47.2.2**

To: bergen-re0.00(47.47.3.3), Local: 47.47.13.1, Remote: 47.47.13.2

Local interface index: 364, Remote interface index: 0

<...>

To: granada-re0-milan.00(47.47.11.11), Local: 111.111.111.1, Remote: 111.111.111.2

Local interface index: 360, Remote interface index: 0

<...>

And additional IP address (47.47.2.2) ended up imported in TED from the received ISIS LSP TLV # 132  originated by the MPLS egress router

and **highlighted** below:

user@bergen-re0> monitor traffic interface xe-2/0/1.0 matching "(ether src host 40:b4:f0:ec:0b:e1)" layer2-headers size 2000 detail no-resolve

Address resolution is OFF.

Listening on xe-2/0/1.0, capture size 2000 bytes

<...>

18:29:23.741591  In 40:b4:f0:ec:0b:e1 > 09:00:2b:00:00:05, ethertype 802.1Q (0x8100), length 421: vlan 10, p 6, LLC, dsap OSI (0xfe) Individual, ssap OSI (0xfe) Command, ctrl 0x03: OSI NLPID IS-IS (0x83): length 400

L2 LSP, hlen: 27, v: 1, pdu-v: 1, sys-id-len: 6 (0), max-area: 3 (0)

lsp-id: 0047.0047.0101.00-00, seq: 0x00001c67, lifetime:   348s

chksum: 0x59de (correct), PDU length: 400, Flags: [ L1L2 IS ]

Area address(es) TLV #1, length: 4

Area address (length: 3): 49.0001

LSP Buffersize TLV #14, length: 2

LSP Buffersize: 1492

Protocols supported TLV #129, length: 2

NLPID(s): IPv4 (0xcc), IPv6 (0x8e)

Traffic Engineering Router ID TLV #134, length: 4

Traffic Engineering Router ID: 47.47.1.1

IPv4 Interface address(es) TLV #132, length: 4

IPv4 interface address: 47.47.1.1

Hostname TLV #137, length: 11

Hostname: granada-re0

Extended IS Reachability TLV #22, length: 170

IS Neighbor: 0047.0047.1111.00, Metric: 10, sub-TLVs present (74)

IPv4 interface address subTLV #6, length: 4, 111.111.111.1

IPv4 neighbor address subTLV #8, length: 4, 111.111.111.2

<...>

IS Neighbor: 0047.0047.0303.00, Metric: 50000, sub-TLVs present (74)

IPv4 interface address subTLV #6, length: 4, 47.47.13.1

IPv4 neighbor address subTLV #8, length: 4, 47.47.13.2

Link Local/Remote Identifier subTLV #4, length: 8, 0x0000016c, 0x00000000

<...>

Extended IPv4 Reachability TLV #135, length: 36

<...>

* *IPv4 Interface address(es) TLV #132, length: 4**

* *IPv4 interface address: 47.47.2.2**

IPv6 reachability TLV #236, length: 80

<...>

<https://kb.juniper.net/InfoCenter/index?page=content&id=KB24612&cat=PTX_SERIES&actp=LIST>

* *SUMMARY:**

This article describes the issue of the secondary IP, which is configured on the loopback interface, not being advertised in the Traffic Engineering Database (TED).

* *SYMPTOMS:**

When the LSP, which is configured on the primary loopback address, goes down, the LSP configured on the secondary loopback address does not come up. This causes an outage in the network.

interfaces {

lo0 {

unit 0 {

family inet {

address 3.3.3.3/32;

address 1.1.1.1/32;

}

}

}

}

* *CAUSE:**

- The secondary loopback address is not advertised in the TED database.
- If CSPF is enabled, the ingress router will consult the TED, in which the secondary loopback address is not advertised; so LSP will not come up.

* *SOLUTION:**

This is expected behavior and working as designed. The workaround is to enable **no-cspf** for the LSP or **inter-domain** under protocols MPLS.
