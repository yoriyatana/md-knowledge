# MPC11E - LACP không up/join

0x7

00000111

11100000

1 Active

1 SHORT timeout

1 WILL aggregate

0 Not in sync

0 Mux is NOT Collecting

0 Mux is NOT Distributing

0 LACP PDU

0 No expired

0x46

01000110

01100010

0 Passive

1 SHORT timeout

1 WILL aggregate

0 Not in sync

0 Mux is NOT Collecting

0 Mux is Distributing

1 default

0 No expired

0x47

01000111

11100010

1 Active

1 SHORT timeout

1 WILL aggregate

0 Not in sync

0 Mux is NOT Collecting

0 Mux is NOT Distributing

1 default

0 No expired

- --

# LACP Port State

```text
The LACP port state (also known as the actor state) field is a single byte, each bit of which is a flag indicating a particular status. In this table, mux (i.e. a multiplexer) refers to the logical unit which aggregates the links into a single logical transmitter/receiver.
```
The meaning of each bit is as follows:

|  |  |  |
| --- | --- | --- |
| Bit | Name | Meaning |
| 0 | LACP\_Activity | Device intends to transmit periodically in order to find potential members for the aggregate. This is toggled by mode active in the channel-group configuration on the member interfaces.  1 = Active, 0 = Passive. |
| 1 | LACP\_Timeout | Length of the LACP timeout.  1 = Short Timeout, 0 = Long Timeout |
| 2 | Aggregation | Will allow the link to be aggregated.  1 = Yes, 0 = No (individual link) |
| 3 | Synchronization | Indicates that the mux on the transmitting machine is in sync with what’s being advertised in the LACP frames.  1 = In sync, 0 = Not in sync |
| 4 | Collecting | Mux is accepting traffic received on this port  1 = Yes, 0 = No |
| 5 | Distributing | Mux is sending traffic using this port  1 = Yes, 0 = No |
| 6 | Defaulted | Whether the receiving mux is using default (administratively defined) parameters, if the information was received in an LACP PDU.  1 = default settings, 0 = via LACP PDU |
| 7 | Expired | In an expired state  1 = Yes, 0 = No |

# Junos OS and NXOS

Junos OS users are probably smiling right now, as this should look very familiar:

```text
john@switch> show lacp interfaces ae1
```
Aggregated interface: ae1

```text
LACP state: Role Exp Def Dist Col Syn Aggr Timeout Activity
```
xe-1/0/0 Actor No No Yes Yes Yes Yes Fast Active

xe-1/0/0 Partner No No Yes Yes Yes Yes Fast Passive

xe-2/0/0 Actor No No No No No Yes Fast Active

xe-2/0/0 Partner No No No Yes Yes Yes Fast Passive

Cisco users on the other hand may be weeping quietly when viewing a port-channel summary:

us-atl01-z1fa07a# show lacp neighbor interface port-channel 101

Flags: S - Device is sending Slow LACPDUs F - Device is sending Fast LACPDUs

A - Device is in Active mode P - Device is in Passive mode

port-channel101 neighbors

Partner's information

Partner Partner Partner

Port System ID Port Number Age Flags

Eth1/6 127,39-0d-12-c2-2b-40 0x3 427434 SA

LACP Partner Partner Partner

```text
Port Priority Oper Key Port State
```
127 0x2 0x3f

Partner's information

Partner Partner Partner

Port System ID Port Number Age Flags

Eth2/6 127,39-0d-12-c2-2b-40 0x1 112 SA

LACP Partner Partner Partner

```text
Port Priority Oper Key Port State
```
127 0x2 0x3f

```text
The partner port state is 0x3f, which is not very helpful. The good news is that looking at individual members does reveal the information in a more human-friendly format:
```
us-atl01-z1fa07a# show lacp interface eth 1/6

Interface Ethernet1/6 is up

[...]

Local Port: Eth1/6 MAC Address= 0-de-fb-11-32-a6

System Identifier=0x8000, Port Identifier=0x8000,0x106

Operational key=100

LACP\_Activity=active

LACP\_Timeout=Long Timeout (30s)

Synchronization=IN\_SYNC

Collecting=true

Distributing=true

Partner information refresh timeout=Short Timeout (3s)

```text
Actor Admin State=(Ac-1:To-1:Ag-1:Sy-0:Co-0:Di-0:De-0:Ex-0)
Actor Oper State=(Ac-1:To-0:Ag-1:Sy-1:Co-1:Di-1:De-0:Ex-0)
Neighbor: 0x3
```
MAC Address= 39-0d-12-c2-2b-40

System Identifier=0x7f, Port Identifier=0x7f,0x3

Operational key=2

LACP\_Activity=active

LACP\_Timeout=short Timeout (1s)

Synchronization=IN\_SYNC

Collecting=true

Distributing=true

```text
Partner Admin State=(Ac-0:To-1:Ag-0:Sy-0:Co-0:Di-0:De-0:Ex-0)
Partner Oper State=(Ac-1:To-1:Ag-1:Sy-1:Co-1:Di-1:De-0:Ex-0)
```
Aggregate or Individual(True=1)= 1

However, for the sake of anybody who has been sent output from show lacp neighbor interface port-channel X and wants to understand the hex value that’s displayed (0x3F in this case), it’s pretty simple.

# Decode-o-matic

- Convert hexadecimal to binary. Hexadecimal 0x3F is 00111111 in binary.
- Flip the bits around. 00111111 becomes 11111100
- Map the bits in this order to the table above:

1 -> ACTIVE mode

1 -> SHORT timeout

1 -> WILL aggregate

1 -> In SYNC

1 -> Mux is Collecting

1 -> Mux is Distributing

0 -> NOT running administratively configured settings

0 -> NOT expired

Alternatively, I suppose, flip the table so that the entries run from 7 to 0 instead of 0 to 7, then you don’t have to flip the bits; either way works. In this case 0x3F indicates a link which is an active part of the aggregated interface.

Clearly what we want from a link is that bit 7 is 0 (not expired) and bits 2-5 are 1 (will aggregate, in sync, collecting, distributing).

```text
A recent port I had trouble with was reported as partner port state 0xC7, which in binary is 11000111, which when flipped to 11100011 means:
```
1 -> ACTIVE mode

1 -> SHORT timeout

1 -> WILL aggregate

0 -> NOT In Sync

0 -> Mux is NOT Collecting

0 -> Mux is NOT Distributing

1 -> Running administratively configured settings

1 -> EXPIRED!

Clearly this link was not happy, but thankfully a shut / no shut sequence was enough to revive the patient.

Happy aggregating!
