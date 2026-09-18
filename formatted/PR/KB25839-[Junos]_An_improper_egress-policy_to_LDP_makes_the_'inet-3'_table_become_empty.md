# KB25839 - [Junos] An improper egress-policy to LDP makes the 'inet.3' table become empty

[https://kb.juniper.net/InfoCenter/index?page=content&id=KB25839&cat=JUNOS_PLATFORM&actp=LIST](https://kb.juniper.net/InfoCenter/index?page=content&id=KB25839&cat=JUNOS_PLATFORM&actp=LIST)

* *SUMMARY:**

This article describes the issue of an improper egress-policy to LDP resulting in the **inet.3** table being empty.

* *SYMPTOMS:**

- The **egress-policy** statement is used to control the set of prefixes that are advertised to LDP from the routing table (such as **inet.0**) and causes the router to be the egress router for these prefixes. By default, only the loopback address is advertised to LDP.
- Explicitly configuring an egress policy for LDP should be done carefully, as an improper egress-policy can result in a empty **inet.3** table.

For example:

An existing IDP session and entry in the **inet.3** is present in a LDP-speaking router, on which **lo0.0** has a primary and preferred address of **5.5.5.5/32** and a normal address of **5.5.5.6/32**. The downstream neighbor's loopback address is **6.6.6.6/32**.

> > show ldp session
>
> Address   State             Connection   Hold time
>
> 6.6.6.6     Operational    Open            23
>
>
>
>
>
> {MASTER}
>
>
>
>
>
> > show route table inet.3
>
>
>
>
>
> inet.3: 1 destinations, 1 routes (1 active, 0 holddown, 0 hidden)
>
> + = Active Route, - = Last Active, * = Both
>
>
>
>
>
> 6.6.6.6/32 *[LDP/9] 00:00:33, metric 1
>
> > to 12.12.12.2 via ge-4/3/4.0
>
>
>
>
>
> {MASTER}

If a default accept is explicity set by mistake, then it is applied to LDP (normally, the accept should be in term 1; but here it is in default accept).

> > show configuration policy-options policy-statement LDP-Export-loopbacks
>
> term 1 {
>
> from {
>
> protocol direct;
>
> route-filter 5.5.5.5/32 exact;
>
> route-filter 5.5.5.6/32 exact;
>
> }
>
> }
>
> then accept;
>
>
>
>
>
> {MASTER}
>
>
>
>
>
> > show configuration protocols ldp
>
> egress-policy LDP-Export-loopbacks;
>
> interface ge-4/3/4.0;
>
> interface lo0.0;
>
>
>
>
>
> {MASTER}

As a result, the **inet.3** table becomes empty:

> > show route table inet.3
>
>
>
>
>
> {MASTER}

* *CAUSE:**

Due to the above improper configuration, LDP just imports all prefixes in the **inet.0** table to its database and announces that they are from it's own FECs. Junos does not store locally originated FECs in the **inet.3** table, as they are used only to be the next-hops for the BGP protocol.

> > show ldp database
>
> Input label database, 5.5.5.5:0--6.6.6.6:0
>
> Label      Prefix
>
> 299888   5.5.5.5/32
>
> 299888   5.5.5.6/32
>
> 3           6.6.6.6/32
>
>
>
>
>
> Output label database, 5.5.5.5:0--6.6.6.6:0
>
> Label      Prefix
>
> 3             5.5.5.5/32
>
> 3             5.5.5.6/32
>
> 3             6.6.6.6/32
>
> 3             9.1.1.2/32
>
> 3             10.0.0.0/8
>
> 3             11.0.0.4/30
>
> 3             11.0.0.6/32
>
> 3             12.12.12.0/30
>
> 3             12.12.12.1/32
>
> 3             100.0.0.1/32
>
> 3             100.0.12.0/30
>
> 3             100.0.12.1/32
>
> 3             172.16.0.0/12
>
> 3             172.27.100.0/24
>
> 3             172.27.100.9/32
>
> 3             172.27.100.109/32
>
> 3             183.81.203.22/32
>
> 3             192.168.0.0/16
>
> 3             192.168.1.0/24
>
> 3             192.168.1.1/32
>
> 3             224.0.0.2/32
>
> 3             224.0.0.5/32
>
> 3             224.0.0.13/32
>
> 3             224.0.0.22/32
>
>
>
>
>
> {MASTER}

* *SOLUTION:**

In the above egress-policy, move the **then accept** action to **term 1** and then commit; both the LDP database and **inet.3** table will become normal:

> > show system rollback compare 1 0
>
> [edit policy-options policy-statement LDP-Export-loopbacks term 1]
>
> + then accept;
>
> [edit policy-options policy-statement LDP-Export-loopbacks]
>
> - then accept;
>
>
>
>
>
> {MASTER}
>
> > show configuration policy-options policy-statement LDP-Export-loopbacks
>
> term 1 {
>
> from {
>
> protocol direct;
>
> route-filter 5.5.5.5/32 exact;
>
> route-filter 5.5.5.6/32 exact;
>
> }
>
> then accept;
>
> }
>
>
>
>
>
> {MASTER}
>
> tomyang@m120-re0> show ldp database
>
> Input label database, 5.5.5.5:0--6.6.6.6:0
>
> Label    Prefix
>
> 299888   5.5.5.5/32
>
> 299888   5.5.5.6/32
>
> 3        6.6.6.6/32
>
>
>
>
>
> Output label database, 5.5.5.5:0--6.6.6.6:0
>
> Label      Prefix
>
> 3             5.5.5.5/32
>
> 3             5.5.5.6/32
>
> 299856     6.6.6.6/32
>
>
>
>
>
> {MASTER}
>
> > show route table inet.3
>
>
>
>
>
> inet.3: 1 destinations, 1 routes (1 active, 0 holddown, 0 hidden)
>
> + = Active Route, - = Last Active, * = Both
>
>
>
>
>
> 6.6.6.6/32 *[LDP/9] 00:03:20, metric 1
>
> > to 12.12.12.2 via ge-4/3/4.0
>
>
>
>
>
> {MASTER}
