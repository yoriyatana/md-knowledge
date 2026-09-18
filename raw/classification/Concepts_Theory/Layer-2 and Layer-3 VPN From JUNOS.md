# Untitled Note

## **[Layer-2 and Layer-3 VPN: From JUNOS](https://ippoint.wordpress.com/2010/11/20/layer-2-and-layer-3-vpn-from-junos/)**

Posted on [November 20, 2010](https://ippoint.wordpress.com/2010/11/20/layer-2-and-layer-3-vpn-from-junos/ "11:49 PM") by [Venkat](https://ippoint.wordpress.com/author/ippoint/ "View all posts by Venkat")

- **Common terminologies:**
    - Customer-edge, provide-edge, provider router.
    - VRF – Virtual Routing and Forwarding table: Used in L3 VPN to store customer routes.
    - VFT – Virtual Forwarding table: Used in L2 VPN where encapsulation type,local interface, local site identifiers and labels are stored.
    - VCT–Vitual connection table: Used in L2 VPN. Information in VFT which is Txed to remote PE

**Layer-3 VPN:**

- PE and CE router exchange routes and the customer routes are propagated to another site via service provider network.
- Customer routes are propagated inside BGP via VPN-IPv4 NLRI format which has following fields:
    - Mask: Displays total length of NLRI advertised in update message.
    - MPLS Label: Local PE router allocates a label to forward receive packet to appropriate CE.
    - Route Distinguisher – 8 octets – unique to each customer VPN. Same prefix from two customers are differentiated by RD
    - IPv4 Prefix: customer routes being advertised to remote PE router.
- Configuring ‘**family inet-vpn unicast**’ command on global/group/neighbor mode enables router to form MBGP and exchange vpn information via above NLRI format.
- Received NLRI information will be saved to ‘**bgp.l3vpn.0**’ routing table.
- Router Distinguisher: (RD)
    - Have three portions: Type (2 octets), administrator field and assigned number. When type=0, AF is 2 byte (usually global AS#) and AN is 4 bytes. When type=1, vice versa.
    - RD to be unique in SP network. Can be configured automatically or manually.
    - Automatic: ‘**route-distinguisher-id**’ command inside [edit routing-options]. Router automatically generates a unique assigned number for each VPN table.
    - Manual: Inside VPN routing instance, configure ‘**route-distinguisher xx:xx**’ command.
- Operational concepts: Control plane:
    - Full mesh BGP connection is established among all PE routers.
    - PE router in site-A receives customer routes via any CE-PE routing protocol (static, OSPF, BGP, ISIS, RIP) and place it in the interfaces’ VPN table. (eg: vpn-a.inet.0)
    - Local PE router advertises customer routes via MBGP with its unique RD and one or more route target (RT) set via ‘**vrf-target**’ or ‘**vrf-export**’ command. Latter overrides former.
    - Receiving PE router compares the received route with its locally configured import policy via ‘‘**vrf-target**’ or ‘**vrf-import**’ command. Matched routes are placed in bgp.l3vpn.0 table. Routes that do not match local route-target are not installed in Adj-RIB-in table.
    - Matched routes’ next-hop are checked in inet.3 routing table which has information about LSP from local PE router  to advertised PE router and uses that LSP label as top label.
    - Above routes are placed into VRF table of corresponding customer and advertise via CE-PE protocol to site-B. Same concepts for route advertisement from site-B to site-A.
- Two labels will be available for VPN transit traffic. Top being LSP label to reach PE and bottom being VPN label used by that PE router to forward packets to appropriate CE router.
- **Difference between RT and RD:**
    - RT is an extended community attribute. RD is a unique value representing each customer.
    - For normal site-site communication for a customer, RD is enough for normal operation.
    - For complex scenarios where some routes from customer-A has to be leaked into customer-B VPN table; RT can used to select those routes.
    - In normal operation, it is recommended to have same RD and RT for easy troubleshooting.

PE-CE protocol- BGP:

- Configure ‘protocols bgp’ inside [edit routing-instances <vpn-name>] mode.
- Need to use ‘as-override’ command on PE routers so that customers’ AS number from site-A will be replaced by local SP AS number and forwarded to site-B

PE-CE protocol- OSPF:

- Configure ‘protocols ospf’ inside [edit routing-instances <vpn-name>] mode.
- BGP extended community variables like domain ID, route-type are used to determine type of OSPF LSA, PE router will re-advertise to CE router.
- **Domain ID:**
    - 32-bit value assigned by PE router for each OSPF instances. Default being 0.0.0.0. Can be configured inside vpn protocols ospf  as ‘domain-id x.x.x.x’
    - Allow PE router to advertise OSPF as type-3 or type-5 LSA. May not contain in all ospf routes. Used in backup WAN + VPN scenario to make VPN routes preferable.
- **Route type:**
    - JUNOS uses this attribute in all advertised OSPF routes. Route type along with domain ID determines whether the route has to advertise as type-3 or 5 to site-B CE router.
        - When the received route is internal route type (1,2 or 3 types) and has
            - no domain ID, it is advertised as type-3 summary LSA.
            - domain ID same as configured ID, advertised as type-3 summary LSA.
            - domain ID different that configured ID, advertised as type-5 external LSA.
            - domain ID but not locally configured,  advertised as type-5 external LSA.
            - When the received route is external route type (5 or 7), advertised as type-5 LSA.
- **VPN route tag:**
    - A 32-bit value generated by PE router and places it within type-5 LSA.
    - When a PE router receives type-5 LSA from CE router with a tag value matching the local tag, the router does not advertise that route across the VPN.
    - Represented as [0xd000:Hex(AS number)]. Displayed as dotted decimal format.
    - Can also manually set for each customer using ‘**domain-vpn-tag**’ inside VPN OSPF process.

**Internet access to customers:**

- Independent Internet access:
    - Customer traffic will never consult the routing table of PE router for internet traffic.
    - Two methods are available: method-1:
        - Packets to internet: directly to internet.
        - Packets to VPN: to PE router
    - Method-2:
        - Packets to VPN: to PE router via one logical circuit
        - Packets to internet: to PE router via another circuit. PE act as L2. Lookup at P router.
- Distributed internet access:
    - Method-1:
        - Packets to VPN: to PE router via one link
        - Packets to internet: to PE router via another link.
    - Method-2:
        - Outgoing internet and VPN via one link
            - Need to configure ‘double lookup’ in PE router, to consult inet.0 table for default route in VPN routing table. ‘static route 0.0.0.0/0 next-table inet.0’
            - Incoming traffic via another link
                - Static route to represent customer network is configured in inet.0 table and distributed via BGP to internet.
    - Method-3:
        - Internet traffic and VPN via same link
            - On PE router, double static lookup is configured for outbound traffic.
            - Need to copy customer routes to both inet.0 and VPN table via rib-group.
- Centralized internet access:
    - Internet traffic allowed on one CE-PE router link. This central CE router advertise default 0/0 route to all other CE routers via VPN.
    - Internet destined traffic from all sites reaches central site and then takes to internet.

**Layer-2 VPN**

- Method to transport any L2 technologies across common IP network using MPLS labels.
- Two varieties are available:
    - Kompella-based VPN: Also called as a layer-2 VPN. Uses MBGP to exchange information about customer connections.
    - Martini-based VPN: Also called as a layer-2 circuit. Uses LDP to exchange information.
- Both methods can form MPLS connectivity (LSP between PE routers) using MBGP or LDP protocol.
- **Layer-2 VPN:**
    - Customer information are exchanged using layer-2 VPN NLRI along with BGP extended communities like route target and  ‘layer-2 information community’.
    - Configure ‘**family l2vpn unicast**’ command inside BGP protocols on PE routers.
    - Layer-2 VPN NLRI format:
        - Length:  total length of L2 VPN information.
        - RD: same as in L3 VPN. Uniquely identifies a customer.
        - Local customer edge ID: assigned by PE router for each site within a customer VPN. Configure ‘**site-identifier**’ inside [edit routing-options <name> protocols l2vpn site].
        - Label block offset/Base: This is used by remote PE to calculate the actual label.
        - Sub-TLVs: only ‘circuit status vector’ sub-TLV is defined.
    - Layer-2 information community:
        - To check whether two PE routers are connecting similar type of L2 network.
        - Encapsulation type: to represent whether frame relay, ATM, VLAN, VPLS etc.
        - Control flag:
            - Bit 1- Control bit. If C=1, control word between L2 and MPLS header is required. If C=0, control word is not required.
            - Bit 0- sequence bit. If S=1, all L2 packets should be sent in sequence.
            - Layer-2 MTU:
                - PE advertises MTU setting of PE-CE interface. Can be set to 0 if not required. MTU values between PE routers should match for connection to work.
    - How labels are calculated in L2 VPN:
        - Label used by local PE = [Label-base-remote+ Local-site-id]-Label-offset-remote.
    - Frame-relay as PE-CE connection:
        - ‘**encapsulation frame-relay**’ on CE interface and ‘**encapsulation frame-relay-ccc**’ on PE interface along with DLCI values.
        - DLCI values between PE and its connected CE should be same.
        - Inside [edit routing-instances <vpn_name> protocols] configure **‘l2vpn encapsulation-type frame-relay’**
    - ATM as PE-CE connection:
        - ‘**encapsulation atm-ccc-vc-mux’�**�on PE router interface facing CE. This enables PE router to reassemble ATM cells from CE and forms AAL5 PDU.
        - ‘**encapsulation-type atm-aal5’�**�inside l2vpn protocol.
    - Ethernet VLANs as PE-CE connection:
        - ‘**encapsulation  vlan-ccc’�**�on PE router interface facing CE.
        - ‘**encapsulation-type ethernet-vlan’�**�inside l2vpn protocol.
        - The VLAN ID should be same on both sides of provider network.
    - IP internetworking as PE-CE connection:
        - Both customer sites of SP can have different Layer-2 encapsulation.
        - Eg: ‘**encapsulation frame-relay-tcc**’ on PE interface of one end and ‘**encapsulation atm-tcc-snap’�**�on PE interface of another end can communicate by using ‘**encapsulation-type internetworking’�**�inside l2vpn protocol of both PE routers.
    - Commands:
        - Show l2vpn connections: calculated values of label and status.
- **Layer-2 Circuits:**
    - Only control plane differs compared to L2 VPN.
    - Two PE routers form LDP neighbors using targeted hellos. New TLV to advertise FEC.
    - Layer-2 circuit FEC advertisement:
        - C-bit and VC-type: C-bit determines whether Control word is required. VC-type determines type of L2 encapsulation.
        - Virtual circuit ID: 32-bit value set by PE for each customer site. A particular circuit is uniquely identified using both VC-type and Virtual circuit ID.
    - The interface configuration on PE/CE is same as in L2 VPN. For L2 circuit, we need to configure ‘neighbor <remote_PE> interface <customer_facing> virtual-circuit-id <xx>’ under [edit protocols l2circuit] configuration mode.
    - Commands:
        - Show l2circuit connections: calculated values of label and status.
