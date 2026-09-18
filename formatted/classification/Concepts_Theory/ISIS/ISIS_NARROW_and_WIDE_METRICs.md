# ISIS NARROW and WIDE METRICs

source: [https://momcanfixanything.com/isis-narrow-and-wide-metrics/](https://momcanfixanything.com/isis-narrow-and-wide-metrics/)

Today we will talk about **ISIS narrow metrics** and **wide metrics**, but as always, let me give you some background first.

We start by looking at the **ISIS PDUs** (Packet Data Units), which is the term used to refer to ISIS packets.

* *ISIS PDU FORMAT**

All ISIS PDUs consist of:

- Protocol ID = 0x83 as specified by ISO 9577
- Header Length
- Version
- ID Length
- **PDU Type**:
    - **Level 1** or **Level 2**
    - **Hello**, **Sequenced Number Packet** (**SNP**) or **Link State Packet** (**LSP**)
- PDU version
- Maximum Number of Areas
- **PDU headers and TLVs**:
    - The PDU headers vary depending on the packet type.

![image-12.png](image/image-12.png)

* *PDU TYPES**

* *1) HELLO PACKETS**

Hello packets are used to discover ISIS neighbors, and determine whether they are Level 1 or Level 2, and to build and maintain adjacencies with those neighbors. They also identify the device, describe its capabilities, and the attributes of the interface where ISIS is running.

There are three types of IS-IS Hello packets:

![image-2.png](image/image-2.png)

In a broadcast network, separate LAN hello packets are exchanged if there are level 1 and level 2 routers . In a point-to-point network, only point-to-point hellos are exchanged regardless of the level.

In the example below, assume that R2 has both L1 and L2 adjacencies with both R1 and R3, and that interface ge-0/0/0 is configured as a broadcast interface, while ge-0/0/1 is configured as point-to-point.

R1 and R2 will exchange both L1 and L2 LAN Hellos, while R2 and R3 will exchange point-to-point hellos only.

![image-52.png](image/image-52.png)

Hello messages are transmitted periodically as multicast packets using:

- **DA = 01-80-C2-00-00-14** (Level 1) and
- **DA = 01-80-C2-00-00-15�**�(Level 2)

The hello interval is 3 sec for the Designated Intermediate System (DIS), and 9 seconds for non-DIS routers by default.  The hold time for an adjacency is 3 times the hello interval.

A hello message includes:

- Circuit Type which indicates the router level.

![image-6.png](image/image-6.png)

- **System ID** of the originator. Example: 0192.0168.0101.02
- **Hold Timer** = time before declaring the neighbor dead.
- **PDU Length**
- **Priority** for DIS election.
    - 0 and 127
    - Default = 64.
- **LAN ID** = System ID plus the Pseudonode ID.  Example: 0192.0168.0101.02
- **TLVs**

Below is an example of a **point-to-point hello packe**t, where you can see some of the fields mentioned above:

![image-10.png](image/image-10.png)

* *2) SEQUENCE NUMBER PDUs (SNPs)**

Sequence Number PDUs or Packets are used to ensure that neighbors have the most recent LSP information from each other. In other words, ensures that their Link State Databases are synchronized.

There are 4 types of SNPs:

![image-14.png](image/image-14.png)

* *Partial Sequence Number PDU**s are used to request a copy of a missing LSP on a broadcast network, or to acknowledge LSPs from a neighbor on a point-to-point network

A Partial Sequence Number packet lists the **most recent sequence number(s) of one or more LSPs**, and can be used to either acknowledge the reception of an LSP, or request details for a missing LSP. **PSNPs are similar in function to the Request and Acknowledgement packets in OSPF**.

* *Complete Sequence Number PDUs�**�are sent by the two ISIS routers on a point-to-point network, but only by the DIS on a broadcast network.

These packets contain the **most recent sequence numbers of all LSPs** in the database. They are sent periodically, or when a link first comes up, and are used to verify that the Link State Database is always in sync. **CSNPs are similar in function to the Database Descriptors in OSPF**, though OSPF DBDs are not sent periodically as CSNPs.

By default, CSNPs are sent every 10 sec on LAN broadcast links, and every 5 sec on point-to-point links.

Below is an example of a **Level 2 CSNP packet**, where you can see the list of LSPs with their IDs, sequence numbers, lifetime, and checksum:

![image-9.png](image/image-9.png)

* *3)** **LINK STATE PACKETS (LSPs)**

