# ecmp-local-bias

By default, equal cost multi-path (ECMP) traffic flows are distributed more-or-less equally between forwarding next-hops. Enable ecmp-local-bias to have ECMP traffic prefer local forwarding next-hops (that is, local to the packet forwarding engine (PFE) that is performing the packet look up) over remote ones, and to distribute the flows among local members. Local bias percentages cannot be assigned. Note that ecmp-local-bias is not intended to be used in conjunction with any other load balancing schemes. This feature applies chassis-wide. It supports BGP prefixes that are directly reachable with IPv4 MPLS ECMP next-hops on Gigabit Ethernet (ge-) and 10-Gigabit Ethernet (xe-) interfaces. Multicast traffic is not affected.

[ Thursday, March 16, 2023 12:04 PM ] ⁨Hung Le⁩: Test Steps:

1. Create ECMP.

```text
Configure BGP between 2 routers, verify BGP neighbourship is formed.
```

3. Verify BGP prefixes are reachable via IPv4->MPLS ECMP next-hops.

```text
Configure ospf/ospfv3 along with BGP.
```

```text
Configure the locality-bias on BGP routes.
```

6. Verify the show command on RE and PFE for the locality-bias percentage.

7. Verify the selector table distribution for the locality-bias percentage.

8. Verify the traffic pattern according to the locality-bias percentage.

```text
Delete/deactivate BGP routes when traffic is flowing
```

10. Add back BGP routes

[ Thursday, March 16, 2023 12:09 PM ] ⁨Hung Le⁩: Configure an  ECMP on the local-bias knob unsupported MPC (MPC10/SONET/SDH )
