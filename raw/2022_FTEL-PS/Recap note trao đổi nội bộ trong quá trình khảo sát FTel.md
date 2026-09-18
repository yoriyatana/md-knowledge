# Recap note trao đổi nội bộ trong quá trình khảo sát FTel

---

**Hiện tượng ghi nhận**

---

**Ý 1:**

[ November 4, 2022 5:16 PM ] ⁨Ju.a.Đăng⁩: Từ Quân

---

Chỗ này em cũng đang trao đổi lại nội bộ cụ thể use case Anh PhươngLD đề cập là như thế nào.

>>> bên họ cũng đang làm rõ lại ý của Phương

Có một số mong muốn cụ thể là nhưhiện tại đối DWDM. Thì có nháy truyền dẫn thì cũng ko ảnh hưởng tới phiên PPPoE.

Nên nếu chạy VPLS. Bọn em cũng mong muốn là giả dụ như có down một hướng thì sẽ ko ko làm out subs.

>>> cái này đúng ra là phải vậy. Trừ khi set interface hold-timer có gì đó ko phù hợp, chứ pppoe session phải 3x60s nó mới timeout. Dwdm flap trong 1-2s ko phải là vấn

Cái thứ 2 là con số redial bọn em mong muống test là tầm 200cps đới với BRAS Center và BRAS Tỉnh tầm 160cps

>>> Anh nghĩ cái này test lab là ok

Cái thứ 3 là bọn em gặp vấn đề về học route chậm, dẫn tới  phiên VPLS up lên chậm, Có khi active lên mà khoảng 5 phút sau mới up.

>>> cái này phải troubleshoot. Nếu bình thường bật config dưới MP lên thì anh nghĩ sau chừng max 30s vpls nó phải up. Route chỉ propagate từ MP lên RR xong tới backup-bras

====

Kiểm tra lại DDoS pppoe theo ý Ngọc ở trên

[ November 4, 2022 5:24 PM ] ⁨SVT.Tùng.NT⁩: chỗ vấn đề số 3 thì bình thường route ở dưới MP đã adv >> RR adv >> MP-Backup rồi ạ. Trên MP-Backup thì reject RT của MP tương ứng nên PW mới không up

[ November 4, 2022 5:24 PM ] ⁨SVT.Tùng.NT⁩: khi cần up PW thì chỉ sửa lại import policy trên MP-Backup để up kênh thôi ạ

[ November 4, 2022 5:24 PM ] ⁨Ju.a.Đăng⁩: vậy chỉ là MP-backup update lại policy nhanh thế nào thôi nhỉ?

[ November 4, 2022 5:24 PM ] ⁨Ju.a.Đăng⁩: đúng ra chỉ 1-2s là hết

**Rà soát trên mạng**

[ November 7, 2022 3:26 PM ] ⁨Ju.a.Đăng⁩: Nhìn ở góc độ bgp performance của mp-backup thì chắc mình ko làm gì được

[ November 7, 2022 3:27 PM ] ⁨Ju.a.Đăng⁩: trừ khi troubleshoot xem chính xác nó là gì như đã bàn

[ November 10, 2022 3:27 PM ] ⁨SVT.Tùng.NT⁩: Hiện chỗ vấn đề \*1. thuê bao lên chậm\* thì chỗ rate PADI nhận trên MP-Backup đang cao thì khả năng là do trên MP-Backup Ftel đang cấu hình loop 11 cặp cổng (1 cặp đang lỗi): 1 chân đưa vào VPLS, 1 chân làm PPPoE termination

[ November 10, 2022 3:28 PM ] ⁨SVT.Tùng.NT⁩: nên gói PADI sẽ bị nhân lên nhiều lần ạ

[ November 10, 2022 3:30 PM ] ⁨Ju.a.Đăng⁩: Loop nhiều nhưng 1 lúc chỉ đưa lên 1 MP thôi nhi?

[ November 10, 2022 3:33 PM ] ⁨Ju.a.Đăng⁩: bình thường backup-MP ko import hướng MP mà?

[ November 10, 2022 3:36 PM ] ⁨Ju.a.Đăng⁩: hay là họ loop 11 x port đơn dẫn đến 1 gói PADI gửi từ dưới lên sẽ thành 11 gói PADI?

[ November 10, 2022 3:37 PM ] ⁨SVT.Tùng.NT⁩: ý này là thiết kế anh ạ, MP-Backup chỉ dùng trong tình huống ứng cứu, nhưng hôm trước check thì vẫn có user online thì ra là do ứng cứu xong ae FTEL vẫn để nguyên không rollback lại ạ

[ November 10, 2022 3:38 PM ] ⁨Ju.a.Đăng⁩: ok Tùng

[ November 10, 2022 3:39 PM ] ⁨Ju.a.Đăng⁩: vậy chắc lúc nào thử lại với chỉ 1 port loop trên backup-mp coi nó có nhanh hơn ko. Hoặc ae act/stb. Lâu dài phải tách riêng 11 port này ra