Link State Packets are used to exchange link state information and are similar in function to LSAs in OSPF.

They contain all the details about the network topology, including ISIS routers system IDs, prefixes, metrics, area IDs, and are used to build the link-state database. Like OSPF LSAs, LSPs are flooded within an an area.

LSPs are sent during adjacency formation, as a result of a topology change and in response to a sequence number PDU.

There are two types:

![image-15.png](image/image-15.png)

An LSP includes:

- **Remaining Lifetime** = how long the LSP is valid for (1200 sec by default).
- **LSP ID** = combination of System ID, Pseudonode ID and LSP number. Example: 0192.0168.0101.02-01
- **Attached (ATT)�**�= bit set by an L1/L2 router to inform an L1 neighbor that it can act as a gateway out of the area (similar to an OSPF ABR).
- **Overload (OL)** = bit that indicates that the router is “overloaded” thus not capable of forwarding transit traffic.
- **IS type =�**�bits that indicate a routers level:
    - Level 1 router = 0x1
    - Level 2 router = 0x3
- **TLVs**

![image-13.png](image/image-13.png)

Below is an example of a** Level 1 LSP**, where you can see different pieces of topology related information: the area the router belongs to, its hostname, the IDs of its neighbors and the metric to reach them, and the prefixes being advertised by the router and their associated metrics. You can also see that these different pieces of information are accompanied by a TLV#.

![image-120.png](image/image-120.png)

* *BUT WHAT ARE TLVs?**

You probably noticed that I colored the TLVs item differently when listing the fields included in the different packet types (hellos, SNPs, and LSPs).

I wanted to highlight that **all 3 types of packets have something in common: the use of TLVs**.

You might have seen the term before, or can deduce by looking at the example of the L1 LSP above, that a TLV is some kind of object or predefined attribute, which is exactly right. **TLVs are objects with three components**:

![image-16.png](image/image-16.png)

TLVs are the building blocks of IS-IS PDUs, and provide ISIS the flexibility to be easily extended to support new protocols and functionalities. One key example of this is the ability to propagate IP and IPv6 information, which was not part of the original design but was included later by defining new TLVs to carry the additional information. Check for example: [RFC1195](https://www.rfc-editor.org/rfc/rfc1195)

We are going to take a deep dive into the TLVs included in LSP packets, and **pay especial attention to those TLVs that include metrics.** From there will get into the different types of metrics and our main topic: narrow vs wide metric.

Some TLVs are common to multiple PDUs, while others are PDU-specific. Also, some TLVs can appear more than once within the same packet.

Here is a summary of the most common TLVs:

![image-17.png](image/image-17.png)

For a more complete list visit:

[https://www.iana.org/assignments/isis-tlv-codepoints/isis-tlv-codepoints.xhtml](https://www.iana.org/assignments/isis-tlv-codepoints/isis-tlv-codepoints.xhtml)

I particularly like how you can sort the list in this document by packet type, TLV number, or by the presence of TLVs in the different packets. Definitively a great resource.

Let’s now take a look at some of the contents of the ISIS database in our lab topology, which is shown below. We will focus on the information advertised by vMX1.

![image-18.png](image/image-18.png)

I split the output of the **show isis database extensive** command into sections because, as you can imagine the output of this command can be very long, and it is easier if we analyze it in smaller sections or blocks.

This first block of the output displays the neighbors of vMX1, and their metric. The metric value of every ISIS interface, as we will see later, is 10 by default.   The IP prefixes listed are the networks vMX1 is connected to, including its loopback interface with IP address **10.100.100.1/32** (metric 0), and the two prefixes configured as static routes.

![image-19.png](image/image-19.png)

The next block displays the LSP header which includes LSP ID, Router ID, remaining lifetime, Level, protocols, and NLPID 0x83 (ISIS).

![image-20.png](image/image-20.png)

And finally, we have the TLVs:

![image-21.png](image/image-21.png)

Notice that TLV 22, contains Sub-TLVs.  These were introduced in [RFC3784 –  Intermediate System to Intermediate System (IS-IS) Extensions for Traffic Engineering (TE)](https://tools.ietf.org/html/rfc3784). We will come back to this later.

* *LINK STATE PACKETS TLVs and METRICs**

We are now going to move our attention to 5 specific TLVs included in the LSP packets: **TLVs 2**, **22,** **128**, **130**, and **135**, which carry either ISIS router reachability or network prefix reachability.

* *1) TLV 2—IS Reachability**

- Describes the IS neighbors of the local router
- Advertises ISIS neighbors and the metric to reach them.

![image-22.png](image/image-22.png)

* *2) TLV 22—Extended IS Reachability**

- Advertises additional capabilities and information about IS neighbors
- Advertises ISIS neighbors and the metric to reach them.

![image-23.png](image/image-23.png)

* *3) TLV 128—IP Internal Reachability**

