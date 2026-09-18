# JunOS-EVO evo-pfemand

```text
admin@HCM-BRAS-PE-01-01> start shell
```

Nov 15 00:14:40

```text
[vrf:none] admin@HCM-BRAS-PE-01-01:~$ journalctl -t evo-pfemand -b | egrep error -i
```

- ---

```text
show interfaces ae2.1003 extensive
```

start shell user root

vty fpc0 // start shell pfe network fpc0

```text
show ifbds
```

```text
show l2 manager bridge-domains
```

```text
show ifbd ifl-index 1052 bd-index 22
```

```text
show evo-pfemand ifl index 1053
```

- ---

```text
show log messages | no-more
```

```text
request support information | no-more
```

```text
request support information | save /var/tmp/RSI\_BDG-AggPE-01-02\_20231220.log
```

```text
file archive compress exclude \*traces\* source /var/log/ destination /var/tmp/varlog-archive\_BDG-AggPE-01-02\_20231220.tgz
```

chvrf iri ssh fpc0

journalctl -b

journalctl -b0 --no-pager

journalctl -f

vssh fpc

```text
cat /var/log/picd.log
```

start shell pfe network fpc0

```text
show syslog
```

- ---

```text
show trace application hwdre | no-more
```

```text
show trace application picd | no-more
```

```text
show trace application lacpd | no-more
```

```text
show trace application evo-pfemand | no-more
```

```text
show trace application alarmd | no-more
```

```text
show trace application alarm-mgmtd | no-more
```

```text
show trace application bfddagent | no-more
```

```text
show trace application cosd | no-more
```

```text
show trace application ddosd | no-more
```

```text
show trace application ppmdagent | no-more
```

```text
show trace application ifmand | no-more
```

```text
show trace application rpdagent | no-more
```

```text
show trace application mgd | no-more
```

start shell

[vrf:none] root@jlab:~#  journalctl -b0 --no-pager

- --

```text
Configure the right supported fec mode for the pic.
```

To find the supported fec modes for a pic , use the following pfe shell command

* PFE Shell cmd : show picd optics fpc\_slot <> pic\_slot <> port <> cmd dump\_devdb\_info*

* labroot@JTAC-ACX1:pfe> show picd optics fpc\_slot 0 pic\_slot 0 port 0 cmd dump\_devdb\_info*

* PICD optics dump\_devdb\_info*

* xcvr-0/0/0*

* xcvr\_type             : 231*

* xcvr\_name             : XCVR\_QSFP28\_100GBASE\_LR4\_T2*

* optics\_type           : lr4*

* ct\_name               : 100GBASE LR4 T2*

* sfp\_name              : QSFP-100GBASE-LR4-T2*

* fiber\_mode            : SM*

* Supported Multi Speed FEC modes*

* Speed\_100G      = none*

* Speed\_25G       = fec91 fec74*

* Speed\_50G       = fec91 fec74*

* --------------------------------------------*

```text
Step#2 : In the error reported pic check link history using the following FPC shell command.
```

FPC shell cmd:  show picd link-history fpc 0 pic  0 port 53 chan 0

* 1  2024-01-04 10:46:45.519640  Xcvr Rx OK change (1 -> 0)*

* 2  2024-01-04 10:46:45.221565  Mac RF Tx set*

* 3  2024-01-04 10:46:45.216809  Xcvr Rx alarm set*

* 4  2024-01-04 10:46:43.516870  Xcvr Rx OK change (0 -> 1)*

* 5  2024-01-04 10:46:43.222949  Mac RF Tx set*

* 6  2024-01-04 10:46:43.218524  Xcvr Rx alarm clear*

* 7  2024-01-04 10:46:41.517393  Xcvr Rx OK change (1 -> 0)*

* 8  2024-01-04 10:46:41.222302  Mac RF Tx set*

* 9  2024-01-04 10:46:41.217295  Xcvr Rx alarm set*

* ---*

```text
You may see firewall filters/terms failed install messages in the logs.
```

