# Configuring BGP for IPv6 Unicast NLRI over an IPv4 Peering session

<https://www.francisluong.com/blog-ideas-living/jncie-sp-notes-on-configuring-bgp-for-ipv6-unicast>

When configuring MP-BGP over an ipv4 peering session, you probably already know that you have to enable family inet6 on your interface. But you also have to make sure to configure an ipv4-mapped inet6 address for your interface because your Juniper device will probably be setting the next-hop to that address unless you’re running older code.

Here is an example of config to get you going.

Diagram

![](image/b499f138ff7477e56032879522d92a76.png)

R2 Config

set interfaces ge-0/0/0 description “Connection to R1”

set interfaces ge-0/0/0 unit 0 family inet address 172.27.0.2/30

set interfaces ge-0/0/0 unit 0 family inet6 address ::ffff:172.27.0.2/126

set protocols bgp group R1-R2 type external

set protocols bgp group R1-R2 family inet unicast

set protocols bgp group R1-R2 family inet6 unicast

set protocols bgp group R1-R2 peer-as 1

set protocols bgp group R1-R2 neighbor 172.27.0.1

R1 Config

set interfaces ge-0/0/0 description “Connection to R2”

set interfaces ge-0/0/0 unit 0 family inet address 172.27.0.1/30

set interfaces ge-0/0/0 unit 0 family inet6 address ::ffff:172.27.0.1/126

set protocols bgp group R1-R2 type external

set protocols bgp group R1-R2 family inet unicast

set protocols bgp group R1-R2 family inet6 unicast

set protocols bgp group R1-R2 peer-as 2

set protocols bgp group R1-R2 neighbor 172.27.0.2

One Last Note

You may need an extra bit of config to get your router to forward packets addressed to ipv4-mapped-addresses:

set system allow-v4mapped-packets

# **IPv4-Compatible Addressing… A Possible Pitfall**

Older versions of JUNOS used IPv4-Compatible addresses for the next-hop field of a BGP update. This would have been something like “::172.27.0.1”.

If you try to configure IPv4-compatible addresses on your interfaces, you will probably see a log message which looks like this:

Jan 16 13:19:02  mrgarrison rpd[1197]: bgp\_nexthop\_sanity: peer 172.27.0.1 (External AS 701) next hop ::ffff:172.27.0.1 unexpectedly remote, ignoring routes in this update.

Do yourself a favor and check your logs for sanity messages if it looks like you’re not receiving any IPv6 routes that the other route claims it is advertising.

- --

Test case từ anh Ngọc

![](image/18371dfdf48c1e5e35e05944f46203a6.pdf)
