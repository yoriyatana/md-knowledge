# Kiểm tra tác động nào liên quan đến software/hardware/config

⁨SVT.Ngọc.NĐ⁩: Câu hỏi mà mình hay hỏi khách hàng hoặc JTAC hỏi mình: "Trước & tại thời điểm lỗi có bất kỳ tác động nào liên quan đến software/hardware/config?"

⁨SVT.Ngọc.NĐ⁩: Bên dưới là các cách mà mình kiểm chứng thông tin trên log/output bên cạnh việc trao đổi với khách hàng

⁨SVT.Ngọc.NĐ⁩: - Cách check tác động liên quan đến cấu hình:

```text
show system commit
```

+ log interactive-commands (Hoặc các file log có ghi log facility là interactive-commands) - match "UI\_CMDLINE\_READ\_LINE: User '"

- Cách check liên quan đến software nếu có upgrade/downgrade:

+ log interactive-commands (Hoặc các file log có ghi log facility là interactive-commands) - match "request system|request vmhost"

- Cách check liên quan đến thay đổi phần cứng:

+ log messages

+ log chassisd (sẽ có các keyword  "CHASSISD\_SNMP\_TRAP.\*FRU")

+ log inventory

SVT.Ngọc.NĐ⁩: 1 lưu ý là khi kiểm tra log  thì trước tiên cần kiểm tra cấu hình syslog của box xem đang cấu hình facility gì? severity cho mỗi facility đang ở mức nào

SVT.Ngọc.NĐ⁩: ngoài ra, log trên local box nếu bị trôi, mà mình kiểm tra cần check kỹ thì có thể nhờ khách hàng chia sẻ thêm log từ syslog server, nếu có thể.
