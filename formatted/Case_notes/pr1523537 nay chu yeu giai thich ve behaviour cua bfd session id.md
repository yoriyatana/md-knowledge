# pr1523537 nay chu yeu giai thich ve behaviour cua bfd session id

[ June 21, 2023 20:54 ] ⁨Hung Le⁩: 1523537 - unilist nexthop is getting set to 65535 due to session mismatch between Anchor FPC and other peers==> pr nay chu yeu giai thich ve behaviour cua bfd session id

```text
[ June 21, 2023 20:55 ] ⁨Hung Le⁩: When panic is triggered on anchor fpc(or reboot), down event is sent to non-anchor fpcs. Non-anchor fpcs set the pfe bfd session state to "down". When anchor fpc comes up, as part of pfe bfd session obj creation, session status is set to "up" locally. Ppman sends "bfd up" event to pfeman. But it is ignored as the status is already up(set by pfeman as part of init, done to avoid unwanted processing). So pfeman does not send session "up" event to other fpcs. Due to this session status remains down at non-anchor fpc even though bfd session is up.
```

[ June 21, 2023 20:55 ] ⁨Hung Le⁩: viec keep session id cua bfd la do phat trien tinh nang bfd session dc frr qua lsp

[ June 21, 2023 20:56 ] ⁨Hung Le⁩: khi phat trien rli cho tinh nang nay thi bfd frr default lun duoc enable

[ June 21, 2023 20:57 ] ⁨Hung Le⁩: do đó viec bfd ở pfe anchor down nhung ppm adj cho bfd đó vẫn giữ session

[ June 21, 2023 20:58 ] ⁨Hung Le⁩: từ đó dẫn đến mismatch thông tin nhdb cua PR 1568879

[ June 21, 2023 20:58 ] ⁨Hung Le⁩: sau đây la 1 ví dụ để ae hình dung tại sao có flow chết có flow không chết do bfd này

[ June 21, 2023 20:59 ] ⁨Hung Le⁩: ======working====ipv4

[ June 21, 2023 20:59 ] ⁨Hung Le⁩: show nhdb id 1048578 extensive

ID      Type      Interface    Next Hop Addr    Protocol       Encap     MTU               Flags  PFE internal Flags

- ----  --------  -------------  ---------------  ----------  ------------  ----  ------------------  ------------------

1048578   Unilist  ae55.0         -                      IPv4      Ethernet     0  0x0000000000000000  0x0000000000000000

<...>

ECMP : YES

614   Unicast  ae55.0         -                IPv4->MPLS      Ethernet  9178  0x0000000000000005  0x0000002000000002

607   Unicast  ae56.0         -                IPv4->MPLS      Ethernet  9178  0x0000000000000005  0x0000002000000002

[ June 21, 2023 21:01 ] ⁨Hung Le⁩: ===non working====

RMPC1(DIS01.LD5-RE0 vty)# show nhdb id 1048585 extensive

ID      Type      Interface    Next Hop Addr    Protocol       Encap     MTU               Flags  PFE internal Flags

- ----  --------  -------------  ---------------  ----------  ------------  ----  ------------------  ------------------

1048585   Unilist  ae55.0         -                      IPv4      Ethernet     0  0x0000000000000000  0x0000000000000000

<...>

ECMP : YES

621   Unicast  ae55.0         -                 CCC->MPLS      Ethernet  9178  0x0000000000000005  0x0000002000000012

622   Unicast  ae56.0         -                 CCC->MPLS      Ethernet  9178  0x0000000000000005  0x0000002000000012

[ June 21, 2023 21:01 ] ⁨Hung Le⁩: kq nay ta thay mac du unicast list cuoi cung đều đc réolve qua ae55.0

[ June 21, 2023 21:01 ] ⁨Hung Le⁩: tuy nhien nh id cho ecmp của 2 services này khác nhau

[ June 21, 2023 21:03 ] ⁨Hung Le⁩: ====bfdsesion ban dau====

[labroot@DIS01.LD](mailto:labroot@DIS01.LD)5-RE0> show bfd session address 81.201.103.92 extensive

Detect   Transmit

```text
Address                  State     Interface      Time     Interval  Multiplier
```

81. 201.103.92            Up        ae55.0         0.150     0.050        3

Client OSPF realm ospf-v2 Area 0.0.0.0, TX interval 0.050, RX interval 0.050

Session up time 00:57:05

Local diagnostic None, remote diagnostic None

```text
Remote state Up, version 1
```

Session type: Single hop BFD

Min async interval 0.050, min slow interval 1.000

Adaptive async TX interval 0.050, RX interval 0.050

Local min TX interval 0.050, minimum RX interval 0.050, multiplier 3

Remote min TX interval 0.050, min RX interval 0.050, multiplier 3

Local discriminator 21, remote discriminator 361

Echo mode disabled/inactive