[ November 10, 2022 4:05 PM ] ⁨Ju.a.Đăng⁩: Nếu giải pháp sử dụng evpn - \*anh em bàn thêm xem có nên đưa thêm option này cho FTel?\*

=========================

- không cần pe

- bras chạy evpn + pwht

- 7100 chạy evpn vpws

- topo sẽ là Act/Stb & cần 50% capacity dự phòng cho tỉnh trên bras vùng

Ưu điểm:

- no mac learning, no L2 loop >>> mạng stable hơn

- giảm được chassis pe-bras

Nhược điểm:

- pwht trên bras. Bugs

- cần thêm  pfe capacity cho ps

- cần đầu tư nhiều hơn để dự phòng (chỉ cụm 2 box 1:1)

- phải chia tải trên các cặp bras thay vì cứ đưa vào cụm nhiều bras

\*Cân nhắc:\*

- có 2 khách hàng lớn ở Asia đang xem xét, chưa có production

- cần tìm thêm info ww

[ November 10, 2022 4:25 PM ] ⁨Ju.a.Đăng⁩: trong cái hình của Tùng thì mình chỉ có 1 chassis

[ November 10, 2022 4:26 PM ] ⁨Ju.a.Đăng⁩: có bỏ loop ngoài đi thì cũng ko bớt được thêm chassis nào

[ November 10, 2022 4:26 PM ] ⁨Ju.a.Đăng⁩: có bớt chăng là optics + cable. với giá phải trả khi chạy pwht là new bugs

[ November 10, 2022 4:27 PM ] ⁨Ju.a.Đăng⁩: còn trường hợp mình dùng 2 box pe/bras rời thì lợi được 1 chassis sẽ là yếu tố để có thể cân nhắc rủi ro pwht nhiều hơn

[ November 10, 2022 5:19 PM ] ⁨Ju.a.Đăng⁩: Vậy 7100 mình đã có - từ 22.1R1 EVO

- no-local-switching

- l2c act/stb

Như vậy thì cơ bản là mình quay lại mô hình H-VPLS được rồi nhé, phần VPLS phải nằm trên mx & 7100 chạy L2c chứ ko bắt buôc phải evpn nữa.

[ November 10, 2022 5:55 PM ] ⁨SVT.Tùng.NT⁩: tài liệu thấy vẫn cho monitor traffic trên cổng ps0 ạ

[ November 10, 2022 6:08 PM ] ⁨Ju.a.Đăng⁩: Giờ thì ps là option thôi. Mình chạy h-vpls như dự tính ban đầu ok rồi

[ November 14, 2022 1:53 PM ] ⁨SVT.Tùng.NT⁩: Cuối tuần rồi em có khả sát chỗ VPLS up chậm như FTEL báo

[ November 14, 2022 1:54 PM ] ⁨SVT.Tùng.NT⁩: em có ghi nhận route l2vpn từ RR adv xuống cho MP-Backup ~650K

[ November 14, 2022 1:54 PM ] ⁨SVT.Tùng.NT⁩: ----

Table bgp.l2vpn.0 Bit: 40004

RIB State: BGP restart is complete

RIB State: VPN restart is complete

Send state: in sync

Active prefixes:              26

Received prefixes:            26

Accepted prefixes:            26

Suppressed due to damping:    0

Advertised prefixes:          654930

----

policy-statement ADSL-Backup-1-Import: 97 term: 78 term inactivate >>> 19 term active

policy-statement ADSL-Backup-2-Import: 96 term: 78 term inactivate >>> 18 term active

[ November 14, 2022 1:56 PM ] ⁨SVT.Tùng.NT⁩: trên MP-Backup mặc định sẽ remove các route mà RT không được accept trong import policy, khi bật active term để up vpls thì MP-Backup sẽ gửi refesh về RR để update lại route

[ November 14, 2022 1:59 PM ] ⁨SVT.Ngọc.NĐ⁩: tức lúc đó mặc dù MP-Backup có route rồi (đang bị hidden do import policy reject), nhưng nó vẫn gửi refresh lên RR để yêu cầu gửi lại cái route mới à Tùng?

[ November 14, 2022 2:00 PM ] ⁨SVT.Ngọc.NĐ⁩: và khi gửi RR gửi route cập nhật lại sau khi nhận được y/c refresh, thì chắc chỉ gửi đúng route cần chứ không phải full 650k routes?

[ November 14, 2022 2:02 PM ] ⁨Ju.a.Đăng⁩: cái này chắc mình có thể quick test trong lab để confirm thử?

[ November 14, 2022 2:03 PM ] ⁨SVT.Tùng.NT⁩: em có giải lập để test rồi anh, thời gian up kênh khoảng 7s ạ

