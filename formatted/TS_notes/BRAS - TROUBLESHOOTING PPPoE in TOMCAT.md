# BRAS - TROUBLESHOOTING PPPoE in TOMCAT

JunOS Troubleshooting Tools

```text
CLI commands
Traceoptions
Shmlogs
Tcpdump
Shell outputs
```

- should be used in case if other tools doesn’t give a clue about an issue

- Live core

```text
Non service-affecting
Contains s snapshot of the process state at the moment of creating
**Should be generated only on JTAC request**
```

CLI Commands (1/11)

```text
Basic Tomcat health check
show system subscriber-management summary
```

root@ams\_bng1\_re> show system subscriber-management summary

General:

Graceful Restart    Enabled

Mastership          Master

Database            Available

Standby              Resync (100%)

```text
Chassisd ISSU State  IDLE
```

```text
ISSU State          IDLE
```

ISSU Wait            0

```text
show system subscriber-management status
```

- shows thread information

root@ams\_bng1\_re> show system subscriber-management status

Subscriber management enabled

BBE\_SMGD\_PARENT thread\_id = 0xa416080

BBE SMGD WORKER thread\_id = 0xa416300

BBE SMD WORKER  thread\_id = 0xa416580

BBE SCHEDULER  thread\_id = 0xa416800

BBE IO          thread\_id = 0xa416a80

last cli locker thread\_id = 0xa416580, lock count = 0

```text
show system subscriber-management info
```

```text
hidden command
shows run-time configuration state
```

root@ams\_bng1\_re> show system subscriber-management info

Session Manager started @    Thu Mar  7 16:56:21 2019

Session Manager cleared @    Thu Mar  7 16:56:21 2019

```text
gres state enabled state                  1
```

```text
commit sync enabled state                1
```

```text
nsr state enabled state                  1
```

```text
gratuitous arp disable state              0
```

```text
gratuitous nd disable state              0
```

```text
nd override preferred src enable state    0
```

```text
force dynamic nd state                    0
```

```text
unsolicted ra disabled state              0
```

```text
force ra unicast dst enabled state        0
```

```text
unsolicted mlr disabled state            0
```

```text
shmlog disabled state                    0
```

```text
vc backup member local switch state      0
```

cold start enabled                        0

```text
force show arp no resolve state          0
```

```text
arp-ping liveness detection enabled state 0
```

```text
ipv6-nud liveness detection enabled state 0
```

```text
gratuitous arp recv proc enabled state    0
```

```text
ipoe dynamic arp enabled state            0
```

CLI commands (2/11)

```text
show subscribers
```

- different filters to check subscriber’s status
- “summary” knob to check subscribers counter per chassis, slot, port, routing instance
- “extensive” knob gives subscriber’s RADIUS attributes and provides VBF flow ID:

```text
lab@BNG-01> show subscribers summary all
```

```text
Subscribers by State
```

```text
Active: 18
```

```text
Total: 18
```

Subscribers by Client Type

```text
VLAN: 2
```

```text
PPPoE: 16
```

```text
Total: 18
```

Subscribers by LS:RI

```text
default: 2
```

default:VR-CGNAT: 16

```text
Total: 18
```

```text
lab@BNG-01> show subscribers summary port
```

Interface          Count

ae5: xe-0/1/2      16

ae5: xe-0/1/5      16

ae5: xe-0/1/7      16

Total Subscribers: 16

```text
PPPoE statistics
```

- Aggregate statistics: show pppoe statistics
- Per underlying interface: show pppoe underlying-interfaces  extensive

```text
lab@BNG-01> show pppoe statistics
```

Active PPPoE sessions: 16

```text
PacketType                      Sent        Received
```

PADI                              0            3752

PADO                            112                0

PADR                              0              112

PADS                            112                0

PADT                            96                5

```text
Service name error                0                0
```

```text
AC system error                  0                0
```

```text
Generic error                    0                0
```

Malformed packets                0                0

Unknown packets                  0                0

```text
lab@BNG-01> show pppoe underlying-interfaces extensive
```

demux0.3221225686 Index 536871166

```text
State: Dynamic, Dynamic Profile: PPPoE-PROFILES,
```

Max Sessions: 32000, Max Sessions VSA Ignore: Off,

Active Sessions: 8,

Service Name Table: None,

Duplicate Protection: On, Short Cycle Protection: mac-address,

Direct Connect: Off,

AC Name: BNG-01,

```text
PacketType                      Sent        Received
```

PADI                              0            1855

PADO                            56                0

PADR                              0              56

PADS                            56                0

PADT                            48                2

```text
Service name error                0                0
```

```text
AC system error                  0                0
```

```text
Generic error                    0                0
```

Malformed packets                0                0

Unknown packets                  0                0

Lockout Time (sec):  Min: 5, Max: 900

Total clients in lockout: 0

Total clients in lockout grace period: 0

```text
show pppoe interfaces brief
```

- Allows to obtain underlying interface name and PPPoE session ID
- Interface name can be an argument in the command

```text
lab@BNG-01> show pppoe interfaces brief
```

```text
Interface      Underlying            State      Session    Remote
```

interface                        ID        MAC

pp0.3221225727  demux0.3221225686    Session Up  10        50:09:00:0A:00:02

pp0.3221225728  demux0.3221225687    Session Up  7          50:09:00:0E:00:03

pp0.3221225729  demux0.3221225687    Session Up  12        50:09:00:0E:00:06

pp0.3221225730  demux0.3221225687    Session Up  13        50:09:00:0E:00:04

pp0.3221225731  demux0.3221225686    Session Up  16        50:09:00:0A:00:07

pp0.3221225732  demux0.3221225686    Session Up  4          50:09:00:0A:00:03

pp0.3221225733  demux0.3221225686    Session Up  6          50:09:00:0A:00:00

pp0.3221225734  demux0.3221225687    Session Up  1          50:09:00:0E:00:01

pp0.3221225735  demux0.3221225687    Session Up  14        50:09:00:0E:00:07

pp0.3221225736  demux0.3221225686    Session Up  2          50:09:00:0A:00:05

pp0.3221225737  demux0.3221225686    Session Up  5          50:09:00:0A:00:04

pp0.3221225738  demux0.3221225687    Session Up  8          50:09:00:0E:00:05

pp0.3221225739  demux0.3221225687    Session Up  3          50:09:00:0E:00:02

pp0.3221225740  demux0.3221225686    Session Up  9          50:09:00:0A:00:01

pp0.3221225741  demux0.3221225687    Session Up  11        50:09:00:0E:00:00

pp0.3221225742  demux0.3221225686    Session Up  15        50:09:00:0A:00:06

```text
show pppoe lockout
```

- Underlying interface can be an argument in the command

  root@ams\_bng1\_re> show subscribers user-name u1@orange.pl extensive | match PFE

  PFE Flow ID: 112 <<<< VBF flow ID
- **show pppoe lockout | match "VLAN|lockout:"**

```text
lab@BNG-01> show pppoe lockout
```

demux0.3221225686 Index 536871166

Device: ae5, VLAN: 100

Short Cycle Protection: mac-address,

Lockout Time (sec):  Min: 5, Max: 900

Total clients in lockout: 0

Total clients in lockout grace period: 0

demux0.3221225687 Index 536871167

Device: ae5, VLAN: 200

Short Cycle Protection: mac-address,

Lockout Time (sec):  Min: 5, Max: 900

Total clients in lockout: 0

Total clients in lockout grace period: 0

```text
lab@BNG-01> show subscribers user-name MIK1-V\_100-HSI2 extensive | match PFE
```

PFE Flow ID: 308

CLI commands (3/11)

```text
lab@BNG-01> show system subscriber-management statistics ppp
```

Session Manager started @ Wed Jun 16 06:29:43 2021

Session Manager cleared @ Wed Jun 16 06:29:43 2021

- -------------------------------------------------------------

Packet Statistics

- -------------------------------------------------------------

I/O Statistics:

- -------------------------------------------------------------

Rx Statistics

packets                          : 77909

invalid ifls                    : 1

unsupported udp protocols        : 6914

Tx Statistics

packets                          : 1212

Layer 3 Statistics

Rx Statistics

packets                          : 47461

Tx Statistics

packets                          : 0

PPP Statistics:

- -------------------------------------------------------------

Rx Statistics

network packets                  : 809

plugin packets                  : 809

lcp config requests              : 118

lcp config acks                  : 112

lcp termination requests        : 3

pap requests                    : 112

ipcp requests                    : 228

ipcp acks                        : 112

ipv6cp requests                  : 4

unknown protocols                : 120

Tx Statistics

packets                          : 892

lcp config requests              : 114

lcp config acks                  : 114

lcp config rejects              : 4

lcp termination requests        : 93

lcp termination acks            : 3

pap acks                        : 112

ipcp requests                    : 112

ipcp acks                        : 112

ipcp nacks                      : 112

ipcp config rejects              : 4

NET Statistics:

- -------------------------------------------------------------

ARP Statistics

