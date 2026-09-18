# [MX/PTX] How to determine which LSP is forwarding traffic on bypass LSP

[https://kb.juniper.net/InfoCenter/index?page=content&id=KB34687&cat=PTX_SERIES&actp=LIST](https://kb.juniper.net/InfoCenter/index?page=content&id=KB34687&cat=PTX_SERIES&actp=LIST)

####

labroot@MX80-r002# run show mpls lsp bypass logical-system r2

labroot@MX80-r002# run show rsvp session name Bypass->1.1.23.2 extensive logical-system r2

labroot@MX80-r002# run show rsvp session interface xe-0/0/0.24 logical-system r2

labroot@MX80-r002# run show rsvp session **ingress** name r1-to-r5 logical-system r2 extensive

labroot@MX80-r002# run show rsvp session **transit** logical-system r2

####

* *SUMMARY:**

For a MPLS LSP, when link or node-link protection is configured and there are redundant links in the network, bypass LSPs are created on transit routers. Sometimes when the primary path fails, traffic shifts to bypass LSP. This article will help you determine which LSP is forwarding the traffic over bypass LSP.

* *SOLUTION:**

This example shows the output from transit router only to explain which LSP is forwarding traffic over bypass LSP.

The following output shows bypass LSP Bypass -> 1.1.23.2 is in BackupActive state, which means bypass LSP is UP and Forwarding Traffic.

> labroot@MX80-r002# run show mpls lsp bypass logical-system r2
>
> Apr 24 13:10:21
>
> Ingress LSP: 1 sessions
>
> To From State Rt Style Labelin Labelout LSPname
>
> 192.168.1.103 192.168.1.102 **BackupActive** 0 1 SE - 299824 Bypass->1.1.23.2 < when the bypass is BackupActive it means its up and forwarding traffic
>
> Total 1 displayed, Up 1, Down 0

In the extensive output "Number of data route tunnel through" field gives the number of LSP using the bypass to forward traffic.

> labroot@MX80-r002# run show rsvp session name Bypass->1.1.23.2 extensive logical-system r2
>
> Apr 24 13:59:50
>
> Ingress RSVP: 2 sessions
>
> 192.168.1.103
>
> From: 192.168.1.102, LSPstate: Up, ActiveRoute: 0
>
> LSPname: Bypass->1.1.23.2
>
> LSPtype: Static Configured
>
> Suggested label received: -, Suggested label sent: -
>
> Recovery label received: -, Recovery label sent: 299824
>
> Resv style: 1 SE, Label in: -, Label out: 299824
>
> Time left: -, Since: Wed Apr 24 09:24:07 2019
>
> Tspec: rate 0bps size 0bps peak Infbps m 20 M 1500
>
> Port number: sender 1 receiver 15931 protocol 0
>
> Type: Bypass LSP
>
> **Number of data route tunnel through: 1** <-- 1 LSP is using this bypass to forward traffic, it can be 0 when bypass LSP is only UP (not BackupActive)
>
> **Number of RSVP session tunnel through: 1** <-- Only 1 LSP is protected on this bypass path
>
> Enhanced FRR: Enabled (Downstream)
>
> PATH rcvfrom: localclient
>
> Adspec: sent MTU 1500
>
> Path MTU: received 1500
>
> PATH sentto: 1.1.24.2 (xe-0/0/0.24) 1 pkts <-- this is the interface on which bypass path is signaled
>
> outgoing message state: refreshing, Message ID: 97, Epoch: 15610269
>
> RESV rcvfrom: 1.1.24.2 (xe-0/0/0.24) 1 pkts, Entropy label: Yes
>
> incoming message handle: R-42/1, Message ID: 43, Epoch: 15610266
>
> Explct route: 1.1.24.2 1.1.43.2

When you check the LSPs signaled through the interface on which bypass LSP is signaled, you will find ingress LSP on that interface which should be transit LSP on this router.

> labroot@MX80-r002# run show rsvp session interface xe-0/0/0.24 logical-system r2 <-- you can see r1-to-r5 is showing as ingress LSP on xe-0/0/0.24 which is protecting xe-0/0/0.23
>
> Apr 24 13:51:52
>
> Ingress RSVP: 2 sessions
>
> To From State Rt Style Labelin Labelout LSPname
>
> 192.168.1.103 192.168.1.102 Up 0 1 SE - 299824 Bypass->1.1.23.2
>
> 192.168.1.105 **1.1.24.1** Up 0 1 SE - 300080 **r1-to-r5** <-- transit LSP showing as ingress LSP on protected interface and ‘from’ address is interface address
>
> Total 2 displayed, Up 2, Down 0

Now if you will check the extensive output for that LSP you will find out that LSP Type is "**Backup LSP at Point-of-Local-Repair"** that means this LSP is currently using the bypass path on that interface.

> labroot@MX80-r002# run show rsvp session **ingress** name r1-to-r5 logical-system r2 extensive < if you check here
>
> Apr 24 13:12:28
>
> Ingress RSVP: 2 sessions
>
> 192.168.1.105
>
> From: 1.1.24.1, LSPstate: Up, ActiveRoute: 0
>
> LSPname: r1-to-r5
>
> LSPtype: Static Configured
>
> Suggested label received: -, Suggested label sent: -
>
> Recovery label received: -, Recovery label sent: 300080
>
> Resv style: 1 SE, Label in: -, Label out: 300080
>
> Time left: -, Since: Wed Apr 24 13:10:05 2019
>
> Tspec: rate 0bps size 0bps peak Infbps m 20 M 1500
>
> Port number: sender 6 receiver 45048 protocol 0
>
> **Type: Backup LSP at Point-of-Local-Repair** <-- this is the LSP which is actively using the bypass path
>
> PATH rcvfrom: localclient
>
> Adspec: sent MTU 1500
>
> Path MTU: received 1500
>
> PATH sentto: 1.1.43.2 (xe-0/0/0.24) 2 pkts
>
> outgoing message state: refreshing, Message ID: 305, Epoch: 15610269
>
> RESV rcvfrom: 192.168.1.103 (xe-0/0/0.24) 1 pkts, Entropy label: Yes
>
> incoming message handle: R-85/1, Message ID: 124, Epoch: 15610266
>
> Explct route: 1.1.43.2 1.1.35.2
>
> Record route: <self> 1.1.43.2 192.168.1.105 (node-id) 1.1.35.2
>
> Total 1 displayed, Up 1, Down 0

The same LSP will show as down on primary path because of the failure on that path, but traffic will be forwarded via bypass LSP. This LSP will show up on ingress.

> labroot@MX80-r002# run show rsvp session **transit** logical-system r2
>
> Transit RSVP: 4 sessions
>
> To From State Rt Style Labelin Labelout LSPname
>
> 192.168.1.101 192.168.1.105 Up 0 1 FF 300160 3 r5-to-r1
>
> 192.168.1.101 192.168.1.104 Up 0 1 FF 300112 3 r4-to-r1
>
> 192.168.1.104 192.168.1.101 Up 0 1 FF 300144 3 r1-to-r4
>
> **192.168.1.105 192.168.1.101 Dn 0 0 - 300192 - r1-to-r5** <-- same LSP is showing down as transit LSP
