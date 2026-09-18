# BFD ISSUE VIETTEL KV3/BRAS28

có 4 BFD session được phân phối xuống 2 FPC 7 & FPC8 để xử lý

1./ TH1: 8-8-7-7

- Disble FPE trên FPC8 bằng câu lệnh request => BFD session (8-8) Init và bị stuck trạng thái, không tự chuyển qua FPC7 còn lại

2./ TH2: 8-8-7-7

- Reboot FPC8 => 2 BFD session trên FPC8 sẽ revert qua FPC7.

3./ TH3: 7-7-7-7

- Disable PFE trên FPC7 bằng câu lệnh request => 4 BFD session stuck ở trạng thái INIT => BGP session DOWN.

4./ TH4: 7-7-7-7

- Reboot FPC7 => 4 BFD session chuyển qua FPC8

5./ TH5: 8-8-8-8

- Reboot nguyên chassis => FPC8 online trước, FPC7 online sau => 4 phiên BFD session ăn theo FPC8.

6./ TH6: 8-8-7-7

- Reboot nguyên chassis => FPC8 online trước, FPC7 online sau => 4 phiên BFD session ăn theo FPC8.

7./ TH7: 8-8-8-8

- Rút hết các member links ra khỏi FPC8 => 4 BFD sessions vẫn ăn theo FPC8, không đổi.

8./ TH8: 7-7-8-8

- Disable PFE trên FPC7 bằng scripts (scripts đánh down PFE khi có major alarm) => BFD (7-7) stuck ở INIT, không tự chuyển qua FPC8. BGP không flap do còn 2 phiên còn lại

9./TH9: 7-7-7-7

- Disable PFE trên FPC7 bằng scripts (scripts đánh down PFE khi có major alarm) => BFD (7-7-7-7) stuck ở INIT, không tự chuyển qua FPC8. BGP session Down.

10./ TC10: 8-8-8-8. Tạm gọi các session là: 8a-8b-8c-8d. Mục tiêu cuối cùng là làm cách nào để 4 BFD trở thành 7-7-8-8 ?

10a./ TC10a: 8a-8b-8c-8d:

- xóa cấu hình lần lượt từng session và cấu hình lại từng phiên BFD => vẫn ghi nhận BFD ăn theo FPC cũ (8-8-8-8).

10b./ TC10b: 8a-8b-8c-8d:

- xóa cấu hình BFD session 8a & 8b. => lúc này chỉ còn lại session 8c & 8d.

- Restart lại FPC7, sau đó cấu hình lại 2 session đã xóa trước đó. => vẫn ghi nhận 2 session mới ăn theo FPC8 (8a-8b-8c-8d)

10c./ TC10c: 8a-8b-8c-8d:

- xóa cấu hình BFD session 8a & 8b. => lúc này chỉ còn lại session 8c & 8d.

- Restart lại FPC8, sau đó cấu hình lại 2 session đã xóa trước đó. => vẫn ghi nhận 2 session mới ăn theo FPC8 (8a-8b). tuy nhiên 2 session cũ (8c-8d) do đã restart lại FPC8 nên đã trở thành (7c-7d)

Từ TC10 có thể thấy, việc xóa đi tạo lại cấu hình session BFD thì Junos vẫn hành xử ăn theo 1 FPC đã được dedicate từ trước. Chỉ có việc reboot FPC thì session BFD mới ăn theo 1 FPC khác.

Từ TC5 & TC6 có thể thấy, khi reboot chassis, card FPC nào online trước thì BFD session sẽ ăn theo FPC đó.