Rx Statistics

```text
request packets                  : 0
```

reply packets                    : 0

invalid iffs                    : 64

Tx Statistics

reply packets                    : 0

```text
request packets                  : 0
```

CLI commands (4/11)

```text
show ppp interface
```

- Gives brief information about states of different phases
- “extensive” knob gives more information:

```text
lab@BNG-01> show ppp interface pp0.3221225736 extensive
```

Session pp0.3221225736, Type: PPP, Phase: Network

Keepalive settings: Interval 60 seconds, Up-count 1, Down-count 3

Magic-Number validation: enable

LCP

```text
State: Opened
```

Last started: 2021-06-16 11:53:41 UTC

Last completed: 2021-06-16 11:53:41 UTC

Negotiated options:

Authentication protocol: pap, Magic number: 301491486, Initial Advertised MRU: 1492, Local MRU: 1492, Peer MRU: 1480

Authentication: PAP

```text
State: Grant
```

Last started: 2021-06-16 11:53:41 UTC

Last completed: 2021-06-16 11:53:41 UTC

IPCP

```text
State: Opened
```

Last started: 2021-06-16 11:53:41 UTC

Last completed: 2021-06-16 11:53:41 UTC

Negotiated options:

Local address: 10.126.0.1, Remote address: 10.126.0.107

Negotiation mode: Passive

CLI command (5/11)

```text
show interface
```

```text
lab@BNG-01> show interfaces pp0.3221225736
```

Logical interface pp0.3221225736 (Index 536871216) (SNMP ifIndex 200000304)

Flags: Up Point-To-Point Encapsulation: PPPoE

PPPoE:

```text
State: SessionUp, Session ID: 2,
```

Session AC name: BNG-01, Remote MAC address: 50:09:00:0a:00:05,

Underlying interface: demux0.3221225686 (Index 536871166)

Ignore End-Of-List tag: Disable

Link:

xe-0/1/2.32767

xe-0/1/5.32767

xe-0/1/7.32767

Input packets : 968

Output packets: 845

Keepalive settings: Interval 60 seconds, Up-count 3, Down-count 3

```text
LCP state: Opened
```

```text
NCP state: inet: Opened, inet6: Not-configured, iso: Not-configured, mpls: Not-configured
```

```text
CHAP state: Closed
```

```text
PAP state: Success
```

Protocol inet, MTU: 1480

Max nh cache: 0, New hold nh limit: 0, Curr nh cnt: 0, Curr new hold cnt: 0, NH drop cnt: 0

Flags: Unnumbered

Donor interface: lo0.13 (Index 71)

Addresses, Flags: Is-Primary

```text
Local: 10.126.0.1
```

CLI commands (6/11)

```text
show network-access aaa statistics
```

- Brief stats about RADIUS communication
- “detail” knob gives more information about reasons of failures:

```text
lab@BNG-01> show network-access aaa statistics authentication detail
```

Authentication module statistics

```text
Requests received: 0
```

```text
Accepts: 0
```

```text
Rejects: 0
```

RADIUS authentication failures: 0

Queue request deleted: 0

Malformed reply: 0

No server configured: 0

Access Profile configuration not found: 0

Unable to create client record: 0

Unable to create client request: 0

Unable to build authentication request: 0

No available server: 0

Unable to create handle: 0

Unable to queue request: 0

Invalid credentials: 0

Malformed request: 0

License unavailable: 0

Redirect requested: 0

Internal failure: 0

Local authentication failures: 0

LDAP lookup failures: 0

```text
Challenges: 0
```

Timed out requests: 0

```text
lab@BNG-01> show network-access aaa statistics accounting detail
```

Accounting module statistics

```text
Requests received: 0
```

Accounting request failures: 0

Accounting request success: 0

Account on requests: 0

Accounting start requests: 0

Accounting interim requests: 0

Accounting stop requests: 0

Timed out requests: 0

Accounting response failures: 0

Accounting response success: 0

Account on responses: 0

Accounting start responses: 0

Accounting interim responses: 0

Accounting stop responses: 0

Accounting rollover requests: 0

Accounting unknown responses: 0

Accounting radius pending requests: 0

Accounting malformed responses: 0

Accounting retransmissions: 0

Accounting bad authenticators: 0

```text
Accounting packets dropped: 0
```

Accounting backup record creation requests: 0

Accounting backup request replay success: 0

Accounting backup request failures: 0

Accounting backup request success: 0

Accounting backup timeouts: 0

Accounting backup in-flight requests: 0

Accounting backup responses success: 0

