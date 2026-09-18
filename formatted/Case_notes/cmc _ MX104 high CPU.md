# cmc _ MX104 high CPU

- --

Phát sinh: CPU tăng cao tại một số thời điểm, gây rớt bgp session

- --

Ghi nhận ban đầu

- CGI01 ghi nhận tình trạng CPU tăng cao
- s
- q
- q
- q
- q
- q
- q
- q
- q
- q
- q

Thu thập thông tin:

- Các thông tin sau thu thập trên cả 2 RE:

- varlog
- RSI
- Core-dumps files
- Đồ thị liên quan thiết bị CPU, RAM, ...

- Thu thập các thông tin sau ở khung giờ thấp điểm:

- Get output for first terminal (Thu thập output ở termial 1)

```text
set cli timestamp
```

* *### (Need root pasword) - (Bước này cần password root của thiết bị)**

start shell user root

* *### ( No impact. It just a dump of top -s ) - Tự động thu thập 10 dòng output lệnh top mỗi 5 giây 1 lần, liên tục 5760 lần (~ 8 tiếng).**

top -s 5 -d 5760 -n 10 >> /var/tmp/PECD\_02\_TOP\_080921.txt &

* *### (Close the window and copy the file after 12 hours) - (tắt cửa sổ và đợi 12 tiếng sau thu thập file output)**

* *### (Continue collect output on Terminal 2) (Tiếp tục thu thập output ở Terminal 2)**

* *### copy file /var/tmp/PECD\_02\_TOP\_080921.txt về máy để gửi SVTECH**

- --

\* Mở case liên quan -

CMC | MX104 | HCM001CGI01 | 17.3R3-S7.2 | BGP flaped and rpd process restart, raised coredump on backup RE (RE1)

- --

S/N to open case

BB048

- --

Hi JTAC,

Our customers observed the high CPU on MX104 caused the BGP session flapped. On RE1 (backup), the rpd process was restarted and core-dump raised.

Apr 19 16:23:51.432 2022  HCM001CGI01\_RE0 master Apr 19 16:23:51.432 2022 HCM001CGI01\_RE0 re1 Apr 19 16:23:51.204 2022 HCM001CGI01\_RE1 init: routing (PID 70445) terminated by signal number 11. Core dumped!

Apr 19 17:08:18.774 2022  HCM001CGI01\_RE0 re1 Apr 19 17:08:18.761 2022 HCM001CGI01\_RE1 init: routing (PID 70756) terminated by signal number 11. Core dumped!

Apr 19 17:08:18.775 2022  HCM001CGI01\_RE0 master Apr 19 17:08:18.774 2022 HCM001CGI01\_RE0 re1 Apr 19 17:08:18.761 2022 HCM001CGI01\_RE1 init: routing (PID 70756) terminated by signal number 11. Core dumped!

Apr 19 17:38:21.636 2022  HCM001CGI01\_RE0 re1 Apr 19 17:38:21.625 2022 HCM001CGI01\_RE1 init: routing (PID 71147) terminated by signal number 11. Core dumped!

Apr 19 17:38:21.637 2022  HCM001CGI01\_RE0 master Apr 19 17:38:21.636 2022 HCM001CGI01\_RE0 re1 Apr 19 17:38:21.625 2022 HCM001CGI01\_RE1 init: routing (PID 71147) terminated by signal number 11. Core dumped!

Apr 19 18:22:54.435 2022  HCM001CGI01\_RE0 re1 Apr 19 18:22:54.426 2022 HCM001CGI01\_RE1 init: routing (PID 71501) terminated by signal number 11. Core dumped!

Apr 19 18:22:54.437 2022  HCM001CGI01\_RE0 master Apr 19 18:22:54.435 2022 HCM001CGI01\_RE0 re1 Apr 19 18:22:54.426 2022 HCM001CGI01\_RE1 init: routing (PID 71501) terminated by signal number 11. Core dumped!

root@HCM001CGI01\_RE1> show system core-dumps no-forwarding

/var/crash/\*core\*: No such file or directory

- rw-rw----  1 root  field  634218036 Mar 28 11:45 /var/tmp/rpd.core-tarball.0.tgz

- rw-rw----  1 root  field  401251550 Mar 29 04:23 /var/tmp/rpd.core-tarball.1.tgz

- rw-rw----  1 root  field  404650737 Mar 29 08:34 /var/tmp/rpd.core-tarball.2.tgz

- rw-rw----  1 root  field  402086564 Mar 29 09:07 /var/tmp/rpd.core-tarball.3.tgz

- rw-rw----  1 root  field  394722236 Apr 19 18:26 /var/tmp/rpd.core-tarball.4.tgz

/var/tmp/pics/\*core\*: No such file or directory

/var/crash/kernel.\*: No such file or directory

/var/jails/rest-api/tmp/\*core\*: No such file or directory

/tftpboot/corefiles/\*core\*: No such file or directory

total files: 5

Please help us RCA for this issue.
