# BRAS - TROUBLESHOOTING PPPoE in TOMCAT

JunOS Troubleshooting Tools

- CLI commands
- Traceoptions
- Shmlogs
- Tcpdump
- Shell outputs
    - should be used in case if other tools doesn’t give a clue about an issue
- Live core
    - Non service-affecting
    - Contains s snapshot of the process state at the moment of creating
    - **Should be generated only on JTAC request**

CLI Commands (1/11)

- Basic Tomcat health check
- show system subscriber-management summary

```
root@ams_bng1_re> show system subscriber-management summary
General:
    Graceful Restart    Enabled
    Mastership          Master
    Database            Available
    Standby              Resync (100%)
    Chassisd ISSU State  IDLE
    ISSU State          IDLE
    ISSU Wait            0
```

- show system subscriber-management status
    - shows thread information

```
root@ams_bng1_re> show system subscriber-management status   
Subscriber management enabled
BBE_SMGD_PARENT thread_id = 0xa416080
BBE SMGD WORKER thread_id = 0xa416300
BBE SMD WORKER  thread_id = 0xa416580
BBE SCHEDULER  thread_id = 0xa416800
BBE IO          thread_id = 0xa416a80
last cli locker thread_id = 0xa416580, lock count = 0
```

- show system subscriber-management info
    - hidden command
    - shows run-time configuration state

```
root@ams_bng1_re> show system subscriber-management info     
Session Manager started @    Thu Mar  7 16:56:21 2019
Session Manager cleared @    Thu Mar  7 16:56:21 2019
gres state enabled state                  1
commit sync enabled state                1
nsr state enabled state                  1
gratuitous arp disable state              0
gratuitous nd disable state              0
nd override preferred src enable state    0
force dynamic nd state                    0
unsolicted ra disabled state              0
force ra unicast dst enabled state        0
unsolicted mlr disabled state            0
shmlog disabled state                    0
vc backup member local switch state      0
cold start enabled                        0
force show arp no resolve state          0
arp-ping liveness detection enabled state 0
ipv6-nud liveness detection enabled state 0
gratuitous arp recv proc enabled state    0
ipoe dynamic arp enabled state            0
```

CLI commands (2/11)

- show subscribers
    - different filters to check subscriber’s status
    - “summary” knob to check subscribers counter per chassis, slot, port, routing instance
    - “extensive” knob gives subscriber’s RADIUS attributes and provides VBF flow ID:

```
lab@BNG-01> show subscribers summary all       

Subscribers by State
  Active: 18
  Total: 18

Subscribers by Client Type
  VLAN: 2
  PPPoE: 16
  Total: 18

Subscribers by LS:RI
  default: 2
  default:VR-CGNAT: 16
  Total: 18

lab@BNG-01> show subscribers summary port 

Interface          Count
ae5: xe-0/1/2      16               
ae5: xe-0/1/5      16               
ae5: xe-0/1/7      16               

Total Subscribers: 16
```

- PPPoE statistics
    - Aggregate statistics: show pppoe statistics
    - Per underlying interface: show pppoe underlying-interfaces <ifl name> extensive

```
lab@BNG-01> show pppoe statistics                                         
Active PPPoE sessions: 16
  PacketType                      Sent        Received
    PADI                              0            3752
    PADO                            112                0
    PADR                              0              112
    PADS                            112                0
    PADT                            96                5
    Service name error                0                0
    AC system error                  0                0
    Generic error                    0                0
    Malformed packets                0                0
    Unknown packets                  0                0

lab@BNG-01> show pppoe underlying-interfaces extensive   
demux0.3221225686 Index 536871166
  State: Dynamic, Dynamic Profile: PPPoE-PROFILES,
  Max Sessions: 32000, Max Sessions VSA Ignore: Off,
  Active Sessions: 8,
  Service Name Table: None,
  Duplicate Protection: On, Short Cycle Protection: mac-address,
  Direct Connect: Off,
  AC Name: BNG-01,
  PacketType                      Sent        Received
    PADI                              0            1855
    PADO                            56                0
    PADR                              0              56
    PADS                            56                0
    PADT                            48                2
    Service name error                0                0
    AC system error                  0                0
    Generic error                    0                0
    Malformed packets                0                0
    Unknown packets                  0                0
  Lockout Time (sec):  Min: 5, Max: 900
    Total clients in lockout: 0
    Total clients in lockout grace period: 0
```

