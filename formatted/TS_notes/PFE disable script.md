# PFE disable script

- Why?

- Lỗi xảy ra trên các block trên PFE:

- Blackhole traffic trên PFE
- Blackhole traffic cả box

- Giảm thời gian ảnh hưởng dịch vụ
- Nếu khách hàng không chấp nhận sử dụng

- -> có thể tham khảo để có dấu hiệu nhận biết các lỗi thường gặp ảnh hưởng dịch vụ

- Yêu cầu khi dùng script:

- Có dự phòng link, node, PFE

- What for?

- Log classification

- Transient hardware ~ one time issue: don't have trigger event, no symptom, no predictable

```text
Parity Error
Thường có KB
Đánh giá được mức độ nghiêm trọng
```

- Hardware
- Software
- Software or hardware

- Phù hợp nhất với MPC dùng XM chip
- Lỗi DDRIF không restart
- Tình trạng Host loopback Wek: lỗi thoáng qua

- How?
- How efficient?

1 LUCHIP có 16 block PPE

```text
Head: header
Tail: payload
```

MPC block diagram

action do script hay do JunOS thực hiện

KB31893

BOUNCING:

RESEAT: cli + physical action

RESET/RESTART: by cli

Action script disable port

```text
show system commit | match script
```

```text
delete inteface  disable
```

Action script offline PFE

```text
request chassis fabric pfe fpc <> pic <>
```

```text
request chassis fpc (offline | online | restart) slot slot-number
```

```text
set chassis fpc 0 error major action <>
```

```text
show chassis fpc errors
```

```text
show chassis fpc errors
```

```text
show interface ext
```

```text
show configure | di s set | match syslog
```

```text
show log  mess
```

```text
show start shell pfe  network
```

```text
show hsl2 statistics crc
```

```text
show hsl2 statistics
```

```text
show cmerror module
```

```text
show cmerror module  error
```

```text
show pfe traffic statistics | match "Hardware.\*|Farbric drops"
```

Normal discard: discard do FF,...

```text
show class-of-service fabric static ## check drop statistics
```

```text
show chassis ethernet statistics
```
