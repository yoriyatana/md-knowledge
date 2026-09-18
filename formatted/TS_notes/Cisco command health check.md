# Cisco command health check

Config loggging

|  |
| --- |
| logging buffered 262144 debugging |
| logging file flash:logtmp.txt 1048576 debugging |
| service timestamps debug datetime localtime |
| service timestamps log datetime localtime |

- --

#### Basic health check

### Check General info

```text
show processes cpu sorted
```

```text
show hardware
```

```text
show inventory
```

```text
show lldp neighbors
```

```text
show lldp interface
```

```text
show spanning-tree
```

```text
show vlan
```

```text
show mac address-table
```

```text
show arp
```

### Check port status

```text
show interface status
```

```text
show ip interface brief
```

```text
show interface summary
```

```text
show interface
```

sho int transceiver detail

### General

```text
show ip protocols
```

```text
show ip route summary
```

```text
show snmp group
```

```text
show snmp view
```

```text
show snmp community
```

### OSPF

```text
show ip ospf neighbor
```

```text
show ip ospf interface
```

```text
show ip ospf database self-originate
```

```text
show ip ospf statistics
```

```text
show ip ospf traffic
```

```text
show ip ospf rib
```

```text
show ip route ospf
```

### End

terminal length 24

exit

- -

### Check stacked status

sh swi

```text
show stackwise-virtual
```

```text
show stackwise-virtual dual-active-detection
```

```text
show switch
```

```text
show redundancy switchover
```

```text
show boot
```

```text
show version
```

```text
show redundancy
```

- --

* *If the active goes down and comes back up, do we preempt? Aka switch old-active back to active role?**

The answer is No.

NDNA-Switch\_Switch-9300-1#sh switch stack-mode

```text
Switch#  Role    Mac Address     Version   Mode  Configured  State
```

- ----------------------------------------------------------------------------------------

1      Member   706b.b929.f700    V01     1+1     Active     Ready

\*2      Active   cc98.911a.0500    V01     1+1     Standby    Ready

3      Member   cc98.911a.c380    V01     1+1     Member     Ready

NDNA-Switch\_Switch-9300-1#

\*Jun 10 11:39:38.046: %STACKMGR-6-STANDBY\_ELECTED: Switch 2 R0/0: stack\_mgr:  Switch 1 has been elected STANDBY.

\*Jun 10 19 11:39:38.047: %IOSXE\_REDUNDANCY-6-PEER: Active detected switch 1 as standby.

\*Jun 10 11:40:03.060: %REDUNDANCY-5-PEER\_MONITOR\_EVENT: Active detected a standby insertion (raw-event=PEER\_FOUND(4))

\*Jun 10 11:40:03.060: %REDUNDANCY-5-PEER\_MONITOR\_EVENT: Active detected a standby insertion (raw-event=PEER\_REDUNDANCY\_STATE\_CHANG

\*Jun 10 11:40:43.060: %HA\_CONFIG\_SYNC-6-BULK\_CFGSYNC\_SUCCEED: Bulk Sync succeeded

```text
\*Jun 10 11:40:53.060: %RF-5-RF\_TERMINAL\_STATE: Terminal state reached for (SSO)
```

NDNA-Switch\_Switch-9300-1#sh switch stack-mode

```text
Switch# Role Mac Address Version Mode Configured State
```

- ------------------------------------------------------------------------

1 Standby 706b.b929.f700 V01 1+1 Active Ready

\*2 Active cc98.911a.0500 V01 1+1 Standby Ready

3 Member cc98.911a.c380 V01 1+1 Member Ready
