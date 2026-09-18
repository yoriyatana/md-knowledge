# PR check

[https://ascp.juniper.net/jsset/PRDetails?id=1718595](https://ascp.juniper.net/jsset/PRDetails?id=1718595)

PR cho BRAS chạy trên AE khi bị đisable-pfe

[https://ascp.juniper.net/jsset/PRDetails?id=1688972](https://ascp.juniper.net/jsset/PRDetails?id=1688972)

PFE wedge will be seen due to fast link flaps

Việc bundle các port thuộc các loại chipset khác nhau AFT (MPC10E / MPC11E) và non-AFT (ví dụ Trio-Chip set: MPC2-3-4-5-6-7E) sẽ dẫn đến một số hành xử không mong muốn, đặc biệt là load-balance traffic.

# 1. PR1648059

This issue might be seen if the following conditions are met:

* MX equipped with AFT FPC (e.g. MPC10E/11E) and non-AFT FPC (e.g. MPC5E)

* AE configured with child links from both AFT and non-AFT FPCs

* Traffic ingress via legacy cards

* Traffic egress on the AE interface via IRB

# 2. PR1639518

This issue might be seen if the following conditions are met:

* MX equipped with AFT FPC (e.g. MPC10E/11E) and non-AFT FPC (e.g. MPC5E)

* Traffic ingressing on a non-AFT line card and destined to go via IRB over AE with member links hosted on both AFT and non-AFT line cards

Khuyến nghị các Anh/Chị FTEL: trong điều kiện cho phép, đừng thực hiện bundle các Interfaces thuộc các loại MPC type khác nhau để tránh các hành xử về traffic không mong muốn.

- --

SR-2023-0425-1650

* Qua quá trình phối hợp thực hiện các test cases:

    * Đấu nối trực tiếp giữa MPC11E và các MPC khác;

    * Đấu nối qua truyền dẫn DWDM (OTN) giữa MPC11E và MX204, MPC9E và MX204;

* Cũng như các thông tin từ JTAC, SVTECH xin thông tin:

    * Việc thời gian chuyển trang thái từ Down --> Up lại của MPC11E sẽ rơi vào khoảng 25s--35s.

    * Đây là hành xử do thiết kế của dòng card MPC11E (sử dụng dòng chip ZT) mới.

    * Với Junos OS từ 21.3R1 về sau, có thể cải thiện thời gian re-up lại port của MPC11E giảm đi 10 seconds, nghĩa là rơi vào khoảng 15s--25s.

    * Đối với các dòng card này, việc cấu hình hình Hold-time Down được khuyến nghị ở mức Seconds, và phải lớn hơn 25s (không hoạt động được ở mức sub-seconds (ms))

* Vì đây là hành xử của card MPC11E, nên xin gửi đến các Anh thông tin, rất mong FTEL sẽ thiết kế & triển khai cards trong các LACP AE interfaces và có dự phòng đủ để tránh đuợc hiện tượng mất traffic dịch vụ của thiết bị tại Tỉnh/TP.

Ngoài ra, như thông tin đã trao đổi, việc port detect down dựa vào tín hiệu LF từ hệ thống DWDM (Mac Fault Change. Mac LF (0 -> 1) Mac RF (0 -> 0)) khi sử dụng truyền dẫn DWDM (OTN | PSM).

* Hành xử này được thấy trên cả MPC11E và MPC9E, nên port et- interface lập tức chuyển trạng thái sang down.

* Vậy nhờ Thọ trao đổi cùng các Anh truyền dẫn FTEL xem có tinh chỉnh Optional trên hệ thống DWDM để không gửi thông tin LF này cho các đầu Local hoặc far end CE (Router) được không? Việc này có thể giúp cho port et- trên card MPC11E không chuyển trạng thái sang “down”.

However, as described in AT#292-B, the hold-down time on MPC11 is still not perfect if tested via toggling laser OFF/ON. For Rx LOS clear, the actual link up recovery time is longer due to a lengthy DFE tune time caused by Inphi gear box. Hold-down time shorter than 25 seconds won't work as expected.

- --

Sau khi làm việc với ATAC Juniper vấn đề gặp phải match với 02  PR1638410 and PR1642584

[ June 24, 2022 10:15 ] ⁨Ju.a.Đăng⁩: Cơ bản thì 2 PR này để xử lý tốt hơn việc port 100/400G bị flap trên ZT chip (mpc10/11), loại trừ việc bị lỗi như đã gặp

[ June 24, 2022 12:23 ] ⁨FTEL.Đạt⁩: Cả 02 PR nêu trên sẽ được fixed trên  junos:21.2R3-S1 junos:22.3R1

[ June 25, 2022 19:19 ] ⁨SVT.Cường.HV⁩: Có step 03 hôm trước a có mail, Nhờ ae sắp xếp apply giúp luôn nhé

3. / Workaround

Cấu hình hold-time up/down với các thông số dưới để delay trong quá trình interface flap quá nhanh tránh hit PR.

set interfaces et-11/5/0 hold-time up 60000

set interfaces et-11/5/0 hold-time down 300

2. / Xóa fabric priority đưa về cấu hình mặc định để tránh hành xử không

mong muốn.

- - Cấu hình hiện hữu----

forwarding-classes {

        class PLATINUM queue-num 2 priority low;

        class CONTROL queue-num 3 priority high;

4/ Resolution:

Cả 02 PR nêu trên sẽ được fixed trên  junos:21.2R3-S1 junos:22.3R1

Sau khi thực hiện workaround FTEL có thể theo dõi thêm và cân nhắc nâng cấp lên Junos khuyến nghị để fix issue. Em gửi PR theo file đính kèm!

[ June 28, 2022 16:08 ] ⁨Ju.a.Đăng⁩: Mình trả lời thay cho bạn Khương nhé:

- Mezz ở đây là mezzanine có nghĩa là board mạch nhỏ hơn lắp chồng lên trên (có thể hiểu như daughter board)

- Wan mezz thưc hiện chức năng khối wan (optical port) kết nối đến khối xử lý trung tâm ( 8 x ZT chip) của mpc11

(optical_ports) WAN<==>ZT<==>Backplane (SFB, RE)

[ June 28, 2022 16:09 ] ⁨Ju.a.Đăng⁩: Junos mới sau nâng cấp cung cấp thêm thông tin chi tiết về hardware bên trong so với bản cũ trước đó

[ July 11, 2022 21:41 ] ⁨Tran Thanh Long⁩: từ bản 19 lên bản 20 là để fix lỗi gì ‪⁨SVT.Cường.HV⁩ nhỉ

[ July 11, 2022 21:47 ] ⁨SVT.Cường.HV⁩: Có 02 lỗi, 1 là không join được ae với mpc11e, 02 là traffic bị drop khi interface mix mpc11e với loại khác

[ July 12, 2022 16:14 ] ⁨SVT.Cường.HV⁩: Em có check lại chỗ này với case owner thì 02 lỗi cũ đều khuyến nghị lên 20.4 để fix a nhé. Qua trao đổi chỗ Thọ cũng chưa ghi nhận 02 lỗi này lặp lại trên 20.4. Trường hợp nâng 19.3 lên 20.4 vẫn cần apply workaround là change schedule priority high->low cho interface thuộc Mpc11e ạ

- --

[ March 6, 2023 10:34 ] ⁨SVT.Tùng.NT⁩: Hi anh ‪⁨Ju.a.Đăng⁩, anh ‪⁨Hung Le⁩, anh ‪⁨Ju.a.Cương⁩ , khách hàng FTEL đang có hỏi về TSB này ạ. Nhờ các anh cho em hỏi số lượng MPC11 được report với TSB này với ạ?

[ March 6, 2023 11:05 ] ⁨Hung Le⁩: sao lai hỏi sl card bi em nhỉ?

[ March 6, 2023 11:12 ] ⁨SVT.Tùng.NT⁩: dạ tại trong TSB đề cập là case report với MPC11E là ít hơn. Nên tụi em muốn biết số lượng để xem mức độ có phổ biến không ạ

[ March 6, 2023 11:13 ] ⁨SVT.Tùng.NT⁩: Hiện FTEL em check thì đang dùng ~ 14 card MPC11E ạ

[ March 7, 2023 14:36 ] ⁨Hung Le⁩: Hi em, voi MPC11 chi ghi nhan:

show system firmware' for MPC11E may go bad after RE SWO or chassisd restart. Unable to proceed firmware upgrade.

[ March 7, 2023 14:36 ] ⁨Hung Le⁩: khong co ghi nhan bi reboot

[ March 7, 2023 14:37 ] ⁨Hung Le⁩: mac du cung 1 TSB

[ March 7, 2023 14:37 ] ⁨Hung Le⁩: trong TSB cung co de cap ne e

[ March 7, 2023 14:37 ] ⁨Hung Le⁩: MPC11E with 21.3 and earlier Junos has a known issue that 'show system firmware' output would become an unexpected state and prevents firmware upgrade. rebooting the MPC11E board resolves the issue and makes firmware upgrade available.

PR1715264 is tracking this. Pelase refer external-tab on the PR for detail.

[ March 7, 2023 14:54 ] ⁨SVT.Tùng.NT⁩: Dạ, vậy em xin trình bày lại ý em đang hiểu về TSB này cho MPC11 xem em đã hiểu đúng chưa các anh ạ:

  - Hiện chưa ghi nhận card MPC11 bị slient reboot như TSB này mô tả

  - MPC11 với JunOS từ 21.3 sẽ hit với PR1715264

[ March 7, 2023 15:01 ] ⁨Hung Le⁩: Ban đầu sẽ là :

[ March 7, 2023 15:01 ] ⁨Hung Le⁩: In rare situations, MPC10E, EX9200-15C, and MPC11E line cards may get silently restarted without any trigger or external event. No core dump is observed during the event.

This problem might be caused by CPU ucode eratta and can be resolved by upgrading MPC BIOS by installing the optional jfirmware package.

The failed device will become online after the silent restarted.

Juniper Networks is aware of multiple production cases for MPC10E and EX9200-15C.

MPC11E potentially has the same problem but less number of cases have been reported so far.

[ March 7, 2023 15:01 ] ⁨Hung Le⁩: sau các lần cập nhật và ghi nhận thực tế thì bổ sung thêm:

> MPC11E with 21.3 and earlier Junos has a known issue that 'show system firmware' output would become an unexpected state and prevents firmware upgrade. rebooting the MPC11E board resolves the issue and makes firmware upgrade available.

PR1715264 is tracking this. Pelase refer external-tab on the PR for detail.

[ March 7, 2023 15:11 ] ⁨SVT.Tùng.NT⁩: vâng ạ, cám ơn anh ‪⁨Hung Le⁩

[ March 7, 2023 15:16 ] ⁨Hung Le⁩: không có chi e 🙂

- --

[ May 5, 2022 10:37 ] ⁨SVT.Anh.VT⁩: Dạ anh Đăng, anh Hưng ơi, bọn em đang rà soát lại mấy case FPC11 vừa rồi bên FTEL thì có vẻ mỗi lần lỗi thì bọn em có quan sát thấy có cái log matching với PR này

[ May 5, 2022 10:38 ] ⁨SVT.Anh.VT⁩: [https://prsearch.juniper.net/problemreport/PR1639518](https://prsearch.juniper.net/problemreport/PR1639518)

[ May 5, 2022 10:38 ] ⁨SVT.Anh.VT⁩: Anh cho bọn em xin thêm thông tin chi tiết hơn của PR được ko anh :D

[ May 5, 2022 10:38 ] ⁨SVT.Anh.VT⁩: Em cám ơn ạ.

[ May 9, 2022 14:30 ] ⁨Hung Le⁩: PR này mở ra để track viec sua lỗi của PR 1601049

[ May 9, 2022 14:32 ] ⁨SVT.Anh.VT⁩: Dạ, PR này thì em thấy nói MPC11E ko hit phải anh ạ

[ May 9, 2022 14:32 ] ⁨SVT.Anh.VT⁩: On all Junos platforms with MPC10E line-cards, repeated 100GE interface link flaps may result in loss of traffic going out of the interface. Each 100GE interface down event might not flush the stream and triggers a major alarm causing disable-pfe action. This is specific to interfaces configured with high priority scheduler. MPC11E card is not exposed.

[ May 9, 2022 14:34 ] ⁨SVT.Anh.VT⁩: tuy nhiên check log của PR1639518 thì em thấy log giống PR đó, còn PR1601049 thì ko thấy log anh ạ

[ May 9, 2022 14:35 ] ⁨SVT.Anh.VT⁩: Em đang đợi hãng confirm xem MPC11E có hit vào PR1639518 hay không và có workaround nào ko anh ạ !

[ May 9, 2022 14:38 ] ⁨Hung Le⁩: 1639518: This PR is to track the cosd related changes from Rajesh which was added in the context of the PR#1601049 for interface flap leading to pfe-disable and wedge condition.

[ May 9, 2022 15:02 ] ⁨Hung Le⁩: (interface not able to send/receive any packet after flapping on MPC10E card)1560772 vi fix loi cho PR nay nen gay ra loi dc mô tả trong PR 1601049(Changes to ensure that COSD does not respond immediately to link flaps

)=>PR1639518 will be used to port the change to all other throttles as original PR tracks

[ May 9, 2022 15:02 ] ⁨Hung Le⁩: zt chip đều bị hit 1560772, nhung lỗi chỉ mới thấy ở mpc10

[ May 9, 2022 15:02 ] ⁨Hung Le⁩: chưa thấy ở mpc11 chứ ko phải ko bị ở mpc11

[ May 9, 2022 15:09 ] ⁨Ju.a.Đăng⁩: Như thường lệ, PR chỉ focus vào data có ở thời điểm đó & cho khách hàng ở thời điểm đó thôi chứ ko bao quát tất cả các trường hợp.

- --

[ March 15, 2022 15:36 ] ⁨Hung Le⁩: Nhận xét chung về MPC10/11 theo PR:

[ March 15, 2022 15:37 ] ⁨Hung Le⁩: -Các lỗi có khách hàng bị đa phần fix 21

- Lỗi trên systest/dev thì đa phần ở EVPN và BNG(PR này do ko có khách hàng bị và ko tái lập đc nên bỏ

[ March 16, 2022 10:36 ] ⁨Ju.a.Đăng⁩: *mpc10e*

- ---

1 khách hàng EU, 21.2R1-S

1 khách hàng Asia, box BRAS, target 19.4R3-Sn

[ March 16, 2022 10:39 ] ⁨SVT.Hoà.Nguyễn⁩: em thấy bản 21R1-S2 trong phần list known PR cũng khá là ít

[ March 16, 2022 10:39 ] ⁨SVT.Hoà.Nguyễn⁩: chắc là dùng ngon anh nhỉ :))

[ March 16, 2022 10:40 ] ⁨Hung Le⁩: khá ít là chưa có nhiều kh dùng nên ít PR

[ March 16, 2022 10:41 ] ⁨Ju.a.Đăng⁩: đây hiện là 2 khách hàng dùng số lượng mpc10e-10c-x lớn nhất rồi
