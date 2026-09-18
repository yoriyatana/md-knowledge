# CFP

[ Tuesday, June 15, 2021 2:03 PM ] ⁨SVT.Thái.NĐ⁩: mấy case module quang, ví dụ như CFP ở đây: bình thường mình sẽ yêu cầu khách hàng làm hard-loop, soft-loop, đấu thẳng.

[ Tuesday, June 15, 2021 2:03 PM ] ⁨SVT.Thái.NĐ⁩: trong quá trình đó thu thập thông tin sau nhé anh chị em:

[ Tuesday, June 15, 2021 2:03 PM ] ⁨SVT.Thái.NĐ⁩: > start shell pfe network fpc#

# show syslog messages

# show cfp list ### get the cfp id from here and below outputs

# show cfp  alarms

# show cfp  diagnostics

# show cfp  identifier

# show cfp  info

# show cfp  mdio-bus-error-count

# show cmic 0 info

# show cmic 0 interrupts

# show syslog messages

# show nvram

```text
>> Thử laser on/ laser off CFP bằng câu lệnh:
```

```text
test cfp  laser  off
```

```text
test cfp  laser  on
```

```text
>> Thu thập rsi, var/log:
```

```text
request support information | save /var/log/rsi-after
```

```text
file archive compress source /var/log/\* destination /var/tmp/varlogs-jtac.tgz
```

[ Tuesday, June 15, 2021 2:06 PM ] ⁨SVT.Thái.NĐ⁩: hard-loop là lấy 1 sợi dây đơn -> 1 đầu cắm vào port Tx (transmit), 1 đầu còn lại cắm vào port Rx (receive)

[ Tuesday, June 15, 2021 2:07 PM ] ⁨SVT.Thái.NĐ⁩: soft-loop là dùng câu lệnh để set interface đó Up (không cắm quang)
