# Example - Understanding Dual-Stack PPPoE Subscriber

[Subscriber Management] Example - Understanding end-to-end IPv6/Dual-Stack PPPoE Subscriber config on MX with Static/Dynamic VLAN option

Article ID**KB36443**

Created2021-01-21

Last Updated2021-02-24

Description

 

This article provides an example of configuring an end-to-end simplified PPPoE IPv6 only or Dual-Stack (IPv4 + IPv6) subscriber on an MX BNG node with generic customer requirements such as firewall filters, fixed/dynamic IP address pools, and framed-route.

This example includes both static and dynamic VLAN configuration options for the PPPoE subscriber interface but does not include any QoS treatment for subscriber traffic, so all traffic are treated as best-effort.

In this example:

1. The RADIUS server used is Freeradius. So Freeradius user examples with multiple RADIUS attributes are included.
2. The dynamic-profile is configured such that the same dynamic-profile can be used for both IPv6 only and Dual-Stack PPPoE subscriber provisioning. It is also configured (predefined-variable-defaults) such that if RADIUS does not send some of the mandatory attributes such as filter name, subscribers will come up using a default filter name.
3. If VRF name, IP pool name/fixed IP, or framed-route are not sent from the RADIUS server, subscribers will come up with a default VRF (global routing instance) and a default pool (as per the "access domain map default" configuration). So except username and password, all other attributes are optional.

 

Solution

 

**Topology**

> IPv4/IPv6/Dual-Stack PPPoE subscriber <----> ([vlan 3320] ge-0/0/2) MX (ge-0/0/0) <----> Radius Server(192.168.40.26)

The RADIUS Server (@192.168.40.26) is reachable via the global routing instance inet.0 table.

 

There are two types of addressing for IPv6 in a subscriber access network: 

- WAN link addressing: For the WAN interface on the CPE (CPE upstream interface)
- Subscriber LAN addressing: For devices connected to the CPE on the subscriber LAN (CPE downstream interfaces)

 

You can use the following methods for assigning IPv6 addresses: 

- For WAN link addressing, you can use ND/RA or DHCPv6 IA_NA to provision a global IPv6 address.
- For subscriber LAN addressing, you can use DHCPv6 prefix delegation to provision global IPv6 addresses to the subscribers on the LAN.

 

IPv6 PPPoE subscriber (WAN link’s IPv6 address assignment of CPE) can be deployed in two ways:

1. Via ND/RA messages
2. Via DHCPv6 IA_NA or PD

 

**MX(BNG) Configuration Steps for IPv4 / IPv6 / Dual-Stack PPPoE Subscriber**

1. Configure the following:
    1. Dynamic profile " **PPPoE** " for both IPv4 and IPv6/Dual-Stack PPPoE subscribers
    2. Access Profile " **ACCESS-FTTH** " for subscriber user authentication via the RADIUS server
    3. IPv4 Address Pool " **dhcpv4-pool** " (default pool) and " **V4-IP-POOL** " (user defined; used via the RADIUS attribute "Framed-Pool")
    4. IPv6 Address pools " **V6-DHCP-POOL** " (default pool) and " **IP-POOL-V6** " (user defined; used via the RADIUS attribute "Framed-IPv6-Pool")
    5. Domain map " **default** " with a default dynamic-profile, access-profile, and address-pool mapping
    6. IPv4 firewall filter " **default** " and IPv6 firewall filter " **default-v6** " to be used by the dynamic-profile " **PPPoE** " as default in/out firewall filter (in case not provided via the RADIUS attribute)
    7. MX as the DHCPv6 (only) server (dhcp-local-server dhcpv6 group " **PPPV6** ") for PPPoE subscriber IPv6 address assignment
    8. Dynamic profile " **PPPoE** " under static VLAN/unit number for an interface with PPPoE encapsulation

> **For Auto-VLAN (dynamic VLAN) Configuration:**  ( Continue after Step f onward as shown below. )

1. Configure a dynamic profile " **AUTO-VLAN-PPP** " (dot1q) or " **AUTO-VLAN-STACK-PPP** " (q-in-q) for the dynamic VLAN PPPoE subscriber interface.
2. Finally configure the physical interface with auto-configure (with dynamic profile  _"_ **AUTO-VLAN-PPP** _" / "_ **AUTO-VLAN-STACK-PPP** _"_ ) to activate dynamic-VLAN-based PPPoE subscribers.

