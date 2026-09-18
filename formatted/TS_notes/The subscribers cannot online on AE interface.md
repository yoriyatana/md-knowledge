# The subscribers cannot online on AE interface

The problem is caused by a flag in bbe-smgd, where the control interface xe-4/0/0.32767 is showing as down. We checked all other interfaces in the ae80 and ae82 lags, and only interface xe-4/0/0 is affected. We believe this may have been triggered when the interface flapped:

hoanganh@CBG-PE1-MX2008\_RE0> **show interfaces xe-4/0/0 extensive**

Physical interface: xe-4/0/0, Enabled, Physical link is Up

Interface index: 245, SNMP ifIndex: 1303, Generation: 318

```text
Description: 10G-CBG-PE1-4/0/0:CBG00TTM-2/2/2:06-Downlink-BNG
```

```text
Link-level type: Flexible-Ethernet, MTU: 9192, MRU: 9200, LAN-PHY mode, Speed: 10Gbps, BPDU Error: None, Loop Detect PDU Error: None, MAC-REWRITE Error: None, Loopback: None, Source filtering: Disabled, Flow control: Disabled,
```

Speed Configuration: Auto

Pad to minimum frame size: Disabled

Device flags   : Present Running

Interface flags: SNMP-Traps Internal: 0x4000

CoS queues     : 8 supported, 8 maximum usable queues

Schedulers     : 0

Hold-times     : Up 0 ms, Down 0 ms

```text
Damping        : half-life: 0 sec, max-suppress: 0 sec, reuse: 0, suppress: 0, state: unsuppressed
```

Current address: f6:bf:a8:79:89:97, Hardware address: f4:bf:a8:79:8c:98

* *Last flapped   : 2021-06-26 04:47:39 ICT (5w6d 19:00 ago)**

```text
This problem will cause the PADI to be dropped when a dynamic vlan must be created. As long as the dynamic vlan remains present on ae80, subscribers can establish PPPoE sessions at any time. With this problem, if all subscribers log out of a dynamic vlan, and that dynamic vlan is removed, it will not be recreated.
```

We are working to reproduce the issue in the JTAC lab, and will let you know once we have more information to share

```text
To recover this issue, we need to correct the flag stats in bbe-smgd. Below is what you can expect to see in the problem state and what you should see once ethe issue is corrected.
```

```text
To view the bbe-smgd ifl state, you can use the following command from CLI:
```

* *start shell csh command "vty -c 'show ifl xe-4/0/0.32767' -s 7208 128.0.0.1"**

```text
*Current Problem state:**
```

hoanganh@CBG-PE1-MX2008\_RE0>  **start shell csh command "vty -c 'show ifl xe-4/0/0.32767' -s 7208 128.0.0.1"**

IFL handle:              0x9e2f750

IFL Name:                xe-4/0/0.32767

IFL Type:                RTSOCK

IFL Index:               910

IFL BBE Index:           502231

IFL Seq num:             2292

IFL Gen num:             1551

IFL RefCnt:              1

IFL Nexthop Total:       0

Installed on PFE:        True

```text
*IFL Flags:               0x10800  ß INCORRECT STATE**
```

IFL Local Flags:         0x0

```text
*Correct state:**
```

hoanganh@CBG-PE1-MX2008\_RE0>  **start shell csh command "vty -c 'show ifl xe-4/0/0.32767' -s 7208 128.0.0.1"**

IFL handle:              0x9e2f750

IFL Name:                xe-4/0/0.32767

IFL Type:                RTSOCK

IFL Index:               910

IFL BBE Index:           502231

IFL Seq num:             2292

IFL Gen num:             1551

IFL RefCnt:              1

IFL Nexthop Total:       0

Installed on PFE:        True

```text
*IFL Flags:               0x10000  ß CORRECT STATE**
```

IFL Local Flags:         0x0Detailed IFL Info

* *Suggested Recovery Steps:**

To clear and correct the bbe-smgd ifl flag, we suggest trying the following actions. As we have not reproduced this issue in the JTAC lab yet, we can not be certain which of these steps will correct the problem, so we request that you verify if the flag is corrected after each step. Once you see “IFL Flags: 0x10000”,  then the issue should be solved and the subscribers from vlans 1131 and 514 should be able to establish sessions on ae80 again.

```text
Deactivate / then activate interface **xe-4/0/0**
```

1. Check if flag is corrected

```text
Delete and then re-add interface **xe-4/0/0**
```

1. First, check active subscribers are cleared from xe-4/0/0 in the output of ‘show interfaces targeting ae80’” (it should be from step 1)
2. If not, deactivate interface xe-4/0/0 again and verify all the subscribers are cleared from xe-4/0/0
3. Once cleared, delete interface xe-4/0/0
4. Wait for 2 minutes, then add interface xe-4/0/0 back
5. Check if flag is corrected

```text
Restart bbe-smgd process
```

1. Issue command “restart smg-service” from cli
2. Wait 5 minutes and check if flag is corrected

4. Perform an RE mastership switchover

1. Check if flag is corrected

We believe that one of the above actions will clear the flag and restore normal operations. If not, a system reboot would be required.
