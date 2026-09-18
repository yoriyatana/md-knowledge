# lacp flap khi dung VC mix-mode

như trao đổi với anh Đính, mình có một số lưu ý sau:

1. Virtual chassis đang config là Mix-mode, Mix-mode chỉ nên cấu hình khi chủng loại thiết bị Switch là khác nhau. trong trường hợp của bên mình thì member Switch đang đều là dòng Switch EX4300 nên khuyến nghị cấu hình Virtual Chassis tiêu chuẩn (non mix)

2. Nhờ anh hỏi bên đối tác FTP xem switch Huawei họ đang dùng là thực sự chỉ 1 Switch vật lý hay nhiều Switch gom lại thành Virtual chassis

3. Bên em sẽ anydesk để kiểm tra trạng thái lacp interface để xem các member link trên VC-EX4300 đang ở trạng thái cùng Active/Active hay ở trạng thái Active/Standby ? có thể monitor traffic interface để kiểm tra Arp Request/ Arp Reply khi thực hiện Ping

- --

"truong hop LACP neu 2 port gan tren 2 member thi bi loi ping á, a chuyển qua 2 port lên 1 member thi ok" , anh @⁨SVT.Thái.NĐ⁩ hỗ trợ giúp em về cơ chế này của VC nhé anh

- --

Em chỉ nhớ case CMC bị y chang hiện tượng : flap bgp 90s, queue bgp bị tăng lên do ko gửi được => lỗi MTU ko đồng nhất trên các phân đoạn.

Case này cấu hình mtu-discovery rồi mà ko giải quyết được, phải nhờ ae CMC trace từng phân đoạn rồi chỉnh lại MTU ở mấy con ở giữa mới OK.
