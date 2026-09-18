# [M/MX/T] Troubleshooting Checklist - BFD

SYMPTOMS:

- BFD session is not coming up or it went down
- BFD flapping

### BFD Session Not UP:

```text
Perform the following steps to troubleshoot a BFD session that is not in the UP state:
```

Step 1: Verify the configuration of the BFD.

```text
> Refer to the technical documentation here:
>
> - [Configuring BFD for Static Routes for Faster Network Failure Detection](https://www.juniper.net/documentation//en_US/junos/topics/example/policy-static-routes-bfd.html)
> - [Configuring BFD on Internal BGP Peer Sessions](https://www.juniper.net/documentation//en_US/junos/topics/example/bgp-bfd-ibgp.html)
> - [Configuring PIM and the Bidirectional Forwarding Detection (BFD) Protocol](http://www.juniper.net/techpubs/en_US/junos/topics/topic-map/mcast-pim-bfd.html)
> - [Configuring BFD for MPLS IPv4 LSPs](http://www.juniper.net/techpubs/en_US/junos/topics/usage-guidelines/mpls-configuring-bfd-for-mpls-ipv4-lsps.html)
>
> Important:  Verify that the configuration settings on both ends match, and verify that both are interoperable for BFD.
```

```text
Step 2: Check if the interface through which BFD is sending packets is in the UP state; use the command
```

```text
show interfaces interface-name extensive
```

```text
> This output also gives error statistics that might indicate if packet drops are seen on the interface.
>
> For more information on troubleshooting Ethernet interfaces, refer to [KB26486 - Troubleshooting Checklist - Ethernet Physical Interfaces](https://kb.juniper.net/KB26486)
```

Step 3: Verify that the next-hop IP route is available on the local router to which the router is sending BFD hello packets; use the command

```text
show route x.x.x.x
```

```text
> Note: For a single-hop BFD, even though the next hop is directly connected and the route is always there on the local router, in some corner cases if this is not the case then the above output gives information related to the next hop.
```

Step 4: Check if there is an issue with any intermediate media/device to the other end router.

```text
> The physical path of a network data circuit sometimes consists of a number of segments interconnected by devices that repeat and regenerate the transmission signal. An issue with any intermediate circuit may lead to packet loss. Hence, to verify or troubleshoot, perform a loopback test and a BERT test.
>
> For more information, refer to [KB26486 - Troubleshooting Checklist - Ethernet Physical Interfaces](https://kb.juniper.net/KB26486).
```

Step 5: Configure bfd and ppmd traceoptions, and review the traceoptions output.

```text
user@Router# show protocols bfd
```

traceoptions {

```text
file bfd-log size 10m files 10;
```

flag all;

}

```text
user@Router# show routing-options ppm
```

traceoptions {

```text
file ppm-log size 10m files 10;
```

flag all;

}