- Describes the internal IP information known by the local router
- Advertises IP prefixes and metric

![image-24.png](image/image-24.png)

* *4) TLV 130—IP External Reachability**

- Describes the external IP information known by the local router
- Advertises IP prefixes and metric

![image-24.png](image/image-24.png)

* *5) TLV 22—Extended IS Reachability**

- Advertises information about the local router’s IP reachability
- Advertises IP prefixes and metric

![image-26.png](image/image-26.png)

You can see that **all 5 TLVs include metrics**, which, as you know, are used by SPF to calculate the best path to destinations.

However, you can also clearly see that depending on the TLV type, these metric can be:

1) **metric**, or **wide metric** (1, 3 or 4 bytes long)

2) a different metric name:  **delay**, **default**, **expense**, and **error**.

![image-27.png](image/image-27.png)

But, what are all these metrics, and how do they work (or not)?

* *METRIC TYPES (names)**:

Maybe this will be just for your general knowledge, but in the ISIS original specifications 4 different metrics were included:

- **default�**�= guess they couldn’t figure out a good name!
- **delay�**�= yes, delay, like in EIGRP, yikes!  LOL!
- **expense** = $$$, OK!?!?
- **error** = how unreliable, how do you figure that out?

Guess what! Only the “default” metric has been implemented by vendors, and sometimes I wish we could just forget about the original specs and just give this “default” metric a proper name and change the outputs of the commands.

Since that is not going to happen, you will probably agree with me that a good reason to be aware of this naming conundrum is so that you don’t get caught by surprise when you check the ISIS database and see the word “default” metric next to a value that is NOT the default value of 10. Or you don’t get caught by surprise if you do a packet capture and see the word default when you are certain that you are NOT using default values for your interfaces.  Been there done that!! Have had to explain this to customers and students a number of times: “no, it’s not a bug, that’s the “name” of the metric!”

You will also find that documents such as RFC 3784, talk about these different metrics a little bit, and then just refer to the only one used as **default metric** in the rest of the document. Maybe there is a good reason they decided to call it default metric, but I cannot think of one.

Here is an example of this confusing naming selection (hopefully no longer confusing after you read this today):

![image-29.png](image/image-29.png)

![image-31.png](image/image-31.png)

![image-34.png](image/image-34.png)

![image-33.png](image/image-33.png)

With all that said, and since you are now aware that the metric everybody uses is actually called **default**, and you saw the examples, please allow me to just call it metric for the rest of the article. It will make my writing and your reading easier.

I am sure you would rather read _“the default metric value is 10” vs “the default value for the default metric is 10”_, and so on!

So yes, **the default metric value is 10 for any interface**, **except for the loopback interface which has a metric of 0**.

The value **can be manually set on a per-interface, per-level basis** as shown in these examples:

![image-35.png](image/image-35.png)

You can also configure the router to automatically calculate the metric using the same formula used by OSPF, by adding a reference bandwidth to the isis configuration as shown in this example:

![image-36.png](image/image-36.png)

After you add this command, the metric for all interface will be calculated as:

![image-37.png](image/image-37.png)

* *NOTE**: in OSPF the router uses a **reference-bandwidth = 10^8** by default.

Back to our TLVs…

If you paid attention to the table that summarizes the metrics included on TLVs 2, 22, 128, 130, and 135, in the previous section, you noticed that some metrics are only 6 bits long, while others are 3 or 4 bytes long.

We refers to the **6-bit long metrics as narrow metrics**, and the **3 or 4-byte metrics as wide metrics**.  Easy to figure out where the names come from!
![1f60a.svg](image/1f60a.svg)

Our 5 TLVs use one or the other as shown in the table:

![image-38.png](image/image-38.png)

O.K. … wide metrics are longer. What’s so interesting about that?

A few things actually!

* *NARROW VS WIDE METRICS**

Narrow metrics are the original metrics, and because they are only **6 bits long**, they **limit the metric of an interface to a maximum of 63**.  **If a larger value is configured, the maximum value is still advertised**.

