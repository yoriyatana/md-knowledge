# Chapter 15: Troubleshooting BGP

**Initial BGP Troubleshooting**

- Ensure BGP protocol traffic is being allowed into the local device
    - Firewall Filters
    - Security Policies (host-inbound-traffic)
- Watch for BGP TCP session issues
    - BGP messages use TCP transport
    - Often BGP peering problems occur because the TCP connection fails

![image.png](image/image.png)

- When the BGP state field in the **show bgp summary** command is **idle**
    - It indicates that the outgoing interface may be down or there is no route in the routing table to forward a TCP SYN message.
- When the BGP state field in the **show bgp summary** command is **Connect**
    - It indicates that TCP messages are being sent but no response has been received.
        - This can be caused by a firewall filter blocking the BGP port or a misconfigured or nonexistent neighbor.
- When the **BGP** state field in the **show bgp summary** command is **Active**
    - It can indicate that the **BGP** session is having an issue.
        - Normal issues that can cause this state are an incorrect AS number or authentication issue.

**IBGP Peering Issues**

- IBGP peering session establishment issues
    - Misconfigured peer IP address
    - Missing local source IP address
    - No route to neighbor
    - Large TCP MSS that causes BGP packet fragmentation and a firewall filter dropping the fragments
    - Passive neighbor setting at both ends
    - Authentication parameters mismatch

**EBGP Peering Issues**

- EBGP peering session establishment issues
    - Misconfigured peer IP address
    - Misconfigured peer or local AS number
    - MTU mismatch
    - One hop (default) or multiple hops
    - Passive setting at both ends
    - Authentication parameters mismatch

**Routing Issues**

- BGP routing issues
    - Received routes
    - BGP next hop is not reachable
    - Import filtering policy
    - Prefix limit is reached
    - Recursive routing failure
- Advertised routes
    - Export filtering policy
    - Configured aggregation with missing contributing routes
    - Inactive routes
    - Well-known route advertisement controlling communities are attached to a route

**General IBGP Troubleshooting Steps**
![image-1.png](image/image-1.png)

**General EBGP Troubleshooting Steps**
![image-2.png](image/image-2.png)

**Useful BGP Operational Commands**

- Check summary information about BGP peers

```
lab@srx> show bgp summary
```

    - A session stays in **idle** state:
        - BGP cannot even attempt to establish the session
    - • A session bounces between **Connect** and **Active** states:    
        - BGP is trying to initiate a TCP session or is waiting for the session to be initiated by a peer
        - BGP is sending open messages out but is not receiving required information in response
        - Use **show system connections** to view TCP connection data
            - Check the TCP MSS for the session

```
user@R1> show system connections inet extensive | find 10.222.1.5
```

- Check summary information about local BGP groups

```
user@srx> show bgp group
```

- Check BGP neighbor session details

```
user@srx> show bgp neighbor <172.22.138.37>
```

- Examine log files
    - Default log file is messages
    - For authentication errors use **| match auth** (short for authentication)
    - For other errors use **| match noti** (short for notification)

```
user@srx> show log messages| match noti
```

**Use Traceoptions**

For difficult problems, use traceoptions

[edit protocols bgp]

```
user@srx# show traceoptions
file bgp_trace.log size 10m files 2;
flag packets detail;
flag general;
flag open;
flag update;
flag all;

user@srx> show log bgp trace.log
```

**Monitor in Real Time**

- View real-time protocol traffic exchanges
    - **monitor traffic interface**

```
user@srx> monitor traffic interface ge-0/0/4.303 no-resolve detail matching tcp
user@srx> monitor traffic interface ge-O/O/4.303 matching "tcp and port 179"
```

**Verify Routing**

- Check which routes are being advertised

```
user@srx> show route advertising-protocol bgp 10.1.254.1
```

- Check which routes are being received

```
user@srx> show route receive-protocol bgp 10.1.254.1 <hidden | all>
```

- Verify Import Policy Changes

```
user@srx> show route protocol bgp source-gateway 10.1.254.1
```

- Verify BGP routes using display options

```
user@srx> show route protocol bgp
user@srx> show route protocol bgp active-path
```

- Using the detail option

```
user@srx> show route protocol bgp detail
```

- Large BGP packets (Updates) being are fragmented due to a low MTU setting on the link
- The firewall filter drops all fragments that are destined for the Routing Engine
- What options do you have to solve this problem?
    - Enable BGP path MTU discovery
    - Make sure that MTU is large enough to support the BGP negotiated TCP MSS
    - Allow the fragments

```
user@R4> show route receive-protocol bgp 10.222.1.2
user@R4> show route hidden
user@R4> show route resolution unresolved
```
