# Lỗi memory trên MPC7E-MRATE cho BNG

Dear anh Đăng, anh Hưng, a Cương

Team em đang test PoC Junos version 20.4R3-S3 cho BNG Viettel, target khuyến nghị nâng cấp OS cho BNG Viettel và cả VnPT lên 20.4R3-S3, tuy nhiên trong quá trình test scaling max subscribers cho các line card KH đang sử dụng thì gặp lỗi với memory của MPC7E-MRATE

1. Test case scenario

- Test scaling quay số PPPoE Dual-stack 32K sub lên 1 PFE của MPC7E-MRATE

2. Lỗi ghi nhận trong quá trình test

1. BNG online đủ 32K subs/1PFE/MPC7E, cấp đủ 32K IPv4 tuy nhiên ko cấp đủ 32K DHCP IPv6
2. Có log báo lỗi memory trong PFE: khi DHCP IPv6 cấp được khoảng 16k IPv6 là đã bắt đầu xuất hiện log này

|  |
| --- |
| [Jun 29 15:40:26.745 LOG: Err] stats\_lu\_policer\_create(2211): pfe 0:[FW Policer] policer\_create error - generic failure  [Jun 29 15:40:26.745 LOG: Err] stats\_lu\_instances\_allocate\_cntr(884): pfe 0, lu 0: [FW Policer] stats\_lu\_seg\_allocate error! addr\_offset 0xe986  [Jun 29 15:40:26.745 LOG: Err] stats\_lu\_policer\_group\_create(2998): pfe 0:[FW Policer] policer\_grp\_inst\_alloc error - generic failure  [Jun 29 15:40:26.745 LOG: Err] stats\_lu\_policer\_group\_create(3023): pfe 0:[FW Policer] policer\_group\_create error - generic failure  [Jun 29 15:40:26.746 LOG: Err] stats\_lu\_instances\_allocate\_cntr(884): pfe 0, lu 0: [FW Policer] stats\_lu\_seg\_allocate error! addr\_offset 0xef90  [Jun 29 15:40:26.746 LOG: Err] stats\_lu\_counter\_group\_create\_pkts\_bytes(1484): pfe 0:[FW Policer] cntr\_grp\_inst\_alloc error - generic failure  [Jun 29 15:40:26.746 LOG: Err] FREE ERR CNTR[0]:  FW Policer, 1 dw (1 blk) @ PA 0x4124ef80 addr 0x94ef80  [Jun 29 15:40:26.746 LOG: Err] stats\_lu\_policer\_create(2211): pfe 0:[FW Policer] policer\_create error - generic failure  [Jun 29 15:40:26.748 LOG: Err] stats\_lu\_instances\_allocate\_cntr(884): pfe 0, lu 0: [FW Policer] stats\_lu\_seg\_allocate error! addr\_offset 0xed90  [Jun 29 15:40:26.748 LOG: Err] stats\_lu\_policer\_group\_create(2998): pfe 0:[FW Policer] policer\_grp\_inst\_alloc error - generic failure  [Jun 29 15:40:26.748 LOG: Err] stats\_lu\_policer\_group\_create(3023): pfe 0:[FW Policer] policer\_group\_create error - generic failure  [Jun 29 15:40:31.647 LOG: Err] stats\_lu\_instances\_allocate\_cntr(884): pfe 0, lu 0: [FW Policer] stats\_lu\_seg\_allocate error! addr\_offset 0xaf2  [Jun 29 15:40:31.647 LOG: Err] stats\_lu\_policer\_group\_create(2998): pfe 0:[FW Policer] policer\_grp\_inst\_alloc error - generic failure  [Jun 29 15:40:31.647 LOG: Err] stats\_lu\_policer\_group\_create(3023): pfe 0:[FW Policer] policer\_group\_create error - generic failure  [Jun 29 15:40:31.647 LOG: Err] stats\_lu\_instances\_allocate\_cntr(884): pfe 0, lu 0: [FW Policer] stats\_lu\_seg\_allocate error! addr\_offset 0x10d8  [Jun 29 15:40:31.647 LOG: Err] stats\_lu\_counter\_group\_create\_pkts\_bytes(1484): pfe 0:[FW Policer] cntr\_grp\_inst\_alloc error - generic failure  [Jun 29 15:40:31.647 LOG: Err] stats\_lu\_policer\_create(2211): pfe 0:[FW Policer] policer\_create error - generic failure  [Jun 29 15:52:08.260 LOG: Err] FREE ERR CNTR[0]:  FW Policer, 10 dw (5 blk) @ PA 0x4126f710 addr 0x96f710  [Jun 29 15:52:11.488 LOG: Err] FREE ERR CNTR[0]:  FW Policer, 10 dw (5 blk) @ PA 0x4127b980 addr 0x97b980 |

3. So sánh với Junos cũ 18.4R3-S7 đang chạy cho BNG, Junos mới 20.4R3-S3 khi quay số PPPoE sẽ tự động sinh ra các memory zone và zone ultilization 100% (free 0%)

