# SR-2021-1223-1336 - Viettel/HĐ SLA 06/Hỗ trợ kiểm tra Thay đổi vlan range cổng downlink BRAS | Không đá thuê bao khỏi cổng

- --

* *K****iểm tra Thay đổi vlan range cổng downlink BRAS | Không đá thuê bao khỏi cổng**

- --

* *Ghi nhận ban đầu**

- Khách hàng yêu cầu kiểm tra việc cấu hình điều chỉnh lại vlan-range có ảnh hưởng đến thuê bao BRAS:

```
icinga@PR02.TET040_RE0> show chassis alarms
1 alarms currently active
Alarm time               Class  Description
2020-11-28 10:09:11 CAT  Major  FPC 1 Major Errors - HSL2 Error code: 0x200001
```

- --

* *Các bước xử lý**

- --

* *Kiểm tra sơ bộ**

- IP MNS thiết bị **10.250.28.36**

* *Thu thập các thông tin liên quan**

```
request support information | no-more | save /var/log/RSI_PR02.TET040_20211222
file archive source /var/log/* destination /var/log/LOG_PR02.TET040_20211222
```

* *Kiểm tra các case cũ, google với alarm phát sinh**

- Ghi nhận giống alarm trên dòng EX có case ID <span style="background-color: #ffaaaa">2021-0401-0787</span>
    - <span style="background-color: #ffaaaa">Hướng xử lý:</span>
        - <span style="background-color: #ffaaaa">restart lại FPC có cảnh báo</span>
        - <span style="background-color: #ffaaaa">reseat lại FPC có cảnh báo</span>
        - <span style="background-color: #ffaaaa">Thay thế vật tư dự phòng</span>

* *Giả lập trên thiết bị lab và máy đo**

- Thu thập baseline

```

```

- Tiến hành reseat FPC1

```
### Thực hiện restart lại FPC1
request chassis fpc slot 1 restart

### Sau khi FPC1 restart và online trở lại thì dịch vụ đã phục hồi, không phát sinh ngoài kế hoạch
```

* *Kết quả xử lý trên thiết bị**

- Khi đổi cấu hình range vlan thì:
    - Những thuê bao nào trong vlan-range bị co lại thì sẽ không kết nối lại được.
        - Khi commit user vẫn ở trạng thái connect và vẫn truy cập được cho đến khi bị đá ra
    - Các vlan khác không bị ảnh hưởng.

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">>>> Trong trường hợp cấu hình như anh cung cấp thì thuê bao ở vlan từ 2-4000 sẽ không bị ảnh hưởng còn vlan từ 4001-4094 sau khi thuê bao đá ra hết sẽ không vào lại được.</span></span>

- Khi đổi cấu hình MTU trên cổng từ 9000 lên 9022:
    - Thay đổi tham số MTU trên cổng sẽ gây down/up port

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">>>> Toàn bộ thuê bao trên cổng sẽ bị đá ra và thực hiện kết nối lại.</span></span>
