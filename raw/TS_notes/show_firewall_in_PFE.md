# show firewall in PFE

=~=~=~=~=~=~=~=~=~=~=~= PuTTY log 2021.08.02 19:50:42 =~=~=~=~=~=~=~=~=~=~=~=

run             exit

Exiting configuration mode

admin-full@NIX-Router> show interfaces filters | no-more

Interface       Admin Link Proto Input Filter         Output Filter

et-0/0/0        up    up  

et-0/0/0.3      up    up   inet

                           multiservice

et-0/0/0.9      up    up   inet

                           multiservice

et-0/0/0.32767  up    up   multiservice

gr-0/0/0        up    up  

ip-0/0/0        up    up  

lc-0/0/0        up    up  

lc-0/0/0.32769  up    up   vpls

lt-0/0/0        up    up  

lt-0/0/0.0      up    up   inet

lt-0/0/0.1      up    up   inet

lt-0/0/0.2      up    up   inet

lt-0/0/0.3      up    up   inet

lt-0/0/0.32767  up    up  

mt-0/0/0        up    up  

pd-0/0/0        up    up  

pe-0/0/0        up    up  

pfe-0/0/0       up    up  

pfe-0/0/0.16383 up    up   inet

                           inet6

pfh-0/0/0       up    up  

pfh-0/0/0.16383 up    up   inet

pfh-0/0/0.16384 up    up   inet

ud-0/0/0        up    up  

ut-0/0/0        up    up  

vt-0/0/0        up    up  

et-0/0/1        up    up  

et-0/0/1.0      up    up   inet

                           multiservice

et-0/0/1.1      up    up   inet

                           multiservice

et-0/0/1.2      up    up   inet

                           multiservice

et-0/0/1.3      up    up   inet

                           multiservice

et-0/0/1.4      up    up   inet

                           multiservice

et-0/0/1.5      up    up   inet

                           multiservice

et-0/0/1.6      up    up   inet

                           multiservice

et-0/0/1.7      up    up   inet

                           multiservice

et-0/0/1.8      up    up   inet

                           multiservice

et-0/0/1.9      up    up   inet

                           multiservice

et-0/0/1.32767  up    up   multiservice

et-0/0/2        up    down

et-0/0/2.16386  up    down

xe-0/1/0        up    up  

xe-0/1/0.0      up    up   inet

                           multiservice

xe-0/1/0.1      up    up   inet

                           multiservice

xe-0/1/0.2      up    up   inet

                           multiservice

xe-0/1/0.32767  up    up   multiservice

xe-0/1/1        up    down

xe-0/1/1.32767  up    down multiservice

xe-0/1/2        up    up  

xe-0/1/2.0      up    up   inet

                           multiservice

xe-0/1/3        up    down

xe-0/1/3.16386  up    down

xe-0/1/4        up    up  

xe-0/1/4.0      up    up   inet

                           multiservice

xe-0/1/4.32767  up    up   multiservice

xe-0/1/5        up    up  

xe-0/1/5.0      up    up   inet

                           multiservice

xe-0/1/5.32767  up    up   multiservice

xe-0/1/6        up    up  

xe-0/1/6.0      up    up   inet

                           multiservice

xe-0/1/7        up    down

xe-0/1/7.0      up    down inet

                           inet6

                           multiservice

cbp0            up    up  

demux0          up    up  

dsc             up    up  

em2             up    up  

em2.32768       up    up   inet

em3             up    up  

em3.0           up    up   inet

                           tnp  

em4             up    up  

em4.0           up    up   inet

                           tnp  

esi             up    up  

fti0            up    up  

fti1            up    up  

fti2            up    up  

fti3            up    up  

fti4            up    up  

fti5            up    up  

fti6            up    up  

fti7            up    up  

fxp0            up    up  

fxp0.0          up    up   inet

gre             up    up  

ipip            up    up  

irb             up    up  

jsrv            up    up  

jsrv.1          up    up   inet

lo0             up    up  

lo0.0           up    up   inet

lo0.1           up    up   inet