**Configuration**

**Dynamic-profile configuration for static VLAN bind IPv4 only, IPv6 (ND/RA, DHCPv6 IA_NA / PD), and Dual-Stack (ND/RA, DHCPv6 IA_NA / PD) PPPoE subscriber deployment**

> dynamic-profiles {
> 
> **PPPoE** { ## "dynamic-profile" name
> 
> predefined-variable-defaults { ## Pre-defines the variable’s default value
> 
> input-filter **default**;
> 
> output-filter **default**;
> 
> output-ipv6-filter **default-v6**;
> 
> input-ipv6-filter **default-v6**;
> 
> }
> 
> routing-instances { ## Enables the PPPoE/LAC subscribers inside VRF
> 
> "$junos-routing-instance" {
> 
> interface "$junos-interface-name" {
> 
> any;
> 
> }
> 
> routing-options {
> 
> rib "$junos-ipv6-rib" { ## IPv6 Access Stanza
> 
> access {
> 
> route $junos-framed-route-ipv6-address-prefix {
> 
> qualified-next-hop "$junos-interface-name";
> 
> metric "$junos-framed-route-ipv6-cost";
> 
> preference "$junos-framed-route-ipv6-distance";
> 
> tag "$junos-framed-route-ipv6-tag";
> 
> }
> 
> }
> 
> }
> 
> access { ## Enables static route via AAA Framed-route - IPv4 Access Stanza
> 
> route $junos-framed-route-ip-address-prefix {
> 
> next-hop "$junos-framed-route-nexthop";
> 
> metric "$junos-framed-route-cost";
> 
> preference "$junos-framed-route-distance";
> 
> tag "$junos-framed-route-tag";
> 
> }
> 
> }
> 
> }
> 
> }
> 
> }
> 
> 
> 
> 
> 
> interfaces {
> 
> pp0 {
> 
> unit "$junos-interface-unit" {
> 
> actual-transit-statistics;
> 
> ppp-options {
> 
> chap; ## Enables chap auth
> 
> pap; ## Enables pap auth
> 
> initiate-ncp {
> 
> ip;
> 
> ipv6;
> 
> dual-stack-passive;
> 
> }
> 
> mtu **1492**; ## PPP mtu to be set during pap auth
> 
> }
> 
> pppoe-options {
> 
> underlying-interface "$junos-underlying-interface";
> 
> server; ## Enables to accept PPPoE/LAC connection
> 
> }
> 
> family inet {
> 
> filter {
> 
> input "$junos-input-filter";
> 
> output "$junos-output-filter";
> 
> }
> 
> unnumbered-address "$junos-loopback-interface";
> 
> }
> 
> family inet6 {
> 
> filter {
> 
> input "$junos-input-ipv6-filter";
> 
> output "$junos-output-ipv6-filter";
> 
> }
> 
> address $junos-ipv6-address;
> 
> unnumbered-address "$junos-loopback-interface";
> 
> }
> 
> }
> 
> }
> 
> }
> 
> 
> 
> 
> 
> protocols {
> 
> router-advertisement { ## For IPv6 IA_NA /128 address, disable "router-advertisement."
> 
> interface "$junos-interface-name" {
> 
> link-mtu;
> 
> prefix $junos-ipv6-ndra-prefix {
> 
> valid-lifetime 14400;
> 
> on-link;
> 
> preferred-lifetime 14400;
> 
> }
> 
> }
> 
> }
> 
> }
> 
> }
> 
> }
> 
> 
> 
> 
> 
> system {
> 
> services {
> 
> dhcp-local-server {
> 
> dhcpv6 {
> 
> group **PPPV6** {
> 
> interface demux0.0;
> 
> interface pp0.0;
> 
> }
> 
> }
> 
> }
> 
> }
> 
> }
> 
> 
> 
> 
> 
> access {
> 
> profile **ACCESS-FTTH** { ## Access-profile name
> 
> accounting-order radius;
> 
> authentication-order radius;
> 
> radius {
> 
> authentication-server **192.168.40.26**;
> 
> accounting-server **192.168.40.26**;
> 
> options {
> 
> accounting-session-id-format description;
> 
> client-authentication-algorithm direct; ## RADIUS authentication request algorithm
> 
> }
> 
> }
> 
> radius-server {
> 
> **192.168.40.26** {
> 
> port **1812**; ## RADIUS authentication port number
> 
> accounting-port **1813**; ## RADIUS accounting port number
> 
> dynamic-request-port **3799**; ## RADIUS CoA/dynamic-request port number
> 
> secret "$ABC123"; ## SECRET-DATA
> 
> source-address 192.168.40.6; ## Source IP to be used for RADIUS messages
> 
> }
> 
> }
> 
> accounting {
> 
> order radius;
> 
> accounting-stop-on-failure;
> 
> accounting-stop-on-access-deny;
> 
> immediate-update;
> 
> coa-immediate-update;
> 
> update-interval **10**; ## Interim accounting update interval in minutes
> 
> statistics volume-time; ## Both data volume & session duration for accounting
> 
> }
> 
> }
> 
> address-assignment {
> 
> neighbor-discovery-router-advertisement **V6-DHCP-POOL**;
> 
> pool **V6-DHCP-POOL** {
> 
> family inet6 {
> 
> prefix 2000:1::/64;
> 
> range ndra-range prefix-length 64;
> 
> }
> 
> }
> 
> pool **IP-POOL-v6** {
> 
> family inet6 {
> 
> prefix 2004:2003::0/64;
> 
> inactive: range ndra-range prefix-length 64;
> 
> range **ixia** {
> 
> low 2004:2003::10/128;
> 
> high 2004:2003::ff/128;
> 
> }
> 
> }
> 
> }
> 
> pool **pppv4-pool** {
> 
> family inet {
> 
> network 10.10.200.0/24;
> 
> }
> 
> }
> 
> pool **V4-IP-POOL** {
> 
> family inet {
> 
> network 192.168.100.0/24;
> 
> range private {
> 
> low 192.168.100.1;
> 
> high 192.168.100.255;
> 
> }
> 
> }
> 
> }
> 
> }
> 
> 
> 
> 
> 
> domain { ## Map domain-id with access-profile, pool, dynamic-profile
> 
> map **default** { ## Default domain map; matches all/no domain-id
> 
> access-profile **ACCESS-FTTH**;
> 
> address-pool **pppv4-pool**;
> 
> dynamic-profile **PPPoE**;
> 
> }
> 
> delimiter "**@**"; ## Delimiter character to identify start of domain-id
> 
> }
> 
> }
> 
> 
> 
> 
> 
> firewall {
> 
> family inet {
> 
> filter **default** {
> 
> interface-specific;
> 
> term T1 {
> 
> then accept;
> 
> }
> 
> }
> 
> }
> 
> 
> 
> 
> 
> family inet6 {
> 
> filter **default-v6** {
> 
> interface-specific;
> 
> term T1 {
> 
> then accept;
> 
> }
> 
> }
> 
> }
> 
> }
> 
> 
> 
> 
> 
> interfaces {
> 
> **ge-0/0/2** {
> 
> hierarchical-scheduler maximum-hierarchy-levels 2;
> 
> flexible-vlan-tagging;
> 
> unit **3320** { ## Static unit number for static VLAN subscriber int.
> 
> encapsulation ppp-over-ether;
> 
> vlan-id **3320**; ## Single stack(dot1q) static VLAN ID for incoming PPPoE
> 
> pppoe-underlying-options {
> 
> dynamic-profile **PPPoE**;
> 
> }
> 
> }
> 
> }
> 
> }