Accounting backup radius requests: 0

Accounting backup radius responses: 0

Accounting backup radius timeouts: 0

Accounting backup radius pending requests: 0

Accounting backup radius retransmissions: 0

Accounting backup malformed responses: 0

Accounting backup bad authenticators: 0

```text
Accounting backup responses dropped: 0
```

Accounting backup rollover requests: 0

Accounting backup unknown responses: 0

CLI commands (7/11)

```text
show network-access aaa terminate-code brief
```

- Shows aggregate counters explaining subscribers’ disconnect reasons
- Most popular codes: https://kb.juniper.net/InfoCenter/index?page=content&id=KB33598

|  |  |  |
| --- | --- | --- |
| Event | Type | Code |
| CLI command "clear pppoe sessions" | ppp | lower-interface-down |
| CLI command "clear network access aaa username" | aaa | shutdown-admin-reset |
| CPE sent PADT | ppp | lower-interface-down |
| CPE sent LCP TermReq | ppp | lcp-peer-terminate-term-req |
| No response received for LCP keepalive requests sent by MX | ppp | lcp-keepalive-failure |

root@ams\_bng1\_re> show network-access aaa terminate-code brief

Terminate-code:

RADIUS    Custom Usage-Count Type Code

5          no    3          aaa  shutdown-session-timeout

1          no    62          ppp  lcp-peer-terminate-protocol-reject

1          no    10          ppp  lcp-peer-terminate-term-req

2          no    3          ppp  lower-interface-down

CLI Commands (8/11)

- Subscriber’s route has “Private Unicast Next-Hop” in ‘show route’ output:

```text
lab@BNG-01> show route 10.126.0.102
```

```text
VR-CGNAT.inet.0: 22 destinations, 22 routes (22 active, 0 holddown, 0 hidden)
```

+ = Active Route, - = Last Active, \* = Both

10. 126.0.102/32    \*[Access-internal/12] 02:11:44

Private unicast

- To define physical next-hop, use ‘show system subscriber-management route’ command

```text
lab@BNG-01> show system subscriber-management route prefix 10.126.0.102
```

```text
Route:  10.126.0.102/32
```

Routing-instance:        default:VR-CGNAT

Kernel rt-table id :      5

Family:                  AF\_INET

Route Type:              Access-internal

Protocol Type:            Unspecified

Interface:                pp0.3221225731

Interface index:          299

Internal Interface index: 299

Route index:              101

Next-Hop index:          616

```text
Reference-count:          1
```

L2 Address:              50:09:00:0a:00:07

```text
Flags:                    0x0
```

CLI Commands (9/11)

```text
Show class-of-service scheduler-hierarchy interface
Shows actual programming of CoS on the subscriber’s interface
```

root@ams\_bng2\_re> show class-of-service scheduler-hierarchy interface pp0.3221941191

Interface/                        Shaping Guaranteed Guaranteed/  Queue  Excess

```text
Resource name                      rate      rate        Excess  weight  weight
```

kbits    kbits        priority          high/low

xe-0/0/5:0                        10000000

xe-0/0/5:0 RTP                  10000000        0                  1    1

best-effort                    10000000        0      Low  Low          95

network-control                10000000        0      Low  Low            5

pp0.3221941191                  2000            0                    500  500

business                      2000            0      Low  Low          95

network-control                2000            0      High High            5

CLI Commands (10/11)

```text
show dynamic-configuration session information session-id
```

```text
display detailed information about dynamic variables and Radius-Returned values
```

root@ams\_bng1\_re> show dynamic-configuration session information session-id 79

Session info:

Accounting session ID: 79

IP address: 10.0.0.1

IP netmask: 255.255.255.255

Logical system name: default

Profile name: DP-PPPOE-NEO$$02

Session version: 3

Physical IFD name of the interface: ae2

MAC address: 56:58:2d:8b:00:00

NAS port type: 15

Routing instance: VR-NEO

Access Profile: ACP-CUA

User name: u1@orange.pl

Interface IFD Name: pp0

Interface name: pp0.3221225550

Unit number of the interface: 3221225550

```text
Dynamic-configuration state: 2
```

Client session type: 64

IFL type: 2

Accounting type: 2

Accounting interval: 0

Underlying logical-interface: demux0.1021001

Client login time: 2019-03-14 07:55:45 CET

Session start time: 572480.690062

VLAN tag: 1001

Service Type: 2

Framed Protocol: 1

Calling station id: cbr\_bng101#

```text
Advisory options upstream rate: 0
```

```text
Advisory options downstream rate: 0
```

