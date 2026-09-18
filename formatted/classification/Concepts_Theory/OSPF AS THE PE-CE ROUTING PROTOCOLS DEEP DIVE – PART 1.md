# Untitled Note

# OSPF AS THE PE-CE ROUTING PROTOCOLS DEEP DIVE – PART 1 OF 3 – REDISTRIBUTION

[JANUARY 3, 2014](http://web.archive.org/web/20140706180615/http://mellowd.co.uk/ccie/?p=4697) [DARREN](http://web.archive.org/web/20140706180615/http://mellowd.co.uk/ccie/?author=1) [4 COMMENTS](http://web.archive.org/web/20140706180615/http://mellowd.co.uk/ccie/?p=4697#comments "Comment on OSPF as the PE-CE routing protocols deep dive – Part 1 of 3 – Redistribution")

[Read part 1](http://web.archive.org/web/20140706180615/http://mellowd.co.uk/ccie/?p=4697)

[Read part 2](http://web.archive.org/web/20140706180615/http://mellowd.co.uk/ccie/?p=4741)

[Read part 3](http://web.archive.org/web/20140706180615/http://mellowd.co.uk/ccie/?p=4814)

When doing L3VPN, using OSPF is actually one of the more complicated options. Vector-based protocols like RIP, EIGRP, and BGP are comparatively simple.

[RFC4577 is a great RFC that goes over how OSPF and BGP should operate when it comes to using OSPF as the PE-CE routing protocol.](http://web.archive.org/web/20140706180615/http://tools.ietf.org/html/rfc4577)

I wanted to go into detail some of what is noted on the RFC to see just how both IOS and IOS-XR interpret the RFC. Also it makes it a bit fun by purposely trying to break the RFC and seeing what happens.

First, a quick refresh of how PE-CE protocols work when **not** using BGP as the PE-CE routing protocol. I’m going to brush **very lightly** over this.

Consider the following network. R2, R3, and R3 are ISP routers in which R2 and R4 are PE routers. R7, R5, and R6 belong to the customer. R7 and R5 are both connected to the same PE while R6 is connected to another PE.

[![](http://web.archive.org/web/20140706180615im_/http://mellowd.co.uk/ccie/wp-content/uploads/2014/01/RFC4577_12.png)](http://web.archive.org/web/20140706180615/http://mellowd.co.uk/ccie/wp-content/uploads/2014/01/RFC4577_12.png)

The CE routers are running OSPF with the PE routers. The PE routers redistribute these OSPF routes into BGP and then converts them to VPNv4 NLRI. These VPNv4 NLRIare advetised to other PE routers via BGP. The PE also converts these VPNv4 routes back into OSPF and then off to the CE router:

[![](http://web.archive.org/web/20140706180615im_/http://mellowd.co.uk/ccie/wp-content/uploads/2014/01/RFC4577_22.png)](http://web.archive.org/web/20140706180615/http://mellowd.co.uk/ccie/wp-content/uploads/2014/01/RFC4577_22.png)

## **LSA Translation**

Taking the above image as an example. R7 is running OSPF with R2. R2 is also running OSPF with R5 and so any LSA updates are sent to R5 from R7 as per standard OSPF rules. When R2 needs to advertise the route over to R4, that LSA needs to be converted to a VPNv4 route. R4 will then convert that VPNv4 route back to an OSPF route on the other side. So how does the RFC state this LSA must be translated?

Section 4.2.6 of the RFC states:

> _For every address prefix that was installed in the VRF by one of its associated OSPF instances, the PE must create a VPN-IPv4 route in BGP. Each such route will have some of the_
>
> _following Extended Communities attributes:_
>
> _- The OSPF Domain Identifier Extended Communities attribute. If the OSPF instance that installed the route has a non-NULL primary Domain Identifier, this MUST be present; if that OSPF instance has only a NULL Domain Identifier, it MAY be omitted. This attribute is encoded with a two-byte type field, and its type is 0005, 0105, or 0205. For backward compatibility, the type 8005 MAY be used as well and is treated as if it were 0005. If the OSPF instance has a NULL Domain Identifier, and the OSPF Domain Identifier Extended Communities attribute is present, then the attribute’s value field must be all zeroes, and its type field may be any of 0005, 0105, 0205, or 8005._
>
> _- OSPF Route Type Extended Communities Attribute. This attribute MUST be present. It is encoded with a two-byte type field, and its type is 0306. To ensure backward compatibility, the type 8000 SHOULD be accepted as well and treated as if it were type 0306. The remaining six bytes of the Attribute are encoded as follows:_
>
> _Area Number – Route Type – Options_

In the test network I have already configured mutual redistribution between OSPF and BGP on both PE routers. Let’s see if the VPNv4 routes match what we expect from the RFC. R7 is advertising it’s loopback into OSPF. R2 converts this to a VPNv4 route. Let’s dig into the VPNv4 route itself:

R2#show bgp vpnv4 un all 7.7.7.7

BGP routing table entry for 2.2.2.2:1:7.7.7.7/32, version 28

Paths: (1 available, best #1, table A)

Advertised to update-groups:

1

Local

10. 0.27.7 from 0.0.0.0 (2.2.2.2)

Origin incomplete, metric 2, localpref 100, weight 32768, valid, sourced, best

Extended Community: RT:1:1 OSPF DOMAIN ID:0x0005:0x000000010200

OSPF RT:0.0.0.0:2:0 OSPF ROUTER ID:2.2.2.2:0

mpls labels in/out 26/nolabel

The route has a number of extended communities. The first one we’ll look at is the domain id value of

OSPF DOMAIN ID:0x0005:0x000000010200

IOS has encoded a type 005 domain ID with a value of 000000010200. This is interesting as I have not hard-coded a domain ID. Section 4.2.4 of the RFC states:

> _Each OSPF instance MUST be associated with one or more Domain Identifiers. This MUST be configurable, and the default value (if none is configured) SHOULD be NULL._

I have not configured one yet there is one. This means IOS is configuring one automatically even though it SHOULD be null.

The second community we’ll look at is the Route Type Extended Communities Attribute:

OSPF RT:0.0.0.0:2:0

The RFC states that the RT is broken up as follows:

1. 32-bit Area number
2. Route-type
3. Options

From our value above we can see that the original OSPF LSA is from area 0. Our RT says that this route comes from a type-2 LSA, but that’s incorrect as 7.7.7.7 is coming in via a type-1 LSA so that is a bit odd (as we shall see in a bit, it doesn’t actually matter whether this value is 1, 2, or 3 at the end of day). The final byte is the Options byte which is currently zero.

This VPNv4 update is now sent over to R4, who needs to take that information and create a new OSPF LSA and advertise it to R6. What does the RFC say about how the PE needs to do this?

## **VPNv4 routes received via BGP**

Sescion 4.2.8.1 of the RFC states:

> _With respect to a particular OSPF instance associated with a VRF, a VPN-IPv4 route that is installed in the VRF and then selected as the preferred route is treated as an External Route if one of the following conditions holds:_
>
> _- The route type field of the OSPF Route Type Extended Community has an OSPF route type of “external”_
>
> _- The route is from a different domain from the domain of the OSPF instance_

What this means is that if a route comes into a PE as an External or NSSA-External , it will always be so. It can never change. If a route comes in with a type of 1, 2, or 3; and the domain-id matches – then the local PE will originate a new type-3 LSA. i.e. the route will appear inter-area on the other customer sites.

If a route comes in with a type of 1, 2, or 3; and the domain-id does not match, then it becomes an external route.

All my routers are currently running IOS and OSPF process ID 100. This means currently all the domain-ids match. This means that R4 should be originating a new type-3 LSA. We can verify this on R6:

R6#sh ip ospf database summary 7.7.7.7

OSPF Router with ID (6.6.6.6) (Process ID 1)

Summary Net Link States (Area 0)

Routing Bit Set on this LSA in topology Base with MTID 0

LS age: 638

Options: (No TOS-capability, DC, Downward)

LS Type: Summary Links(Network)

Link State ID: 7.7.7.7 (summary Network Number)

Advertising Router: 4.4.4.4

LS Seq Number: 80000001

Checksum: 0x1EDF

Length: 28

Network Mask: /32

MTID: 0 Metric: 2

We see the 7.7.7.7/32 LSA coming from 4.4.4.4. This means the OSPF route should be inter area:

R6#sh ip route 7.7.7.7

Routing entry for 7.7.7.7/32

Known via "ospf 1", distance 110, metric 3, type inter area

Last update from 10.0.46.4 on FastEthernet1/0, 00:11:25 ago

Routing Descriptor Blocks:

* 10.0.46.4, from 4.4.4.4, 00:11:25 ago, via FastEthernet1/0

Route metric is 3, traffic share count is 1

Let’s change the domain-id on R4 to Null to see if this will change the route-type:

R4#conf t

Enter configuration commands, one per line. End with CNTL/Z.

R4(config)#router ospf 1

R4(config-router)#domain-id Null

R4(config-router)#end

Verify:

R6#sh ip route 7.7.7.7

Routing entry for 7.7.7.7/32

Known via "ospf 1", distance 110, metric 2

Tag Complete, Path Length == 1, AS 100, , type extern 2, forward metric 1

Last update from 10.0.46.4 on FastEthernet1/0, 00:00:08 ago

Routing Descriptor Blocks:

* 10.0.46.4, from 4.4.4.4, 00:00:08 ago, via FastEthernet1/0

Route metric is 2, traffic share count is 1

Route tag 3489661028

R6#sh ip ospf database external 7.7.7.7

OSPF Router with ID (6.6.6.6) (Process ID 1)

Type-5 AS External Link States

Routing Bit Set on this LSA in topology Base with MTID 0

LS age: 69

Options: (No TOS-capability, DC)

LS Type: AS External Link

Link State ID: 7.7.7.7 (External Network Number )

Advertising Router: 4.4.4.4

LS Seq Number: 80000001

Checksum: 0x863A

Length: 36

Network Mask: /32

Metric Type: 2 (Larger than any link state path)

MTID: 0

Metric: 2

Forward Address: 0.0.0.0

External Route Tag: 3489661028

As expected, the route is now external.

## **IOS-XR**

I’ve swapped out R4 with an IOS-XR box and configured it the same. How has R6′s loopback been converted into a VPNv4 route?

R2#show bgp vpnv4 un all 6.6.6.6

BGP routing table entry for 1:1:6.6.6.6/32, version 4

Paths: (1 available, best #1, table A)

Not advertised to any peer

Local

4. 4.4.4 (metric 4) from 4.4.4.4 (4.4.4.4)

Origin incomplete, metric 2, localpref 100, valid, internal, best

Extended Community: RT:1:1 OSPF RT:0.0.0.0:2:0 OSPF ROUTER ID:4.4.4.4:0

mpls labels in/out nolabel/16012

What’s interesting here is that IOS-XR follows the RFC a little bit more closely in that there is no implicit default Domain-ID. This means a L3VPN where some of your routers are IOS and some are IOS-XR, their Domain-IDs are not going to match unless you change the defaults. This should also mean on R6 I should be seeing external routes from R7 and R5:

RP/0/3/CPU0:R6#sho route ipv4 7.7.7.7

Thu Jan 2 17:05:59.526 UTC

Routing entry for 7.7.7.7/32

Known via "ospf 1", distance 110, metric 2

Tag 3489661028, type extern 2

Installed Jan 2 17:01:21.626 for 00:04:38

Routing Descriptor Blocks

10. 19.20.19, from 4.4.4.4, via POS0/7/0/0

Route metric is 2

No advertising protos.

RP/0/3/CPU0:R6#sho route ipv4 5.5.5.5

Thu Jan 2 17:06:05.378 UTC

Routing entry for 5.5.5.5/32

Known via "ospf 1", distance 110, metric 2

Tag 3489661028, type extern 2

Installed Jan 2 17:01:21.625 for 00:04:43

Routing Descriptor Blocks

10. 19.20.19, from 4.4.4.4, via POS0/7/0/0

Route metric is 2

No advertising protos.

Let’s hard-code the Domain-ID on R4 to ensure they now match:

RP/0/0/CPU0:R4#conf

Thu Jan 2 17:06:40.703 UTC

RP/0/0/CPU0:R4(config)#router ospf 100 vrf A domain-id type 0005 value 0000006$

RP/0/0/CPU0:R4(config)#end

Uncommitted changes found, commit them before exiting(yes/no/cancel)? [cancel]:yes

RP/0/3/CPU0:R6#sho route ipv4 5.5.5.5

Thu Jan 2 17:08:01.164 UTC

Routing entry for 5.5.5.5/32

Known via "ospf 1", distance 110, metric 3, type inter area

Installed Jan 2 17:07:33.737 for 00:00:27

Routing Descriptor Blocks

10. 19.20.19, from 4.4.4.4, via POS0/7/0/0

Route metric is 3

No advertising protos.

Knowing the implicit defaults on both platforms can certainly save you from headaches.

## **Multiple Domain-IDs**

IOS gives you the option to have secondary domain-IDs. The configuration guide doesn’t give all that information on what exactly it does, so it’s time to break out Wireshark. First I’ll configure multiple secondary domain-ids on R2:

R2#sh run | sec router ospf

router ospf 1 vrf A

domain-id type 0005 value 000000010200

domain-id type 0005 value 000000020200 secondary

domain-id type 0005 value 000000030200 secondary

domain-id type 0005 value 000000040200 secondary

log-adjacency-changes

redistribute bgp 100 subnets

Will this make R2 generate VPNv3 update with multiple extended OSPF communities? I’m capturing BGP traffic on R4′s core interface and done a route refresh:

[![](http://web.archive.org/web/20140706180615im_/http://mellowd.co.uk/ccie/wp-content/uploads/2014/01/RFC4577_3.png)](http://web.archive.org/web/20140706180615/http://mellowd.co.uk/ccie/wp-content/uploads/2014/01/RFC4577_3.png)

No. The VPNv4 update still only has a single domain-id. Secondary domain-ids are for a receiving PE to look at. If it receives OSPF updates from multiple different domain-id’s, if the ID matches any of the local secondary IDs, then it is considered a match. In order for this to work, all sides will need to match multiple IDs to consider everything internal as each PE can only originate a single ID outbound.
