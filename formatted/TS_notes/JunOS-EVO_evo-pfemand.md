# JunOS-EVO evo-pfemand

admin@HCM-BRAS-PE-01-01> start shell

Nov 15 00:14:40

[vrf:none] admin@HCM-BRAS-PE-01-01:~$ journalctl -t evo-pfemand -b | egrep error -i

- ---

show interfaces ae2.1003 extensive

start shell user root

vty fpc0 // start shell pfe network fpc0

show ifbds

show l2 manager bridge-domains

show ifbd ifl-index 1052 bd-index 22

show evo-pfemand ifl index 1053

- ---

show log messages | no-more

request support information | no-more

request support information | save /var/tmp/RSI_BDG-AggPE-01-02_20231220.log

file archive compress exclude *traces* source /var/log/ destination /var/tmp/varlog-archive_BDG-AggPE-01-02_20231220.tgz

chvrf iri ssh fpc0

journalctl -b

journalctl -b0 --no-pager

journalctl -f

vssh fpc

cat /var/log/picd.log

start shell pfe network fpc0

show syslog

- ---

show trace application hwdre | no-more

show trace application picd | no-more

show trace application lacpd | no-more

show trace application evo-pfemand | no-more

show trace application alarmd | no-more

show trace application alarm-mgmtd | no-more

show trace application bfddagent | no-more

show trace application cosd | no-more

show trace application ddosd | no-more

show trace application ppmdagent | no-more

show trace application ifmand | no-more

show trace application rpdagent | no-more

show trace application mgd | no-more

start shell

[vrf:none] root@jlab:~#  journalctl -b0 --no-pager

- --

Configure the right supported fec mode for the pic.

To find the supported fec modes for a pic , use the following pfe shell command

_PFE Shell cmd : show picd optics fpc_slot <> pic_slot <> port <> cmd dump_devdb_info_

_labroot@JTAC-ACX1:pfe> show picd optics fpc_slot 0 pic_slot 0 port 0 cmd dump_devdb_info�_�

_  PICD optics dump_devdb_info_

_  xcvr-0/0/0_

_  xcvr_type             : 231_

_  xcvr_name             : XCVR_QSFP28_100GBASE_LR4_T2_

_  optics_type           : lr4_

_  ct_name               : 100GBASE LR4 T2_

_  sfp_name              : QSFP-100GBASE-LR4-T2_

_  fiber_mode            : SM_

_  Supported Multi Speed FEC modes_

_        Speed_100G      = none_

_        Speed_25G       = fec91 fec74_

_        Speed_50G       = fec91 fec74�_�

_--------------------------------------------_

Step#2 : In the error reported pic check link history using the following FPC shell command.

FPC shell cmd:  show picd link-history fpc 0 pic  0 port 53 chan 0

_  1  2024-01-04 10:46:45.519640  Xcvr Rx OK change (1 -> 0)_

_  2  2024-01-04 10:46:45.221565  Mac RF Tx set_

_  3  2024-01-04 10:46:45.216809  Xcvr Rx alarm set_

_  4  2024-01-04 10:46:43.516870  Xcvr Rx OK change (0 -> 1)_

_  5  2024-01-04 10:46:43.222949  Mac RF Tx set_

_  6  2024-01-04 10:46:43.218524  Xcvr Rx alarm clear_

_  7  2024-01-04 10:46:41.517393  Xcvr Rx OK change (1 -> 0)_

_  8  2024-01-04 10:46:41.222302  Mac RF Tx set_

_  9  2024-01-04 10:46:41.217295  Xcvr Rx alarm set_

_---_

1. You may see firewall filters/terms failed install messages in the logs.