NAS port: 1001

Interface set: ae2-1001

Next Hop MAC address: 56:58:2d:8b:00:00

Next Hop Ipv6 MAC address: 56:58:2d:8b:00:00

Configuration bits: 0xff 0xc0

Dynamic configuration:

TCP-NEO-QOS-GENERIC-PROFILE: TCP-NEO-QOS-GENERIC-PROFILE\_UID1013

```text
dyn\_TCP-NEO-QOS-GENERIC-PROFILE: 0795e8c9c6fae9746bba5052d36dca02
```

junos-cos-scheduler-map: SCM-B2B-DATA-ONLY

```text
junos-cos-shaping-rate: 2M
```

```text
junos-cos-shaping-rate-burst: 2M
```

junos-input-filter: FF-V4-NEO-DSL-50M-IN

junos-output-filter: FF-V4-NEO-32K-VOIP-OUT

junos-routing-instance: VR-NEO

junos-tagged-vlan-interface-set-name: ae2-1001

junos-underlying-interface: demux0.1021001

CLI Commands (11/11)

```text
show dynamic-profile session client-id
```

```text
lab@BNG-01> show dynamic-profile session client-id 1
```

SINGLE-VLAN {

routing-instances {

default {

interface demux0.3221225472;

}

}

interfaces {

demux0 {

no-traps;

unit 3221225472 {

vlan-id 100;

demux-options {

underlying-interface ae5;

}

family {

```text
pppoe {
```

access-concentrator BNG-01;

duplicate-protection;

dynamic-profile PPPoE-PROFILES;

short-cycle-protection {

lockout-time-min 5;

lockout-time-max 900;

}

}

}

}

}

}

}

- --

Traceoptions

- In vast majority of the situation bbe-smgd logs are needed together with protocol logs:

```text
set system processes general-authentication-service traceoptions file debug\_gauthd
```

```text
set system processes general-authentication-service traceoptions file size 10m
```

```text
set system processes general-authentication-service traceoptions file files 10
```

```text
set system processes general-authentication-service traceoptions flag all
```

```text
set system processes smg-service traceoptions file debug\_bbe-smgd
```

```text
set system processes smg-service traceoptions file size 10m
```

```text
set system processes smg-service traceoptions file files 10
```

```text
set system processes smg-service traceoptions level all
```

```text
set system processes smg-service traceoptions flag all
```

```text
set protocols ppp-service traceoptions file debug\_ppp
```

```text
set protocols ppp-service traceoptions file size 10m
```

```text
set protocols ppp-service traceoptions file files 10
```

```text
set protocols ppp-service traceoptions level all
```

```text
set protocols ppp-service traceoptions flag all
```

```text
set protocols pppoe traceoptions file debug\_pppoe
```

```text
set protocols pppoe traceoptions file size 10m
```

```text
set protocols pppoe traceoptions file files 10
```

```text
set protocols pppoe traceoptions level all
```

```text
set protocols pppoe traceoptions flag all
```

```text
set system services dhcp-local-server traceoptions file debug\_dhcp
```

```text
set system services dhcp-local-server traceoptions file size 10m
```

```text
set system services dhcp-local-server traceoptions file files 10
```

```text
set system services dhcp-local-server traceoptions flag all
```

- -

### DHCP new traceoption

```text
set system processes dhcp-service traceoptions file debug\_dhcp
```

```text
set system processes dhcp-service traceoptions file size 10m
```

```text
set system processes dhcp-service traceoptions file files 10
```

```text
set system processes dhcp-service traceoptions flag all
```

- --

```text
clear log debug\_gauthd all
```

```text
clear log debug\_bbe-smgd all
```

```text
clear log debug\_ppp all
```

```text
clear log debug\_pppoe all
```

```text
clear log debug\_dhcp all
```

- That’s possible to filter events related to only one subscriber using “filter user” knob

- Example: set system processes general-authentication-service traceoptions filter user [u1@orange.pl](mailto:u1@orange.pl)
- Useful for initial analyze of the issue
- Normally CFTS will ask level all/flag all without filter

- --

Shmlogs (1/3)

- Junos OS uses a shared memory space to store log entries for subscriber service daemons, such as:

- bbe-smgd
- jpppd
- authd
- cosd,
- dfwd.

- Enabled by default
- Contains similar information as daemon traceoptions

- Key advantage is that all daemon logs are present by default whereas traceoptions must be explicitly enabled
- Writing shmlogs in memory does not slow down the system compared to writing traceoptions files to disk

Shmlogs (2/3)

- Can be displayed from CLI

