# [M/MX] How to check PPMD mode and troubleshooting tips

* *SUMMARY:**

This article provides 3 methods for identifying Periodic Packet Management Daemon (PPMD) work mode, troubleshooting tips, and data collection commands for PPMD issues issue.

* *SYMPTOMS:**

PPMD off-loads time-sensitive periodic processing from various clients to a single daemon. It is responsible for periodic transmission of packets on behalf of its various clients. Clients establish adjacencies with PPMD to send/receive packets on their behalf. When packets are not received, the adjacency is marked down and the client is informed.

There are two types of PPMD:

1. Centralized Mode - RE based; PPMD runs on RE
2. Distributed Mode - PFE based. Currently BFD, LFM, CFM, LACP and VRRP are in distribute mode as default. (except BFD for OSPFv3)

* *SOLUTION:**

How to check PPMD Mode:

* *Method 1**

'show ppm adjacencies detail'

* *OSPFv2**

lab@mx240-3-re0> show ppm adjacencies detail

Protocol: OSPF2, Hold time: 40000, IFL-index: 359

Distributed: FALSE

OSPF source key: 88.1.1.2, OSPF area ID: 0.0.0.0

In the example above, the “Distributed” flag is false. Hence, OSPF is running on RE PPMD

* *BFD**

lab@mx240-3-re0# run show ppm adjacencies detail

Protocol: BFD, Hold time: 900, IFL-index: 359

Distributed: TRUE

BFD discriminator: 16, BFD routing table index: 0

Here, the “Distributed” flag is TRUE. Hence BFD is distributed to PFE

* *Method 2**

Go to PFE shell and run 'show ppm adjacencies' or 'show ppm transmits' . It will list all the distributed PPMD:

NPC1(mx240-3-re0 vty)# show ppm adjacencies

PPM distributed adjacencies

Protocol Holdtime (msec) PPM handle Inline

BFD 900 2 No

Total adjacencies: 1

NPC1(mx240-3-re0 vty)# show ppm transmits

Protocol Tx Interval (msec) PPM handle Inline Quick Xmit

BFD 300 1 No No

Total transmit entries: 1

* *Method 3**

Run 'show ppm adjacencies protocol XXX detail'

lab@mx240-3-re0# run show ppm adjacencies protocol lacp detail

Protocol: LACP, Hold time: 3000, IFL-index: 361

Distributed: TRUE

Distribution handle: 30, Distribution address: fpc1

Adjacencies: 1, Remote adjacencies: 1

* *Troubleshooting Tips**

As a troubleshooting method, use the command 'set routing-options ppm no-delegate-processing' to make PPMD centralized. This will reveal if the issue is due to PFE failure itself or not. In other words, if a protocol is having an issue running on distributed mode, but not with centralized mode. Then we can narrow down the issue.

lab@mx240-3-re0#set routing-options ppm no-delegate-processing

lab@mx240-3-re0#commit

lab@mx240-3-re0#run clear bfd session

lab@mx240-3-re0#run show ppm adjacencies detail

Protocol: BFD, Hold time: 900, IFL-index: 359

Distributed: FALSE

BFD discriminator: 17, BFD routing table index: 0

* *Useful Commands**

* *Collect the below from RE:**

- show ppm connections detail
- show bfd session extensive (if BFD is what we are interested in)
- show ppm interfaces detail
- show ppm adjacencies detail
- show ppm transmissions detail
- After JUNOS 12.1 release, collect the below additional commands
- show ppm distribution-statistics
- show ppm dfw-statistics
- show ppm packet-snapshot
- show ppm reques-queue
- show ppm rpd-statistics

* *Collect the below from PFE (for distributed):**

- show ppm adjacencies
- show ppm info
- show ppm local adjacencies protocol cfm (for CFM)
- show ppm objects
- show ppm statistics detail
- show ppm statistics protocol <bfd lacp cfm lfm stp vrrp>
- show ppm transmits
- show threads
- show pfe statistics traffic [5 snapshots 30 sec apart]
- show pfe statistics error
- show pfe statistics notification
