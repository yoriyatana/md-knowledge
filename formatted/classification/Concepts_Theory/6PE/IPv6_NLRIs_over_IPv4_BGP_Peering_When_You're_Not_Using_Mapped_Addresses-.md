# IPv6 NLRIs over IPv4 BGP Peering When You're Not Using Mapped Addresses.

[https://www.francisluong.com/blog-ideas-living/jncie-sp-ipv6-nlris-over-ipv4-bgp-peering-when](https://www.francisluong.com/blog-ideas-living/jncie-sp-ipv6-nlris-over-ipv4-bgp-peering-when)

I [previously posted about a way to configure BGP for IPv6 Unicast NLRI over an IPV4 session](http://francisluong.tumblr.com/post/40710653501/jncie-sp-notes-on-configuring-bgp-for-ipv6-unicast-nlri). Well, sometimes you don’t get to choose the address that the interface is running and it may be the ::1.2.3.4 ipv4-compatible style instead of the the ::ffff:mapped style.

This post is about how you get it to work.

In this scenario we have our PE, R1 and the CE, R3.

This is R1’s config.

```
 set interfaces ge-0/0/2 unit 0 family inet address 172.27.0.5/30
 set interfaces ge-0/0/2 unit 0 family inet6 address ::172.27.0.5/126
 set protocols bgp group ebgp type external
 set protocols bgp group ebgp family inet unicast
 set protocols bgp group ebgp family inet6 unicast
 set protocols bgp group ebgp peer-as 3
 set protocols bgp group ebgp neighbor 172.27.0.6

```

This is R3’s config

```
 set interfaces ge-0/0/2 unit 0 family inet address 172.27.0.5/30
 set interfaces ge-0/0/2 unit 0 family inet6 address ::172.27.0.5/126
 set protocols bgp group ebgp type external
 set protocols bgp group ebgp family inet unicast
 set protocols bgp group ebgp family inet6 unicast
 set protocols bgp group ebgp export export-ebgp
 set protocols bgp group ebgp peer-as 701
 set protocols bgp group ebgp neighbor 172.27.0.5
 set policy-options policy-statement export-ebgp term 1 from protocol aggregate
 set policy-options policy-statement export-ebgp term 1 from rib inet6.0
 set policy-options policy-statement export-ebgp term 1 from route-filter 3333:3333::/32 exact
 set policy-options policy-statement export-ebgp term 1 then accept

```

This is the sad situation on R1 and R3:

```
 lab@R1&gt; show bgp summary
 172. 27.0.6                3         51         53       0       0       20:31 Establ
   inet.0: 0/0/0/0
   inet6.0: 0/0/0/0

 lab@R1&gt; show log messages | grep sanity
 Feb 13 17:15:01  R1 rpd[1131]: bgp_nexthop_sanity: peer 172.27.0.6 (External AS 3) next hop ::ffff:172.27.0.6 unexpectedly remote, ignoring routes in this update

 lab@R3&gt; show log messages | grep sanity
 Feb 13 21:46:27  R3 rpd[1135]: bgp_nexthop_sanity: peer 172.27.0.5 (External AS 701) next hop ::ffff:172.27.0.5 unexpectedly remote, ignoring routes in this update

```

Per standard, BGP sets the next-hop to it’s IPv4 address using ::ffff ipv4-mapped addressing. If we add “accept-remote-nexthop” R1’s BGP config, we get this:

```
 lab@R1# activate protocols bgp group ebgp accept-remote-nexthop

 [edit]
 lab@R1# commit and-quit
 commit complete
 Exiting configuration mode

 lab@R1&gt; show bgp summary
 172. 27.0.6                3         58         61       0       0       23:06 Establ
   inet.0: 0/0/0/0
   inet6.0: 0/1/1/0

 lab@R1&gt; show route resolution unresolved
 Tree Index 1
 Tree Index 2
 Tree Index 3
 3333:3333::/32
         Protocol Nexthop: ::ffff:172.27.0.6
         Indirect nexthop: 0 -

```

We now see the route but it is not resolvable. So to fix it, we need to change the next hop to the inet6 address assigned to our peering interface. I’m going to fix both directions from R1’s policy since I am assuming no control over R3.

```
 ## the route we are advertising to R3 comes from IBGP, so we simply adjust the next-hop
 set policy-options policy-statement export-ebgp term reset-v6-nexthop from protocol bgp
 set policy-options policy-statement export-ebgp term reset-v6-nexthop from rib inet6.0
 set policy-options policy-statement export-ebgp term reset-v6-nexthop then next-hop ::172.27.0.5

 ## we do similar handing for routes received from R3
 set policy-options policy-statement import-ebgp from protocol bgp
 set policy-options policy-statement import-ebgp from rib inet6.0
 set policy-options policy-statement import-ebgp from next-hop ::ffff:172.27.0.6
 set policy-options policy-statement import-ebgp then next-hop ::172.27.0.6
 set policy-options policy-statement import-ebgp then accept

 ## apply policy configs to bgp
 set protocols bgp group ebgp import import-ebgp
 set protocols bgp group ebgp export export-ebgp

```

After we commit this config change on R1, we now have reachability both ways.

```
 lab@R1&gt; show bgp summary
 Groups: 2 Peers: 2 Down peers: 0
 Table          Tot Paths  Act Paths Suppressed    History Damp State    Pending
 inet.0                 0          0          0          0          0          0
 inet6.0                2          2          0          0          0          0
 Peer                     AS      InPkt     OutPkt    OutQ   Flaps Last Up/Dwn State|#Active/Received/Accepted/Damped...
 10. 255.1.32             701         94         97       0       0       41:04 Establ
   inet.0: 0/0/0/0
   inet6.0: 1/1/1/0
 172. 27.0.6                3         67         71       0       0       27:15 Establ
   inet.0: 0/0/0/0
   inet6.0: 1/1/1/0

 lab@R1&gt; show route table inet6 3333:3333::/32

 inet6.0: 7 destinations, 8 routes (7 active, 0 holddown, 0 hidden)
 + = Active Route, - = Last Active, * = Both

 3333:3333::/32     *[BGP/170] 00:04:18, localpref 100, from 172.27.0.6
                       AS path: 3 I
                     &gt; to ::172.27.0.6 via ge-0/0/2.0

```

And R3.

```
 lab@R3&gt; show bgp summary
 Groups: 1 Peers: 1 Down peers: 0
 Table          Tot Paths  Act Paths Suppressed    History Damp State    Pending
 inet.0                 0          0          0          0          0          0
 inet6.0                1          1          0          0          0          0
 Peer                     AS      InPkt     OutPkt    OutQ   Flaps Last Up/Dwn State|#Active/Received/Accepted/Damped...
 172. 27.0.5              701         77         72       0       0       29:23 Establ
   inet.0: 0/0/0/0
   inet6.0: 1/1/1/0

 lab@R3&gt; show route protocol bgp

 inet.0: 13 destinations, 13 routes (13 active, 0 holddown, 0 hidden)

 inet6.0: 8 destinations, 8 routes (8 active, 0 holddown, 0 hidden)
 + = Active Route, - = Last Active, * = Both

 4444:4444::/32     *[BGP/170] 00:02:55, localpref 100, from 172.27.0.5
                       AS path: 701 4 I
                     &gt; to ::172.27.0.5 via ge-0/0/1.0

 lab@R3&gt; show route protocol bgp detail

 inet.0: 13 destinations, 13 routes (13 active, 0 holddown, 0 hidden)

 inet6.0: 8 destinations, 8 routes (8 active, 0 holddown, 0 hidden)
 4444:4444::/32 (1 entry, 1 announced)
         * BGP    Preference: 170/-101
                 Next hop type: Router, Next hop index: 587
                 Address: 0x934c688
                 Next-hop reference count: 2
                 Source: 172.27.0.5
                 Next hop: ::172.27.0.5 via ge-0/0/1.0, selected
                 State:
                 Local AS:     3 Peer AS:   701
                 Age: 3:22
                 Task: BGP_701.172.27.0.5+52965
                 Announcement bits (1): 0-KRT
                 AS path: 701 4 I Aggregator: 4 10.255.1.34
                 Accepted
                 Localpref: 100
                 Router ID: 10.255.1.31

```

There you have it: accept-remote-nexthop, and some resetting of the next-hop works by either import or export policy.