[ November 14, 2022 2:03 PM ] ⁨SVT.Tùng.NT⁩: e có trao đổi với a Quân

[ November 14, 2022 2:04 PM ] ⁨SVT.Tùng.NT⁩: ảnh đang hỏi lại thiết kế yêu cầu bâo nhiêu s

[ November 14, 2022 2:09 PM ] ⁨Ju.a.Đăng⁩: mình có optimize để giảm xuống được ko Tùng?

[ November 14, 2022 2:09 PM ] ⁨Ju.a.Đăng⁩: Thời gian 7s theo anh so với thời gian để up toàn bộ sub ko đáng kể. đúng ko?

[ November 14, 2022 2:10 PM ] ⁨Ju.a.Đăng⁩: làm sao để dial rate tăng lên mới là quan trọng

[ November 14, 2022 2:13 PM ] ⁨Ju.a.Đăng⁩: khi giải quyết xong vụ padi bị x11 lần lên thì thử lại rồi quyét định có cân optimize cái thời gian up kênh này ko

[ November 14, 2022 2:15 PM ] ⁨SVT.Tùng.NT⁩: này em lab thì chỉ là thời gian kênh VPLS up lên thôi anh ạ

[ November 14, 2022 2:16 PM ] ⁨SVT.Tùng.NT⁩: chỗ này route sẽ bị remove luôn anh ạ, mình check route reveive-protocol bgp cũng không thấy ạ

[ November 14, 2022 2:17 PM ] ⁨SVT.Tùng.NT⁩: chỗ này em bắt gói thì là gửi update cho tất cả 650K route luôn anh ạ

[ November 16, 2022 8:45 AM ] ⁨Ju.a.Đăng⁩: thay vì deactive/act term, mình shut/no-shut port thì có ok hơn ko Tùng?

[ November 16, 2022 8:48 AM ] ⁨SVT.Tùng.NT⁩: Shut port ở đầu nào vậy anh?

[ November 16, 2022 8:50 AM ] ⁨Ju.a.Đăng⁩: đầu backup bras

[ November 16, 2022 8:51 AM ] ⁨Ju.a.Đăng⁩: thử lab

[ November 16, 2022 8:51 AM ] ⁨Ju.a.Đăng⁩: xem nó chỉ gửi prefix liên quan đến vpls này hay là toàn bộ luôn

[ November 16, 2022 8:57 AM ] ⁨SVT.Tùng.NT⁩: chỗ này do ftel đang có sử dụng nên tắt đầu BRAS-backup có vẻ không hợp lý lắm ạ

[ November 16, 2022 9:00 AM ] ⁨Ju.a.Đăng⁩: Anh nghĩ nếu tách vpls instance ra và off lúc ko dùng thì ok chứ nhỉ?

[ November 16, 2022 9:01 AM ] ⁨Ju.a.Đăng⁩: Quan trọng là performance có cải thiện so với act/deact term ko

[ November 16, 2022 9:02 AM ] ⁨Ju.a.Đăng⁩: Vì thay đổi policy mà upd lại 650k route thì nhiều và mất 7s

[ November 16, 2022 9:02 AM ] ⁨SVT.Tùng.NT⁩: em cũng thấy ý chỗ này là hợp lý, nhưng chỗ chị Vân thì quan tâm đến vấn đề nhiều VPLS instance sẽ gây tốn tài nguyên

[ November 16, 2022 9:02 AM ] ⁨Ju.a.Đăng⁩: Ok

[ November 16, 2022 9:02 AM ] ⁨Ju.a.Đăng⁩: Còn vụ 11x padi thì làm thế nào nhỉ? Cũng phải tách ra thoi

[ November 16, 2022 9:02 AM ] ⁨SVT.Tùng.NT⁩: chỗ này thì nếu bật thêm route-filtering family thì có cải thiện được không anh nhỉ?

[ November 16, 2022 9:02 AM ] ⁨Ju.a.Đăng⁩: Anh nghĩ là ko

[ November 16, 2022 9:07 AM ] ⁨SVT.Tùng.NT⁩: ý em chỗ này là family route-target

[ November 16, 2022 9:08 AM ] ⁨Ju.a.Đăng⁩: Route-target cung sẽ giúp 1 phần

[ November 16, 2022 9:09 AM ] ⁨Ju.a.Đăng⁩: Nhưng cái behavior gui route lại khi thay đổi policy hơi lạ

[ November 16, 2022 9:14 AM ] ⁨SVT.Anh.VT⁩: Gửi lại là chuẩn đúng ko anh, em nhớ default juniper là mấy route ko đưa vào RI là nó ko lưu trên router, trừ phi là RR or conf keep all.

[ November 16, 2022 9:18 AM ] ⁨Ju.a.Đăng⁩: Vậy thì trò off/on int chắc sẽ ko bị gửi lại