root@ams\_bng1\_re> show shmlog entries logname

- Shmlogs entries filtering functionality is subscriber centric i.e. filter per subscriber specific logs.

```text
> show shmlog entries logname all | match "session\_id=1"
```

- Events can be filtered for particular daemon log

- Example: logname jpppd\* or logname authd\*

- If interested in the events happened in a specific time entries may be filtered as:

root@ams\_bng1\_re> show shmlog entries logname all start-from-latest-?

start-from-latest-days  Show entries starting with specified duration from latest(1..1000000000)

start-from-latest-hours  Show entries starting with specified duration from latest (1..1000000000)

start-from-latest-minutes  Show entries starting with specified duration from latest (1..1000000000)

start-from-latest-seconds  Show entries starting with specified duration from latest (1..1000000000)

Shmlogs (3/3)

- Shmlogs statistics can be displayed from CLI

```text
> show shmlog statistics logname
```

- Stores aggregated statistics about events happened on the router
- Contains information about events, number of occurrence the particular event and timestamp of last event

- root@ams\_bng1\_re> show shmlog statistics logname all

bbe-debug            statistics... (wrapped count =          0)

id id name                                                              last\_log\_date\_time          log\_cnt      notlog\_cnt        total\_cnt

4 BBE\_MESSAGE\_ENQUEUE                                                                                    0              12

6 BBE\_MESSAGE\_DEQUEUE                                                                                    0              12

- Important source of information about abnormalities during troubleshooting process

- --

Subscriber’s HOST RECEIVE/TRANSMIT PATH

![](image/8b637a720634e5bae4d65072c0496d9c.png)

Capture subscriber’s control packets on RE level

root@ams\_bng1\_re> monitor traffic interface demux0.1021001 matching "ether host 56:58:2d:8b:00:00"

verbose output suppressed, use  or  for full protocol decode

Address resolution is ON. Use  to avoid any reverse lookup delay.

Address resolution timeout is 4s.

Listening on demux0.1021001, capture size 96 bytes

```text
15:23:15.666304  In PPPoE PADI
```

```text
15:23:15.667966 Out PPPoE PADO [AC-Name "ams\_bng1\_re"] [Service-Name] [AC-Cookie UTF8]
```

```text
15:23:15.731384  In PPPoE PADR [Service-Name] [AC-Cookie UTF8]
```

```text
15:23:15.734075 Out PPPoE PADS [ses 1] [Service-Name] [AC-Name "ams\_bng1\_re"] [AC-Cookie UTF8]
```

```text
15:23:15.803997 Out PPPoE  [ses 1]LCP, Conf-Request (0x01), id 54, length 21
```

```text
15:23:15.810060  In PPPoE  [ses 1]LCP, Conf-Request (0x01), id 0, length 16
```

```text
15:23:15.810626 Out PPPoE  [ses 1]LCP, Conf-Ack (0x02), id 0, length 16
```

```text
15:23:15.843885  In PPPoE  [ses 1]LCP, Conf-Nack (0x03), id 54, length 10
```

```text
15:23:15.844520 Out PPPoE  [ses 1]LCP, Conf-Request (0x01), id 55, length 21
```

```text
15:23:15.953335  In PPPoE  [ses 1]LCP, Conf-Ack (0x02), id 55, length 21
```

```text
15:23:15.954706 Out PPPoE  [ses 1]CHAP, Challenge (0x01), id 163, Value cc121a30f59566e5c03924d37c249f234372b4b45b0ccbd190, Name JUNOS
```

```text
15:23:16.036460  In PPPoE  [ses 1]CHAP, Response (0x02), id 163, Value 9edf1d25a67432569e9b35458c4e2d6d, Name u1@orange.pl
```

```text
15:23:16.158802 Out PPPoE  [ses 1]CHAP, Success (0x03), id 163, Msg
```

```text
15:23:16.187564  In PPPoE  [ses 1]IPCP, Conf-Request (0x01), id 0, length 12
```

```text
15:23:16.188347 Out PPPoE  [ses 1]IPCP, Conf-Request (0x01), id 242, length 12
```

```text
15:23:16.188461 Out PPPoE  [ses 1]IPCP, Conf-Nack (0x03), id 0, length 12
```

```text
15:23:16.190952  In PPPoE  [ses 1]IPCP, Conf-Ack (0x02), id 242, length 12
```

```text
15:23:16.190957  In PPPoE  [ses 1]IPCP, Conf-Request (0x01), id 1, length 12
```

```text
15:23:16.348215 Out PPPoE  [ses 1]IPCP, Conf-Ack (0x02), id 1, length 12
```

