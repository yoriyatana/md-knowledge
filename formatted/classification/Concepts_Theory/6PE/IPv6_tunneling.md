# IPv6 tunneling

# **Enable IPv6 tunneling**

You can configure the IPv6 tunneling for MPLS to tunnel IPv6 traffic over an MPLS-based IPv4 network. This configuration allows you to interconnect a number of smaller IPv6 networks over an IPv4-based network core, giving you the ability to provide IPv6 service without having to upgrade the switches in your core network. BGP is configured to exchange routes between the IPv6 networks, and data is tunneled between these IPv6 networks by means of IPv4-based MPLS.

When the PEs advertise the IPv6 route for the VRF, the next-hop attribute is an IPv4-mapped IPv6 address that is automatically derived from the loopback IP address of the advertising PE.

When we configure IPv6 tunneling on a Juniper device, we copy all the IPv4 destinations from the **inet.3** table to the **inet6.3** table. This step is required on Juniper devices only.

Configure the LSP to allow IPv6 routes to be resolved over an MPLS network by converting all routes stored in the inet3 routing table to IPv4-mapped IPv6 addresses and then copying them into the inet6.3 routing table

```
# set mpls ipv6-tunneling
```

After enabling IPv6 tunneling, we can use the following commands to verify that the IPv4 addresses have been copied over to the **inet6.3** table on **vmx5**:

```
salt@vmx5> show route table inet.3

inet.3: 9 destinations, 9 routes (9 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

10. 0.0.1/32        *[LDP/9] 3d 06:14:59, metric 200
                    >  to 192.168.5.1 via ge-0/0/1.5, Push 321
10. 0.0.2/32        *[LDP/9] 3d 06:14:59, metric 200
                    >  to 192.168.7.1 via ge-0/0/1.7, Push 324
10. 0.0.3/32        *[LDP/9] 3d 06:14:59, metric 100
                    >  to 192.168.7.1 via ge-0/0/1.7
10. 0.0.4/32        *[LDP/9] 3d 06:14:59, metric 100
                    >  to 192.168.5.1 via ge-0/0/1.5
10. 0.0.6/32        *[LDP/9] 3d 06:14:59, metric 200
                       to 192.168.5.1 via ge-0/0/1.5, Push 319
                    >  to 192.168.7.1 via ge-0/0/1.7, Push 327
10. 0.0.14/32       *[LDP/9] 3d 06:14:59, metric 200
                    >  to 192.168.5.1 via ge-0/0/1.5, Push 320
10. 0.0.15/32       *[LDP/9] 3d 06:14:59, metric 300
                    >  to 192.168.5.1 via ge-0/0/1.5, Push 322
10. 0.1.1/32        *[LDP/9] 3d 06:14:59, metric 301
                       to 192.168.5.1 via ge-0/0/1.5, Push 325
                    >  to 192.168.7.1 via ge-0/0/1.7, Push 333
10. 0.1.2/32        *[LDP/9] 3d 06:14:59, metric 301
                       to 192.168.5.1 via ge-0/0/1.5, Push 326
                    >  to 192.168.7.1 via ge-0/0/1.7, Push 334

salt@vmx5> show route table inet6.3

inet6.3: 9 destinations, 9 routes (9 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

::ffff:10.0.0.1/128*[LDP/9] 3d 06:15:02, metric 200
                    >  to 192.168.5.1 via ge-0/0/1.5, Push 321
::ffff:10.0.0.2/128*[LDP/9] 3d 06:15:02, metric 200
                    >  to 192.168.7.1 via ge-0/0/1.7, Push 324
::ffff:10.0.0.3/128*[LDP/9] 3d 06:15:02, metric 100
                    >  to 192.168.7.1 via ge-0/0/1.7
::ffff:10.0.0.4/128*[LDP/9] 3d 06:15:02, metric 100
                    >  to 192.168.5.1 via ge-0/0/1.5
::ffff:10.0.0.6/128*[LDP/9] 3d 06:15:02, metric 200
                       to 192.168.5.1 via ge-0/0/1.5, Push 319
                    >  to 192.168.7.1 via ge-0/0/1.7, Push 327
::ffff:10.0.0.14/128
                   * [LDP/9] 3d 06:15:02, metric 200
                    >  to 192.168.5.1 via ge-0/0/1.5, Push 320
::ffff:10.0.0.15/128
                   * [LDP/9] 3d 06:15:02, metric 300
                    >  to 192.168.5.1 via ge-0/0/1.5, Push 322
::ffff:10.0.1.1/128*[LDP/9] 3d 06:15:02, metric 301
                       to 192.168.5.1 via ge-0/0/1.5, Push 325
                    >  to 192.168.7.1 via ge-0/0/1.7, Push 333
::ffff:10.0.1.2/128*[LDP/9] 3d 06:15:02, metric 301
                       to 192.168.5.1 via ge-0/0/1.5, Push 326
                    >  to 192.168.7.1 via ge-0/0/1.7, Push 334
```

- --

From Juniper documents:

This example includes the following settings:

- In addition to configuring the family inet6 statement on all the CE router–facing interfaces, you must also configure the statement on all the core-facing interfaces running MPLS. Both configurations are necessary because the router must be able to process any IPv6 packets it receives on these interfaces. You should not see any regular IPv6 traffic arrive on these interfaces, but you will receive MPLS packets tagged with Label 2. Even though Label 2 MPLS packets are sent in IPv4, these packets are treated as native IPv6 packets.
- **NOTE:** BGP automatically runs its import policy even when copying routes from a primary routing table group to a secondary routing table group. If IPv4 labeled routes arrive from a BGP session (for example, when you have configured the labeled-unicast statement at the [edit protocols bgp family inet] hierarchy level on the PE router), the BGP neighbor’s import policy also accepts IPv6 routes, since the neighbor’s import policy is run while doing the copy operation to the inet6.3 routing table.
    You enable IPv6 tunneling by including the ipv6-tunneling statement in the configuration for the PE routers. This statement allows IPv6 routes to be resolved over an MPLS network by converting all routes stored in the inet.3 routing table to IPv4-mapped IPv6 addresses and then copying them into the inet6.3 routing table. This routing table can be used to resolve next hops for both inet6 and inet6-vpn routes.
- When you configure MP-BGP to carry IPv6 traffic, the IPv4 MPLS label is removed at the destination PE router. The remaining IPv6 packet without a label can then be forwarded to the IPv6 network. To enable this, include the explicit-null statement in the BGP configuration.

- --

Regarding your question as to why we need the **family inet6** in the core-facing interfaces, it was not needed in the past (17.x versions). And indeed, these are treated and go through as IPv6 packets internally.