- show pppoe interfaces brief
    - Allows to obtain underlying interface name and PPPoE session ID
    - Interface name can be an argument in the command

```
lab@BNG-01> show pppoe interfaces brief
Interface      Underlying            State      Session    Remote                                 
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
```

- show pppoe lockout
    - root@ams_bng1_re> show subscribers user-name u1@orange.pl extensive | match PFE
        PFE Flow ID: 112 <<<< VBF flow ID
        Underlying interface can be an argument in the command
    - **show pppoe lockout | match "VLAN|lockout:"**

```
lab@BNG-01> show pppoe lockout
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
```

```
lab@BNG-01> show subscribers user-name MIK1-V_100-HSI2 extensive | match PFE
PFE Flow ID: 308
```

CLI commands (3/11)

```
lab@BNG-01> show system subscriber-management statistics ppp
Session Manager started @ Wed Jun 16 06:29:43 2021
Session Manager cleared @ Wed Jun 16 06:29:43 2021
--------------------------------------------------------------
                    Packet Statistics
--------------------------------------------------------------
I/O Statistics:
--------------------------------------------------------------
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
--------------------------------------------------------------
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
--------------------------------------------------------------
  ARP Statistics
    Rx Statistics
        request packets                  : 0
        reply packets                    : 0
        invalid iffs                    : 64
    Tx Statistics
        reply packets                    : 0
        request packets                  : 0
```

CLI commands (4/11)

- show ppp interface <name>
    - Gives brief information about states of different phases
    - “extensive” knob gives more information:

```
lab@BNG-01> show ppp interface pp0.3221225736 extensive
  Session pp0.3221225736, Type: PPP, Phase: Network
  Keepalive settings: Interval 60 seconds, Up-count 1, Down-count 3
              Magic-Number validation: enable
    LCP
      State: Opened
      Last started: 2021-06-16 11:53:41 UTC
      Last completed: 2021-06-16 11:53:41 UTC
      Negotiated options:
        Authentication protocol: pap, Magic number: 301491486, Initial Advertised MRU: 1492, Local MRU: 1492, Peer MRU: 1480
    Authentication: PAP
      State: Grant
      Last started: 2021-06-16 11:53:41 UTC
      Last completed: 2021-06-16 11:53:41 UTC
    IPCP
      State: Opened
      Last started: 2021-06-16 11:53:41 UTC
      Last completed: 2021-06-16 11:53:41 UTC
      Negotiated options:
        Local address: 10.126.0.1, Remote address: 10.126.0.107
      Negotiation mode: Passive
```

CLI command (5/11)

- show interface <subscriber’s interface>

```
lab@BNG-01> show interfaces pp0.3221225736
  Logical interface pp0.3221225736 (Index 536871216) (SNMP ifIndex 200000304)
    Flags: Up Point-To-Point Encapsulation: PPPoE
    PPPoE:
      State: SessionUp, Session ID: 2,
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
  LCP state: Opened
  NCP state: inet: Opened, inet6: Not-configured, iso: Not-configured, mpls: Not-configured
  CHAP state: Closed
  PAP state: Success
    Protocol inet, MTU: 1480
    Max nh cache: 0, New hold nh limit: 0, Curr nh cnt: 0, Curr new hold cnt: 0, NH drop cnt: 0
      Flags: Unnumbered
      Donor interface: lo0.13 (Index 71)
      Addresses, Flags: Is-Primary
        Local: 10.126.0.1
```

CLI commands (6/11)