- Packet capture on interface downlink

```text
monitor traffic interface ae0 matching "ether host 00:1d:aa:9b:71:31" no-resolve detail|extensive
```

```text
monitor traffic interface xe-0/0/0 matching "ether host 54:A6:78:CA:00:00" size 1500 extensive write-file PPPOE-capture.pcap
```

```text
monitor traffic interface ae3 extensive matching "ether host 4c:d9:8f:ff:c8:ed" no-resolve extensive size 9000 /var/tmp/ECC-BDH2.pcap
```

capture SUBSCRIBERS’S PACKET on PFE level

- PFE complex number based on the physical interface and MPC Type
- Do it in production with caution only if it is absolutely necessary
- Pattern can be any string uniquely identify the packet (subscriber’s MAC address in that case)
- By default pattern searched in the first 32 bytes
- If pattern locates after that value, offset must be defined
- Do not forget to turn feature off after capturing

```text
test jnh 0 packet-via-dmem disable
```

VMX-0(ams\_bng1\_re vty)# test jnh 0 packet-via-dmem disable

VMX-0(ams\_bng1\_re vty)# test jnh 0 packet-via-dmem enable 16000

VMX-0(ams\_bng1\_re vty)# test jnh 0 packet-via-dmem capture 0x3 0x56582d8b0000 0

VMX-0(ams\_bng1\_re vty)# test jnh 0 packet-via-dmem capture 0

VMX-0(ams\_bng1\_re vty)# test jnh 0 packet-via-dmem dump

```text
Wallclock: 0x47859a3c
```

```text
Received 74 byte parcel:
```

Dispatch cookie: 0x004a000000000000

0x00 0x00 0xc0 0x30 0x14 0x08 0xff 0xff

0xff 0xff 0xff 0xff 0x56 0x58 0x2d 0x8b

0x00 0x00 0x81 0x00 0x23 0xe9 0x88 0x63

0x11 0x09 0x00 0x00 0x00 0x04 0x01 0x01

0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00

0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00

0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00

0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00

0x00 0x00

VMX-0(ams\_bng1\_re vty)# test jnh 0 packet-via-dmem disable

High CPU utilization of the bbe-smgd process

- It might happens a situation that bbe-smgd process has 100% of CPU utilization

root@ams\_bng1\_re> show system processes extensive | match bbe-smgd

89544 root          8  46    0  957M  504M uwait  2  1:24 100.00% bbe-smgd

- Usually caused by software bug and service-affecting
- Better to engage JTAC for live troubleshooting
- If live troubleshooting is not possible and service needs to be restored quickly please collect from RE shell as root user

root@ams\_bng1\_re:~ # vty -s 7208 128.0.0.1

```text
show smd throttle ###collect output at least 3 times with 1 minute time interval
```

- from RE shell as a root user collect bbe-smgd live core at least two times with 1 minute interval

# gcore -s -c bbesmgd.live.core.0 `cat /var/run/bbe-smgd.pid`

- From CLI collect twice with 1 minute interval:

```text
> show shmlog statistics logname all | save /var/log/jtac-shmlog-stats.log.0
```

```text
> show shmlog entries logname all | save /var/log/jtac-shmlog-entries.log
```

- Normally issue resolves after restarting bbe-smgd:

root@ams\_bng1\_re> restart smg-service

Wrong CHAP Password Configured on CPE

```text
Step 1: check for amount of Access Reject received from RADIUS:
```

root@ams\_bng1\_re> show network-access aaa statistics authentication

Authentication module statistics

```text
Requests received: 99
```

```text
Accepts: 89
```

```text
Rejects: 10
```

```text
Challenges: 0
```

Timed out requests: 0

- Alternatively can be found in shmlogs:

root@ams\_bng1\_re> show shmlog statistics logname all | match Fail

148 chapTxFailure                                    Mar 14 16:41:47.624765              15                0

256 authNotifySessionResponseFail                    Mar 14 16:41:47.624527              15                0

- Step 2: Check authd to confirm that it is related to problematic subscriber:

root@ams\_bng1\_re> show log debug\_gauthd | match "username|reject"

Mar 14 16:42:59.605918 authd\_radius\_build\_basic\_auth\_request: session-id:123 profile=ACP-CUA, username=u2@orange.pl

Mar 14 16:43:00.608711 authd\_radius\_callback: RADIUS server sent an ACCESS\_REJECT, failing login for session-id:123

```text
Wrong FIREWALL PARAMETERS received from Radius
```