|  |
| --- |
| {master}  juniper@TEST\_OS\_VIETTEL\_BRAS\_RE0> show subscribers summary physical-interface et-3/0/2  Jun 29 22:46:51    Subscribers by State  Active: 50072  Total: 50072    Subscribers by Client Type  DHCP: 18070  VLAN: 2  PPPoE: 32000  Total: 50072    Subscribers by LS:RI  default: 2  default:default: 50070  Total: 50072    {master}  juniper@TEST\_OS\_VIETTEL\_BRAS\_RE0> start shell pfe network fpc3  Jun 29 22:47:01      SMPC platform (1750Mhz Intel(R) Atom(TM) CPU processor, 3168MB memory, 8192KB flash)    SMPC3(TEST\_OS\_VIETTEL\_BRAS\_RE0 vty)# show jnh 0 pool summary  Name        Size      Allocated     % Utilization  EDMEM    33324800       10498927               31%  IDMEM      471040         459222               97%  Bulk DMEM   196083712       11109740                5%    SMPC3(TEST\_OS\_VIETTEL\_BRAS\_RE0 vty)# show jnh 0  pool usage  EDMEM overall usage:  [NH////////|HASH/////|------------------------------------------------------------]  0          4.0       7.8                                                          31.8M    Next Hop  [\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*|------------------------] 4.0M (69% | 31%)    HASH  [\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*] 3.8M (100% | 0%)    Shared Memory - NH/HASH  [\*\*\*\*\*\*\*\*\*\*\*|---------------------------------------------------------------------] 19.0M (14% | 86%)    Free Shared Memory - NH/HASH  [\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*|----------------------------------------------------------------] 19.0M (21% | 79%)    RO\_EDMEM overall usage:  [NH//////////////////////////////////////////|FW/////////////////////////////////|]  0                                            5.0                                 9.0 9.0M    Next Hop  [\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*|-------------------------] 5.0M (67% | 33%)    Firewall  [|---------------------------------------|RRRRRRRRRRRRRRRRRRRRRRRR] 4.0M (<1% | >99%)    Shared Memory - NH/FW  [\*\*\*\*\*\*\*\*\*\*|----------------------------------------------------------------------] 1.0M (13% | 87%)    Free Shared Memory - NH/FW  [\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*] 1.0M (100% | 0%)    DMEM overall usage:  [CNTR/|HASH|SVC NH|-------------------------------------------------------------------------]  0     12.0 13.6   15.6                                                                      187.0M    Counters  [\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*|-----------------|RRRRRRRRRRRRRRRRRRRRRRRR] 12.0M (47% | 53%)    HASH  [\*\*\*\*\*\*\*\*\*\*] 1.6M (100% | 0%)    Services NH  [|------------] 2.0M (<1% | >99%)    Shared Memory - CNTR/HASH/SVC NH  [--------------------------------------------------------------------------------] 168.2M (0% | 100%)    Free Shared Memory - CNTR/HASH/SVC NH  [--------------------------------------------------------------------------------] 168.2M (0% | 100%) |

3. Jtac/Engineering phản hồi

- Case-id: 2022-0629-502042
- Jtac giả lập trên lab xác nhận đúng lỗi như lab Svtech
- Jtac involve Engineering và xác nhận lỗi này match PR1645505

Tuy nhiên bọn em đọc PR1645505 không thấy trigger hay lỗi liên quan lắm để case bọn em đang ghi nhân thấy, và Jtac support case này hơi chậm. Do số lượng box BNG sử dụng MPC7E cần nâng cấp của VTel và VnPT là rất nhiều

Nhờ anh Đăng/a Hưng/a Cương hỗ trợ thêm giúp bọn em

1. Làm rõ hơn giúp em về PR1645505 có totally match case này không ạ è case này match đúng PR này. Do từ 20.1 có sự thay đổi về cơ chế xử lý JNH nên sinh ra 1 segment mới để dùng cho EA chip.

“With moderate NH/FW scale (more than 2M DWORDS), JNH Partition may choose to use the excess unused part of

the segment added by the aforementioned FAB/ENCAP to NH change.  Since those tables are configured to be in

Bulk DMEM, the expanding NH/FW that was expecting EDMEM will use the slower Bulk DMEM from the excess.

In general this is not a problem, the issue is reported when performance is checked.  Using the Bulk Mem can

cause some apps to run much slower compared to using the desired EDMEM location.

“

è PR161911 đã fixed để xử lý giảm việc excess này đên nhỏ nhất có thể.

Tuy nhiên việc này làm cho “       This is primarily a memory scale issue encountered due to unaligned memory“

“'show jnh  pool layout verbose'”

Dùng lệnh này có thể thấy đuợc việc unaligned đó.

“3. Is this a timing issue?

No, primarily a ASIC memory footprint scale issue.

4. What's the trigger of this PR?

There are multiple triggers, all are differing manifestations of the growing scale encountering the

unaligned memory.  Triggers include non-ZPL ISSU on Stout, STATS scale showing unaliged segments, etc.

Most commmonly affecting MX with Stout card

5. What's the impact /of this PR ?  Hope its crash on FPC.Please confirm

A crash is common, though possible that a simple allocation will fail.

”

2. Làm rõ hơn về các memory tự động sinh ra: Free Shared Memory - NH/FW trong RO\_EDMEM overall usage:

è Cơ chế này quá phức tạp anh cần phải xem xét lại mất nhiều thời gian hơn.

3. Hỗ trợ request Engineering đưa bản fix PR1645505 (nếu totally matching case này) vào Junos 20.4R3-S4, vì nếu đợi đến bản 20.4R3-S5 thì lâu quá

è NHờ Cương hỗ trợ xem được không?
