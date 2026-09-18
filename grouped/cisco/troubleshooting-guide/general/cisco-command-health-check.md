# Cisco Command Health Check

## Source: `formatted/TS_notes/Cisco command health check.md`

### Config loggging

```cisco
logging buffered 262144 debugging 
logging file flash:logtmp.txt 1048576 debugging 
service timestamps debug datetime localtime 
service timestamps log datetime localtime 
```

### Basic health check

#### Check General info

```cisco
show processes cpu sorted
show hardware
show inventory
show lldp neighbors
show lldp interface
show spanning-tree
show vlan
show mac address-table
show arp
```
#### Check port status

```cisco
show interface status
show ip interface brief
show interface summary
show interface
show int transceiver detail
```
#### General

```cisco
show ip protocols
show ip route summary
show snmp group
show snmp view
show snmp community
```
#### OSPF

```cisco
show ip ospf neighbor
show ip ospf interface
show ip ospf database self-originate
show ip ospf statistics
show ip ospf traffic
show ip ospf rib
show ip route ospf
```
#### End

```cisco
terminal length 24
exit
```

#### Check stacked status

```cisco
sh swi
show stackwise-virtual
show stackwise-virtual dual-active-detection
show switch
show redundancy switchover
show boot
show version
show redundancy
```

---
**If the active goes down and comes back up, do we preempt? Aka switch old-active back to active role?**

The answer is **No**.
```cisco
NDNA-Switch_Switch-9300-1#sh switch stack-mode 
Switch#  Role    Mac Address     Version   Mode  Configured  State 
-----------------------------------------------------------------------------------------
 1      Member   706b.b929.f700    V01     1+1     Active     Ready     
*2      Active   cc98.911a.0500    V01     1+1     Standby    Ready     
 3      Member   cc98.911a.c380    V01     1+1     Member     Ready 


NDNA-Switch_Switch-9300-1#
*Jun 10 11:39:38.046: %STACKMGR-6-STANDBY_ELECTED: Switch 2 R0/0: stack_mgr:  Switch 1 has been elected STANDBY. 
*Jun 10 19 11:39:38.047: %IOSXE_REDUNDANCY-6-PEER: Active detected switch 1 as standby.
*Jun 10 11:40:03.060: %REDUNDANCY-5-PEER_MONITOR_EVENT: Active detected a standby insertion (raw-event=PEER_FOUND(4))

*Jun 10 11:40:03.060: %REDUNDANCY-5-PEER_MONITOR_EVENT: Active detected a standby insertion (raw-event=PEER_REDUNDANCY_STATE_CHANG
*Jun 10 11:40:43.060: %HA_CONFIG_SYNC-6-BULK_CFGSYNC_SUCCEED: Bulk Sync succeeded
*Jun 10 11:40:53.060: %RF-5-RF_TERMINAL_STATE: Terminal state reached for (SSO)

NDNA-Switch_Switch-9300-1#sh switch stack-mode 
Switch# Role Mac Address Version Mode Configured State 
-------------------------------------------------------------------------
 1 Standby 706b.b929.f700 V01 1+1 Active Ready 
*2 Active cc98.911a.0500 V01 1+1 Standby Ready 
 3 Member cc98.911a.c380 V01 1+1 Member Ready
```