Remote is control-plane independent

Session ID: 0x140 ======================>320

RMPC0(DIS01.LD5-RE0 vty)# show pfe bfd id 320 extensive

- ------------------ =====> lets check 320

SESSION ID: 320

- ------------------

Session Status : UP

Session Version : 0xfffffffe

NHID list : 632 629 627 626 625 624

622 621 619 613

===>moi nguoi nhin thay nhid list o day 614 va 607 cua truong hop working đã được release ra khoi session bfd nay

622 va 621 van bi giu lai

[ June 21, 2023 21:04 ] ⁨Hung Le⁩: do đó dẫn đới mismatch giữa control plane và data plane

[ June 21, 2023 21:07 ] ⁨SVT.Khương.TQ⁩: Dạ em cảm ơn anh Hưng. Để em đọc và suy ngẫm thêm ạ.

[ June 21, 2023 21:07 ] ⁨Hung Le⁩: pr nay phải chpwf phát triển 1 tính năng mới ở 21.4R thi moi thay đổi behaviour này được

[ June 21, 2023 21:08 ] ⁨Hung Le⁩: do đó để hạn chế lỗi phải WA bằng cách set routing-options no-bfd-triggered-local-repair

[ June 21, 2023 21:08 ] ⁨Hung Le⁩: để session id sẽ ko giữ lại phiên với nh đầu tiên mà bfd up

[ June 21, 2023 21:13 ] ⁨Hung Le⁩: 1 cai wa nữa là dung micro bfd cung ko bi

[ June 21, 2023 21:13 ] ⁨Hung Le⁩: clarification from Engineering, remove BFD/OSPF just keep AE BFD (microBFD) will not trigger  “persistent” traffic black holing issue.

[ June 21, 2023 21:13 ] ⁨Hung Le⁩: vi micro bfd ko co tinh nang local-repair nhu bfd inline

[ June 21, 2023 21:14 ] ⁨Hung Le⁩: Just checked 21.4R1 would had the fix of the issue:

<https://www.juniper.net/documentation/us/en/software/junos/release-notes/21.4/junos-release-notes-21.4r1/junos-release-notes-21.4r1.pdf>

######

Enhancements to BFD-triggered FRR for unicast next hops and forwarding-table session-id-changelimiter-indirect to address issue of |r-Lc being silently discarded (MX150, MX204, MX240, MX304, MX480, MX960, MX2008, MX2010, MX2020, MX10003, MX10008, MX10016, PTX1000,PTX3000, PTX5000, PTX10001, PTX10002, PTX10016, QFX10002-60C, QFX10002, QFX10008, QFX10016, and vMX)—In Junos OS Release 21.4R1, we've enhanced the BFD-triggered fast reroute (FRR) for unicast next hops and forwarding-table session-id-change-limiter-indirect to address the issue of |r-Lc being silently discarded because of a session mismatch between the control plane and data plane. To align the |r-Lc by cr;-ঞn] session-id-change-limiter indirect next hop, set the set routing-options forwarding-table session-id-change-limiter-indirect conC]†r-ঞon statement at the [edit routing-options forwarding-table] hierarchy level.

[ June 21, 2023 21:14 ] ⁨Hung Le⁩: còn đây là thông tin mà 21.4 sẽ thay đổi

[ June 21, 2023 21:15 ] ⁨Hung Le⁩: có 1 case của kh tương tự như CMC: jtac cũng tách thành 2 lỗi

[ June 21, 2023 21:15 ] ⁨Hung Le⁩: 1 RMA FPC

[ June 21, 2023 21:15 ] ⁨Hung Le⁩: 2 la nói về PR này

[ June 21, 2023 21:16 ] ⁨Hung Le⁩: Thanks TA đã cung cấp PR

[ June 21, 2023 21:34 ] ⁨SVT.Anh.VT⁩: PR này 2 tuần trc em có view mà lúc đó đọc ko kĩ anh ạ, em thấy bfd with ae (em tưởng micro bfd) với cái wa ko liên quan đến tính năng kh đang chạy. Nên bỏ qua :D

[ June 21, 2023 21:36 ] ⁨SVT.Anh.VT⁩: Thanks thông tin của anh Hưng nhé, để bọn em đọc kĩ xem anh nhé. Chỗ micro bfd + bỏ protocol bfd anh em cũng có trong plan khuyến nghị rồi anh ạ.

[ June 21, 2023 21:37 ] ⁨Hung Le⁩: Micro bfd m dễ bị vướn chỗ interop

[ June 21, 2023 21:37 ] ⁨Hung Le⁩: Nếu jnpr ko thì ok

[ June 21, 2023 21:37 ] ⁨Hung Le⁩: A nhớ mấy lần interop cisco và hw toàn bỏ đi

