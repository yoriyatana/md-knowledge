# SCB

Hi Huy,

Anh có một số comments thêm ở phản hồi dưới để em review thêm:

* *1/.** Trước khi thực hiện master RE switchover thì cần thực hiện thêm các bước kiểm tra sau để xem trạng thái đồng bộ giữa 2 RE đang hoạt động bình thường không để đảm bảo việc switchover không ảnh hưởng đến dịch vụ đang chạy. Box này khách hàng đang chạy GRES kết hợp với NSR thì cách kiểm tra cụ thể như sau:

   - Thực hiện ở master RE:

          + show task replication >> All task synchronization status should be complete.

          + show bgp replication  >> Synchronization state should be complete.

   - Thực hiện ở **backup** RE:

          + show system switchover >> Observe the status (On/Ready/Ready/Ready).

   - Thực hiện ở master RE:

          + request chassis routing-engine master switch check >> Output must show switchover ready and not show any warning message.

* *2/.** Bước online lên lại RE1 ở step 1 & online CB1/RE1 ở step 2 như Huy đề cập bên dưới là không cần thực hiện vì RE sẽ tự động online khi CB được gắn vào. Xem lại thủ tục thay thế SCB ở link sau để nắm rõ hơn.

[https://www.juniper.net/documentation/en_US/release-independent/junos/topics/task/installation/scb-mx960-replacing.html](https://www.juniper.net/documentation/en_US/release-independent/junos/topics/task/installation/scb-mx960-replacing.html)

* *    Step 1:**

    Nếu các plane hoạt động lại bình thường thì online RE1 và kiểm tra alarm

    > request vmhost power-on other-routing-engine

* *    Step 2:**

    Cắm lại card SCB1 và đợi 5 phút.

    Online bằng lệnh:

    > request chassis cb online slot 1

    > request vmhost power-on other-routing-engine

* *_Note_**_: FPC / MIC gắn vào thì bắt buộc phải dùng lệnh CLI để online lên, nhưng RE & SCB thì không cần. Lý do thì anh chưa thấy tài liệu Juniper đề cập, nhưng theo anh hiểu SCB/RE là những thành phần điều khiển, việc gắn nó vào mà nó không tự online lại thì sẽ không hợp lý ở 1 số trường hợp._

* *3/.** Ngoài ra, giữa việc **reset** (khởi động / tắt mở lại thiết bị bằng cách dùng lệnh) và **reseat** (rút thiết bị ra và gắn thiết bị vào lại) thì mình cũng nên cân nhắc thêm với khách hàng để xem có thực sự cần thiết phải thực hiện cả 2 bước này hay không. Vì nếu thực hiện theo tuần tự 2 bước này, thì thời gian thực hiện sẽ phải kéo dài - có thể 2 lần ảnh hưởng đến dịch vụ khách hàng, tùy trường hợp.

Do đó, nếu việc thao tác vật lý đối với khách hàng nếu không là vấn đề thì có thể thực hiện luôn bước reseat (bỏ qua bước reset). Trường hợp khách hàng khó sắp xếp được thao tác vật lý - không quan tâm lắm đến 2 lần thực hiện thì lúc đó có thể làm bước reset trước.

* *_Note_**_: khác biệt giữa reset và reseat, thì theo kinh nghiệm và sự hiểu của anh thì reseat sẽ refresh trạng thái của thiết bị hoàn toàn, bao gồm: bộ nhớ & điện. Nên thực hiện reseat thì thiết bị sẽ "sạch sẽ" hoàn toàn. Nhưng khi thực hiện reseat thì phải cẩn thận khi thực hiện các thao tác vật lý để tránh thiết bị bị hỏng do thao tác sai quy trình như gây phóng điện do không đeo vòng tĩnh điện hay cong chân cắm "bent pins" tiếp xúc giữa RE với SCB hoặc tiếp xúc SCB/FPC với midplane/backplane của box._

AE trong Team nắm luôn các ý anh note với Huy để khi xử lý mình cũng nên cân nhắc thêm.