lo0.2           up    up   inet

lo0.16385       up    up   inet

lsi             up    up  

mif             up    up  

mtun            up    up  

pimd            up    up  

pime            up    up  

pip0            up    up  

pp0             up    up  

rbeb            up    up  

tap             up    up  

vtep            up    up  

admin-full@NIX-Router> show firewall filter PROTECT-RE | no-more

Filter: PROTECT-RE                                             

Policers:

Name                                                Bytes              Packets

POLICER-10M-ACCEPT-FTP                                  0                    0

POLICER-1M-ACCEPT-TRACEROUTE-UDP                        0                    0

POLICER-2M-ACCEPT-ICMP-EXTERNAL                         0                    0

POLICER-2M-ACCEPT-SSH                                   0                    0

POLICER-3M-ACCEPT-ICMP-INTERNAL                         0                    0

admin-full@NIX-Router> show firewall filter PROTECT-RE-LS logical-system vsys-int-nix | no-more

admin-full@NIX-Router> show firewall filter PROTECT-RE-LS-lo0.0-i logical-system vsys-int-nix | no-more

admin-full@NIX-Router> show firewall filter PROTECT-RE-LS logical-system vsys-bgp-nix | no-more

admin-full@NIX-Router> show firewall filter PROTECT-RE-LS-lo0.1-i logical-system vsys-bgp-nix | no-more

admin-full@NIX-Router> start shell pfe network fpc0

SMPC platform (1601Mhz Intel(R) Atom(TM) CPU processor, 3168MB memory, 8192KB flash)

SMPC0(NIX-Router vty)# show filter

    <carriage return>     Completes command

    aggregate-policer     display aggregate policer details

    counters              display filter counter information

    dram                  display total filter dram usage

    filter-chain-info     display global chain filter info(for testing)

    hierarchical-policer   display hierarchical policer details

    hw                    display shim specific information

    implicit              display implicit filter information

    index                 display filter

    log                   display filter log information

    manager               display filter manager information

    memory                display total dfw instructions and ktree memory used by all filters

    next-intf-info        show next-intf info

    nexthops              display nexthops available for NH usage

    policer               display policer details

    service-msg           display DFW service message information

    shared-pol            display all shared policer information

    state                 show filter state info

    summary               display filter summary information

    svc-tmplt             display service filter template details

    three-color-policer   display three-color-policer details

SMPC0(NIX-Router vty)# show filter    index SMPC0(NIX-Router vty)# show filter index    

    <number>              filter index

SMPC0(NIX-Router vty)# show filter index                          summary SMPC0(NIX-Router vty)# show filter summary          

Filter Summary:

Number of Program  Filters = 0

Number of Term     Filters = 19

Number of Resolve  Filters = 0

Number of Simple  Filters = 0

Number of Implicit Filters = 15

Number of Other    Filters = 0

Number of cached non-local Filters = 0

Number of post cli Implicit Filters = 0

Number of service filter templates = 0

Total Number of Filters = 19

Protocol Filters:

Number of PROTO_IP Filters = 3

Number of PROTO_IP6 Filters = 1

Number of PROTO_MPLS Filters = 0

Number of PROTO_VPLS Filters = 4

Number of PROTO_CCC Filters = 0

Number of PROTO_ANY Filters = 10

Number of PROTO_BRIDGE Filters = 0

Number of Filters with unknown protocols = 1

Application Filters:

Number of Implicit Filters from OAM = 0

Number of Implicit Filters from JDHCPD = 0

Number of Implicit Filters from L2CPD = 1

Number of Implicit Filters from DHCP L2 = 0

Number of Implicit Filters from PGCPD_COMPILED = 0

Number of Implicit Filters from PGCPD_FUF = 0

Number of Implicit Filters from FTAPLITE = 0

Number of Implicit Filters from SA_VAL = 0

Number of Implicit Filters from JDHCPD_L2_FUF = 0

Number of Implicit Filters from SDK1 = 0

Number of Implicit Filters from SDK2 = 0

Number of Implicit Filters from SDK3 = 0

