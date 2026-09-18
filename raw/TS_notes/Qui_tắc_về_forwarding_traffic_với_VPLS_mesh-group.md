# Qui tắc về forwarding traffic với VPLS mesh-group

Qui tắc về forwarding traffic với VPLS mesh-group:

● CE mesh-group (group mặc định)

    ○ Tất cả các interface nối đến CE sẽ nằm trong group này

    ○ Local-switching ON (default), có thể OFF bằng cách dùng no-local-switching ở mức [routing-instance <instance-name>].

    ○ Lưu ý, traffic multicast không bị ảnh hưởng bởi lệnh no-local-switching.

    ○ Flood traffic đến VE mesh-group và tất cả các mesh-group định nghĩa thêm

● VE mesh-group (group mặc định)

    ○ Tất cả các neighbor (pw) nếu không nằm trong mesh-group nào thì sẽ nằm trong

    mesh-group này

    ○ mặc định là no-local-switching, không thể thay đổi.

    ○ Floods tới CE mesh-group và tất cả mesh-group được định nghĩa thêm

● mesh-group định nghĩa thêm:

- mặc định no-local-switching, có thể thay đổi bằng lệnh local-switching ở mức

[routing-instance <instance-name> protocols vpls mess-group <mess-group-name>]

- Floods tới CE meshgroup và tất cả mesh-group khác

Cấu hình core-facing:

- Tại [interfaces <interface-name> unit <n> family vpls]

- Config này chuyển CE interface từ CE meshgroup tới VE mesh-group (default mesh-group).

Lệnh này sẽ cách ly hoàn toàn traffic giữa các port CE, kể cả traffic multicast.
