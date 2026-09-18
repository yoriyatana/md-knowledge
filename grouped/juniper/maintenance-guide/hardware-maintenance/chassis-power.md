# Chassis Power-Cycle and SFB Restart

> Generated deterministically from the approved grouping manifest.


## Source: `formatted/TS_notes/Restart SFB 4 MX2K.md`

# Restart SFB 4 MX2K

@⁨SVT.Huy.NQ⁩ - Case 2021-0519-0076 này anh có cái comment ở bước 1 bên dưới:

Step 1: Restart SFB 4 :

```text
> request chassis fabric plane 4 offline
> request chassis fabric plane 4 online
```
Reseat SFB 4 (if still alarm)

Trên MX2K ở các version sau này fabric plane thay đổi từ 8 -> 24 fabric plane (hình như từ Junos 17 trở đi). Như vậy 1 SFB ở các version sau này sẽ có 3 fabric plane.

- --> Để tránh confuse cũng như thay vì restart ở mức logical (fabric plane) thì việc restart ở mức vật lý (SFB) sẽ triệt để/sạch sẽ hơn:

```text
Restart SFB bằng lệnh:
request chassis sfb slot  offline
request chassis sfb slot  online
```

## Source: `formatted/TS_notes/support RE and Chassis power-cycle.md`

# support RE and Chassis power-cycle

New CLI commands addition to support RE and Chassis power-cycle under request vmhost hierarchy. These are the "request vmhost power-cycle-re", and "request vmhost power-cycle-cb".
