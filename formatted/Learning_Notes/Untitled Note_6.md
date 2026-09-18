# Untitled Note

# OSPF AS THE PE-CE ROUTING PROTOCOLS DEEP DIVE – PART 2 OF 3 – THE SHAM LINK

[JANUARY 6, 2014](http://web.archive.org/web/20140706194319/http://mellowd.co.uk/ccie/?p=4741) [DARREN](http://web.archive.org/web/20140706194319/http://mellowd.co.uk/ccie/?author=1) [1 COMMENT](http://web.archive.org/web/20140706194319/http://mellowd.co.uk/ccie/?p=4741#comments "Comment on OSPF as the PE-CE routing protocols deep dive – Part 2 of 3 – The SHAM Link")

[Read part 1](http://web.archive.org/web/20140706194319/http://mellowd.co.uk/ccie/?p=4697)

[Read part 2](http://web.archive.org/web/20140706194319/http://mellowd.co.uk/ccie/?p=4741)

[Read part 3](http://web.archive.org/web/20140706194319/http://mellowd.co.uk/ccie/?p=4814)

In order to understand the purpose of the sham link, you first need to understand the problem it is trying to fix. If we look at the topology used last time again for a refresh:

[![](http://web.archive.org/web/20140706194319im_/http://mellowd.co.uk/ccie/wp-content/uploads/2014/01/RFC4577_12.png)](http://web.archive.org/web/20140706194319/http://mellowd.co.uk/ccie/wp-content/uploads/2014/01/RFC4577_12.png)

## The Problem

From the previous post it was clear that it did not matter if the LSA received by a PE from a CE was type1, type2, or type3. That LSA would always be either type3 or type5 on the remote side. While this is perfectly fine most of the time, there are times when this is less than ideal. I’ll add a low-speed serial link between R5 and R6 and enable regular OSPF over the link like so:

[![](http://web.archive.org/web/20140706194319im_/http://mellowd.co.uk/ccie/wp-content/uploads/2014/01/RFC4577_4.png)](http://web.archive.org/web/20140706194319/http://mellowd.co.uk/ccie/wp-content/uploads/2014/01/RFC4577_4.png)

R5 config:

interface Serial2/0

ip address 10.0.56.5 255.255.255.0

ip ospf 1 area 0

If I check the route to R6′s loopback, it’ll be going over the slow serial link:

R5#sh ip route 6.6.6.6

Routing entry for 6.6.6.6/32

Known via "ospf 1", distance 110, metric 65, type intra area

Last update from 10.0.56.6 on Serial2/0, 00:01:26 ago

Routing Descriptor Blocks:

\* 10.0.56.6, from 6.6.6.6, 00:01:26 ago, via Serial2/0

Route metric is 65, traffic share count is 1

Changing the metric of the link will have no effect whatsoever:

R5#conf t

Enter configuration commands, one per line. End with CNTL/Z.

R5(config)#int s2/0

R5(config-if)#ip ospf cost 50000

R5(config-if)#end

R5#

\*Jan 6 12:01:52.747: %SYS-5-CONFIG\_I: Configured from console by console

R5#sh ip route 6.6.6.6

Routing entry for 6.6.6.6/32

Known via "ospf 1", distance 110, metric 50001, type intra area

Last update from 10.0.56.6 on Serial2/0, 00:00:01 ago

Routing Descriptor Blocks:

\* 10.0.56.6, from 6.6.6.6, 00:00:01 ago, via Serial2/0

Route metric is 50001, traffic share count is 1

OSPF has it’s own internal route-selection decision. Intra-area routes from type1 LSAs are always preferred over summaries from type3 LSAs. Summaries are also preferred over E1s, then E2, then N1, then finally N2 OSPF routes.

R5 and R6 are in the same area, hence they are currently learning each others prefixes through the type1 LSAs between then. Regardless of metric, this route will always be preferred over the type3 learned over the MPLS cloud.

## The Sham Link

[RFC 4577 Section 4.2.7](http://web.archive.org/web/20140706194319/http://tools.ietf.org/html/rfc4577#section-4.2.7) gives us one option to fix this problem. The sham-link essentially allows the PE routers to share OSPF routes via type1 LSAs. When this LSA reaches the PE on the other side, it is still a type1 LSA. That LSA is flooded to the connected PE. This means all internal OSPF routes at one site can appear internal on the other side. The sham-link cost can be adjusted to be lower than the backdoor OSPF link and therefore traffic will prefer going over the MPLS core first.

[Unlike the previous post in which IOS and IOS-XR had minor differences in interpreting the RFC](http://web.archive.org/web/20140706194319/http://mellowd.co.uk/ccie/?p=4697), for this second part they are very different indeed.

## IOS Sham-Link

Sham-links can be placed into any area you wish. As the CE’s are all in area 0 we’ll just stick to area 0. Both PEs will create a sham-link to each other. Both PEs need to be able to send packets to the other PE over the MPLS cloud. These end-points need to be in the customer’s VRF. Generally the easiest way to do this is to create a new loopback on both PEs in the VRF, and then advertise those addresses via BGP in a VPNv4 address.

[![](http://web.archive.org/web/20140706194319im_/http://mellowd.co.uk/ccie/wp-content/uploads/2014/01/RFC4577_5.png)](http://web.archive.org/web/20140706194319/http://mellowd.co.uk/ccie/wp-content/uploads/2014/01/RFC4577_5.png)

R2:

interface Loopback20

vrf forwarding A

ip address 20.20.20.20 255.255.255.255

!

router bgp 100

!

address-family ipv4 vrf A

network 20.20.20.20 mask 255.255.255.255

From R2 we should be able to reach the new loopback on R4 through the VRF:

R2#traceroute vrf A 40.40.40.40 so lo20

Type escape sequence to abort.

Tracing the route to 40.40.40.40

1 10.0.23.3 [MPLS: Labels 16/21 Exp 0] 40 msec 48 msec 44 msec

2 40.40.40.40 72 msec 64 msec 40 msec

Now that they have connectivity via a label-switched-path we can create the sham-link:

R2#conf t

Enter configuration commands, one per line. End with CNTL/Z.

R2(config)#router ospf 1 vrf A

R2(config-router)#area 0 sham-link 20.20.20.20 40.40.40.40

R2(config-router)#end

Once both sides are configured we can see the sham-link up:

R2#sh ip ospf 1 sham-links

Sham Link OSPF\_SL0 to address 40.40.40.40 is up

Area 0 source address 20.20.20.20

Run as demand circuit

DoNotAge LSA allowed. Cost of using 1 State POINT\_TO\_POINT,

Timer intervals configured, Hello 10, Dead 40, Wait 40,

Hello due in 00:00:04

Adjacency State FULL (Hello suppressed)

Index 3/3, retransmission queue length 0, number of retransmission 0

First 0x0(0)/0x0(0) Next 0x0(0)/0x0(0)

Last retransmission scan length is 0, maximum is 0

Last retransmission scan time is 0 msec, maximum is 0 msec

Before we continue with the verification of the sham-link, I want you to take a step back and think about how each router in the path learns and forwards traffic from R5 to R6. This is essential when dealing with the differences between IOS and IOS-XR.

#### No Sham-link

- R6 originates it’s loopback in a type-1 LSA to R4
- R4 installs a route to R6 via the type1 LSA in the VRF
- R4 redistributes that route into BGP, converts it to VPNv4 and advertises it over to R2
- R2 redistributes the VPNv4 route into OSPF and originates a type3 LSA to R5

#### Sham-link

- R6 originates it’s loopback in a type-1 LSA to R4
- R4 installs a route to R6 via the type1 LSA in the VRF
- R4 advertises the LSA over the sham-link to R2
- R2 installs a route based on the LSA and forwards that LSA to R5

What’s interesting about the sham-link here is that there is no redistribution between BGP and OSPF. So do we need to redistribute at all? It’s an interesting question as we shall soon see. Let’s remove all redistribution on R2 and R4 to see what happens.

R2#conf t

Enter configuration commands, one per line. End with CNTL/Z.

R2(config)#router ospf 1 vrf A

R2(config-router)#no redi bgp 100

R2(config-router)#router bgp 100

R2(config-router)#add ipv4 vrf A

R2(config-router-af)#no red ospf 1

R2(config-router-af)#end

This has been completed on both PEs. Do we see the route to R6′s loopback as a intra-area OSPF route over the MPLS cloud on R5?

R5#sh ip route 6.6.6.6

Routing entry for 6.6.6.6/32

Known via "ospf 1", distance 110, metric 4, type intra area

Last update from 10.0.25.2 on FastEthernet1/0, 00:00:04 ago

Routing Descriptor Blocks:

\* 10.0.25.2, from 6.6.6.6, 00:00:04 ago, via FastEthernet1/0

Route metric is 4, traffic share count is 1

So our control-plane is working, but as we shall see next the data-plane will not work:

R5#ping 6.6.6.6 so lo0 re 3

Type escape sequence to abort.

Sending 3, 100-byte ICMP Echos to 6.6.6.6, timeout is 2 seconds:

Packet sent with a source address of 5.5.5.5

...

Success rate is 0 percent (0/3)

Section 4.2.7.4 of the RFC tells us why this is happening:

> Any other route advertised in an LSA that is transmitted over a sham link MUST also be redistributed (by the PE flooding the LSA over the sham link) into BGP. This means that if the preferred (OSPF) route for a given address prefix has the sham link as its next hop interface, then there will also be a “corresponding BGP route”, for that same address prefix, installed in the VRF. Per Section 4.1.2, the OSPF route is preferred. However, when forwarding a packet, if the preferred route for that packet has the sham link as its next hop interface, then the packet MUST be forwarded according to the corresponding BGP route. That is, it will be forwarded as if the corresponding BGP route had been the preferred route. The “corresponding BGP route” is always a VPN-IPv4 route; the procedure for forwarding a packet over a VPN-IPv4 route is described in [VPN].

The part of section 4.1.2 reffered to in the section above states:

> If a VRF contains both an OSPF-distributed route and a VPN-IPv4 route for the same IPv4 prefix, then the OSPF-distributed route is preferred. In general, this means that forwarding is done according to the OSPF route. The one exception to this rule has to do with the “sham link”. If the next hop interface for an installed (OSPFdistributed) route is the sham link, forwarding is done according to a corresponding BGP route. This is detailed in Section 4.2.7.4.

So while R2 has an OSPF-learned route through the sham-link, it does NOT have a BGP-learned route to actually do the forwarding on. R2 and R4 will have to redistribute the OSPF routes into BGP. They do NOT however have to move those BGP routes back into OSPF on the other side.

While it may be a little confusing it makes perfect sense. If R2 needs to send a packet to a VPN attached to R4 it needs two labels. The top-most label is the transport label needed to get the packet through the ISP core. The second label is the VPN label needed to let R4 know which VPN that packet belongs to. MP-BGP is able to advertise a VPN label with it’s VPNv4 NLRI update. OSPF does not have the same capibility. Therefore the BGP route is needed on the PEs so they know which labels to impose on ingress through the core.

If we look at the current CEF table on R2 to get to R6, we’ll see it is doesn’t know how to handle it:

R2#show ip cef vrf A 6.6.6.6/32 detail

6. 6.6.6/32, epoch 0

recursive via 40.40.40.40 unusable: no label, unresolved

The RFC states that the next-hops need to be resolved via BGP, so I’ll ensure both routers are redistributing OSPF routes into BGP. I won’t, however, redistributes BGP routes back into OSPF as it’s not required:

R2#conf t

Enter configuration commands, one per line. End with CNTL/Z.

R2(config)#router bgp 100

R2(config-router)#add ipv4 vrf A

R2(config-router-af)#red ospf 1

R2(config-router-af)#end

From R2′s perspective, the route to 6.6.6.6/32 will be an OSPF route through the sham-link, but will be forwarded via the BGP link.

- OSPF Route:

R2#sh ip route vrf A 6.6.6.6

Routing Table: A

Routing entry for 6.6.6.6/32

Known via "ospf 1", distance 110, metric 3, type intra area

Redistributing via bgp 100

Last update from 4.4.4.4 00:01:34 ago

Routing Descriptor Blocks:

\* 4.4.4.4 (default), from 6.6.6.6, 00:01:34 ago

Route metric is 3, traffic share count is 1

MPLS label: 23

MPLS Flags: MPLS Required

- Forwarding BGP route:

R2#show bgp vpnv4 un rd 4.4.4.4:1 6.6.6.6

BGP routing table entry for 4.4.4.4:1:6.6.6.6/32, version 48

Paths: (1 available, best #1, no table)

Not advertised to any peer

Local

4. 4.4.4 (metric 30) from 4.4.4.4 (4.4.4.4)

Origin incomplete, metric 2, localpref 100, valid, internal, best

Extended Community: RT:1:1 OSPF DOMAIN ID:0x0005:0x000000030200

OSPF RT:0.0.0.0:2:0 OSPF ROUTER ID:40.40.40.40:0

mpls labels in/out nolabel/23

- CEF entry showing two label imposition:

R2#show ip cef vrf A 6.6.6.6/32 detail

6. 6.6.6/32, epoch 0, flags rib defined all labels

recursive via 4.4.4.4 label 23

nexthop 10.0.23.3 GigabitEthernet1/0 label 16

- Finally we should now be able to get from R5 to R6:

R5#traceroute 6.6.6.6 so lo0

Type escape sequence to abort.

Tracing the route to 6.6.6.6

1 10.0.25.2 24 msec 8 msec 44 msec

2 10.0.23.3 [MPLS: Labels 16/23 Exp 0] 64 msec 88 msec 60 msec

3 10.0.46.4 [MPLS: Label 23 Exp 0] 56 msec 88 msec 12 msec

4 10.0.46.6 152 msec 76 msec 128 msec

It does raise a question though. If OSPF had the ability to advertise VPN labels in it’s LSAs, it might be possible to do away with BGP in this specific type of topology. It may be that OSPFv3 and IS-IS, both easily extended, would be able to do this. That will have to be another post for another day.

## IOS-XR Sham-Link

IOS-XR, at least in version 3.9.1, has an odd behaviour when it comes to an OSPF sham link. Note that I have only tested version 3.9.1 so if this behaviour changes in newer versions I’m not aware of them yet.

Like the first post in this series, I’ll swap out R4 for an IOS-XR box. R2 will continue to run regular IOS.

I’m going to configure the sham-link between R2 and R4. I’ll also redistribute from OSPF into BGP, but not the other way around. This will match the working configuration on IOS. I’ll show the XR config of R4 for this:

RP/0/0/CPU0:R4#sh run router ospf 100

Mon Jan 6 16:35:46.369 UTC

router ospf 100

vrf A

domain-id type 0005 value 000000640200

area 0

sham-link 40.40.40.40 20.20.20.20

!

interface POS0/6/0/0

!

!

!

!

RP/0/0/CPU0:R4#sh run router bgp

Mon Jan 6 16:36:04.374 UTC

router bgp 100

address-family vpnv4 unicast

!

neighbor 2.2.2.2

remote-as 100

update-source Loopback0

address-family vpnv4 unicast

!

!

vrf A

rd 1:1

address-family ipv4 unicast

network 40.40.40.40/32

redistribute ospf 100

!

!

!

So now the sham-link should come up. But it doesn’t… It never comes up. Doing a debug on R2 shows something interesting:

R2#debug ip ospf hello

OSPF hello events debugging is on

OSPF: Send hello to 40.40.40.40 area 0 on OSPF\_SL0 from 20.20.20.20

R2 is sending OSPF hellos to R4, but R4 is simply not responding. It can also be a bit cryptic as R2 considers the sham-link ‘up’ – but there is no neighbourship:

R2#sh ip ospf sham-links

Sham Link OSPF\_SL0 to address 40.40.40.40 is up

Area 0 source address 20.20.20.20

Run as demand circuit

DoNotAge LSA allowed. Cost of using 1 State POINT\_TO\_POINT,

Timer intervals configured, Hello 10, Dead 40, Wait 40,

Hello due in 00:00:02

R2#

R2#

R2#sh ip ospf 100 neigh

Neighbor ID Pri State Dead Time Address Interface

7. 7.7.7 1 FULL/DR 00:00:38 10.1.2.1 FastEthernet1/0

5. 5.5.5 1 FULL/DR 00:00:33 20.2.4.4 FastEthernet0/0.24

On R4 we see the following:

RP/0/0/CPU0:R4# show ospf 100 vrf A sham-links

Mon Jan 6 16:39:41.808 UTC

Sham Links for OSPF 100, VRF A

Sham Link OSPF\_SL0 to address 20.20.20.20 is down

Area 0, source address 40.40.40.40

IfIndex = 2

Run as demand circuit

DoNotAge LSA allowed., Cost of using 1

Transmit Delay is 1 sec, State DOWN,

Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5

RP/0/0/CPU0:R4# show ospf 100 vrf A neighbor

Mon Jan 6 16:39:51.085 UTC

\* Indicates MADJ interface

Neighbors for OSPF 100, VRF A

Neighbor ID Pri State Dead Time Address Interface

6. 6.6.6 1 FULL/ - 00:00:31 10.19.20.20 POS0/6/0/0

Neighbor is up for 00:30:14

Total neighbor count: 1

Each PE only has their neighbourships to their directly connected CEs as fully up. They are not adjacent on the sham-link.

The only way to get the sham-link up on IOS-XR, is to redistribute the VPNv4 routes back into OSPF on the XR side. This makes little sense considering what I have covered above in the IOS-only side.

P/0/0/CPU0:R4#conf

Mon Jan 6 16:42:09.978 UTC

RP/0/0/CPU0:R4(config)#router ospf 100 vrf A

RP/0/0/CPU0:R4(config-ospf-vrf)#redistribute bgp 100

RP/0/0/CPU0:R4(config-ospf-vrf)#end

Uncommitted changes found, commit them before exiting(yes/no/cancel)? [cancel]:yes

RP/0/0/CPU0:Jan 6 16:42:29.374 : ospf[482]: %ROUTING-OSPF-5-ADJCHG :

Process 100, Nbr 20.20.20.20 on OSPF\_SL0 in area 0 from LOADING to FULL, Loading Done,vrf A vrfid 0x60000012

As you can see, the sham-link comes up straight away as soon as this is done.

We can confirm from the CE’s perspective that the route is intra-area over the MPLS cloud and is label-switched that way:

R5#show ip route 6.6.6.6

Routing entry for 6.6.6.6/32

Known via "ospf 1", distance 110, metric 4, type intra area

Last update from 20.2.4.2 on FastEthernet0/0.24, 00:01:37 ago

Routing Descriptor Blocks:

\* 20.2.4.2, from 6.6.6.6, 00:01:37 ago, via FastEthernet0/0.24

Route metric is 4, traffic share count is 1

R5#traceroute 6.6.6.6

Type escape sequence to abort.

Tracing the route to 6.6.6.6

1 20.2.4.2 0 msec 4 msec 0 msec

2 20.2.3.3 [MPLS: Labels 21/16028 Exp 0] 0 msec 4 msec 0 msec

3 20.3.6.6 [MPLS: Labels 22/16028 Exp 0] 0 msec 4 msec 0 msec

4 20.6.19.19 [MPLS: Label 16028 Exp 0] 4 msec 0 msec 4 msec

5 10.19.20.20 4 msec \* 4 msec

So why does IOS-XR have this behaviour? I’m not entirely sure, but checking the route table on both PE does give us a hint. Let’s go over the RFC statements once again:

> Any other route advertised in an LSA that is transmitted over a sham link MUST also be redistributed (by the PE flooding the LSA over the sham link) into BGP. This means that if the preferred (OSPF) route for a given address prefix has the sham link as its next hop interface, then there will also be a “corresponding BGP route”, for that same address prefix, installed in the VRF. Per Section 4.1.2, the OSPF route is preferred. However, when forwarding a packet, if the preferred route for that packet has the sham link as its next hop interface, then the packet MUST be forwarded according to the corresponding BGP route. That is, it will be forwarded as if the corresponding BGP route had been the preferred route. The “corresponding BGP route” is always a VPN-IPv4 route; the procedure for forwarding a packet over a VPN-IPv4 route is described in [VPN].

> If a VRF contains both an OSPF-distributed route and a VPN-IPv4 route for the same IPv4 prefix, then the OSPF-distributed route is preferred. In general, this means that forwarding is done according to the OSPF route. The one exception to this rule has to do with the “sham link”. If the next hop interface for an installed (OSPFdistributed) route is the sham link, forwarding is done according to a corresponding BGP route. This is detailed in Section 4.2.7.4.

The RFC states that each PE should be learning a BGP and OSPF route. The OSPF route should be installed into the RIB, while the BGP route is used for the actual forwarding thanks to it’s label carrying capability. What we see on IOS-XR is different.

- IOS:

R2#sho ip route vrf A 6.6.6.6

Routing Table: A

Routing entry for 6.6.6.6/32

Known via "ospf 100", distance 110, metric 3, type intra area

Redistributing via bgp 100

Advertised by bgp 100 match internal external 1 & 2

Last update from 4.4.4.4 00:04:28 ago

Routing Descriptor Blocks:

\* 4.4.4.4 (default), from 6.6.6.6, 00:04:28 ago

Route metric is 3, traffic share count is 1

MPLS label: 16028

MPLS Flags: MPLS Required

The active route on R2 is the OSPF sham-link route as expected.

- IOS-XR:

RP/0/0/CPU0:R4#sh route vrf A 5.5.5.5

Mon Jan 6 16:47:44.109 UTC

Routing entry for 5.5.5.5/32

Known via "bgp 100", distance 200, metric 2, type internal

Installed Jan 6 16:42:29.984 for 00:05:14

Routing Descriptor Blocks

2. 2.2.2, from 2.2.2.2

Nexthop in Vrf: "default", Table: "default", IPv4 Unicast, Table Id: 0xe0000000

Route metric is 2

No advertising protos.

The active route on R4 is the BGP route, not the OSPF route as the RFC tells us it should be. Even if R4 uses the BGP route as an active route and forwarding route, it still makes no sense for it to have to redistribute into OSPF first. The PE router already has the VPNv4 update. It has no need to share that information with it’s directly connected CEs.

From R6′s perspective, it still has a type 1 intra-area route to R5:

P/0/3/CPU0:R6#show route ipv4 5.5.5.5

Mon Jan 6 16:51:22.808 UTC

Routing entry for 5.5.5.5/32

Known via "ospf 1", distance 110, metric 4, type intra area

Installed Jan 6 16:42:29.798 for 00:08:53

Routing Descriptor Blocks

10. 19.20.19, from 5.5.5.5, via POS0/7/0/0

Route metric is 4

No advertising protos.

R4 has two valid routes to 5.5.5.5/32, an OSPF route and a BGP route. Both prefix-lengths are the same. OSPF has a lower AD than BGP, so I would expect to see the OSPF route in the VRF table as the active route.

What’s even more odd is that R4 simply needs to redistribute. But it doesn’t have to redistribute an actual route. As an example I’ll create a policy that blocks everything and use that :

route-policy BLOCK

drop

end-policy

!

router ospf 100

vrf A

redistribute bgp 100 route-policy BLOCK

!

!

end

RP/0/0/CPU0:R4#clear ospf 100 process

Mon Jan 6 17:08:20.284 UTC

Reset OSPF process 100? [no]: yes

RP/0/0/CPU0:R4#show ospf 100 vrf A neigh

Mon Jan 6 17:10:20.440 UTC

\* Indicates MADJ interface

Neighbors for OSPF 100, VRF A

Neighbor ID Pri State Dead Time Address Interface

20. 20.20.20 1 FULL/ - - 20.20.20.20 OSPF\_SL0

Neighbor is up for 00:04:37

6. 6.6.6 1 FULL/ - 00:00:36 10.19.20.20 POS0/6/0/0

Neighbor is up for 01:00:44

Total neighbor count: 2

IOS-XR seems to simply want the redistribute command configured, regardless of whether its doing anything…

Regardless of all of that, the sham-link now works in both directions and boths CEs are forwarding over the MPLS cloud.

## Sham-link conclusions

- Know the difference between the behaviour of IOS and IOS-XR
- Sham-links are point-to-point. If you had to create sham-links between four PEs you are going to need six sham-links
- A loopback in a VRf can be the end-point for multiple sham-links
- Avoid sham-links if you can! Might be easier to just give a VPLS solution and let the customer run OSPF directly between their CE’s over the VPLS
