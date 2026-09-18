# pfe local-bias

The following forwarding topologies MUST be supported:

1. Forwarding through Aggregated Ethernet interfaces. Local member links should be preferred over remote ones;

The following topologies SHOULD be supported:

1. ECMP. Local forwarding next-hops should be preferred;

2. ECMP over AE. Local forwarding next-hops should be preferred.

With this feature enabled, local forwarding next-hops should receive higher priority than remote PFE next-hops.

Tính năng này có vẻ phát triển cho anchor-pfe & pwht

—

[ May 24, 2023 12:04 PM ] ⁨SVT.Minh.Nguyễn⁩: @HHT9602.PECD.MX2020.02\_RE0> request pfe execute command "show jnh if 365 aggregate-ifd" target fpc15 | no-more

SENT: Ukern command: show jnh if 365 aggregate-ifd

ae31 (148), IFL's Attached: 1

Statistics:

IFL attach count: 1, IFL detach count: 0, IFL Max count: 1

Selector states created: 9, Selector states deleted: 8

PFE  0: Default link: (hits: 0, loops detected: 0)

PFE  1: Default link: (hits: 0, loops detected: 0)

IFD Selector State [0]:

Ref Count: 1, Child Count: 6, selp:[0] 0x4dd30d00

Symmetric LB: No

Adaptive LB: No, Per Packet LB: No, Local bias percent: 0%

Child [0]: et-7/0/6 (328), orig\_weight: 1, link\_index: 64, state: UP

Child [1]: et-7/0/7 (329), orig\_weight: 1, link\_index: 64, state: UP

Child [2]: et-5/0/0 (332), orig\_weight: 1, link\_index: 64, state: UP

Child [3]: et-5/0/1 (333), orig\_weight: 1, link\_index: 64, state: UP

Child [4]: et-5/1/1 (335), orig\_weight: 1, link\_index: 64, state: UP

Child [5]: et-9/0/1 (656), orig\_weight: 1, link\_index: 64, state: UP

ID:1370249(3), Ref:1, Type:2 (Regular), subtype:0, Symmetric-LB: Off, Target\_id:0

Key:FRR:Y, Balances:N, Locality:N/unicast, Type:LAG-IFD, Size:6, flags:0x4, dist-mode-default

SelPtr:inst0:0x963fc0 inst1:0x982840

PFE  0 [fe: 0] : Default child: et-7/0/6 (non-local)

PFE  0 [fe: 1] : Default child: et-7/0/6 (non-local)

Unilist JNH: 0x20aa1ed00000000c, default link: 0x20aa1ed40000000c

PFE  1 [fe: 0] : Default child: et-7/0/6 (non-local)

PFE  1 [fe: 1] : Default child: et-7/0/6 (non-local)

Unilist JNH: 0x20a3fc1c0000000c, default link: 0x20a3ff040000000c

[ May 24, 2023 12:06 PM ] ⁨SVT.Minh.Nguyễn⁩: @HHT9602.PECD.MX2020.02\_RE0> request pfe execute command "show jnh if 365 aggregate-ifd" target fpc5 | no-more

SENT: Ukern command: show jnh if 365 aggregate-ifd

ae31 (148), IFL's Attached: 1

Statistics:

IFL attach count: 1, IFL detach count: 0, IFL Max count: 1

Selector states created: 9, Selector states deleted: 8

PFE  0: Default link: (hits: 0, loops detected: 0)

PFE  1: Default link: (hits: 0, loops detected: 0)

IFD Selector State [0]:

Ref Count: 1, Child Count: 6, selp:[0] 0x52e05ef8

Symmetric LB: No

Adaptive LB: No, Per Packet LB: No, Local bias percent: 0%

Child [0]: et-7/0/6 (328), orig\_weight: 1, link\_index: 64, state: UP

Child [1]: et-7/0/7 (329), orig\_weight: 1, link\_index: 64, state: UP

Child [2]: et-5/0/0 (332), orig\_weight: 1, link\_index: 64, state: UP

Child [3]: et-5/0/1 (333), orig\_weight: 1, link\_index: 64, state: UP

Child [4]: et-5/1/1 (335), orig\_weight: 1, link\_index: 64, state: UP

Child [5]: et-9/0/1 (656), orig\_weight: 1, link\_index: 64, state: UP

ID:1370252(3), Ref:1, Type:2 (Regular), subtype:0, Symmetric-LB: Off, Target\_id:0

Key:FRR:Y, Balances:N, Locality:N/unicast, Type:LAG-IFD, Size:6, flags:0x4, dist-mode-default

SelPtr:inst0:0x990bc0 inst1:0x9a24c0

PFE  0 [fe: 0] : Default child: et-5/0/0

PFE  0 [fe: 1] : Default child: et-5/0/1

Unilist JNH: 0x20c9d2e40000000c, default link: 0x20c9d0180000000c

PFE  1 [fe: 0] : Default child: et-7/0/6 (non-local)

PFE  1 [fe: 1] : Default child: et-5/1/1

Unilist JNH: 0x20c57f5c0000000c, default link: 0x20c57f080000000c