[ November 16, 2022 10:45 AM ] ⁨Ju.a.Đăng⁩: vụ backup-bras lên chậm này bên mình lead hay FTel lead nhỉ?

[ November 16, 2022 10:51 AM ] ⁨SVT.Tùng.NT⁩: hiện là phối hợp với FTEL thực hiện test anh ạ

[ November 16, 2022 10:51 AM ] ⁨SVT.Tùng.NT⁩: nhưng đang vướng có thuê bao nên chưa làm được

---

**Phân tích**

---

**P**

- Em cập nhật kết quả health check thiết bị HCM-MP-Backup-01. Sơ bộ ghi nhận 2 vấn đề sau:
- 1. Trên thiết bị có nhiều log log lỗi liên quan FPC4, ngoài ra không ghi nhận thuê bao online trên cổng thuộc FPC4 >>> Đề nghị reseat lại FPC4 để khôi phục lại, nếu không thành công thì thay thế bằng vật tư dự phòng.
- 2. Với 2 VPLS instance phục vụ mô hình dự phòng BRAS tỉnh (ADSL-Backup-1/ADSL-Backup-2), hiện trạng đang dùng 11 cặp cổng loop vật lý để kết cuối VPLS từ MP tỉnh và trả lại lưu lượng để quay số PPPoE nên 1 PADI từ tỉnh gửi lên sẽ được nhân bản và gửi ra các cổng loop làm tăng lượng PADI nhận trên MP-Backup nhiều lần. Đây có thể là nguyên nhân việc thuê bao online lên chậm. Vấn đề này sẽ thực hiện test lại để đánh giá chính xác.
- ---> next actions:
- 1. Thực hiện test và tìm nguyên nhân thời gian up VPLS chậm giữa MP-Backup và MP ở tỉnh. Dự kiến test giữa MP chưa dịch vụ ở BDG và HCM-MP-Backup-01.
- 2. Thực hiện test trên BRAS-Backup:
- a. Mô hình tương tự MP-Backup để kiểm chứng lại vấn đề thuê bao online chậm có phải do đang loop vật lý nhiều cổng vào cùng VPLS.
- b. Test tính năng liên quan PWHT.

**P**

- 1. Thực hiện test và tìm nguyên nhân thời gian up VPLS chậm giữa MP-Backup và MP ở tỉnh. Dự kiến test giữa MP chưa dịch vụ ở BDG và HCM-MP-Backup-01.
- >>> Chỗ này em có rà soát và test trên lab thì hiện trạng MP đang nhận ~ 650K route L2vpn
- Table bgp.l2vpn.0 Bit: 40004
- RIB State: BGP restart is complete
- RIB State: VPN restart is complete
- Send state: in sync
- Active prefixes:              26
- Received prefixes:            26
- Accepted prefixes:            26
- Suppressed due to damping:    0
- Advertised prefixes:          654930
- Trên MP-Backup mặc định sẽ remove các route mà RT không được accept trong import policy, khi bật active term để up vpls thì MP-Backup sẽ gửi refesh về RR để update lại route
- >>> Thời gian up VPLS khi đổi policy test lab ghi nhận ~ 7s, chưa thực hiện test được trên mạng thực tế
- 2. Thực hiện test trên BRAS-Backup:
- a. Mô hình tương tự MP-Backup để kiểm chứng lại vấn đề thuê bao online chậm có phải do đang loop vật lý nhiều cổng vào cùng VPLS.
- >>> Chưa thực hiện
- b. Test tính năng liên quan PWHT.
- >>> hiện đã cấu hình PWHT trên VPLS để test

**z**

- 1. Thực hiện test up kênh VPLS trên mạng production ghi nhận ~7s - trùng với kết quả test trên lab
- 2. a.Test mô hình tương tự MP-Backup (với 13 cặp loop vật lý) ghi nhận:
- Bắn 100 sub:
- Lần 1-với 13 cặp loop vật lý: online 5 sub
- Lần 2-với 13 cặp loop vật lý: online 42 sub
- Lần 3-với 1 cặp loop vật lý: thì 100 sub onl ngay
- b. Test tính năng PWHT:
- Cấu hình trên BRAS-Backup, thuê bao chỉ online được với cấu hình ifl tĩnh
- Cấu hình tương tự trên LAB SVTECH ghi nhận thuê bao online với dynamic ifl vẫn OK
- -> Dự kiến reboot lại BRAS-Backup và test lại
- ---
- Kết luận đến thời điểm hiện tại:
- **1. Hiện kênh VPLS up chậm là do có nhiều route L2VPN từ RR adv xuống MP-Backup** mỗi lần BGP gửi update lại khi thay đổi policy để up VPLS - Hiện trạng ghi nhận ~ 7s mới up kênh VPLS sau khi commit change policy
- **2. CPS thấp là do trên MP-Backup đang dùng nhiều b2b dẫn đến số lượng PADI bị nhân bản lên nhiều lần** gây violation DDoS protection nên bị drop. CPS ghi nhận ~ 40 subs/giây