Narrow metrics also set a limitation for the** total metric on a given path. The maximum value allowed is 1023**.

On the other hand, wide metrics, either **3 or 4 bytes long**, **allow configuring the metric of an interface up to 16,777,215**.

The 4-byte value allows for inter-area advertisements, which could potentially have accumulated metrics larger than 16,777,215.

So, wide metric allows a maximum value of 16,777,215, pretty large number! Why do I need that? The reasoning behind this big change was to remove the limitations caused by the 6-bit metrics, and allow ISIS to support larger networks, and provide granularity for traffic engineering purposes, specially when combined with MPLS.

Now, **when your router advertises wide-metrics, that doesn’t just mean that the metric is larger, it actually means that the router is using TLVs, and Sub-TLVs defined to carry these longer metrics (TLVs 22, and sub-TLVs, and TLV 135).**

[RFC4784](https://tools.ietf.org/html/rfc3784) describes all the details of the new TLVs/Sub-TLVs.

But let’s jump back to our lab, and take a look at some of these ideas before we continue:

We have ISIS configured on all the routers in the lab, using the default values.

Here is the configuration of vMX1, for example:

![image-40.png](image/image-40.png)

If we check the ISIS interfaces, and the database, we can see how the metric of all interfaces is currently set to 10.

![image-41.png](image/image-41.png)

We now change the metric of ge-0/0/0.0 to 100:

![image-42.png](image/image-42.png)

and we check the results:

![image-43.png](image/image-43.png)

So far, so good!

But when we check the ISIS database we find a couple of interesting things:

![image-44.png](image/image-44.png)

First, the prefix configured under ge-0/0/0.0 is being advertised twice, using both a TLV 128 (IP Internal Reachability), and TLV 135 (Extended IP Reachability).

Section 5 of [RFC3787](https://tools.ietf.org/html/rfc3787#section-5), describes the migrating path from Narrow Metrics to Wide metrics, and basically states that unless all ISIS devices have been migrated to wide metrics, devices that support wide metrics MUST continue to support and use narrow metrics.

Thus, the default behavior in Juniper devices, as well as other vendors, is to advertise both narrow and wide metrics.

We also noticed, that the **metrics was set to 63**, which is probably not as surprising since I said before: **_because narrow metrics are only 6 bits long, the maximum interface metric is 63 and if a larger value is configured, the maximum value is still advertised._**

What you might have not expected is that **BOTH the narrow metric and the wide metric are set to 63**.

Because of the same reasoning behind advertising both metrics, **the value of the wide metrics is limited by the limitations of the narrow metrics**. Yes, that essentially defeats the purpose of using wide metrics.

Then, how do we fix it? Easy! Get rid of the narrow metrics! All your routers can do wide metrics these days (hopefully) thus, you don’t need to keep the narrow metrics.  Just be aware that there are some side effects of changing from dual metrics to wide metrics only.

* *CONFIGURING WIDE METRICS ONLY**

We can stop the advertisement of narrow metrics by saying: “only send wide metrics” using the **wide-metrics-only** command. This is **configured for an entire level, not per interface**, and preferable you want to do it on all routers.

If we add this command to VMX1 on our previous scenario:

![image-46.png](image/image-46.png)

We now see this in our database:

![image-45.png](image/image-45.png)

The advertised metric is now 100, which is what we had configure, but where did the other TLV go?

* *WIDE METRICS ONLY means: only send TLVs with wide metrics!!!** That means:

![image-48.png](image/image-48.png)

* *TLVs 2, 128, and 130 are gone!** And with them, **the metric value limit of 63 is also gone!** Which is great, but again, there are other implications you would need to keep an eye on after making this change.

Why is that?

* *With narrow metrics**, we have two TLVs to advertise IP reachability: **TLV 128 for internal, and TLV130 for external prefixes** (redistributed into ISIS). **With wide metrics there is only ONE TLV (135)**.

* *With the Extended IP Reachability TLV there is no distinction between internal and external prefixes** which affects ISIS preferences and ISIS propagation rules.

* *WIDE METRICS AND ISIS PREFERENCES**

When Junos learns about a destination from different sources, it uses preference values to decide which route should become the active route, and be installed in the forwarding table.  Each source of routing information, including direct routes, static routes, or routes learn from dynamic routing protocols such as ISIS, OSPF, or BGP have **one or more** such preference values.

OSPF for example, has 2 different values:

![image-49.png](image/image-49.png)

ISIS has 4:

![image-50.png](image/image-50.png)

When you configure **wide-metrics-only** only two of these preference values are used. Remember that the difference between internal and external routes disappears:

![image-51.png](image/image-51.png)

This could have a significant impact in the route selection process depending on the topology and protocols running in the network.

In the following example, router vR1 is redistributing the static route for 172.16.1/24 into both OSPF and ISIS.

![image-53.png](image/image-53.png)

* *NOTE**: for the next few examples I am using routing instances (virtual routers) connected using logical tunnel interface (lt) so keep an eye on the name of the routing table in the examples.

* *Without wide-metric-only**, this is how the routing tables look like:

![image-54.png](image/image-54.png)

![image-55.png](image/image-55.png)

Notice that for both ISIS and OSPF there is a combination of internal (preference 10 for OSPF and 18 for ISIS), and external routes (preference 150 for OSPF and 165 for ISIS)

We take a closer look at the route being redistributed:

The routing table of vR2 shows that the route was learned from OSPF, and has a preference value of 150. The route was learned from an **LSA type 5�**�that was injected by vR1 as a result of redistributing the static route into OSPF.

![image-56.png](image/image-56.png)

The routing table of vR3 shows that the route was learned via ISIS and has a preference value of 165. This route was advertised by vR1 using **TLVs 130 (IP external prefix)** and also TLV **135 (IP extended prefix)**. **TLV 130 is used by the receiving router for route calculations. Thus the preference value is 165**.

![image-57.png](image/image-57.png)

We also check vR4, and we find two routes. One was learned from OSPF (from the LSA type 5), and the other one from ISIS (from TLVs 130).

![image-58.png](image/image-58.png)

![image-59.png](image/image-59.png)

The router compares the preference values of the two routes, and chooses the OSPF route because it has the lowest preference value.

We are now going to configure **wide-metrics-only**. We are not touching the metrics, we are not touching the preference values, or configuring policies. **Nothing but wide-metrics-only!**

![image-60.png](image/image-60.png)

There are no changes on the routing table of vR2, as expected:

![image-61.png](image/image-61.png)

On vR3, **the preference value for the route in now 18, instead of 165**. The next-hop and output interface did not change, so there is not a significant difference.

![image-62.png](image/image-62.png)

On vR4 however, the result is a drastic change in the way traffic going to 172.16.1/24 will be forwarded.

![image-63.png](image/image-63.png)

Before, the OSPF route was selected because the ISIS route had a preference of 165 (vs. 150 for OSPF):

![image-64.png](image/image-64.png)

Now, the ISIS route is selected because it had a preference value of 18 (vs. 150 for OSPF):

![image-65.png](image/image-65.png)

* *WIDE METRICS AND ISIS ROUTE PROPAGATION RULES.**

By default:

1) L1 **interna**l routes are advertised to both L1 and L2 neighbors

2) L1 **external** routes are advertised to L1 neighbors but NOT to L2 neighbors