**Extra dynamic-profile and interface configurations for dot1q / single VLAN IPv4 PPPoE subscriber deployment**

> dynamic-profiles {
> 
> **AUTO-VLAN-PPP** {
> 
> interfaces {
> 
> demux0 {
> 
> unit "$junos-interface-unit" {
> 
> actual-transit-statistics;
> 
> proxy-arp;
> 
> vlan-id "$junos-vlan-id";
> 
> demux-options {
> 
> underlying-interface "$junos-interface-ifd-name";
> 
> }
> 
> family pppoe {
> 
> dynamic-profile **PPPoE**;
> 
> }
> 
> }
> 
> }
> 
> }
> 
> }
> 
> }
> 
> 
> 
> 
> 
> interfaces {
> 
> **ge-0/0/2** {
> 
> hierarchical-scheduler maximum-hierarchy-levels 2;
> 
> flexible-vlan-tagging;
> 
> auto-configure {
> 
> vlan-ranges {
> 
> dynamic-profile **AUTO-VLAN-PPP** {
> 
> accept pppoe;
> 
> ranges {
> 
> **3000-4000**; ## VLAN ranges for incoming PPPoE connection
> 
> }
> 
> }
> 
> }
> 
> remove-when-no-subscribers;
> 
> }
> 
> }
> 
> }

