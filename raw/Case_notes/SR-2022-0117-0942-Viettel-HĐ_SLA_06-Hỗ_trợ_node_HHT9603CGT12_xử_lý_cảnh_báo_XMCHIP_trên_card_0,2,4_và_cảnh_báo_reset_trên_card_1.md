# SR-2022-0117-0942 - Viettel/HĐ SLA 06/Hỗ trợ node HHT9603CGT12 xử lý cảnh báo XMCHIP trên card 0,2,4 và cảnh báo reset trên card 1

---

**Phát sinh: alarm XMCHIP trên card 0,2,4, 1 card bị reset**

---

**Ghi nhận ban đầu**

- Trên HHT9603CGT12 phát sinh các cảnh báo lỗi:

**Thu thập thông tin**

```
Nhờ anh sắp xếp thu thập các thông tin sau để hỗ trợ phân tích:

show log messages | no-more
show log messages.0.gz | no-more
show log messages.1.gz | no-more
show log messages.2.gz | no-more
show log messages.3.gz | no-more
show log messages.4.gz | no-more
show log messages.5.gz | no-more
show log messages.6.gz | no-more
show log messages.7.gz | no-more
show log messages.8.gz | no-more
show log messages.9.gz | no-more

show log chassisd | no-more
show log chassisd.0.gz | no-more
show log chassisd.1.gz | no-more
show log chassisd.2.gz | no-more
show log chassisd.3.gz | no-more
show log chassisd.4.gz | no-more
show log chassisd.5.gz | no-more
show log chassisd.6.gz | no-more
show log chassisd.7.gz | no-more
show log chassisd.8.gz | no-more
show log chassisd.9.gz | no-more

##Regarding to FPC
show chassis hardware | no-more
show system alarms | no-more
show chassis alarms | no-more
show system core-dumps | no-more
show version | no-more
show chassis fpc | no-more
show chassis fpc pic-status | no-more
show chassis fpc errors | no-more
show chassis fabric fpcs | no-more
show chassis fabric plane | no-more
show chassis fabric summary  | no-more
show chassis fabric map | no-more
show chassis fabric plane-location | no-more
show chassis fabric destinations | no-more
show system resource-monitor fpc | no-more
show pfe statistics traffic | no-more
show pfe statistics traffic detail  | no-more
show pfe statistics error | no-more

Ngoài ra vào giờ thấp điểm, nhờ bên anh lấy giúp em các thông tin sau:
* RSI và var/log thiết bị
* Core-dump nếu có
* Output các câu lệnh sau:

###PFE level information
request pfe execute command "show syslog messages" target fpc0
request pfe execute command "show nvram" target fpc0
request pfe execute command "show ttp statistics" target fpc0
request pfe execute command "show hsl2 statistics" target fpc0
request pfe execute command "show hsl2 statistics crc" target fpc0
request pfe execute command "show cmerror module" target fpc0
request pfe execute command "show sched" target fpc0
request pfe execute command "show threads cpu" target fpc0
request pfe execute command "show jnh 0 exceptions" target fpc0
request pfe execute command "show cmerror level" target fpc0
request pfe execute command "show cmerror module brief" target fpc0
request pfe execute command "show cmerror statistics" target fpc0

request pfe execute command "show syslog messages" target fpc1
request pfe execute command "show nvram" target fpc1
request pfe execute command "show ttp statistics" target fpc1
request pfe execute command "show hsl2 statistics" target fpc1
request pfe execute command "show hsl2 statistics crc" target fpc1
request pfe execute command "show cmerror module" target fpc1
request pfe execute command "show sched" target fpc1
request pfe execute command "show threads cpu" target fpc1
request pfe execute command "show jnh 0 exceptions" target fpc1
request pfe execute command "show cmerror level" target fpc1
request pfe execute command "show cmerror module brief" target fpc1
request pfe execute command "show cmerror statistics" target fpc1

request pfe execute command "show syslog messages" target fpc2
request pfe execute command "show nvram" target fpc2
request pfe execute command "show ttp statistics" target fpc2
request pfe execute command "show hsl2 statistics" target fpc2
request pfe execute command "show hsl2 statistics crc" target fpc2
request pfe execute command "show cmerror module" target fpc2
request pfe execute command "show sched" target fpc2
request pfe execute command "show threads cpu" target fpc2
request pfe execute command "show jnh 0 exceptions" target fpc2
request pfe execute command "show cmerror level" target fpc2
request pfe execute command "show cmerror module brief" target fpc2
request pfe execute command "show cmerror statistics" target fpc2

request pfe execute command "show syslog messages" target fpc4
request pfe execute command "show nvram" target fpc4
request pfe execute command "show ttp statistics" target fpc4
request pfe execute command "show hsl2 statistics" target fpc4
request pfe execute command "show hsl2 statistics crc" target fpc4
request pfe execute command "show cmerror module" target fpc4
request pfe execute command "show sched" target fpc4
request pfe execute command "show threads cpu" target fpc4
request pfe execute command "show jnh 0 exceptions" target fpc4
request pfe execute command "show cmerror level" target fpc4
request pfe execute command "show cmerror module brief" target fpc4
request pfe execute command "show cmerror statistics" target fpc4
```

**Thu thập thông tin**

- Trên HHT9603CGT12 phát sinh các cảnh báo lỗi:

---

**Phát sinh: alarm CB1 trên�**�**ME_AR03.MAP018**

---

**Ghi nhận ban đầu**

- Trên ME_AR03.MAP018 phát sinh các cảnh báo lỗi:

---

**Phát sinh: alarm CB1 trên�**�**ME_AR03.MAP018**

---

**Ghi nhận ban đầu**

- Trên ME_AR03.MAP018 phát sinh các cảnh báo lỗi:
