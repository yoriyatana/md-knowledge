# Không commit được khi delete routing-instance ở trạng thái deactivate

SR-2021-1125-0914

SVTech gửi lại thông tin phân tích lỗi:

- Hiện tượng:

```text
Khi thực hiện khai báo routing-instances q510\_ll\_ihictcpgdtt3 trên PE thì commit gặp lỗi trên RE1 backup và không thể apply cấu hình.
Commit báo lỗi trên RE1 do RE1 đang tồn tại từ trước cấu hình của routing-instances q510\_ll\_ihictcpgdtt3, vì vậy khi khai báo lại RI q510\_ll\_ihictcpgdtt3 thì RE1 sẽ check cấu hình hiện tại và thông báo lỗi RI đã tồn tại, dẫn đến không thể commit cấu hình
Kiểm tra cấu hình 2 RE thì thấy trên RE0 hiện không có cấu hình RI q510\_ll\_ihictcpgdtt3, nhưng RE1 backup lại có cấu hình RI q510\_ll\_ihictcpgdtt3 và ở trạng thái deactivate
```
- Nguyên nhân:

- Kiểm tra log tác động thì trước đó có thực hiện delete routing-instances q510\_ll\_ihictcpgdtt3
- Thiết bị hiện tại đang gặp vấn đề:

- Khi vào mode configuration bằng lệnh “configure hoặc edit” và thực hiện delete interface/routing-instances trong khi interface/routing-instances đang deactivate thì thiết bị sẽ chỉ xóa cấu hình trên RE master và không đồng bộ việc xóa này trên RE backup dẫn đến RE backup vẫn tồn tại cấu hình.

- Giải pháp:

- Xử lý vấn đề hiện tại:

|  |
| --- |
| ===Bổ sung cấu hình để đồng bộ lại cấu hình giữa RE0 và RE1====  configure private  set system commit no-delta-synchronize       /\* Cấu hình để đồng bộ toàn bộ cấu hình trên RE master với RE backup \*/  commit   - Kiểm tra so sánh lại cấu hình giữa 2 RE đảm bảo trùng khớp nhau.   ===Remove cấu hình vừa bổ sung=====  configure private  delete system commit no-delta-synchronize  commit |

- Thay đổi cách tác động sau này:

- Trước khi thực hiện xóa các hình interface/routing-instances đang ở trạng thái deactivate cần thực hiện activate lại cấu hình interface/routing-instances trước, sau đó mới thực hiện xóa