**Extra dynamic-profile and interface configurations for q-in-q / stacked VLAN IPv4/IPv6 PPPoE subscriber deployment**

> dynamic-profiles {
> 
> **AUTO-VLAN-STACK-PPP** {
> 
> interfaces {
> 
> demux0 {
> 
> unit "$junos-interface-unit" {
> 
> actual-transit-statistics;
> 
> proxy-arp;
> 
> vlan-tags outer "$junos-stacked-vlan-id" inner "$junos-vlan-id";
> 
> demux-options {
> 
> underlying-interface "$junos-interface-ifd-name";
> 
> }
> 
> family pppoe {
> 
> dynamic-profile **PPPoE**;
> 
> }
> 
> }
> 
> }
> 
> }
> 
> }
> 
> }
> 
> interfaces {
> 
> **ge-0/0/2** {
> 
> hierarchical-scheduler maximum-hierarchy-levels 2;
> 
> flexible-vlan-tagging;
> 
> auto-configure {
> 
> stacked-vlan-ranges {
> 
> dynamic-profile **AUTO-VLAN-STACK-PPP** {
> 
> accept pppoe;
> 
> ranges {
> 
> **3000-4000,any**; ## Outer, inner VLAN ranges for incoming PPPoE connection
> 
> }
> 
> }
> 
> }
> 
> remove-when-no-subscribers;
> 
> }
> 
> }
> 
> }

**RADIUS User Configuration**

RADIUS Attributes Specific to IPv6

- Jnpr-IPv6-Ingress-Policy-Name
- Jnpr-IPv6-Egress-Policy-Name
- Framed-IPv6-Prefix
- Framed-IPv6-Pool
- Delegated-Ipv6-Prefix
- Framed-IPv6-Route

**RADIUS User Example (can be used in addition with PPPoE IPv4 attributes) specific for IPv6 / Dual-Stack User**

1. **Fixed IA_NA IPv6 /128 IPv6 Address User Example:�**� (for IA_NA address, disable dynamic-profiles > protocols > router-advertisement)

> _Username1@domain_ Auth-Type := Local, User-Password := "_Password_"
> 
> Service-Type = Framed-User,
> 
> Framed-Protocol = PPP,
> 
> Framed-IPv6-Prefix = _"4001:1:1:1::100/128"_,
> 
> Framed-IP-Address = _10.200.200.26_

1. **NDRA/IPv6 Prefix Address Assignment User Example:**

> _Username1@domain_ Auth-Type := Local, User-Password := "_Password_"
> 
> Service-Type = Framed-User,
> 
> Framed-Protocol = PPP,
> 
> # Framed-IPv6-Prefix = _"4001:1:1:1::100/128"_,
> 
> Framed-IPv6-Prefix = _"4010:1:1:10::/64"_,
> 
> Framed-IP-Address = 10.200.200.26

1. **IPv6 Address Assignment via IPv6 Pool Name User Example:**

> _Username1@domain_ Auth-Type := Local, User-Password := "_Password_"
> 
> Service-Type = Framed-User,
> 
> Framed-Protocol = PPP,
> 
> Framed-Pool = "V4-DHCP-POOL",
> 
> Framed-IPv6-Pool = _"IP-POOL-V6"_,
> 
> ERX-Primary-Dns = 8.8.8.8

1. **IPv6 Prefix Delegation Address Assignment User Example:**

> _Username1@domain_ Auth-Type := Local, User-Password := "_Password_"
> 
> Service-Type = Framed-User,
> 
> Framed-Protocol = PPP,
> 
> Framed-IP-Address = _10.200.200.26,_
> 
> Framed-IPv6-Prefix = _"4001:1:1:1::/64"_,
> 
> # Framed-IPv6-Route = "2000:a600:0106::/48 :: 1",
> 
> Delegated-IPv6-Prefix = _"4001:1:1:10::/64"_,
> 
> ERX-Primary-Dns = 8.8.8.8