---

**Actions**

---

**Pzz**

- Mạng hiện hữu cung cấp cho nhiều dịch vụ

[ November 9, 2022 11:27 ] ⁨Ju.a.Đăng⁩: mô hình bras tập trung cho region nếu mình sử dụng 2 x bras thôi thì sao nhỉ?

- chi phí protection sẽ cao

- acx7100 hiện tại tính năng đang focus vào evpn chứ ko phải là vpls

Đã có demo giải pháp evpn-vpws + pwht với acx7100 + mx204

[ November 9, 2022 11:28 ] ⁨Ju.a.Đăng⁩: Do tính năng evpn được ưu tiên nên hiện acx7100 ko có đủ vpls/l2c để làm vai trò mình đang mong muốn trong mô hình h-vpls của FTel

[ November 9, 2022 11:49 ] ⁨Ju.a.Đăng⁩: Do giải pháp evpn-vpws ~ l2vpn nên chỉ support act/stb hoặc act/act = chỉ support 2 bras

[ November 9, 2022 11:49 ] ⁨Ju.a.Đăng⁩: Đươc cái là ko cần mac-learning gì

[ November 9, 2022 11:59 ] ⁨SVT.Tùng.NT⁩: Hoặc nếu chấp nhận học mac thì mình dẫn về aggSW

[ November 9, 2022 14:00 ] ⁨Ju.a.Đăng⁩: Vụ acx7100 chốt lại như vầy - mình có thể sử dụng evpn-vpws thay cho l2c để nối về cặp vpls trung tâm.  Vẫn có mô hình H-VPLS.

[ November 9, 2022 14:00 ] ⁨SVT.Tùng.NT⁩: vâng, tí chỗ đó nhờ a Đăng hỗ trợ giúp em ạ

[ November 9, 2022 14:00 ] ⁨Ju.a.Đăng⁩: Như vậy cặp pe-bras chạy vpls, còn acx sẽ chạy evpn-vpws

[ November 9, 2022 14:55 ] ⁨SVT.Ngọc.NĐ⁩: nếu vẫn giữ bras hỗ trợ redundance ở mức 7+1, thì cũng có thể dùng evpn mac-vrf anh Đăng nhỉ?

[ November 9, 2022 14:56 ] ⁨Ju.a.Đăng⁩: vụ này thì mình ngại bgp-based mac-learning

[ November 9, 2022 14:56 ] ⁨Ju.a.Đăng⁩: về lý thuyết là có thể, nhưng triển khai thực tế thì ko rõ

[ November 9, 2022 14:56 ] ⁨SVT.Ngọc.NĐ⁩: ngại ở đầu BRAS-PE đúng ko anh nhỉ?

[ November 9, 2022 14:56 ] ⁨Ju.a.Đăng⁩: cả triệu mac

[ November 9, 2022 14:56 ] ⁨Ju.a.Đăng⁩: yes

[ November 9, 2022 14:57 ] ⁨Ju.a.Đăng⁩: vpls thì dù sao mình production nhiều, giờ dồn mac-learn lên bgp ko sure

[ November 9, 2022 14:57 ] ⁨SVT.Ngọc.NĐ⁩: dạ, tại trên ACX7100 thì em thấy test 6k instances + ~600k MAC

[ November 9, 2022 14:58 ] ⁨Ju.a.Đăng⁩: ý là mình chưa thấy production với HSI

[ November 9, 2022 14:58 ] ⁨SVT.Ngọc.NĐ⁩: dạ

[ November 9, 2022 15:00 ] ⁨SVT.Ngọc.NĐ⁩: Juniper dạo này có vẻ khuyến khích khách hàng dùng ACX hay sao ấy, mà em thấy có nhiều bài viết rất hay, chi tiết về dòng này trên Juniper Blog ở thời gian gần đây.

[ November 9, 2022 15:28 ] ⁨SVT.Ngọc.NĐ⁩: không rõ evpn này thì hỗ trợ h-vpls được không anh nhỉ?

[ November 9, 2022 15:29 ] ⁨SVT.Ngọc.NĐ⁩: Nếu được, thì chỗ ACX7100 (PE-Tỉnh) sẽ dùng evpn mac-vrf, đầu BRAS-PE sẽ chạy evpn vpws, như vậy sẽ loại trừ việc scaling mac learning qua bgp?

[ November 9, 2022 15:36 ] ⁨Ju.a.Đăng⁩: evpn-vpws ~ l2vpn

[ November 9, 2022 15:37 ] ⁨Ju.a.Đăng⁩: còn pwht là support sub trên vpws trực tiếp mà ko cần loop port vật lý ngoài (nhưng lại tốn tunnel bw bên trong)