3) L2 (**both internal and external**) routes are advertised to L2 neighbors but NOT to L1 neighbors

![image-67.png](image/image-67.png)

The rule that we care about right now is the one about L1 external routes which we can state this way:

* *L1 routes that were injected into ISIS via redistribution, are treated by default as L1 external routes, and are NOT advertised to L2 neighbors by default.**

We know now that the difference between internal and external routes disappears when we configure wide metrics only.

And if there is no difference between L1 routes that are created because ISIS was configured on an interface (internal) or redistributed into ISIS, all L1 routes are treated equally and are now advertised to L2 neighbors.

![image-68.png](image/image-68.png)

* *NOTES**:

– It is very important that you understand that it is NOT that the second rule no longer applies to external routes, but that the routes are no longer considered external routes even though they are being injected into ISIS via redistribution!!!

– These rules can always be bypassed using a routing policy.

![image-70.png](image/image-70.png)

![image-69.png](image/image-69.png)

This policy would NOT be needed if R3 was configured with **wide-metrics-only**, because vR11 would be learning the route as an “internal” level 1 route:

![image-71.png](image/image-71.png)

Now, consider this maybe unusual situation (that I came up with); maybe some legacy that we inherited from someone else and that we are now responsible for.

We have two sites, with end users that should be able to communicate with users on the other site, or with the rest of the network. There are also some local resources that are only to be accessed by users in the same site.

