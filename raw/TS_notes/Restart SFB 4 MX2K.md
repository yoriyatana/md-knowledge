# Restart SFB 4 MX2K

@⁨SVT.Huy.NQ⁩ - Case 2021-0519-0076 này anh có cái comment ở bước 1 bên dưới:

Step 1: Restart SFB 4 :

> request chassis fabric plane 4 offline

> request chassis fabric plane 4 online

Reseat SFB 4 (if still alarm)

Trên MX2K ở các version sau này fabric plane thay đổi từ 8 -> 24 fabric plane (hình như từ Junos 17 trở đi). Như vậy 1 SFB ở các version sau này sẽ có 3 fabric plane.

---> Để tránh confuse cũng như thay vì restart ở mức logical (fabric plane) thì việc restart ở mức vật lý (SFB) sẽ triệt để/sạch sẽ hơn:

Restart SFB bằng lệnh:

request chassis sfb slot  offline

request chassis sfb slot  online