- Step 1: check shmlogs statistics for any uncommon amount failures. Failures related to this situation are:

root@ams\_bng1\_re> show shmlog statistics logname all | match Fail

109 BBE\_DPROF\_GET\_SERVICE\_FLAG\_FAILED                                Mar 14 17:00:44.251969                8                0

296 dynProfActNakFail                                                Mar 14 17:00:44.346802                8                0

392 sesSubscriberActivateFailed                                      Mar 14 17:00:44.346954                8                0

- Step 2: check shmlogs entries:

root@ams\_bng1\_re> show shmlog entries logname bbe-dfw-\* start-from-latest-minutes 5 | match ERR

bbe-dfw-prio            254 Mar 14 17:00:44.251891 BBE\_DFW\_DYN\_PROF\_ERR\_STR      session\_id=167: Can't find filter template named FF-V4-NEO-32K-VOIP-OU.

```text
bbe-dfw-prio            255 Mar 14 17:00:44.251898 BBE\_DFW\_DYN\_PROF\_ERR\_CODE  session\_id=167: Error code 13 (config err TRUE): Filter template not found.
```

- Step 3: confirm that logs belong to the problematic subscriber:

root@ams\_bng1\_re> show log jtac-authd.log | match "session-id:167" | match username

Mar 14 17:00:43.604816 authd\_radius\_build\_basic\_auth\_request: session-id:167 profile=ACP-CUA, username=u1@orange.pl

Mar 14 17:00:44.194294 authd\_radius\_send\_acctg\_msg: session-id:167 profile=ACP-CUA username=u1@orange.pl acctg\_id=(167), ls=default, lr=default

```text
Clear Subscriber’s Session
```

```text
clear pppoe session interface
clear network-access aaa subscriber username
request system subscriber-management release-session id
```

- Hidden command of last resort to clear stuck session
- Forcibly clears the client session

- Pre-installed op script to collect information about stuck session

- Usage: op url /usr/libexec/scripts/op/bbe\_debug.slax sessionid
- Stores collected information at /var/tmp/subscribers\_debug\_sid\_session\_id\_cleanup.tar.gz
- Forcibly clears the client session

- --

```text
show route 203.113.131.2 | no-more
```

```text
show route 203.113.131.2 extensive | no-more
```

```text
show route forwarding-table destination 203.113.131.2 | no-more
```

```text
show route forwarding-table destination 203.113.131.2 extensive | no-more
```

- --

1. First test is to validate the PADI packet capture on PFE for GOOD connection on ae81.

```text
>start shell pfe network FPC2
```

```text
test jnh 0 packet-via-dmem disable
```

```text
test jnh 0 packet-via-dmem enable
```

```text
test jnh 0 packet-via-dmem capture 0x3 0x  20
```

```text
test jnh 0 packet-via-dmem capture 0x0
```

```text
test jnh 0 packet-via-dmem dump
```

```text
test jnh 0 packet-via-dmem disable
```

- --

flow-detection

global {

flow-detection;

```text
flow-report-rate 100;
```

flow-detection-mode off;  ###GLOBAL OFF

}

protocols {  #### ON FOR SPECIFIC PROTOCOLS

icmp {

aggregate {

flow-detection-mode automatic;

flow-level-control {

subscriber keep;  ### KEEP FOR AVOID BUG AND NOT DROP BY POLICY

logical-interface keep;

physical-interface keep;

}

}

}

}

```text
lab@batman-re0> show configuration groups debug
```

system {

kernel-replication {

traceoptions {

```text
file ksyncd size 100m;
```

level detail;

flag all;

}

}

services {

subscriber-management-helper {

traceoptions {

```text
file subshelper.log;
```

flag all;

}

}

subscriber-management {

traceoptions {

```text
file subs.log;
```

flag all;

flag database;

flag session-db;

flag general;

}

}

}

auto-configuration {

traceoptions {

```text
file autoconfd.log size 10m;
```

flag all;

}

}

processes {

general-authentication-service {

traceoptions {

```text
file authd.log size 100m files 2;
```

flag all;

}

}

dhcp-service {

traceoptions {

```text
file jdhcpd.log size 150m files 2;
```

flag all;

}

}

}

}

interfaces {

traceoptions {

```text
file dcd.log size 100m files 2;
```

flag all;

}

}

```text
lab@batman-re0> show configuration apply-groups
```

## Last commit: 2012-06-13 13:45:24 EST by lab

apply-groups [ anz-defaults member0-re0 member0-re1 member1-re0 member1-re1 debug ];    <------ apply the debug group here