Number of Implicit Filters from SDK4 = 0

Number of Implicit Filters from SDK5 = 0

Number of Implicit Filters from TEST1 = 0

Number of Implicit Filters from TEST2 = 0

Number of Implicit Filters from DOT1XD = 0

Number of Implicit Filters from DYNAMIC SERVICES = 0

Number of Implicit Filters from LPDFD = 0

Number of Implicit Filters from Propagated Config = 0

Number of Implicit Filters from RPD = 0

Number of Implicit Filters from unknown = 0

Number of Implicit Filters from unknown = 14

Number of Implicit Filters from LI_DFCD = 0

Number of Implicit Filters from ESWD = 0

Number of Implicit Filters from ESWD EVB = 0

Number of Implicit Filters from PPMD = 0

Number of Implicit Filters from SPD = 0

Number of Implicit Filters from RMOPD = 0

Number of Implicit Filters from unknown = 0

Number of Implicit Filters from UACD = 0

Number of Implicit Filters from MCOS = 0

Number of Implicit Filters from RMPSD = 0

Number of Implicit Filters from DHCP L2 DAI = 0

Number of Implicit Filters from OPENFLOWD = 0

Number of Implicit Filters from VMOND = 0

Number of Implicit Filters from DHCP IPV6 = 0

Number of Implicit Filters from DHCP ICMPV6 = 0

Number of Implicit Filters from JDHCPD L3 TAG = 0

Number of Implicit Filters from BBE1 = 0

Number of Implicit Filters from BBE1_LI = 0

Number of Implicit Filters from BBE1_BGF = 0

Number of Implicit Filters from URL-FILTERD = 0

Number of Implicit Filters from TWAMP = 0

Number of Implicit Filters from CAED-GLOBAL = 0

Number of Implicit Filters from IDS_FILTER = 0

Number of Implicit Filters from RTLOGD = 0

Number of Implicit Filters from CAED-LOCAL = 0

SMPC0(NIX-Router vty)# q   show SMPC0(NIX-Router vty)# show     fi

                            ^

'fi' is ambiguous.  Possible choices:

    filter                show filter info

    filter-block          filter-block

    firewall              Display filter information

SMPC0(NIX-Router vty)# show fi   l

                            ^

'fil' is ambiguous.  Possible choices:

    filter                show filter info

    filter-block          filter-block

terSMPC0(NIX-Router vty)# show filter   

    filter                show filter info

    filter-block          filter-block

SMPC0(NIX-Router vty)# show filter    

    <carriage return>     Completes command

    aggregate-policer     display aggregate policer details

    counters              display filter counter information

    dram                  display total filter dram usage

    filter-chain-info     display global chain filter info(for testing)

    hierarchical-policer   display hierarchical policer details

    hw                    display shim specific information

    implicit              display implicit filter information

    index                 display filter

    log                   display filter log information

    manager               display filter manager information

    memory                display total dfw instructions and ktree memory used by all filters

    next-intf-info        show next-intf info

    nexthops              display nexthops available for NH usage

    policer               display policer details

    service-msg           display DFW service message information

    shared-pol            display all shared policer information

    state                 show filter state info

    summary               display filter summary information

    svc-tmplt             display service filter template details

    three-color-policer   display three-color-policer details

SMPC0(NIX-Router vty)# show filter    

Program Filters:

---------------

   Index     Dir     Cnt    Text     Bss  Name

--------  ------  ------  ------  ------  --------

Term Filters:

------------

   Index    Semantic  Properties   Name

--------  ---------- --------  ------

       1  Classic    -         PROTECT-RE

       2  Classic    -         __default_bpdu_filter__

   17000  Classic    -         __default_arp_policer__

   65280  Classic    -         __auto_policer_template__

   65281  Classic    -         __auto_policer_template_1__

   65282  Classic    -         __auto_policer_template_2__

   65283  Classic    -         __auto_policer_template_3__

   65284  Classic    -         __auto_policer_template_4__

   65285  Classic    -         __auto_policer_template_5__

   65286  Classic    -         __auto_policer_template_6__

   65287  Classic    -         __auto_policer_template_7__

   65288  Classic    -         __auto_policer_template_8__

   65536  Classic    -         PROTECT-RE-LS