- show network-access aaa statistics <authentication|accounting|dynamic-requests>
    - Brief stats about RADIUS communication
    - “detail” knob gives more information about reasons of failures:

```
lab@BNG-01> show network-access aaa statistics authentication detail
Authentication module statistics
  Requests received: 0
  Accepts: 0
  Rejects: 0
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
  Challenges: 0
  Timed out requests: 0

lab@BNG-01> show network-access aaa statistics accounting detail
Accounting module statistics
  Requests received: 0
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
  Accounting packets dropped: 0
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
  Accounting backup responses dropped: 0
  Accounting backup rollover requests: 0
  Accounting backup unknown responses: 0
```

CLI commands (7/11)

- show network-access aaa terminate-code brief
    - Shows aggregate counters explaining subscribers’ disconnect reasons
    - Most popular codes: https://kb.juniper.net/InfoCenter/index?page=content&id=KB33598

|Event                                                     |Type|Code                       |
|----------------------------------------------------------|----|---------------------------|
|CLI command "clear pppoe sessions"                        |ppp |lower-interface-down       |
|CLI command "clear network access aaa username"           |aaa |shutdown-admin-reset       |
|CPE sent PADT                                             |ppp |lower-interface-down       |
|CPE sent LCP TermReq                                      |ppp |lcp-peer-terminate-term-req|
|No response received for LCP keepalive requests sent by MX|ppp |lcp-keepalive-failure      |

```
root@ams_bng1_re> show network-access aaa terminate-code brief

Terminate-code:
  RADIUS    Custom Usage-Count Type Code
  5          no    3          aaa  shutdown-session-timeout                 
  1          no    62          ppp  lcp-peer-terminate-protocol-reject       
  1          no    10          ppp  lcp-peer-terminate-term-req             
  2          no    3          ppp  lower-interface-down
```

CLI Commands (8/11)

- Subscriber’s route has “Private Unicast Next-Hop” in ‘show route’ output:

```
lab@BNG-01> show route 10.126.0.102

VR-CGNAT.inet.0: 22 destinations, 22 routes (22 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

10.126.0.102/32    *[Access-internal/12] 02:11:44
                      Private unicast
```

- To define physical next-hop, use ‘show system subscriber-management route’ command

```
lab@BNG-01> show system subscriber-management route prefix 10.126.0.102 

Route:  10.126.0.102/32
    Routing-instance:        default:VR-CGNAT
    Kernel rt-table id :      5
    Family:                  AF_INET
    Route Type:              Access-internal
    Protocol Type:            Unspecified
    Interface:                pp0.3221225731
    Interface index:          299
    Internal Interface index: 299
    Route index:              101
    Next-Hop index:          616
    Reference-count:          1
    L2 Address:              50:09:00:0a:00:07
    Flags:                    0x0
```

CLI Commands (9/11)

- Show class-of-service scheduler-hierarchy interface <subscriber’s interface>
- Shows actual programming of CoS on the subscriber’s interface

```
root@ams_bng2_re> show class-of-service scheduler-hierarchy interface pp0.3221941191   
Interface/                        Shaping Guaranteed Guaranteed/  Queue  Excess
Resource name                      rate      rate        Excess  weight  weight
                                  kbits    kbits        priority          high/low
xe-0/0/5:0                        10000000
  xe-0/0/5:0 RTP                  10000000        0                  1    1
    best-effort                    10000000        0      Low  Low          95
    network-control                10000000        0      Low  Low            5
  pp0.3221941191                  2000            0                    500  500
    business                      2000            0      Low  Low          95
    network-control                2000            0      High High            5
```

CLI Commands (10/11)

- show dynamic-configuration session information session-id <session-id>
    - display detailed information about dynamic variables and Radius-Returned values

```
root@ams_bng1_re> show dynamic-configuration session information session-id 79   
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
  Dynamic-configuration state: 2
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
  Calling station id: cbr_bng101#
  Advisory options upstream rate: 0
  Advisory options downstream rate: 0
  NAS port: 1001
  Interface set: ae2-1001
  Next Hop MAC address: 56:58:2d:8b:00:00
  Next Hop Ipv6 MAC address: 56:58:2d:8b:00:00
  Configuration bits: 0xff 0xc0 
Dynamic configuration: 
  TCP-NEO-QOS-GENERIC-PROFILE: TCP-NEO-QOS-GENERIC-PROFILE_UID1013
  dyn_TCP-NEO-QOS-GENERIC-PROFILE: 0795e8c9c6fae9746bba5052d36dca02
  junos-cos-scheduler-map: SCM-B2B-DATA-ONLY
  junos-cos-shaping-rate: 2M
  junos-cos-shaping-rate-burst: 2M
  junos-input-filter: FF-V4-NEO-DSL-50M-IN
  junos-output-filter: FF-V4-NEO-32K-VOIP-OUT
  junos-routing-instance: VR-NEO
  junos-tagged-vlan-interface-set-name: ae2-1001
  junos-underlying-interface: demux0.1021001
```

CLI Commands (11/11)

- show dynamic-profile session client-id <session-id>

```
lab@BNG-01> show dynamic-profile session client-id 1
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
                    pppoe {
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
```

---

Traceoptions

- In vast majority of the situation bbe-smgd logs are needed together with protocol logs:

```
set system processes general-authentication-service traceoptions file debug_gauthd
set system processes general-authentication-service traceoptions file size 10m
set system processes general-authentication-service traceoptions file files 10
set system processes general-authentication-service traceoptions flag all

set system processes smg-service traceoptions file debug_bbe-smgd
set system processes smg-service traceoptions file size 10m
set system processes smg-service traceoptions file files 10
set system processes smg-service traceoptions level all
set system processes smg-service traceoptions flag all

set protocols ppp-service traceoptions file debug_ppp
set protocols ppp-service traceoptions file size 10m
set protocols ppp-service traceoptions file files 10
set protocols ppp-service traceoptions level all
set protocols ppp-service traceoptions flag all

set protocols pppoe traceoptions file debug_pppoe
set protocols pppoe traceoptions file size 10m
set protocols pppoe traceoptions file files 10
set protocols pppoe traceoptions level all
set protocols pppoe traceoptions flag all

set system services dhcp-local-server traceoptions file debug_dhcp
set system services dhcp-local-server traceoptions file size 10m
set system services dhcp-local-server traceoptions file files 10
set system services dhcp-local-server traceoptions flag all

--
### DHCP new traceoption
set system processes dhcp-service traceoptions file debug_dhcp
set system processes dhcp-service traceoptions file size 10m
set system processes dhcp-service traceoptions file files 10
set system processes dhcp-service traceoptions flag all

---
clear log debug_gauthd all
clear log debug_bbe-smgd all
clear log debug_ppp all
clear log debug_pppoe all
clear log debug_dhcp all
```

- That’s possible to filter events related to only one subscriber using “filter user” knob
    - Example: set system processes general-authentication-service traceoptions filter user [u1@orange.pl](mailto:u1@orange.pl)
    - Useful for initial analyze of the issue
    - Normally CFTS will ask level all/flag all without filter

---

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

```
root@ams_bng1_re> show shmlog entries logname <all |specific daemon>
```

- Shmlogs entries filtering functionality is subscriber centric i.e. filter per subscriber specific logs. 

```
> show shmlog entries logname all | match "session_id=1"
```

- Events can be filtered for particular daemon log
    - Example: logname jpppd* or logname authd*
- If interested in the events happened in a specific time entries may be filtered as:

```
root@ams_bng1_re> show shmlog entries logname all start-from-latest-?     
  start-from-latest-days  Show entries starting with specified duration from latest(1..1000000000)
  start-from-latest-hours  Show entries starting with specified duration from latest (1..1000000000)
  start-from-latest-minutes  Show entries starting with specified duration from latest (1..1000000000)
  start-from-latest-seconds  Show entries starting with specified duration from latest (1..1000000000)
```