[ November 9, 2022 16:08 ] ⁨SVT.Ngọc.NĐ⁩: hỗ trợ interop đc evpn-vpws với vpls thì tốt quá ạ

[ November 9, 2022 16:36 ] ⁨SVT.Ngọc.NĐ⁩: ‪⁨Ju.a.Đăng⁩ chỗ xem nguyên nhân gốc tại MP-Backup cho 2 vấn đề dưới:

- thuê bao online lên chậm

- kênh vpls up lên chậm

[ November 9, 2022 16:36 ] ⁨SVT.Ngọc.NĐ⁩: Em nghĩ chắc cứ phối hợp online để xử lý trước xem như thế nào

[ November 9, 2022 16:37 ] ⁨SVT.Ngọc.NĐ⁩: chứ chắc bước đầu cũng đâu cần phải onsite để xử lý việc này anh Đăng nhỉ?

[ November 10, 2022 09:52 ] ⁨Ju.a.Đăng⁩: giải pháp evpn-vpws phức tạp hơn mình nghĩ, anh phải xem kỹ lại

[ November 10, 2022 09:53 ] ⁨Ju.a.Đăng⁩: Vụ pwht Tùng hỏi lại chỗ Dũng nhé, lúc trước mình có test cho VT hay VnPT gì đó rồi

[ November 10, 2022 09:56 ] ⁨SVT.Dũng.TQ⁩: File Message

[ November 10, 2022 09:56 ] ⁨SVT.Dũng.TQ⁩: em gửi kết quả ngày trước test nhé anh

[ November 10, 2022 10:12 ] ⁨Ju.a.Đăng⁩: Thật ra anh thấy dùng physical loopback tốn ít optics & cáp nhưng an toàn hơn là bật PWHT :)

[ November 10, 2022 10:13 ] ⁨Ju.a.Đăng⁩: Ko tốn port ngoài nhưng lại mất capacity pfe do inline tunneling cũng vậy

[ November 10, 2022 12:48 ] ⁨Ju.a.Đăng⁩: giải pháp chạy evpn-vpws từ acx7100 nối vào vpls thì phải dùng ps interface trên pe-bras. Tức sẽ mất thêm pfe capacity cho cái ps này!

Hiện 7100 support vpls với các giới hạn như sau trên 21.2R1:

- H-VPLS and user defined mesh group

- VT/LT for VPLS

- GRES/ISSU

- IRB

- No local switching (always local sw?)

- Multihoming (active-standby for VPLS)

- Firewall support on VPLS

- IGMPV2/V3 MLD snooping

- PWE redundancy

- Vlan id all

[ November 10, 2022 14:42 ] ⁨Ju.a.Đăng⁩: Sample config:

---------------

et-0/0/5 {

flexible-vlan-tagging;

encapsulation flexible-ethernet-services;

unit 0 {

encapsulation vlan-bridge;

vlan-id 200;

}

}

vpls1 {

instance-type virtual-switch;

protocols {

vpls {

neighbor 140.140.140.140;

no-tunnel-services;

vpls-id 200;

}

}

vlans {

vlan2 {

vlan-id 200;

interface et-0/0/5.0;

}

}

}

[ November 10, 2022 14:43 ] ⁨Ju.a.Đăng⁩: Vụ ko support no-local-switching là mệt rồi nhỉ?

[ November 10, 2022 14:43 ] ⁨SVT.Ngọc.NĐ⁩: tức là những tính năng mà đang được liệt kê là không dùng được trên AC7100 đúng không anh nhỉ?

[ November 10, 2022 14:43 ] ⁨Ju.a.Đăng⁩: yes

[ November 10, 2022 14:44 ] ⁨Ju.a.Đăng⁩: Giờ lựa chọn ráng xài 7100 vpls hoặc chuyển qua evpn-vpws + PS để stiching bên pe-bras thì option nào sẽ ok hơn?

[ November 10, 2022 14:47 ] ⁨SVT.Ngọc.NĐ⁩: anh Đăng đang sợ đoạn POP+ đấu lên VPLS instance ở ACX7100 đúng không nhỉ?

[ November 10, 2022 14:47 ] ⁨Ju.a.Đăng⁩: ko biết hiện tại FTel có đang cần no-local-sw gì ko

[ November 10, 2022 14:47 ] ⁨SVT.Ngọc.NĐ⁩: Nếu đúng, thì chắc mấy local-AC đấy mình chuyển qua hết core-facing chắc cũng ổn nhỉ?

[ November 10, 2022 14:48 ] ⁨Ju.a.Đăng⁩: ko biết có feature đó ko

[ November 10, 2022 14:48 ] ⁨Ju.a.Đăng⁩: ko define mesh-group là chắc. còn nhét vào core-facing thì ko rõ

