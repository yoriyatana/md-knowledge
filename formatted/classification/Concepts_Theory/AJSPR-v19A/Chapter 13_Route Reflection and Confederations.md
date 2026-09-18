# Chapter 13:Route Reflection and Confederations

* *Route Reflection Concepts**

- Allows an IBGP speaker to re-advertise an IBGP-learned route to another IBGP speaker
- Route reflector only re-advertises the active route to clients
- Route reflector does not, by default, change existing IBGP attributes
- Two new BGP attributes to prevent loops:

- Cluster list

- Contains one or more cluster ID values

- Originator ID

* *Route Reflection Attributes**

- Cluster list:

- Operates like an AS path, used by RR for loop prevention
- Also used in the route selection algorithm
- Contains a sequence of cluster IDs

- Cluster ID represents each RR cluster in the network
- RR drops routes that have already transited the cluster
- Added to the cluster list when a RR touches a route

- Originator ID:

- Identifies the first router to inject a route in an RR network

* *Basic Route Reflection**

- Client > RR > Clients and Non-clients
- Non-client > RR > Clients Only

* *RR Client Full Mesh**

- You can disable the internal cluster readvertisements using the **no-client-reflect** command. Once configured, the route reflector only forwards to the clients routes that arrive from outside of the cluster.

* *RR Designs**

- Inline

- RRs are in the path of forwarding traffic
- Commonly deployed
- Hierarchical RR normally used
- RRs perform route reflection and forwarding

- Off-path

- Supports a centralized route reflection design
- Becoming more prevalent as virtual RRs are being used
- Does not require BGP forwarding information in the FIB

* *Virtual Route Reflector**

- A software only implementation of Juniper’s RR functionality
- Improved scalability (depending on the server core hardware use)
- Scalability of the BGP network with lower cost using vRR at multiple locations in the network
- Fast and more flexible deployment using Intel servers rather than router hardware
- Space savings through elimination of router hardware

- Can be installed on a general purpose virtual machine
- KVM, VMware, and OpenStack supported
- 64-bit Intel-based blade server or appliance

* *What is BGP ORR**

- IETF draft

- Draft-ietf-idr-bgp-optimal-route-reflection, (2011)
- As of July 2019 in its 19th revision

- Two types of ORR

- 1. Optimal BGP path selection based on client perspective

- Software solution only, no BGP protocol changes

- 2. Optimal BGP path selection based on policy (traffic engineering data)

- Not fully defined

- Juniper’s implementation of ORR

- Needs full knowledge of network topology
- Requires link state protocol: OSPF or IS-IS

* *Why ORR is Needed**

When a RR is not near the clients it is serving, the following issue is possible

* *Possible Suboptimal RR Issue Solutions**

- Hierarchical RRs

- • RRs in close proximity to clients
- • Limits where you can deploy RR

- Advertise multiple paths through the RR

- • Add-path reduces the benefit of route reflection as additional route information is reintroduced
- • More BGP update churns

- Internet in a VRF with unique RDs per peering router
- Use tunnels to make farther locations look closer
- Optimal Route Reflection

* *Advantages of Optimal Route Reflection**

- Place RR anywhere in the topology
- Solves Hot Potato routing
- No change needed to BGP RR clients
- Can work with Add-Path

* *RFC3345 Oscillation**

* *Scaling BGP—Confederations**

- Breaks a global AS into multiple pieces (sub-AS)
- Within each sub-AS:

- Use private AS numbers
- An IBGP full-mesh topology is still required

- Between each sub-AS:

- EBGP-type configurations are required (multihop, and so forth)
- Only the AS path attribute is changed

- Prevents loops in the network
- Sub-AS networks are *not* used when comparing AS path lengths

- Other BGP attributes are not modified by default

- Next hop, local preference, and MED are all unaffected

* *Confederation AS Path Segments**

- AS confederation sequence:

- • Each sub-AS is added to the AS path attribute
- • ( 65000 65001 65002 ) 100 200 shows a sequence
- • Used for loop prevention only
- • Sequence values are not counted as AS hops

- AS confederation set is used when an aggregated route loses the granularity of the sequence:

- •192.168.24.0/24 ( 65000 65001) 100
- • 192.168.100.0/24 ( 65000 65002 ) 100
- • 192.168.0.0/16 ( { 65000 65001 65002 } ) 100

* *Confederation Configuration**

- The global AS appears as a whole network when viewed externally by peer networks
- All routers remove all confederation information at the edge of the global AS

- Other AS peers do not see the details of the confederation
- No need for **remove-private**