Shmlogs (3/3)

- Shmlogs statistics can be displayed from CLI

```
> show shmlog statistics logname <all | specific daemon>
```

- Stores aggregated statistics about events happened on the router
- Contains information about events, number of occurrence the particular event and timestamp of last event

```
- root@ams_bng1_re> show shmlog statistics logname all
  bbe-debug            statistics... (wrapped count =          0)
    id id name                                                              last_log_date_time          log_cnt      notlog_cnt        total_cnt
    4 BBE_MESSAGE_ENQUEUE                                                                                    0              12
    6 BBE_MESSAGE_DEQUEUE                                                                                    0              12
```

- Important source of information about abnormalities during troubleshooting process

---

Subscriber’s HOST RECEIVE/TRANSMIT PATH
![image.png](image/image.png)

Capture subscriber’s control packets on RE level

```
root@ams_bng1_re> monitor traffic interface demux0.1021001 matching "ether host 56:58:2d:8b:00:00"
verbose output suppressed, use <detail> or <extensive> for full protocol decode
Address resolution is ON. Use <no-resolve> to avoid any reverse lookup delay.
Address resolution timeout is 4s.
Listening on demux0.1021001, capture size 96 bytes
15:23:15.666304  In PPPoE PADI
15:23:15.667966 Out PPPoE PADO [AC-Name "ams_bng1_re"] [Service-Name] [AC-Cookie UTF8]
15:23:15.731384  In PPPoE PADR [Service-Name] [AC-Cookie UTF8]
15:23:15.734075 Out PPPoE PADS [ses 1] [Service-Name] [AC-Name "ams_bng1_re"] [AC-Cookie UTF8]
15:23:15.803997 Out PPPoE  [ses 1]LCP, Conf-Request (0x01), id 54, length 21
15:23:15.810060  In PPPoE  [ses 1]LCP, Conf-Request (0x01), id 0, length 16
15:23:15.810626 Out PPPoE  [ses 1]LCP, Conf-Ack (0x02), id 0, length 16
15:23:15.843885  In PPPoE  [ses 1]LCP, Conf-Nack (0x03), id 54, length 10
15:23:15.844520 Out PPPoE  [ses 1]LCP, Conf-Request (0x01), id 55, length 21
15:23:15.953335  In PPPoE  [ses 1]LCP, Conf-Ack (0x02), id 55, length 21
15:23:15.954706 Out PPPoE  [ses 1]CHAP, Challenge (0x01), id 163, Value cc121a30f59566e5c03924d37c249f234372b4b45b0ccbd190, Name JUNOS
15:23:16.036460  In PPPoE  [ses 1]CHAP, Response (0x02), id 163, Value 9edf1d25a67432569e9b35458c4e2d6d, Name u1@orange.pl
15:23:16.158802 Out PPPoE  [ses 1]CHAP, Success (0x03), id 163, Msg
15:23:16.187564  In PPPoE  [ses 1]IPCP, Conf-Request (0x01), id 0, length 12
15:23:16.188347 Out PPPoE  [ses 1]IPCP, Conf-Request (0x01), id 242, length 12
15:23:16.188461 Out PPPoE  [ses 1]IPCP, Conf-Nack (0x03), id 0, length 12
15:23:16.190952  In PPPoE  [ses 1]IPCP, Conf-Ack (0x02), id 242, length 12
15:23:16.190957  In PPPoE  [ses 1]IPCP, Conf-Request (0x01), id 1, length 12
15:23:16.348215 Out PPPoE  [ses 1]IPCP, Conf-Ack (0x02), id 1, length 12
```

- Packet capture on interface downlink

```
monitor traffic interface ae0 matching "ether host 00:1d:aa:9b:71:31" no-resolve detail|extensive
monitor traffic interface xe-0/0/0 matching "ether host 54:A6:78:CA:00:00" size 1500 extensive write-file PPPOE-capture.pcap
monitor traffic interface ae3 extensive matching "ether host 4c:d9:8f:ff:c8:ed" no-resolve extensive size 9000 /var/tmp/ECC-BDH2.pcap
```

capture SUBSCRIBERS’S PACKET on PFE level

- PFE complex number based on the physical interface and MPC Type
- Do it in production with caution only if it is absolutely necessary
- Pattern can be any string uniquely identify the packet (subscriber’s MAC address in that case)
- By default pattern searched in the first 32 bytes
- If pattern locates after that value, offset must be defined
- Do not forget to turn feature off after capturing
    - test jnh 0 packet-via-dmem disable

```
VMX-0(ams_bng1_re vty)# test jnh 0 packet-via-dmem disable   
VMX-0(ams_bng1_re vty)# test jnh 0 packet-via-dmem enable 16000
VMX-0(ams_bng1_re vty)# test jnh 0 packet-via-dmem capture 0x3 0x56582d8b0000 0
VMX-0(ams_bng1_re vty)# test jnh 0 packet-via-dmem capture 0
VMX-0(ams_bng1_re vty)# test jnh 0 packet-via-dmem dump
<snip>
Wallclock: 0x47859a3c
Received 74 byte parcel:
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
<snip>
VMX-0(ams_bng1_re vty)# test jnh 0 packet-via-dmem disable   
```

High CPU utilization of the bbe-smgd process

- It might happens a situation that bbe-smgd process has 100% of CPU utilization

```
root@ams_bng1_re> show system processes extensive | match bbe-smgd   
89544 root          8  46    0  957M  504M uwait  2  1:24 100.00% bbe-smgd
```

- Usually caused by software bug and service-affecting
- Better to engage JTAC for live troubleshooting
- If live troubleshooting is not possible and service needs to be restored quickly please collect from RE shell as root user

```
root@ams_bng1_re:~ # vty -s 7208 128.0.0.1
show smd throttle ###collect output at least 3 times with 1 minute time interval
```

    - from RE shell as a root user collect bbe-smgd live core at least two times with 1 minute interval

```
#gcore -s -c bbesmgd.live.core.0 `cat /var/run/bbe-smgd.pid`
```

    - From CLI collect twice with 1 minute interval:

```
> show shmlog statistics logname all | save /var/log/jtac-shmlog-stats.log.0
```

```
> show shmlog entries logname all | save /var/log/jtac-shmlog-entries.log
```

- Normally issue resolves after restarting bbe-smgd:

```
root@ams_bng1_re> restart smg-service
```

Wrong CHAP Password Configured on CPE

- Step 1: check for amount of Access Reject received from RADIUS:

```
root@ams_bng1_re> show network-access aaa statistics authentication
Authentication module statistics
  Requests received: 99
  Accepts: 89
  Rejects: 10
  Challenges: 0
  Timed out requests: 0
```

    - Alternatively can be found in shmlogs:

```
root@ams_bng1_re> show shmlog statistics logname all | match Fail     
148 chapTxFailure                                    Mar 14 16:41:47.624765              15                0
256 authNotifySessionResponseFail                    Mar 14 16:41:47.624527              15                0
```

- Step 2: Check authd to confirm that it is related to problematic subscriber:

```
root@ams_bng1_re> show log debug_gauthd | match "username|reject"
Mar 14 16:42:59.605918 authd_radius_build_basic_auth_request: session-id:123 profile=ACP-CUA, username=u2@orange.pl
Mar 14 16:43:00.608711 authd_radius_callback: RADIUS server sent an ACCESS_REJECT, failing login for session-id:123
```

Wrong FIREWALL PARAMETERS received from Radius

- Step 1: check shmlogs statistics for any uncommon amount failures. Failures related to this situation are:

```
root@ams_bng1_re> show shmlog statistics logname all | match Fail                                           
109 BBE_DPROF_GET_SERVICE_FLAG_FAILED                                Mar 14 17:00:44.251969                8                0
296 dynProfActNakFail                                                Mar 14 17:00:44.346802                8                0
392 sesSubscriberActivateFailed                                      Mar 14 17:00:44.346954                8                0
```

- Step 2: check shmlogs entries:

```
root@ams_bng1_re> show shmlog entries logname bbe-dfw-* start-from-latest-minutes 5 | match ERR
bbe-dfw-prio            254 Mar 14 17:00:44.251891 BBE_DFW_DYN_PROF_ERR_STR      session_id=167: Can't find filter template named FF-V4-NEO-32K-VOIP-OU.
bbe-dfw-prio            255 Mar 14 17:00:44.251898 BBE_DFW_DYN_PROF_ERR_CODE  session_id=167: Error code 13 (config err TRUE): Filter template not found.
```

- Step 3: confirm that logs belong to the problematic subscriber:

```
root@ams_bng1_re> show log jtac-authd.log | match "session-id:167" | match username
Mar 14 17:00:43.604816 authd_radius_build_basic_auth_request: session-id:167 profile=ACP-CUA, username=u1@orange.pl
Mar 14 17:00:44.194294 authd_radius_send_acctg_msg: session-id:167 profile=ACP-CUA username=u1@orange.pl acctg_id=(167), ls=default, lr=default
```

Clear Subscriber’s Session

- clear pppoe session interface <interface>
- clear network-access aaa subscriber username <username>
- request system subscriber-management release-session id <session-id>
    - Hidden command of last resort to clear stuck session
    - Forcibly clears the client session
- Pre-installed op script to collect information about stuck session
    - Usage: op url /usr/libexec/scripts/op/bbe_debug.slax sessionid <session-id>
    - Stores collected information at /var/tmp/subscribers_debug_sid_session_id_cleanup.tar.gz
    - Forcibly clears the client session

---

```
show route 203.113.131.2 | no-more
show route 203.113.131.2 extensive | no-more
show route forwarding-table destination 203.113.131.2 | no-more
show route forwarding-table destination 203.113.131.2 extensive | no-more
```

---

1. First test is to validate the PADI packet capture on PFE for GOOD connection on ae81.

 

```
>start shell pfe network FPC2
test jnh 0 packet-via-dmem disable
test jnh 0 packet-via-dmem enable
test jnh 0 packet-via-dmem capture 0x3 0x<client MAC>  20
test jnh 0 packet-via-dmem capture 0x0
test jnh 0 packet-via-dmem dump       
test jnh 0 packet-via-dmem disable
```

---

flow-detection

```
global {
    flow-detection;
    flow-report-rate 100;
    flow-detection-mode off;   ###GLOBAL OFF
}
protocols {   #### ON FOR SPECIFIC PROTOCOLS
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
```

```
lab@batman-re0> show configuration groups debug 
system {
    kernel-replication {
        traceoptions {
            file ksyncd size 100m;
            level detail;
            flag all;
        }
    }
    services {
        subscriber-management-helper {
            traceoptions {
                file subshelper.log;
                flag all;
            }
        }
        subscriber-management {
            traceoptions {
                file subs.log;
                flag all;
                flag database;
                flag session-db;
                flag general;
            }
        }
    }
    auto-configuration {
        traceoptions {
            file autoconfd.log size 10m;
            flag all;
        }
    }
    processes {
        general-authentication-service {
            traceoptions {
                file authd.log size 100m files 2;
                flag all;
            }
        }
        dhcp-service {
            traceoptions {
                file jdhcpd.log size 150m files 2;
                flag all;
            }
        }
    }
}
interfaces {
    traceoptions {
        file dcd.log size 100m files 2;
        flag all;
    }
}

lab@batman-re0> show configuration apply-groups
## Last commit: 2012-06-13 13:45:24 EST by lab
apply-groups [ anz-defaults member0-re0 member0-re1 member1-re0 member1-re1 debug ];    <------ apply the debug group here
```