[ November 10, 2022 14:49 ] ⁨SVT.Ngọc.NĐ⁩: mà ko define đc mesh-group mà đẩy local-AC vào VE meshgroup thì dịch vụ lại không chạy đc anh ạ :)

[ November 10, 2022 14:51 ] ⁨SVT.Ngọc.NĐ⁩: em đang hiểu đám local-AC trên ACX7100, bắt buộc phải bật phải chặn traffic qua lại giữa local-AC

[ November 10, 2022 14:51 ] ⁨Ju.a.Đăng⁩: vay ko the ko co feature nay roi

[ November 10, 2022 15:04 ] ⁨Ju.a.Đăng⁩: Slide của PLM thì nói no-local-sw là non-goal nhưng trong test case thì thấy có case nói là config no-local-sw. anh phải đi hỏi lại

>>> Tài lieu test có nói config no-local-sw nhưng test case này ko thực hiện

[ November 10, 2022 16:28 ] ⁨Ju.a.Đăng⁩: còn mô hình ko vpls/mac-learn thì lợi điểm này có thể đủ lớn để chấp nhận các bất lợi khác

[ November 10, 2022 16:29 ] ⁨Ju.a.Đăng⁩: Nếu ko vpls áp vào cái mô hình Tùng nói thì đúng là ko cần loop ngoài nữa (smiley) vì nó chạy ps/LT bên trong rồi

[ November 10, 2022 16:43 ] ⁨Ju.a.Đăng⁩: RLI45799 - Storm Control & \*No Local Switching trên ACX7100\*. Junos 21.3R1 EVO

- Packets arriving on a CE interface are sent to a VPLS edge (VE) device or core-facing interfaces only.

- No Local Switching enables E-tree functionality.

- No local switching is applicable to SP style vlans and not applicable to DC style vlans.

Config example:

----

et-0/0/6 {

flexible-vlan-tagging;

encapsulation flexible-ethernet-services;

unit 0 {

encapsulation vlan-bridge;

vlan-id 200;

}

}

et-0/0/10 {

flexible-vlan-tagging;

encapsulation flexible-ethernet-services;

unit 0 {

encapsulation vlan-bridge;

vlan-id 10;

family ethernet-switching {

core-facing;

}

}

}

routing-instances {

vpls1 {

instance-type virtual-switch;

protocols {

vpls {

neighbor a.b.c.d;

service-type single;

no-tunnel-services;

vpls-id 200;

}

}

}

}

vlans {

vlan2 {

vlan-id 200;

interface et-0/0/6.0;

interface et-0/0/10.0;

no-local-switching;

}

}

}

}

[ November 10, 2022 16:45 ] ⁨SVT.Ngọc.NĐ⁩: lý do anh Đăng đang đề xuất chỗ pwht là do Juniper đã có test giải pháp chỗ này với ACX7100 + MX204 phải không ạ?

[ November 10, 2022 16:46 ] ⁨SVT.Ngọc.NĐ⁩: Tụi em đang sợ khi dùng PWHT thì lúc debug không rõ như thế nào với interface PS/LT

[ November 10, 2022 16:48 ] ⁨Ju.a.Đăng⁩: lý do đề xuất PWHT là với case pe-bras + bras thì mình có thể giảm chi phí đầu tư cho khách hàng. Bớt được 1 box

[ November 10, 2022 16:50 ] ⁨Ju.a.Đăng⁩: PWHT thì rõ ràng là sẽ phức tạp & rủi ro hơn so với bras đang chạy hiện tại

[ November 10, 2022 16:50 ] ⁨SVT.Ngọc.NĐ⁩: nếu vậy thì giải pháp dùng b2b tại BRAS vẫn đáp ứng được anh nhỉ?

[ November 10, 2022 16:50 ] ⁨Ju.a.Đăng⁩: yes.

[ November 10, 2022 16:51 ] ⁨Ju.a.Đăng⁩: và còn thêm 1 vấn đề VPLS nữa (khác), nếu bỏ được cái này thì sẽ ko cần lo mac-learn

[ November 10, 2022 16:53 ] ⁨Ju.a.Đăng⁩: nếu giữ topo này + chuyển sang ko dùng vpls (pw act/stb 1:1) thì có khả năng khách hàng ok ko?

[ November 10, 2022 17:05 ] ⁨Ju.a.Đăng⁩: RLI 44271 - 7100 - PWE Redundancy Support for L2 Circuit. Junos 22.1R1-EVO

-----

