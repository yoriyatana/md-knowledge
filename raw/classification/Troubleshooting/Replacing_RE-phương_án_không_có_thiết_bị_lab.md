# Thực hiện thay thế (replacing) RE - phương án không có thiết bị lab

        1. ### **Thực hiện thay thế RE**

<span style="background-color: #ffaaaa">Khuyến nghị thực hiện trong thời gian thấp điểm (maintenance window)</span>

- B1: Telnet/ssh vào thiết bị và thực hiện backup cấu hình thiết bị
- B2: Disable cấu hình Graceful-switchover và NSR

 

|# deactivate routing-options nonstop-routing

# deactivate system commit synchronize

# deactivate system switchover-on-routing-crash

# deactivate routing-options nsr-phantom-holdtime

# commit
# deactivate chassis redundancy graceful-switchover|
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

- B3: Rút RE lỗi, cắm RE dự phòng thay thế, cắm console và máy tính vào RE mới và đợi cho RE mới boot thành công.
            - Lưu ý: thường các RE dự phòng của khách hàng có thể là RE thu hồi, điều chuyển từ nơi khác nên trên RE sẽ có sẵn cấu hình cũ của thiết bị khác, và có sẵn cấu hình Graceful-switchover và NSR, nên sẽ có 1 số vấn đề:
                - Không thể nâng cấp OS cho RE mới này lên đúng bản của thiết bị, do khi add software validate sẽ báo fail.
                - Cần thực hiện đúng quy trình để tránh RE mới sync ngược cấu hình cho RE master của box đang chạy, làm mất cấu hình và ảnh hưởng dịch vụ của box đang chạy.
- B4: Console RE dự phòng gõ lệnh “request system zeroize local”, lệnh này sẽ reboot RE và set cấu hình RE về factory-default.

|warning: System will be rebooted and may not boot without configuration

Erase all data, including configuration and log files? [yes,no] (no) yes

<span style="background-color: #ffaaaa">/*Với NG-RE*/</span>

<span style="background-color: #ffaaaa">juniper@PE03_RE1> request vmhost zeroize local</span>

warning: System will be rebooted and may not boot without configuration

Erase all data, including configuration and log files? [yes,no] (no) yes
juniper@PE03_RE1> request system zeroize local|
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

<span style="background-color: #ffaaaa">Lưu ý: luôn có keyword</span> **local** <span style="background-color: #ffaaaa">để thiết bị chỉ reset cấu hình của RE đang tác động, nếu ko có keyword này thiết bị sẽ reset cấu hình của cả 2 RE.</span>

- B5: Thực hiện nâng cấp OS cho RE này lên đúng với version của box đang chạy.
        - Thực hiện copy OS từ RE master vào RE mới (giả sử RE0 là master, RE mới là RE1)

|> file copy /var/tmp/junos-install-mx-x86-64-17.3R3-S9.3.tgz re1:/var/tmp/junos-install-mx-x86-64-17.3R3-S9.3.tgz|
|-----------------------------------------------------------------------------------------------------------------|

            - Console vào RE mới và nâng cấp OS

|/<span style="background-color: #ffaaaa">*Với NG-RE*/</span>

<span style="background-color: #ffaaaa">> request vmhost software add</span> /var/tmp/junos-vmhost-mx-x86-64-17.3R3-S9.3.tgz reboot
> request system software add /var/tmp/junos-install-mx-x86-64-17.3R3-S9.3.tgz reboot|
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

 

- Kiểm tra RE mới đã được nâng cấp lên OS mới thành công

|Hostname: PE03_RE1

Model: mx480

Junos: 17.3R3-S9.3

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">/*Với NG-RE*/</span></span>

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">> show vmhost version</span></span>
juniper@PE03_RE1> show version|
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

<span style="background-color: #ffaaaa">Lưu ý: nếu quá trình copy hoặc nâng cấp OS không thành công, có thể thực hiện nâng cấp bằng USB boot như mục 2.2</span>

 

- B6: Trên RE master, gõ lệnh “commit synchronize scripts” để đồng bộ cấu hình và toàn bộ scripts của thiết bị trên RE master hiện tại qua RE mới

 

|# commit synchronize scripts|
|----------------------------|

- B7: Reboot RE mới (Reboot the new RE to propagate the network-service mode confguration change to the new RE's kernel.)
        - Console vào RE mới

|<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">/*Với NG-RE*/</span></span>

<span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">> request vmhost reboot</span></span>
> request system reboot|
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

- B8: Trên RE master: Enable lại cấu hình Graceful-switchover và NSR ở B2

|# activate routing-options nonstop-routing

# activate system commit synchronize

# activate system switchover-on-routing-crash

# activate routing-options nsr-phantom-holdtime

# commit synchronize
# activate chassis redundancy graceful-switchover|
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

- B9: (Optional) switchover lại RE master để RE mới làm master.
        - <span style="background-color: #ffaaaa"><span style="background-color: #ffaaaa">Thực hiện bước này sau B6 khoảng 10-15 phút để cho RE mới đồng bộ xong trạng thái với RE master.</span></span>
        - Kiểm tra trạng thái đồng bộ giữa 2 RE đã sẵn sang để việc switchover không gây ảnh hưởng dịch vụ/hoặc gây ảnh hưởng dịch vụ là nhỏ nhất.

|{master}

juniper@PE03_RE1> show task replication

        Stateful Replication: Enabled

        RE mode: Master

    Protocol                Synchronization Status

    OSPF                    Complete             

    BGP                     Complete             

    MPLS                    Complete             

    RSVP                    Complete             

    LDP                     Complete             

{master}

juniper@PE03_RE1> show database-replication summary

General:

    Graceful Restart           Enabled

    Mastership                 Master

    Connection                 Up

    Database                   Synchronized

    Message Queue              Ready

{master}

juniper@PE03_RE1> request chassis routing-engine master switch check

Switchover Ready

/*show on backup RE*/

{master}

juniper@PE03_RE1> request routing-engine login other-routing-engine

Last login: Sun Sep 27 21:55:17 from re1

--- JUNOS 17.3R3-S9.3 Kernel 64-bit  JNPR-10.3-20200624.0e4f83a_buil

{backup}

juniper@PE03_RE0> show system switchover

Graceful switchover: On

Configuration database: Ready

Kernel database: Ready

Switchover Status: Ready

{backup}

juniper@PE03_RE0> show task replication

        Stateful Replication: Enabled

        RE mode: Backup
/*show on master RE*/|
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

        -   Thực hiện switchover master RE

|juniper@PE03_RE1> request chassis routing-engine master switch         

Toggle mastership between routing engines ? [yes,no] (no) yes
{master}|
|--------------------------------------------------------------------------------------------------------------------------------------------|

        1. ### **Kiểm tra lại toàn bộ dịch vụ trên box**

- Kiểm tra đảm bảo các dịch vụ trên box vẫn hoạt động bình thường, box không có alarm, log message bất thường.