![image-72.png](image/image-72.png)

We are running ISIS level 1 on each site, and the interfaces were the users are connected are part of ISIS. The interfaces connected to the servers (172.16.1/24) are NOT, because we do not want these networks to be advertised anywhere else. And yes, the same prefix is being used on both sites.

In order to provide connectivity between the users and the local servers, someone decided to redistribute the 172.16.1/24 prefix, knowing that it would not be advertised to level 2, because of the rules we previously described.

Checking the routing tables confirms that the L1/L2 routers have routes to 172.16.1/24 as external routes:

![image-73.png](image/image-73.png)

![image-74.png](image/image-74.png)

![image-75.png](image/image-75.png)

![image-76.png](image/image-76.png)

The backbone L2 routes don’t have this prefix in the routing table. as expected.

![image-77.png](image/image-77.png)

We also confirm that we can reach 172.16.1/24 from the users’ networks:

![image-78.png](image/image-78.png)

Everything looks good!!!

Then one day, we are required to move to **wide-metric-only**.

I am sure you know where I am going now…

After we add **wide-metric-only** everywhere, **without changing anything else at all**!, we check the routing tables again and find that:

There is no difference on the routing tables of the L1/L2 routers in terms of metric or the next hop being used, BUT the routes now show as “internal” level 1 instead of external. We know that because the preference value is now 15 instead of 160.

![image-79.png](image/image-79.png)

![image-80.png](image/image-80.png)

![image-81.png](image/image-81.png)

![image-82.png](image/image-82.png)

Not only that, we find that the L1/L2 routers are now advertising propagating the route for 172.16.1/24 to the L2 backbone!!!!

![image-83.png](image/image-83.png)

![image-84.png](image/image-84.png)

Which might be setting us up for a rough day at work later on.

Just for fun let’s try something:

Let’s trace 172.16.1.2 from router vR12.

![image-85.png](image/image-85.png)

As expected, traffic is going straight down to vR14.

Let’s now shutdown the interface facing the servers on the same site:

![image-86.png](image/image-86.png)

And try traceroute again:

![image-87.png](image/image-87.png)

Just imagine yourself or one of your coworker seeing this in your network, and going: “Wait.., what? (or something like that)” How is this happening?

Let’s take a look at the routes to find the answer:

![image-88.png](image/image-88.png)

vR12, the router we are tracing from, has a default route that it created upon receiving an LSP from vR11 with the Attach bit set. The specific route to 172.16.1.2 is no longer present because it is not being advertised by vR14 any more.

Router vR11 now has a level 2 route for 172.16.1.0/24 that he learned from router vR21.

![image-90.png](image/image-90.png)

vR21 learned it from vR22, which knows about it because vR31 and vR33 are now advertising the route to the L2 backbone (remember we enabled **wide-metrics-only** everywhere).

![image-89.png](image/image-89.png)

![image-92.png](image/image-92.png)

Yes, we should not be using the same prefix in these two sites, BUT most importantly, we should be using some policies to control what gets advertised instead of relying on a propagation rule that just went poof, as soon as we changed the metrics behavior of our protocols.

We are going to this the correct way:

* *Keeping wide-metric-only configured everywhere**, we add the servers facing interface on both routers vR14 and vR34 to isis, as shown in the diagram.

![image-93.png](image/image-93.png)

We could also change the address of the interface facing the servers on router vR34 but let’s just leave it as it is just to show how the policy fixes things.

Here is how our routing tables look like now after adding the interfaces to ISIS:

Routers vR11 to vR13 as well as vR31 to vR33 have the route to 172.16.1.0/24 as an L1 route (preference 15).

![image-94.png](image/image-94.png)

![image-95.png](image/image-95.png)

![image-96.png](image/image-96.png)

![image-99.png](image/image-99.png)

![image-100.png](image/image-100.png)

![image-101.png](image/image-101.png)

vR21 and vR22 have learned the route as Level 2 routes (preference 18) from vR13 and vR33 respectively.

![image-97.png](image/image-97.png)

![image-98.png](image/image-98.png)

In order to stop the advertisement of the route beyond the L1/L2 routers (vR11, vR13,  vR31, and vR33), we create a routing policy and apply it to all 4 routers .

![image-102.png](image/image-102.png)

Routers vR11 to vR13 and vR31 to vR33 will still have the route to 172.16.1.0/24 as an L1 route (preference 15) as shown before, but neither vR21 nor vR22 will know about 172.16.1.0/24 anymore.  Just as we needed.