l2circuit {

neighbor 1.100.2.1 {

interface et-0/0/0.0 {

virtual-circuit-id 1;

}

interface et-0/0/15.1601 {

virtual-circuit-id 1601;

pseudowire-status-tlv;

backup-neighbor 1.100.3.1 {

virtual-circuit-id 1605;

hot-standby;

}

}

interface et-0/0/15.1602 {

virtual-circuit-id 1602;

}

}

local-switching {

interface et-0/0/15.801 {

end-interface {

interface et-0/0/24.801;

}

description lsint2;

encapsulation-type ethernet-vlan;

}

interface et-0/0/15.802 {

end-interface {

interface et-0/0/24.802;

}

description lsint2;

encapsulation-type ethernet-vlan;

}

}

[ November 10, 2022 17:19 ] ⁨Ju.a.Đăng⁩: Vậy 7100 mình đã có - từ 22.1R1 EVO

- no-local-switching

- l2c act/stb

Như vậy thì cơ bản là mình quay lại mô hình H-VPLS được rồi nhé, phần VPLS phải nằm trên mx & 7100 chạy L2c chứ ko bắt buôc phải evpn nữa.

---

[ November 22, 2022 11:11 ] ⁨Ju.a.Đăng⁩: Anh chỉ comment là nên có 7100 để lab trước (tốt nhất là trước khi mua) ít nhất 3 tháng. Có gì còn fix lỗi.

[ November 22, 2022 11:12 ] ⁨Ju.a.Đăng⁩: FTel có tester nên để họ chủ động, mình support?

- Scale tester phải đủ để test theo giá trị định sử dụng

- cần test failover performance với scale

[ November 22, 2022 11:15 ] ⁨Ju.a.Đăng⁩: cơ bản mình cũng chỉ cần phối hợp, FTel lead. Giá trị đóng góp bên mình là:

- thông tin chi tiết về 7100

- bug scrubs

- config best practice nếu có

- review

hay bên mình test luôn?

[ November 22, 2022 11:16 ] ⁨Ju.a.Đăng⁩: Ý tưởng HLD thì cũng đã hòm hòm, phần LLD khi nào test+bug-fix xong thì cũng là lúc hoàn chỉnh

[ November 28, 2022 18:13 ] ⁨Ju.a.Đăng⁩: quá chi tiết rồi, anh chỉ comment thêm:

- acx7100 3 tháng chỉ đủ ra bản service release. tốt nhất là cho 6 tháng để fix lỗi. E là ko phải lỗi nào cũng  fix được trong service release thì mình có thể phải chờ thêm. May mắn thì workaround

- làm rõ trách nhiệm build lab (thiết bị, máy đo)

Còn về man-day thì cần làm rõ ai lead trong các nhiệm vụ trên. FTel làm chính, mình chỉ comment về idea? Hay mình làm chính, FTel input/comment?

[ November 28, 2022 18:14 ] ⁨Ju.a.Đăng⁩: Cái này tuỳ bên mình nhé. Nếu nhắm ko bán được thì để FTel lead, hoặc ngược lại để optimize resource. Hoặc tuỳ strategy của Sale

[ December 13, 2022 10:59 ] ⁨SVT.Ngọc.NĐ⁩: Để AE có comment thì anh nghĩ em cần làm rõ mô hình mà mình đang định setup:

- Chức năng, vai trò của từng box trong mô hình đang setup

- Liệt kê những tính năng cần test trên ACX7100

- Review lại mô hình vật lý và luận lý như vậy thì đã đáp ứng được các tiêu chí/features mà Ftel đang yêu cầu cho vị trí POP-QTE & ACX7100

Trong topo vật lý, cần bổ sung rõ hơn:

- Port đấu nối

- Loại transceiver cần dùng

- Linecard/MIC phải gắn thêm, nếu có

- Version dùng trên từng box (có thể em tìm hiểu qua và đề xuất trước - rồi AE comment thêm)

---

Cập nhật acx7100:

- tính năng L2c act/stb hỗ trợ từ junos 21.3R1

- tính năng no-local-switching từ junos 22.1R1

- tính năng vpls mesh-group từ junos 24.1R1

Do vậy ở thời điểm hiện tại với 21.3 thì 7100 có thể chạy mô hình h-vpls với vpls trên mx + l2c trên acx & khi có 24.1 thì có thể đưa vpls quay về 7100 như dự tính ban đầu.

----

Mô hình evpn-vpws hôm trước đề cập là do thông tin chưa thể triển khai được h-vpls với cặp mx-acx

---

[ February 16, 2023 09:45 ] ⁨Ju.a.Đăng⁩: Update cho vụ H-VPLS & mesh-group trên acx7100. Hiện tại mặc dù tính năng này được release tuy nhiên ở trạng thái là

State: closed-unsupported - Shipped with release but not supported in the field

Có nghĩa là sẽ ko có support gì cả từ Tac/Engineer.

Mình phải chờ bản 24.1R1-EVO (thiết kế lại tính năng này cho toàn bộ dòng ACX (7100 ... 7509...) nếu muốn production

[ February 16, 2023 09:47 ] ⁨Ju.a.Đăng⁩: Do vậy trong 18 tháng tới chắc vẫn phải xài tiếp MX, hoặc dùng 7100 mà ko có h-vpls
