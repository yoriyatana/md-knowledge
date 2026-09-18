# How to disable PFE inline PPP keepalive messages

<https://www.configrouter.com/disable-pfe-inline-ppp-keepalive-messages-5823/>

This article outlines how to disable PFE inline PPP keepalive messages, periodic messages sent at predefined intervals to determine whether the underlying TCP connection is still up.

Thanks to Release Line Item 6162 (RLI6162), the PFE can now handle client-initiated PPP LCP Echo Request/Reply packets.

The PFE can now receive and process the client Echo Request and generate a Reply automatically.

Using the PFE this way instead of the RE saves CPU cycles on the processor and exception queue resources, allowing for increased subscriber scale and improved system stability.

One side effect of having the PFE handle the PPP Echo Requests instead of the RE: When the interface is monitored via the command monitor traffic, the packets are not displayed because the RE does not see or process them.

This situation begs the questions below:

- Can PFE keepalive processing be disabled so that logs can be collected?
- Or, Can PFE involvement be disabled to help troubleshoot problems arising from how inline keepalive messages are processed?

If, for whatever reason, you do not want the packets to be processed by the PFE, you can toggle a sysctl, an interface for examining and dynamically changing parameters in the operating system.

The sysctl requires root access to the shell of the RE. The default value of ‘6’ indicates that the PFE will handle the keepalive messages. Changing it to ‘4’ causes all packets to be exceptioned to the RE:

root@MX240% sysctl net.link.ppp.ppp\_dist\_ka=4

net.link.ppp.ppp\_dist\_ka: 6 -> 4

Notes:

- The change takes effect only for new PPP interfaces that come up after the sysctl is modified.
- Care should be taken to make the modification only to a system that can handle the increased volume of exception packets that will be sent to the RE.

Below are sample logs with the sysctl set to disable PFE keepalive messages:

lab@MX240> show subscribers

Interface IP Address/VLAN ID User Name LS:RI

pp0.1073746225 123.123.123.123 [kc@kc.com](mailto:kc@kc.com) default:internet

lab@MX240> show interfaces pp0.1073746225 | match Underlying

Underlying interface: demux0.100 (Index 373)

lab@MX240> monitor traffic interface demux0.100 extensive no-resolve

Address resolution is OFF.

Listening on demux0.100, capture size 1514 bytes

18:11:34.163752 In

Juniper PCAP Flags [Ext, In], PCAP Extension(s) total length 22

Device Media Type Extension TLV #3, length 1, value: Unspecified (0)

Logical Interface Encapsulation Extension TLV #6, length 1, value: Ethernet (14)

Device Interface Index Extension TLV #1, length 2, value: 160

Logical Interface Index Extension TLV #4, length 4, value: 373

Logical Unit Number Extension TLV #5, length 4, value: 100

- ----original packet-----

00:00:69:03:01:02 > 88:e0:f3:84:a7:c1, ethertype 802.1Q (0x8100), length 34: vlan 100, p 0, ethertype PPPoE S, PPPoE [ses 1]LCP (0xc021), length 10: LCP, Echo-Request (0x09), id 58, length 10

encoded length 8 (=Option(s) length 4)

0x0000: c021 093a 0008

Magic-Num 0x0f47d4f8

18:11:34.163766 Out

Juniper PCAP Flags [Ext], PCAP Extension(s) total length 22

Device Media Type Extension TLV #3, length 1, value: Unspecified (0)

Logical Interface Encapsulation Extension TLV #6, length 1, value: Ethernet (14)

Device Interface Index Extension TLV #1, length 2, value: 160

Logical Interface Index Extension TLV #4, length 4, value: 373

Logical Unit Number Extension TLV #5, length 4, value: 100

- ----original packet-----

88:e0:f3:84:a7:c1 > 00:00:69:03:01:02, ethertype 802.1Q (0x8100), length 34: vlan 100, p 6, ethertype PPPoE S, PPPoE [ses 1]LCP (0xc021), length 10: LCP, Echo-Reply (0x0a), id 58, length 10

encoded length 8 (=Option(s) length 4)

0x0000: c021 0a3a 0008

Magic-Num 0x70fd8b2d

^C

2 packets received by filter

0 packets dropped by kernel

And, as a final check, if all interfaces on a given PFE are logged in after you have changed to the sysctl, the PFE inline keepalive statistics should no longer increment:

NPC1(MX240 vty)# show jnh inline-ka session 0 ppp global-stats

PPP Inline keepalive Global Stats:

Total Rx PPP Echo Request pkts : 12881

Total Rx PPP Echo Reply pkts : 0

Total Tx PPP Echo Request pkts : 0

Total Tx PPP Echo Reply pkts : 12881

Total PPP Magic Number Mismatch pkts : 0

NPC1(MX240 vty)# show jnh inline-ka session 0 ppp global-stats

PPP Inline keepalive Global Stats:

Total Rx PPP Echo Request pkts : 12881

Total Rx PPP Echo Reply pkts : 0

Total Tx PPP Echo Request pkts : 0

Total Tx PPP Echo Reply pkts : 12881

Total PPP Magic Number Mismatch pkts : 0
