# Chapter 12:BGP Attributes and Policy - Part 2

* *The Origin Code**

- Installed by the originating router for the prefix (route)
- A tag of believability as to the origin of the route information _(Where did you get it from?)_
- BGP origin code is a well-known, mandatory attribute
- Origin can be internal, external, or unknown
    - I: Internal (0)—Learned from an IGP
    - E: External (1)—Learned from EGP
    - ?: Incomplete (2)—NLRI found by some other means
- I (0) is better than E (1), which is better than ? (2)
- **All Junos OS BGP routes have origin IGP by default**
- To the Juniper Networks router, it does not matter that these routes are advertised to another AS through EBGP; the BGP origin code is not altered as the routes are advertised to an EBGP peer.

* *Multi-Exit Discriminator**

- An optional, nontransitive attribute, MED is never passed through one AS to another AS
- A neighboring AS can use MED to prefer one of several paths to the local AS
- Informs neighboring AS which ingress path to use to reach the local AS in an attempt to influence inbound traffic
- Can perform some primitive load balancing
- Routes that are redistributed into BGP will have a BGP MED value equal to the metric of the original route
- Other AS networks can preempt MED with other BGP attributes

* *Path Selection and MEDs**

- By default, the Junos OS uses a deterministic MED comparison scheme for routes from the same AS
- **always-compare-med** compares MED values, regardless of whether the neighboring AS is the same
    - Use with caution—every network has a different interpretation of a _good_ MED
- **cisco-non-deterministic** compares paths based on when they are received
    - _Not_ recommended for use in your network
    - Can cause incorrect route selections

```
[edit]
user@router# set protocols bgp path-selection ?
Possible completions:
always-compare-med                        Always compare MED values, regardless of neighbor AS
cisco-non-deterministic                    Use Cisco IOS nondeterministic path selection algorithm
```

* *BGP Communities**

- BGP attribute (optional) passed along to other BGP peers (transitive)
- A group of destinations that share a common property
- Simplify routing policies by identifying routes based on logical bounds you establish
    - AS number is very broad (lots of routes)
    - IP prefix is very granular (route filter for each route)
- Used with other attributes to accept, prefer, or advertise BGP routes

* *Notes on Communities**

- Establishes _categories_ for routes and prefixes
- Often sets local preference for a group
- Cuts down on manual reconfiguration and complexity of maintenance
- If a new prefix is placed in a community, no other changes to routing policy are necessary
- Too many communities require more manual maintenance
- Too many overlapping communities can be a nightmare
- Well-known communities have a global meaning
- Must define local-use communities
- Community attribute is a list of four-octet, individual community
- attribute values associated with a route
    - Route can belong to many communities
    - Two high-order octets represent an AS number
    - Two low-order octets represent a value unique to that AS
    - Represented in decimal form of _AS:number_ (for example: 200:123)
    - All values in AS 0 and 65535 are reserved
    - 4 Byte ASNs have the format: 1234567L:456 where L indicates the long format
    - 4 Byte ASNs can also be represented using format: 12345.12345:789

* *Well-Known Communities**

- Three standard values:
    - No-export (OxFFFFFFOl): These routes must be distributed within the confederation (or AS), but no farther
    - No-advertise (0xFFFFFF02): These routes must not be advertised to other BGP peers
    - No-export-subconfed (0xFFFFFF03): These routes must not be advertised to external BGP peers (confined to sub-AS)
- No-export typically keeps aggregation optimal
- No-advertise has narrower scope
    - Often used when dual links exist between two routers
- Well-known communities must be defined as named objects in Junos in order to use them in policies

* *Common Community Groupings**

- Allows for documentation of information and actions useful for Service Providers and their Customers.
    - Informational Communities
        - Can be used to convey SP specific information (i.e. how and where a route is learned)
    - Action Communities
        - Can be used to control route attributes and how they should be exported to EBGP neighbors (i.e. AS-Path prepend, MED preference)
    - Local Preference Communities
        - Used to influence for best-path selection, (i.e. values for backup routes, and setting various local preference values)
    - Other Communities
        - Implement the ability to blackhole disruptive traffic
        - Congestion

* *Configuring a BGP Community**

- Community ID format:
    - **_as-number:community-value_**
    - Well-known communities can be created using the following Community-ID as the name:
        - **no-export**
        - **no-advertise**
        - **no-export-subconfed**
- Must be configured in Junos as a named object

```
[edit policy-options]
community <name> members community-id;
```

- Using multiple community-ids in a community is a logical AND

```
[edit policy-options]
community <name> members [community-id community-id];
```

* *Community Actions**

- **add**: Leave existing communities alone and add in the specified value
- **delete**: Remove only the specified values and leave other existing communities alone
- **set**: Remove ALL existing communities and add the specified values

* *Community Matching**

- show route community *:20 terse
- show route community *:20 detail
- show route community-name community-1 detail

* *More Complex Regex**

- Can use more complex regular expressions with communities
    - Community regex is _character based_ (not like AS path)
    - Format is still _term operator_
    - Regex anchors ( A) and ($) are not required, but can be helpful
    - Used in both **show route** and within a policy as a match condition
        - **show route community _regex_**
        - **community _match-this_ members _regex_**
- The combination of wildcards (. *) results in matching one or more digits in either the AS number portion or community value portion of the community string
