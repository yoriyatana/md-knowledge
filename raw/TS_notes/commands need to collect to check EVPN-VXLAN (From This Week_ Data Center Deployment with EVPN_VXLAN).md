# commands need to collect to check EVPN-VXLAN (From This Week: Data Center Deployment with EVPN/VXLAN)

tung.nt@MX960-01\_RE1> show ddos-protection protocols statistics brief | no-more

check crc >>> có tính băng link-direct

---

Underlay

jnpr@LEAF-1> show route table inet.0 | match “10.1.1.[1-6]/32”

Overlay (Data Plane – VXLAN)

jnpr@LEAF-1> show interfaces vtep

jnpr@LEAF-1> show route table :vxlan.inet.0

jnpr@LEAF-1> show route forwarding-table table default-switch extensive

jnpr@LEAF-1> show ethernet-switching vxlan-tunnel-end-point source

jnpr@LEAF-1> show ethernet-switching vxlan-tunnel-end-point remote

Overlay (Control Plane – EVPN)

IBGP sessions are established between all leaf nodes with only the “evpn” NLRI.

jnpr@LEAF-1> show bgp summary

jnpr@LEAF-1> show bgp neighbor 10.1.1.2 | match NLRI

jnpr@LEAF-1> show bfd session

Verify exchange of Ethernet Segment (Type 4) routes used for ES Discovery to enable multihoming, DF Election, and Split Horizon/Local Bias.

jnpr@LEAF-1> show route instance \_\_default\_evpn\_\_ detail

jnpr@LEAF-1> show policy \_\_vrf-import-\_\_default\_evpn\_\_-internal\_\_

jnpr@LEAF-1> show route community-name \_\_vrf-community-\_\_default\_evpn\_\_-import-internal\_\_

jnpr@LEAF-1> show route table bgp.evpn.0 extensive | find ^4:

jnpr@LEAF-1> show evpn instance designated-forwarder esi 00:11:11:11:11:11:11:11:11:11

jnpr@LEAF-1> show evpn instance backup-forwarder esi 00:11:11:11:11:11:11:11:11:11

jnpr@LEAF-1> show evpn instance extensive

Now let’s verify exchange of Inclusive Multicast (Type 3) routes from each peer.

jnpr@LEAF-1> show route table bgp.evpn.0 | match ^3:

jnpr@LEAF-1> show route table bgp.evpn.0 extensive

jnpr@LEAF-1> show interfaces extensive vtep | match “vxlan endpoint|logical interface”

jnpr@LEAF-1> show ethernet-switching flood vlan-name bd5010 extensive

jnpr@LEAF-1> show ethernet-switching flood vlan-name bd5020 extensive

Verify exchange of Ethernet AutoDiscovery (Type 1) routes (Per ES and Per EVI) used for Aliasing and MAC Mass Withdraw

jnpr@LEAF-1> show route table bgp.evpn.0 | match ^1:

jnpr@LEAF-1> show route table bgp.evpn.0 extensive

jnpr@LEAF-2> show evpn database extensive mac-address 00:00:1e:63:c8:7c

jnpr@LEAF-1> show route table bgp.evpn.0 evpn-mac-address 00:00:1e:63:c8:7c

jnpr@LEAF-3> show ethernet-switching table 00:00:1e:63:c8:7c

jnpr@LEAF-3> show ethernet-switching vxlan-tunnel-end-point esi

jnpr@LEAF-3> show route table bgp.evpn.0 | match 00:00:d4:37 | except ::100 | count

jnpr@LEAF-3> show route table bgp.evpn.0 | match “00:00:d4:37”

jnpr@LEAF-3> show evpn database extensive

jnpr@LEAF-3> show route forwarding-table table default-switch | match 00:00:d4:37

jnpr@LEAF-3> show log evpn-trace.log

jnpr@LEAF-3> show route table bgp.evpn.0 | match ^1:10.1.1.2 | match 111

jnpr@LEAF-3> show log evpn-trace

jnpr@LEAF-3> show route table bgp.evpn.0 | match ^1:10.1.1.2 | match 111

jnpr@LEAF-3> show route forwarding-table table default-switch | match 00:00:d4:37

jnpr@LEAF-1> show route advertising-protocol bgp 10.1.1.3 extensive

jnpr@LEAF-1> show evpn instance extensive

jnpr@LEAF-1> show ethernet-switching table

jnpr@LEAF-1> show ethernet-switching vxlan-tunnel-end-point esi

---

jnpr@Leaf-2> show evpn database extensive mac-address 00:00:1e:63:c8:7c

jnpr@Leaf-2> show ethernet-switching table vlan-id 10 00:00:1e:63:c8:7c