```text
evo-pfemand[8502]: [Error] BrcmPlusDfw: Stat-id: 154 and policer-id: 153 are not equal for StatAndPolicer
```

```text
evo-pfemand[8502]: [Error] BrcmPlusPfe: Dfw: fp action add Counter failed , ret = Internal error
```

```text
evo-pfemand[8502]: [Error] BrcmPlusPfe: hwInstallDfwRule failed., ret = Internal error
```

```text
evo-pfemand[8502]: [Error] Dfw: Failed to install rules for term  in hardware
```

```text
evo-pfemand[8502]: [Error] Dfw: Failed to install Term
```

```text
evo-pfemand[8502]: [Error] Dfw: Failed to install in hw for filter
```

```text
evo-pfemand[8502]: [Error] Dfw: Failed to install filter bind
```

```text
evo-pfemand[8502]: [Error] Dfw:  IFF Bind Failed for Ifl-Index:1030 Proto:2 flavor:1 Direction:0
```

2. If there are firewall filter counters configurations, the counters are not working as expected, and they will be displayed as all 0s.

```text
> show firewall
```

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

```text
TRACEROUTE-POLICER-lo0.0-i                                                          0                    0
```

3. From the PFE, the firewall filter is not installed.

pfe> show evo-pfemand filter

Filter-Name                              Filter-index  Installed

ROUTER-PROTECT-lo0.0-i                    48106          No

\_\_ArpIrbTrap0\_unit0\_\_                    4294901813    Yes

<...>

4. Non-working configuration example.

```text
set firewall policer ICMP-POLICER filter-specific
```

```text
set firewall policer ICMP-POLICER if-exceeding bandwidth-limit 10m
```

```text
set firewall policer ICMP-POLICER if-exceeding burst-size-limit 625k
```

```text
set firewall policer ICMP-POLICER then discard
```

```text
*Solution**"filter-specific" knob is not supported in firewall policer configuration on the ACX EVO platforms.
```

Please remove the configuration from the firewall policers.

# delete firewall policer  filter-specific

After removing the knob, the firewall filters are working good.

1. From the log messages, firewall fiilters/terms are bound.

evo-pfemand[8502]: [Info] Dfw: Eal FOH\_I OnAdd called

```text
evo-pfemand[8502]: [Info] Dfw: Filter Bind-IFF received from BQ
```

evo-pfemand[8502]: [Info] Dfw: Processing IFF filter-bind for Ifl-Index:1030 Proto:2 flavor:1 Direction:0 for chain/filter-index:48106

evo-pfemand[8502]: [Info] BrcmPlusDfw: Created group IN-IFF-INET-Lo0 in unit 0 in stage IPMF1 Hw-Id: 50

evo-pfemand[8502]: [Info] Dfw: Filter Bind success for filter:  (Type: LO0, Prot: 2, Ctx: 150)

2. Firewall filter counters start working.

Filter: ROUTER-PROTECT-lo0.0-i

Counters:

Name                                                                            Bytes              Packets

ACCEPT-INTERNAL-ICMP-lo0.0-i                                                  268158                2629

ACCEPT-TCP-ESTABLISHED-lo0.0-i                                                      0                    0

BFD-ACCEPT-lo0.0-i                                                                  0                    0

BGP-ACCEPT-lo0.0-i                                                                  0                    0

<...>

Policers:

Name                                                                            Bytes              Packets

ICMP-POLICER-lo0.0-i                                                                0                    0

INTERNAL-UNKNOWN-TRAFFIC-POLICER-lo0.0-i                                            0                    0

```text
TRACEROUTE-POLICER-lo0.0-i                                                          0                    0
```

3. From the PFE, the firewall filter is installed now.

pfe> show evo-pfemand filter

Filter-Name                              Filter-index  Installed

ROUTER-PROTECT-lo0.0-i                    48106          Yes

\_\_ArpIrbTrap0\_unit0\_\_                    4294901813    Yes

<...>
