# BGP flap

Hiện tượng:

Policy export apply trong group BGP.

```text
group policy gồm 2 neighbor trở lên.
```
Các neigbor không apply policy.

Khi cấu hình policy export cho 1 neighbor trong group --> phiên BGP đó bị reset.

Solution:

Apply policy trong 1 group chung cho tất cả các neighbor.

Trong group mỗi neighbor phải có 1 policy riêng

Trong 1 group chỉ có 1 neigbor.