```
evo-pfemand[8502]: [Error] BrcmPlusDfw: Stat-id: 154 and policer-id: 153 are not equal for StatAndPolicer
evo-pfemand[8502]: [Error] BrcmPlusPfe: Dfw: fp action add Counter failed , ret = Internal error
evo-pfemand[8502]: [Error] BrcmPlusPfe: hwInstallDfwRule failed., ret = Internal error
evo-pfemand[8502]: [Error] Dfw: Failed to install rules for term <term name> in hardware
evo-pfemand[8502]: [Error] Dfw: Failed to install Term <term name>
evo-pfemand[8502]: [Error] Dfw: Failed to install in hw for filter <filter name>
evo-pfemand[8502]: [Error] Dfw: Failed to install filter bind
evo-pfemand[8502]: [Error] Dfw:  IFF Bind Failed for Ifl-Index:1030 Proto:2 flavor:1 Direction:0
```

2. If there are firewall filter counters configurations, the counters are not working as expected, and they will be displayed as all 0s.

```
> show firewall
Filter: ROUTER-PROTECT-lo0.0-i
Counters:
Name                                                                            Bytes              Packets
ACCEPT-INTERNAL-ICMP-lo0.0-i                                                        0                    0
ACCEPT-TCP-ESTABLISHED-lo0.0-i                                                      0                    0
BFD-ACCEPT-lo0.0-i                                                                  0                    0
BGP-ACCEPT-lo0.0-i                                                                  0                    0
<...>
Policers:
Name                                                                            Bytes              Packets
ICMP-POLICER-lo0.0-i                                                                0                    0
INTERNAL-UNKNOWN-TRAFFIC-POLICER-lo0.0-i                                            0                    0
TRACEROUTE-POLICER-lo0.0-i                                                          0                    0
```

3. From the PFE, the firewall filter is not installed.

```
pfe> show evo-pfemand filter
Filter-Name                               Filter-index   Installed
ROUTER-PROTECT-lo0.0-i                    48106          No
__ArpIrbTrap0_unit0__                     4294901813     Yes
<...>

```

4. Non-working configuration example.

```
set firewall policer ICMP-POLICER filter-specific
set firewall policer ICMP-POLICER if-exceeding bandwidth-limit 10m
set firewall policer ICMP-POLICER if-exceeding burst-size-limit 625k
set firewall policer ICMP-POLICER then discard
```

* *Solution**"filter-specific" knob is not supported in firewall policer configuration on the ACX EVO platforms.

Please remove the configuration from the firewall policers.

                # delete firewall policer <policer name> filter-specific

After removing the knob, the firewall filters are working good.

1. From the log messages, firewall fiilters/terms are bound.

```
evo-pfemand[8502]: [Info] Dfw: Eal FOH_I OnAdd called
evo-pfemand[8502]: [Info] Dfw: Filter Bind-IFF received from BQ
evo-pfemand[8502]: [Info] Dfw: Processing IFF filter-bind for Ifl-Index:1030 Proto:2 flavor:1 Direction:0 for chain/filter-index:48106
evo-pfemand[8502]: [Info] BrcmPlusDfw: Created group IN-IFF-INET-Lo0 in unit 0 in stage IPMF1 Hw-Id: 50
evo-pfemand[8502]: [Info] Dfw: Filter Bind success for filter: <filter name> (Type: LO0, Prot: 2, Ctx: 150)
```

2. Firewall filter counters start working.

```
Filter: ROUTER-PROTECT-lo0.0-i
Counters:
Name                                                                            Bytes              Packets
ACCEPT-INTERNAL-ICMP-lo0.0-i                                                   268158                 2629
ACCEPT-TCP-ESTABLISHED-lo0.0-i                                                      0                    0
BFD-ACCEPT-lo0.0-i                                                                  0                    0
BGP-ACCEPT-lo0.0-i                                                                  0                    0
<...>

```

```
Policers:
Name                                                                            Bytes              Packets
ICMP-POLICER-lo0.0-i                                                                0                    0
INTERNAL-UNKNOWN-TRAFFIC-POLICER-lo0.0-i                                            0                    0
TRACEROUTE-POLICER-lo0.0-i                                                          0                    0

```

3. From the PFE, the firewall filter is installed now.

```
pfe> show evo-pfemand filter
Filter-Name                               Filter-index   Installed
ROUTER-PROTECT-lo0.0-i                    48106          Yes
__ArpIrbTrap0_unit0__                     4294901813     Yes
<...>
```