For help on how to configure traceoptions and view debug output, refer to [KB16108 - Configuring Traceoptions for Debugging and Trimming Output](https://kb.juniper.net/KB16108).

Step 6:  Configure a specific firewall filter term under the lo0 interface to check if the first two packets are being processed by routing engine. Look for any BFD policer that might be dropping the session

to come up.

```text
> In addition to checking whether packets are being reached at the routing engine, an FW can be configured to count the BFD packets to confirm the same quantity is being sent and received. It can also be correlated with the filter configured under lo0.
>
> Example of the firewall filter that can be used:
>
> set firewall filter family inet BFD interface-specific
>
> set firewall filter family inet BFD term In from protocol udp
>
> set firewall filter family inet BFD term In from port [4784 3784 3785]
>
> set firewall filter family inet BFD term In from source-address <>
>
> set firewall filter family inet BFD term In from destination-address <>
>
> set firewall filter family inet BFD term In then accept
>
> set firewall filter family inet BFD term In then count BFD-In
>
> set firewall filter family inet BFD term In then log
>
> set firewall filter family inet BFD term Out from protocol udp
>
> set firewall filter family inet BFD term Out from port  [4784 3784 3785]
>
> set firewall filter family inet BFD term Out from destination-address <>
>
> set firewall filter family inet BFD term Out from source-address <>
>
> set firewall filter family inet BFD term Out then accept
>
> set firewall filter family inet BFD term Out then count BFD-OUT
>
> set firewall filter family inet BFD term Out then log
>
> set firewall filter family inet BFD term anything then accept
>
> This FW should apply in/out direction in the outgoing interface along with lo0, so make sure first packets are handled by the RE, then moving to the pfed/ppmd.
```

- --

### BFD Flapping:

BFD flapping can be verified with repeated syslog messages indicating BFD session churning UP and DOWN states, as shown below:

```text
bfdd[711]: BFDD\_TRAP\_STATE\_DOWN: local discriminator: 3, new state: down rpd[819]: RPD\_OSPF\_NBRDOWN: OSPF neighbor 208.108.231.66 (realm ospf-v2 vlan.1933 area 0.0.0.0) state changed from Full to Down due to InActiveTimer (event reason: BFD session timed out and neighbor was declared dead)
```

```text
bfdd[711]: BFDD\_TRAP\_STATE\_DOWN: local discriminator: 3, new state: down rpd[819]: RPD\_OSPF\_NBRDOWN: OSPF neighbor 208.108.231.66 (realm ospf-v2 vlan.1933 area 0.0.0.0) state changed from Full to Init due to 1WayRcvd (event reason: neighbor is in one-way mode)
```

Also, the current status of the BFD session may be down:

```text
User@Router> show bfd session
```

```text
Detect   Transmit Address    State     Interface      Time     Interval  Multiplier
```

1. 1.100.1     Down         4.000     0.900                        1

To fix BFD flapping issues, perform the following steps:

CAUTION: Some of the command outputs in the following steps are not officially supported by Juniper Networks; nevertheless, they are helpful in troubleshooting. It is not recommended to run these commands in a 'live' production network.  A maintenance window is recommended.

Note: The default operational mode of BFD for all protocols is distributed mode (runs on PFE), one exception being OSPFv3 which runs on the Routing Engine by default (centralized mode).

1. Identify the current affected BFD session, whether belonging to single hop or multihops.

   Single-hop BFD control packets use UPD port 3784, and multihop BFD control packets use UDP port 4784. The single-hop BFD may or may not use distributed ppmd, but the multihop BFD is always Routing Engine-based, with no relation to the ppman on the PFE.

   Note: Multihop BFD can be deployed by distributed ppmd  through RLI 13271- Distributed BFD for multi-hop protocols (BGP, static routes, and so on) .

   Starting with Junos Release 12.3, multihop BFD is not Routing Engine-based.
2. If it is a non-distributed (Routing Engine-based) BFD, then verify if any process is hogging the CPU and hence missing the processing of BFD packets.

```text
Verify the CPU utilization on the Routing Engine with show chassis routing-engine or show system process extensive commands.  If the CPU is high, refer to [KB26261 - Troubleshooting Checklist - Routing Engine High CPU](https://kb.juniper.net/KB26261) to troubleshoot the high CPU. One way to mitigate BFD flapping due to high Routing Engine CPU is to increase the minimum interval of BFD keepalives; for more information, see Step 8 below.
Monitor the interface on which the affected BFD session is running and verify if the BFD control traffic is hitting the local interface.
```

   If there are no inbound packets or if some of them are dropping somewhere in between, then the issue is external (with the asymmetric traffic path or the intermediate device suffered from a hardware or transmission issue).
4. Check the Ethernet switch errors between the CB/FPC/RE.

   To do this, review the output of the following commands:

```text
show chassis ethernet-switch statistics
```

```text
show chassis ethernet-switch error
If it is distributed, then check PPM stats.
```

   Delegate the BFD processing job to the PFE (also called distributed mode, which is the default). BFD sessions are very lightweight, hence flaps generally do not occur when sessions are distributed. If they do, then it could be a PFE issue.

   To check PPM stats, first login to the corresponding PFE using >start shell pfe network fpcX, then use the show ppm statistics protocol bfd command:

   ADPC5( vty)# show ppm statistics protocol bfd

   BFD input errors:

   No interface            : 0

   No family               : 0

   Not IPv4                : 0

   Bad IP checksum         : 0

   Bad IP options          : 0

   Bad IP len              : 0

   Bad UDP checksum        : 0

   Bad UDP len             : 0

   Unknown UDP ports       : 0

   Local ifl failures      : 0

   Prefix len mismatch     : 0

   Authentication failure  : 0

   RX Queue overflow       : 0

```text
Packet get failed       : 0
```

   Total BFD Packets       : 0

   Absorbed BFD Packets    : 0

   Packet send drops       : 0

   Refresh stats:

   Adjacencies : Refreshed     0    Not-refreshed     0

   Transmits   : Refreshed     0    Not-refreshed     0

   Interfaces  : Refreshed     0    Not-refreshed     0

   Stats Groups: Refreshed     0    Not-refreshed     0

```text
Verify that no error counters are incrementing.
Check if any packet drops are reported on the Packet Forwarding Engine.
```

   To do this, use the show pfe statistics traffic command:

   lab# run show pfe statistics traffic

   Packet Forwarding Engine traffic statistics:

   Input packets: 2004354 0 pps

   Output packets: 2008275 0 pps

   Packet Forwarding Engine local traffic statistics:

   Local packets input : 870715

   Local packets output : 923411

   Software input control plane drops : 0

   Software input high drops : 0

   Software input medium drops : 0

   Software input low drops : 0

   Software output drops : 0

   Hardware input drops : 0

   Packet Forwarding Engine local protocol statistics:

   HDLC keepalives : 0

   ATM OAM : 0

   Frame Relay LMI : 0

   PPP LCP/NCP : 0

   OSPF hello : 224323

   OSPF3 hello : 0

   RSVP hello : 0

   LDP hello : 0

   BFD : 0

   IS-IS IIH : 0

   LACP : 0

   ARP : 39370

   ETHER OAM : 0

   Unknown : 42774

   Packet Forwarding Engine hardware discard statistics:

   Timeout : 0

   Truncated key : 0

   Bits to test : 0

```text
Data error : 0
```

   Stack underflow : 0

   Stack overflow : 0

   Normal discard : 51395

   Extended discard : 0

   Invalid interface : 0

   Info cell drops : 0

   Fabric drops : 0

```text
Packet Forwarding Engine Input IPv4 Header Checksum Error and Output MTU Error statistics:
```

   Input Checksum : 0

   Output MTU

```text
If packet drops are seen, then the packets that are being dropped randomly could be BFD packets. All BFD packets are treated as data packets, so it could be possible that they are being dropped randomly.
```

```text
Verify if packets are getting dropped by issuing the following commands:
```

```text
show system queues
```

```text
show ttp statistics  (you need to log in to the corresponding FPC, as shown in Step 5)
Check which threads are consuming the CPU.
```

   Usually D-BFD flaps are seen when an ukernel thread hogs the CPU.  To check, issue the show threads command at the corresponding PFE.

   ADPC5( vty)# show threads

```text
PID PR State Name Stack Use Time (Last/Max/Total)
```

   - -- -- ------- --------------------- --------- ---------------------

   1 H asleep Maintenance 296/2048 0/0/0 ms

   2 L ready Idle 280/2056 5/5/327341520 ms

   3 H asleep Timer Services 288/2056 0/0/0 ms

   5 L asleep Sheaf Background 376/2048 5/5/5 ms

   6 H asleep IPv4 PFE Control Background 296/8200 0/0/0 ms

   7 M asleep DCC Background 280/4104 0/0/0 ms

   8 M asleep OTN 360/4104 0/0/0 ms

   This should give us an indication about which threads hog the CPU. If a flap is seen when a link is disabled or enabled, then it could be an issue with a CPU hog and should be investigated.

```text
If you doubt that BFD packets are being dropped, then first make it centralized with the command set routing-option ppm no-delegate-ppm, followed by clear bfd session.
```

   Increase the timer of the BFD session; minimum on the RE should be 100 ms.

```text
Start monitoring the interface; if there is a lag in packets received, then you know there is an issue with the PFE.
Check the minimum-interval.
```

   When configuring BFD, care should be taken when choosing minimum-interval under bfd-liveness-detection. If you choose a very low minimum-interval, then BFD will send hello packets very aggressively, which in some cases might lead to BFD flap.

   For a recommendation on the optimal values to choose for  minimum-interval, refer to the technical documentation on [Configuring BFD for Static Routes for Faster Network Failure Detection](https://www.juniper.net/documentation//en_US/junos/topics/example/policy-static-routes-bfd.html).
9. Capture the BFD packets using ip-filter in order to identify if packets are hitting from the issued BFD interface.

```text
User@Router# show firewall filter test-in
```

   term 10 {

   from {

   protocol udp;

   destination-port 4784;

   }

   then {

   count bfd-in;

   syslog;

   accept;

   }

   }

   term 20 {

   then accept;

   }

   [edit]

```text
User@Router# show firewall filter test-out
```

   term 10 {

   from {

   protocol udp;

   destination-port 4784;

   }

   then {

   count bfd-out;

   syslog;

   accept;

   }

   }

   term 20 {

   then accept;

   }

   [edit]

```text
User@Router# show system syslog
```

```text
file bfd-log {
```

   firewall any;

   }

```text
User@Router# show configuration interfaces
```

   ge-0/0/4 {

   unit 100 {

   vlan-id 100;

   family inet {

   filter {

   input bfd-in;

   output bfd-out;

   }

   address 172.1.0.1/30;

   }

   }

   }

```text
If the filter is applied to the incoming interface, and you don't see packets coming in, investigate where the packets are getting dropped.
```

If the filter is applied to the outgoing interface, and you're not seeing packets going out, check the configuration (this is a local issue).