![image-103.png](image/image-103.png)

Now it does not matter if you use wide or narrow/wide metrics, or if you redistribute the route, or add it to ISIS. As long as this policy is in place, a level 1 route (internal or external) to 172.16.1.0/24 will NOT be advertised to L2 neighbors.

One last thing before we finish todays’ topic:  is it possible to have a mix of routers doing wide metrics only and routers doing narrow metrics? Yes! maybe not a good idea, but yes!

* *WHAT IF NOT ALL ROUTERS ARE CONFIGURED WITH WIDE METRICS ONLY?**

We now have the topology below:

![image-104.png](image/image-104.png)

The interfaces facing the end users are NOT part of ISIS, and are being redistributed into ISIS. Also, all routers except for vR14 and vR34 are configured with **wide-metric-only**.

![image-105.png](image/image-105.png)

![image-106.png](image/image-106.png)

You would think that the adjacencies between vR14 and its neighbors vR12 and vR13 or between vR34 and its neighbors vR32 and vR33 would fail, since they are not configured the same in terms of metrics, but that is NOT the case.

![image-107.png](image/image-107.png)

If we clear the adjacencies they come back up without an issue, which confirms that not having the routers consistently configured with wide-metric-only has no effect over adjacency formation.

![image-108.png](image/image-108.png)

We see the effect of not having consistent configuration in the way routes propagate:

![image-109.png](image/image-109.png)

![image-110.png](image/image-110.png)

![image-111.png](image/image-111.png)

![image-112.png](image/image-112.png)

![image-113.png](image/image-113.png)

![image-114.png](image/image-114.png)

The routing tables on vR11, vR12, and vR13 have **Level 1 external route (with preference 160) for 172.10.2.0/24** even though they are **configured with wide-metrics-only**!!

On the other hand, vR14, which is **NOT configured with wide-metrics-only** has a **level 1 “internal” route (preference 15) for 172.10.1.0/24**  in its routing table**.**

Also, as a result of the routes to 172.10.2.0/24 being external, they are NOT being advertised to the L2 backbone routers. The routes to 172.10.1.0/24 are.

Here is what is happening:

vR13 which IS configured with **wide-metrics-only**, is advertising 172.10.1.0/24 using ONLY a TLV 135:

![image-115.png](image/image-115.png)

vR14, which is NOT configured with **wide-metrics-only**, is advertising 172.10.2.0/24 using both TLV 130 (external) and TLV 135 (extended):

![image-116.png](image/image-116.png)

That is why vR11, for example, has a L1 “internal” route for 172.10.1.0/24, and a L1 external route for 172.10.2.0/24.

![image-117.png](image/image-117.png)

* *Configuring wide-metrics-only affects what the router advertises, not what the router accepts and uses for route calculation purposes.**

* *Summarizing what we have learned:**

Link State Packets (LSPs) carry ISIS neighbor information within TLVs 2, and 22, and prefix information within TLVs 128,130, and 135.

These TLVs advertise IS and prefix reachability using either narrow or wide metrics.

![image-118.png](image/image-118.png)

Junos advertises all 5 TLVs by default, which means IS and prefix reachability are advertised with both narrow and wide metrics by default.

Narrow metrics **limit the metric of an interface to a maximum of 63** while wide metrics allow configuring the metric of an interface up to 16,777,215.  However, when both types are advertised, wide metrics are limited by the narrow metric limitations.

To remove the limitations and take full advantage of the longer metrics, **wide-metrics-only** can be configured. This stops the router from advertising TLVs 2, 128, and 130.

![image-119.png](image/image-119.png)

If a router stops advertising TLVs 128, and 130, and advertises prefixes using TLV 135 only, there is NO distinction between routes that were injected into ISIS because the interface where the prefix is configured was added under ISIS (which would make the route internal), or because redistribution (which would make the route external).

As a result:

– There is no preference value difference between two routes for the same prefix, even if one was injected into ISIS as “internal” and the other as “external”.  Only two preference values are used with wide-metrics-only (15 for L1, and 18 for L2)

– Prefixes that were injected into ISIS as “external” routes are automatically advertised to L2 neighbors, because the propagation rule that states “L1 external routes are advertised to L1 neighbors but NOT to L2 neighbors” does not apply to these routes anymore.

* *Thank you for reading!!**