[ June 21, 2023 21:37 ] ⁨SVT.Anh.VT⁩: Dạ, cái box này của CMC thì OK, còn mấy box khác thì cần xem anh ạ.

[ June 21, 2023 21:38 ] ⁨Hung Le⁩: Isp nhỏ hay dùng nhiều vendor

[ June 21, 2023 21:39 ] ⁨SVT.Khương.TQ⁩: Nếu ko qua truyền dẫn hoặc sw thì có thể bỏ qua BFD được ko anh?

[ June 21, 2023 21:39 ] ⁨Hung Le⁩: Đc

[ June 21, 2023 21:39 ] ⁨Hung Le⁩: Cái này a nhớ hồi làm mane hcm có nói

[ June 21, 2023 21:40 ] ⁨Hung Le⁩: Dùng bfd là do ko đấu trực tiếp

[ June 21, 2023 21:43 ] ⁨Hung Le⁩: Coi như giờ case cmc cũng có hướng sáng

[ June 21, 2023 21:43 ] ⁨Hung Le⁩: Ngủ ngon đêm nay

```text
>>>>>>>>>>>>>>>>>>>>>>>
```

[ June 21, 2023 20:36 ] ⁨Hung Le⁩: If FPC0 PFE0 has the AE membership port, FPC1 also has the AE membership port:

- PFE0 disabe can cause max weight on both FPCs.

- FPC0 reboot will make the anchor FPC switch to FPC1, and BFD session ID on FPC1 will change to a new ID. FPC1 nh weight will move back to 1.

- Problem can be resovled by FPC0 reboot.

If FPC0 PFE0 doesn't have the AE membership port, and FPC1 also has the AE membership port:

```text
PFE0 disable will \*not\* cause the max weight issue, even the BFD remains in Down state and BFD session ID remains in Down state on FPC.
```

- Issue is not seen in this scenario - I can't explain the reason.

If FPC0 PFE0 doesn't have the AE membership port, and FPC0 PFEx have the membership port:

- PFE0 disabe can cause max weight on both FPCs.

- FPC0 reboot will \*not\* make the anchor FPC switch to FPC1, but the BFD session ID on FPC1 will remain. Hence max weight on FPC1 will also remain.

- Problem can be resolved by restarting all FPCs....

[ June 21, 2023 21:20 ] ⁨Hung Le⁩: từ đó dẫn đến mismatch thông tin nhdb cua PR 1568879

[ June 21, 2023 21:20 ] ⁨Hung Le⁩: Khả năng phải xem xét vì mô hình triển khai của mình lqf bfd ospf hoặc bfd isis

[ June 21, 2023 21:54 ] ⁨SVT.Hoà.Nguyễn⁩: cái PR này ko thấy bản fix anh nhỉ ?

[ June 21, 2023 21:55 ] ⁨Hung Le⁩: Xem như là behaviour đến khi 21.4r1 ra đời

[ June 21, 2023 21:55 ] ⁨Hung Le⁩: Just checked 21.4R1 would had the fix of the issue:

<https://www.juniper.net/documentation/us/en/software/junos/release-notes/21.4/junos-release-notes-21.4r1/junos-release-notes-21.4r1.pdf>

######

Enhancements to BFD-triggered FRR for unicast next hops and forwarding-table session-id-changelimiter-indirect to address issue of |r-Lc being silently discarded (MX150, MX204, MX240, MX304, MX480, MX960, MX2008, MX2010, MX2020, MX10003, MX10008, MX10016, PTX1000,PTX3000, PTX5000, PTX10001, PTX10002, PTX10016, QFX10002-60C, QFX10002, QFX10008, QFX10016, and vMX)—In Junos OS Release 21.4R1, we've enhanced the BFD-triggered fast reroute (FRR) for unicast next hops and forwarding-table session-id-change-limiter-indirect to address the issue of |r-Lc being silently discarded because of a session mismatch between the control plane and data plane. To align the |r-Lc by cr;-ঞn] session-id-change-limiter indirect next hop, set the set routing-options forwarding-table session-id-change-limiter-indirect conC]†r-ঞon statement at the [edit routing-options forwarding-table] hierarchy level.

[ June 21, 2023 21:56 ] ⁨SVT.Hoà.Nguyễn⁩: vâng anh

[ June 21, 2023 21:56 ] ⁨SVT.Hoà.Nguyễn⁩: để tụi em xem thêm

[ June 21, 2023 21:56 ] ⁨Hung Le⁩: do đó để hạn chế lỗi phải WA bằng cách set routing-options no-bfd-triggered-local-repair

[ June 21, 2023 21:56 ] ⁨Hung Le⁩: Hoặc dùng micro bfd

[ June 21, 2023 22:09 ] ⁨SVT.Hoà.Nguyễn⁩: hôm trước anh @⁨Hung Le⁩ có nói là lên Junos nào là có nhiều cái behavior thay đổi anh nhỉ ?
