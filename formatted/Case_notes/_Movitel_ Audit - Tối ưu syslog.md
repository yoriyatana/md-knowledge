# [Movitel] Audit - Tối ưu syslog

- --

Tối ưu hoá cấu hình syslog các thiết bị

- --

Ghi nhận ban đầu

- Thông nhất template syslog
- Dùng tool automation để đẩy vào thiết bị - trừ thiết bị PE2G

```text
delete system syslog file messages
```

```text
delete system syslog host 10.229.17.21
```

```text
delete system syslog host 10.229.17.36
```

```text
set system syslog archive size 10m
```

```text
set system syslog archive files 20
```

```text
set system syslog host 10.229.17.21 any notice
```

```text
set system syslog host 10.229.17.21 daemon any
```

```text
set system syslog host 10.229.17.21 kernel notice
```

```text
set system syslog host 10.229.17.21 interactive-commands any
```

```text
set system syslog host 10.229.17.21 match "!(UI\_JUNOSCRIPT\_CMD)"
```

```text
set system syslog host 10.229.17.21 facility-override local7
```

```text
set system syslog host 10.229.17.21 log-prefix AR03.GAZ080
```

```text
set system syslog host 10.229.17.21 explicit-priority
```

```text
set system syslog host 10.229.17.21 structured-data brief
```

```text
set system syslog host 10.229.17.36 any notice
```

```text
set system syslog host 10.229.17.36 daemon any
```

```text
set system syslog host 10.229.17.36 kernel notice
```

```text
set system syslog host 10.229.17.36 interactive-commands any
```

```text
set system syslog host 10.229.17.36 authorization any   /\* thêm do thiếu cái nàythì phần xử lý access control khi trước đã làm cho họ không đủ dữ liệu để chạy nhé ~ from Tu.Doan \*/
```

```text
set system syslog host 10.229.17.36 match "!(UI\_JUNOSCRIPT\_CMD)"
```

```text
set system syslog host 10.229.17.36 port 5514
```

```text
set system syslog host 10.229.17.36 log-prefix AR03.GAZ080
```

```text
set system syslog host 10.229.17.36 explicit-priority
```

```text
set system syslog host 10.229.17.36 structured-data     /\* Đừng để structured brief cho con elasticsearch của SVT nhé ~ from Tu.Doan \*/
```

```text
set system syslog file messages any info
```

```text
set system syslog file messages authorization none
```

```text
set system syslog file messages firewall none
```

```text
set system syslog file messages interactive-commands none
```

```text
set system syslog file messages archive world-readable
```

```text
set system syslog file messages explicit-priority
```

```text
set system syslog file messages structured-data brief
```

```text
set system syslog time-format year
```

```text
set system syslog time-format millisecond
```

Phát sinh trong quá trình thực hiện

- Một số thiết bị đang cấu hình 3 syslog server

- Rà soát để điều chỉnh lại.
