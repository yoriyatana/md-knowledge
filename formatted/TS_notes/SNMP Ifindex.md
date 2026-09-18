# SNMP Ifindex

Trên Junos, \*SNMP Ifindex\* được quản lý và tạo dynamic bởi mib2d.

Khi một interface mới được tạo ra, mib2d sẽ tự động kiểm tra và cấp phát SNMP Ifindex cho interface đó và lưu vào trong database file \*/var/db/dcd.snmp\_ix\*

```text
File này sẽ lưu lại mọi thông tin SNMP Ifindex đã được cấp phát khi tạo ra các interfaces trước đó, bất kể khi xóa các interfaces đó đi thì thông tin SNMP Ifindex của các interfaces này vẫn sẽ còn.
```
Do vậy khi tạo mới một interface mib2d sẽ check trong file này trước, nếu đã có sẵn thông tin Ifindex rồi, thì nó sẽ được dùng lại luôn.

Việc cấp phát SNMP Ifindex này chủ yếu phụ thuộc vào thứ tự các interface được tạo ra, nên giá trị này hoàn toàn có thể khác nhau trên các box khác nhau.

Bình thường file này sẽ được đồng bộ và lưu trữ local trong DB của các REs, nên khi khởi động lại hoặc nâng cấp OS thì giá trị Ifindex sẽ không thay đổi.

Tuy nhiên với trường hợp swap all REs hoặc \*nâng cấp OS bằng USB\* thì file này sẽ được renew nên giá trị Ifindex update lại có thể sẽ khác và ảnh hưởng đến việc giám sát qua SNMP.

- --

[ June 13, 2023 15:30 ] ⁨SVT.Ngọc.NĐ⁩: không rõ, nếu mình lấy backup file  /var/db/dcd.snmp\_ix ra trước, rồi sau khi thay RE xong, thì chép đè file này vào lại RE mới thì lúc đó giám sát theo thông tin cũ còn ok ko nhỉ?

[ June 13, 2023 15:32 ] ⁨Tan Pham⁩: trc e test thì chép ok đấy a ah, chép xong phải reboot lại để nó đọc theo file dcd mới đó

[ June 13, 2023 15:32 ] ⁨SVT.Ngọc.NĐ⁩: test kỹ quá (like)
