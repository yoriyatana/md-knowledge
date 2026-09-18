# Tcpdump packet on RE MX

Wireshare NN

Dump PADx

```text
monitor traffic interface ae3 extensive show
```

Dump MAC

```text
monitor traffic interface ae3 extensive matching "ether src/dst/host 00:50:7f:e2:f8:12"
```

Dump Q-in-Q SVLAN 206 CVLAN 245

```text
monitor traffic interface ae3 extensive matching "ether[14:2]&0x0FFF=0x7D0 && ether[18:2]&0x0FFF=0xF5 && ether[20:2]=0x8863"
```

- --

To use Wireshark read capture file, you can use a hidden knob "write-file filename.pcap" in monitor command

```text
Monitor Layer 2 based on MAC address:
```

```text
monitor traffic interface xe-7/3/0 matching "ether host/src/dst A0:65:18:0E:E1:F3" no-resolve layer2-headers detail
```

1/. Monitor all:

```text
monitor traffic interface ge-0/0/2.17 no-resolve size 1500 detail
```

2/. Monitor ospf traffic:

```text
monitor traffic interface ge-0/0/2.17 no-resolve size 1500 detail matching "proto 89"
```

Or:

```text
monitor traffic interface ge-0/0/2.17 no-resolve size 1500 detail matching "ip proto ospf"
```

Or:

```text
monitor traffic interface ge-0/0/2.17 no-resolve size 1500 detail matching "ip proto 89"
```

3/. Monitor isis traffic:

```text
monitor traffic interface ge-0/0/2.17 no-resolve size 1500 detail matching iso
```

```text
monitor traffic interface ge-0/0/2.17 no-resolve size 1500 detail matching "not ip"
```

4/. Monitor BGP traffic:

```text
monitor traffic interface ge-0/0/2.17 no-resolve size 1500 detail matching "tcp port 179"
```

5/. All other remaining:

Host:

root# run monitor traffic interface ge-0/0/x matching "host 10.130.38.94" no-resolve

Protocol:

root# run monitor traffic interface ge-0/0/x matching arp

Port:

root# run monitor traffic interface ge-0/0/x matching "port 22"

IP address:

root# run monitor traffic interface ge-0/0/x matching "host 10.130.38.94" no-resolve detail

Source host:

```text
monitor traffic interface ge-0/0/0 detail no-resolve matching "src host 1.1.1.1"
```

Destination host and port:

```text
monitor traffic interface fxp0 extensive matching "dst host 10.254.5.1 and port 162"
```

A network:

root# run monitor traffic interface ge-0/0/x matching "net 225.1.1.0/24" no-resolve detail

UDP port 646:

root# run monitor traffic interface ge-0/0/x matching "udp port 646"

Increase the size of capture:

root# run monitor traffic interface ge-0/0/x matching arp size 1500

Save the capture to a file:

root# run monitor traffic interface ge-0/0/x matching arp write-file capture.pcap <<<<< write-file is a hidden command so type it out

Matching "not tcp port 3128” and matching tcp port 23

root# run monitor traffic interface ge-0/0/x matching "not tcp port 3128 and tcp port 23"

A more complicated combination but might be useful in some cases:

root# run monitor traffic interface ge-0/0/x matching "arp or (icmp and host 3.3.3.2)"

From <<https://kb.juniper.net/InfoCenter/index?page=content&id=KB16385&actp=search>>

https://kb.juniper.net/InfoCenter/index?page=content&id=KB33629

<https://kb.juniper.net/InfoCenter/index?page=content&id=KB34714&actp=METADATA>

Having VLAN tag packet

```text
user@R2> monitor traffic interface ae0.0 layer2-headers matching "ether[12:2] == 0x8100" extensive print-hex
```

SVLAN tag ID is "1418", VLAN tag ID is "7"

```text
user@R2> monitor traffic interface ge-2/2/0 no-resolve layer2-headers matching "ether[14:2] & 0x0fff == 0x58a && ether[18:2] & 0x0fff == 0x7" extensive print-hex
```

Multicast frame

```text
user@R2> monitor traffic matching "ether[0] & 1 != 0" extensive layer2-headers print-hex
```

Source MAC address begins with "56:00".

```text
user@R1> monitor traffic interface ge-0/0/1 matching "ether[6:2] == 0x5600" extensive layer2-headers print-hex
```

TOS is not zero.

```text
user@R2> monitor traffic interface ge-0/0/1 matching "ip[1] & 0xff != 0" extensive print-hex
```

IP source address is 192.168.\*.2 (3-octet is wildcard but other octets are exact match).

```text
user@R2> monitor traffic interface ge-0/0/1 layer2-headers matching "ip[12:4] & 0xffff00ff == 0xc0a80002" extensive print-hex
```

IP packet whose size is more than 1000 bytes

```text
user@R1> monitor traffic interface ge-0/0/1 matching "ip[2:2] >= 1000" extensive layer2-headers print-hex
```

VRRP(protocol 112=0x70)

```text
user@R2> monitor traffic interface ge-0/0/1 layer2-headers matching "ip[9:1] == 0x70" extensive print-hex
```

VRRP group-id = 99(0x63)

```text
user@R2> monitor traffic interface ge-0/0/1 layer2-headers matching "vrrp[1:1] == 0x63" extensive print-hex
```

PADx on vlan tag packet

matching "ether[16:2] == 0x8863" extensive print-hex

Note: L2 header

- ethernet index start from 0

PADx on double vlan tag packet

matching "ether[20:2] == 0x8863" extensive print-hex

In the capture filter expressions "ether[0:4]" and "ether[6:4]", 0 and 6 are the starting bytes for the destination MAC address field and the source MAC address field respectively, and 4 is the number of bytes to examine. Unfortunately, you want to examine three bytes, but you can only put 1, 2, or 4 after the colon, so three is not a valid value. However, the "& 0xffffff00" expression masks off the fourth byte.

PADO on vlan tag packet

matching "ether[19:1] == 0x9" extensive print-hex
