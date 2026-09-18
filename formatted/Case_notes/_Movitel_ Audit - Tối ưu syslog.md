# [Movitel] Audit - Tối ưu syslog

- --

Tối ưu hoá cấu hình syslog các thiết bị

- --

Ghi nhận ban đầu

- Thông nhất template syslog
- Dùng tool automation để đẩy vào thiết bị - trừ thiết bị PE2G

```text
delete system syslog file messages
delete system syslog host 10.229.17.21
delete system syslog host 10.229.17.36
set system syslog archive size 10m
set system syslog archive files 20
set system syslog host 10.229.17.21 any notice
set system syslog host 10.229.17.21 daemon any
set system syslog host 10.229.17.21 kernel notice
set system syslog host 10.229.17.21 interactive-commands any
set system syslog host 10.229.17.21 match "!(UI\_JUNOSCRIPT\_CMD)"
set system syslog host 10.229.17.21 facility-override local7
set system syslog host 10.229.17.21 log-prefix AR03.GAZ080
set system syslog host 10.229.17.21 explicit-priority
set system syslog host 10.229.17.21 structured-data brief
set system syslog host 10.229.17.36 any notice
set system syslog host 10.229.17.36 daemon any
set system syslog host 10.229.17.36 kernel notice
set system syslog host 10.229.17.36 interactive-commands any
set system syslog host 10.229.17.36 authorization any   /\* thêm do thiếu cái nàythì phần xử lý access control khi trước đã làm cho họ không đủ dữ liệu để chạy nhé ~ from Tu.Doan \*/
set system syslog host 10.229.17.36 match "!(UI\_JUNOSCRIPT\_CMD)"
set system syslog host 10.229.17.36 port 5514
set system syslog host 10.229.17.36 log-prefix AR03.GAZ080
set system syslog host 10.229.17.36 explicit-priority
set system syslog host 10.229.17.36 structured-data     /\* Đừng để structured brief cho con elasticsearch của SVT nhé ~ from Tu.Doan \*/
set system syslog file messages any info
set system syslog file messages authorization none
set system syslog file messages firewall none
set system syslog file messages interactive-commands none
set system syslog file messages archive world-readable
set system syslog file messages explicit-priority
set system syslog file messages structured-data brief
set system syslog time-format year
set system syslog time-format millisecond
```
Phát sinh trong quá trình thực hiện

- Một số thiết bị đang cấu hình 3 syslog server

- Rà soát để điều chỉnh lại.