16777216  Classic    -         fnp-filter-level-all

46137345  Classic    -         HOSTBOUND_IPv4_FILTER

---(more)---             46137346  Classic    -         HOSTBOUND_IPv6_FILTER

46137353  Classic    -         filter-control-subtypes

46137354  Classic    -         snoop-arp-filter

46137355  Classic    -         snoop-ns-na-filter

Resolve Filters:

---------------

   Index

--------

SMPC0(NIX-Router vty)# show SMPC0(NIX-Router vty)# show     i   fil

                             ^

'fil' is ambiguous.  Possible choices:

    filter                show filter info

    filter-block          filter-block

terSMPC0(NIX-Router vty)# show  filter    1

                                    ^

Syntax error at `1'.

SMPC0(NIX-Router vty)# [A      show SMPC0(NIX-Router vty)# show       fil

                             ^

'fil' is ambiguous.  Possible choices:

    filter                show filter info

    filter-block          filter-block

terSMPC0(NIX-Router vty)# show  filter    index SMPC0(NIX-Router vty)# show  filter index    1

Term Filters:

------------

   Index    Semantic  Properties   Name

--------  ---------- --------  ------

       1  Classic    -         PROTECT-RE

SMPC0(NIX-Router vty)# [A[A[A                  show SMPC0(NIX-Router vty)# show           fil

                             ^

'fil' is ambiguous.  Possible choices:

    filter                show filter info

    filter-block          filter-block

terSMPC0(NIX-Router vty)# show  filter    index SMPC0(NIX-Router vty)# show  filter index    65536

Term Filters:

------------

   Index    Semantic  Properties   Name

--------  ---------- --------  ------

   65536  Classic    -         PROTECT-RE-LS

SMPC0(NIX-Router vty)# show SMPC0(NIX-Router vty)# show    fi

                            ^

'fi' is ambiguous.  Possible choices:

    filter                show filter info

    filter-block          filter-block

    firewall              Display filter information

SMPC0(NIX-Router vty)# show fi   l

                            ^

'fil' is ambiguous.  Possible choices:

    filter                show filter info

    filter-block          filter-block

terSMPC0(NIX-Router vty)# show filter          

                            ^

'filte' is ambiguous.  Possible choices:

    filter                show filter info

    filter-block          filter-block

rSMPC0(NIX-Router vty)# show filter    i    index SMPC0(NIX-Router vty)# show filter index    1

    <carriage return>     Completes command

    counters              filter counters

    detail                detailed filter information

    dram                  filter dram usage

    fuf                   display FUF filter

    instances             list of filter instances

    jnh                   Show nexthops for filter

    memory                display dfw instruction and ktree memory used by a filter

    nexthops              filter action nexthops

    policers              Show list of policers

    prefix-count          display number of prefixes in each term

    program               filter program

    psa                   show all psa

    psc                   show prefix specific counter

    psp                   show prefix specific policer

    timestamp             filter timestamp of last change or counter clear

    version               Show filter version

SMPC0(NIX-Router vty)# show filter index 1    detail SMPC0(NIX-Router vty)# show filter index 1 detail    

Term Filters:

------------

   Index    Semantic  Properties   Name

--------  ---------- --------  ------

       1  Classic    -         PROTECT-RE

filter has no flow cache requested

Current context : 0.

SMPC0(NIX-Router vty)# [A          show filter index 1 detail pro

    <carriage return>     Completes command

SMPC0(NIX-Router vty)# show filter index 1 detail pro      f   g

    <carriage return>     Completes command

SMPC0(NIX-Router vty)# show filter index 1 detail prog                                    program SMPC0(NIX-Router vty)# show filter index 1 program              

Filter index = 1

Optimization flag: 0xf7

Filter notify host id = 0

Pfe Mask = 0xFFFFFFFF

jnh inst = 0x0

Filter properties: None

Filter state = CONSISTENT

term DISCARD-SMALL-PACKETS

term priority 0

    packet-length  

         0-24

        true branch to match action in rule DISCARD-NTP

        false branch to match is-fragment in rule DISCARD-FIRST-FRAG

term DISCARD-FIRST-FRAG

term priority 0

    is-fragment  

        value & 0x3fff  = 0x2000

        true branch to match action in rule DISCARD-NTP

        false branch to match is-fragment in rule DISCARD-NEXT-FRAG

term DISCARD-NEXT-FRAG

term priority 0

    is-fragment  

        value & 0x3fff != 0x0000

        true branch to match action in rule DISCARD-NTP

        false branch to match protocol in rule ACCEPT-BFD

---(more)---             term ACCEPT-BFD

term priority 0

    protocol  

         1  -> icmp-type in ACCEPT-ICMP-INTERNAL

        6  -> port in ACCEPT-LDP-UNICAST

        17

        46  -> source-address in ACCEPT-RSVP

        89  -> source-address in ACCEPT-OSPF

        false branch to match action in rule DISCARD-ALL

    destination-port  

         3784-3785

        4784

        false branch to match port in rule ACCEPT-LDP-DISCOVER

    source-address  

    10.10.10/24

    10.151.3/24

    14.225.229.44/30

    42.114.208.68/30

    103.144.152.0/25

    103.144.153.240/28

    103.152.48/24

    103.152.49.0/28

    !103.152.49.12/30

    103.152.49.16/30

    103.152.49.128/27

    103.152.49.160/28

    103.152.49.192/29

    103.152.49.224/27

    112.197.11.150/31

    119.82.139.232/29

    127.0.0.1/32

    192.168.1.3/32

    192.168.1.4/32

    192.168.9.0/30

    192.168.12.0/29

        true branch to match action in rule ACCEPT-LSP-PING

        false branch to match port in rule ACCEPT-LDP-DISCOVER

---(more)---             term ACCEPT-LDP-DISCOVER

term priority 0

    port  

         646

        false branch to match port in rule ACCEPT-SELF-PING

    source-address  

    10.10.10/24

    10.151.3/24

    14.225.229.44/30

    42.114.208.68/30

    103.144.152.0/25

    103.144.153.240/28

    103.152.48/24

    103.152.49.0/28

    !103.152.49.12/30

    103.152.49.16/30

    103.152.49.128/27

    103.152.49.160/28

    103.152.49.192/29

    103.152.49.224/27

    112.197.11.150/31

    119.82.139.232/29

    127.0.0.1/32

    192.168.1.3/32

    192.168.1.4/32

    192.168.9.0/30

    192.168.12.0/29

        true branch to match action in rule ACCEPT-LSP-PING

        false branch to match port in rule ACCEPT-SELF-PING

---(more)---             term ACCEPT-LDP-UNICAST

term priority 0

    port  

         646

        false branch to match port in rule ACCEPT-BGP

    source-address  

    10.10.10/24

    10.151.3/24

    14.225.229.44/30

    42.114.208.68/30

    103.144.152.0/25

    103.144.153.240/28

    103.152.48/24

    103.152.49.0/28

    !103.152.49.12/30

    103.152.49.16/30

    103.152.49.128/27

    103.152.49.160/28

    103.152.49.192/29

    103.152.49.224/27

    112.197.11.150/31

    119.82.139.232/29

    127.0.0.1/32

    192.168.1.3/32

    192.168.1.4/32

    192.168.9.0/30

    192.168.12.0/29

        true branch to match action in rule ACCEPT-LSP-PING

        false branch to match port in rule ACCEPT-BGP

---(more)---             term ACCEPT-RSVP

term priority 0

    source-address  

    10.10.10/24

    10.151.3/24

    14.225.229.44/30

    42.114.208.68/30

    103.144.152.0/25

    103.144.153.240/28

    103.152.48/24

    103.152.49.0/28

    !103.152.49.12/30

    103.152.49.16/30

    103.152.49.128/27

    103.152.49.160/28

    103.152.49.192/29

    103.152.49.224/27

    112.197.11.150/31

    119.82.139.232/29

    127.0.0.1/32

    192.168.1.3/32

    192.168.1.4/32

    192.168.9.0/30

    192.168.12.0/29

        true branch to match action in rule ACCEPT-LSP-PING

        false branch to match action in rule DISCARD-ALL

---(more)---             term ACCEPT-SELF-PING

term priority 0

    port  

         8503

        false branch to match destination-port in rule ACCEPT-SNMP

    source-address  

    127.0.0.1/32

        true branch to match action in rule ACCEPT-LSP-PING

        false branch to match destination-port in rule ACCEPT-SNMP

term ACCEPT-BGP

term priority 0

    port  

         179

        false branch to match port in rule ACCEPT-SSH

    source-address  

    14.225.229.45/32

    42.114.208.69/32

    112.197.11.150/32

    119.82.139.233/32

    192.168.1.1/32

    192.168.1.2/31

    192.168.1.4/32

    192.168.9.1/32

        true branch to match action in rule ACCEPT-LSP-PING

        false branch to match port in rule ACCEPT-SSH

---(more)---             term ACCEPT-OSPF

term priority 0

    source-address  

    10.10.10/24

    10.151.3/24

    14.225.229.44/30

    42.114.208.68/30

    103.144.152.0/25

    103.144.153.240/28

    103.152.48/24

    103.152.49.0/28

    !103.152.49.12/30

    103.152.49.16/30

    103.152.49.128/27

    103.152.49.160/28

    103.152.49.192/29

    103.152.49.224/27

    112.197.11.150/31

    119.82.139.232/29

    127.0.0.1/32

    192.168.1.3/32

    192.168.1.4/32

    192.168.9.0/30

    192.168.12.0/29

        true branch to match action in rule ACCEPT-LSP-PING

        false branch to match action in rule DISCARD-ALL

---(more)---             term ACCEPT-SSH

term priority 0

    port  

         22

        false branch to match destination-port in rule ACCEPT-NETCONF

    source-address  

    10.151.3/24

    127.0.0.1/32

        false branch to match destination-port in rule ACCEPT-NETCONF

    then

    accept

    policer template POLICER-2M

    policer POLICER-2M-ACCEPT-SSH

        app_type 0

        bandwidth-limit 2000000 bits/sec

        burst-size-limit 25000 bytes

        discard

term ACCEPT-NETCONF

term priority 0

    destination-port  

         830

        false branch to match port in rule ACCEPT-FTP

    source-address  

    10.151.3/24

        true branch to match action in rule ACCEPT-LSP-PING

        false branch to match port in rule ACCEPT-FTP

---(more)---             term ACCEPT-FTP

term priority 0

    port  

         20-21

        false branch to match action in rule DISCARD-ALL

    source-address  

    10.151.3/24

        false branch to match action in rule DISCARD-ALL

    then

    accept

    policer template POLICER-10M

    policer POLICER-10M-ACCEPT-FTP

        app_type 0

        bandwidth-limit 10000000 bits/sec

        burst-size-limit 125000 bytes

        discard

term ACCEPT-SNMP

term priority 0

    destination-port  

         161

        false branch to match port in rule DISCARD-NTP

    source-address  

    10.151.3.142/32

    10.151.3.145/32

    10.151.3.249/32

        true branch to match action in rule ACCEPT-LSP-PING

        false branch to match port in rule DISCARD-NTP

---(more)---             term DISCARD-NTP

term priority 0

    port  

         123

        false branch to match port in rule ACCEPT-LSP-PING

    then

    discard

term ACCEPT-ICMP-INTERNAL

term priority 0

    icmp-type  

         0

        3

        8

        11

        false branch to match action in rule DISCARD-ALL

    source-address  

    10.151.3/24

    127.0.0.1/32

        false branch to match action in rule ACCEPT-ICMP-EXTERNAL

    then

    accept

    policer template POLICER-3M

    policer POLICER-3M-ACCEPT-ICMP-INTERNAL

        app_type 0

        bandwidth-limit 3000000 bits/sec

        burst-size-limit 37000 bytes

        discard

---(more)---             term ACCEPT-ICMP-EXTERNAL

term priority 0

    then

    accept

    policer template POLICER-2M

    policer POLICER-2M-ACCEPT-ICMP-EXTERNAL

        app_type 0

        bandwidth-limit 2000000 bits/sec

        burst-size-limit 25000 bytes

        discard

term ACCEPT-LSP-PING

term priority 0

    port  

         3503

        false branch to match port in rule ACCEPT-TRACEROUTE-UDP

    source-address  

    127.0.0.1/32

        false branch to match port in rule ACCEPT-TRACEROUTE-UDP

    then

    accept

term ACCEPT-TRACEROUTE-UDP

term priority 0

    port  

         33434-33523

        false branch to match action in rule DISCARD-ALL

    ttl  

         1

        false branch to match action in rule DISCARD-ALL

    then

    accept

    policer template POLICER-1M

    policer POLICER-1M-ACCEPT-TRACEROUTE-UDP

        app_type 0

        bandwidth-limit 1000000 bits/sec

        burst-size-limit 15000 bytes

        discard

---(more)---             term DISCARD-ALL

term priority 0

    then

    discard

    syslog

SMPC0(NIX-Router vty)#                [A[A                                                         show SMPC0(NIX-Router vty)# show                       fil

                            ^

'fil' is ambiguous.  Possible choices:

    filter                show filter info

    filter-block          filter-block

terSMPC0(NIX-Router vty)# show filter    index SMPC0(NIX-Router vty)# show filter index     1 counters SMPC0(NIX-Router vty)# show filter index  1 counters    

Filter Counters/Policers:

   Index               Packets                 Bytes  Name

--------  --------------------  --------------------  --------

       1                     0                         POLICER-10M-ACCEPT-FTP

       1                     0               POLICER-1M-ACCEPT-TRACEROUTE-UDP

       1                     0                POLICER-2M-ACCEPT-ICMP-EXTERNAL

       1                     0                          POLICER-2M-ACCEPT-SSH

       1                     0                POLICER-3M-ACCEPT-ICMP-INTERNAL

SMPC0(NIX-Router vty)# exit

admin-full@NIX-Router> show route 218.92.150.130 |no-more

admin-full@NIX-Router> show route 129.211.94.30 |no-more

admin-full@NIX-Router> show route 81.70.57.192 |no-more

admin-full@NIX-Router> show route 129.211.119.145 |no-more

admin-full@NIX-Router> show route 49.234.109.61 |no-more

admin-full@NIX-Router> show route 186.188.80.244 |no-more

admin-full@NIX-Router> show route 220.179.5.252 |no-more

admin-full@NIX-Router> show route 104.236.35.211 |no-more

admin-full@NIX-Router> show route 106.75.251.140 |no-more

admin-full@NIX-Router> show route 159.203.119.1 |no-more

admin-full@NIX-Router> show route 189.113.131.44 |no-more

admin-full@NIX-Router> show route 61.177.173.17 |no-more

admin-full@NIX-Router> show route 218.92.150.130 logical-system vsys-bgp-nix | no-more

inet.0: 16315 destinations, 39858 routes (16315 active, 0 holddown, 0 hidden)

+ = Active Route, - = Last Active, * = Both

0.0.0.0/0          *[BGP/170] 00:34:52, localpref 250, from 192.168.1.1

                      AS path: 45543 I, validation-state: unverified

                    >  to 103.152.49.1 via xe-0/1/0.0

                    [BGP/170] 00:35:41, localpref 100

                      AS path: 18403 I, validation-state: unverified

                    >  to 42.114.208.69 via xe-0/1/6.0

                    [BGP/170] 00:34:57, localpref 100

                      AS path: 45903 I, validation-state: unverified

                    >  to 119.82.139.233 via xe-0/1/5.0

admin-full@NIX-Router>
