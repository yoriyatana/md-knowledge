# SPNWHCM - TSB74336

# 1. Summary thông tin

Hiện tại đang ghi nhận một số case matching TSB74336. Ở thời điểm T1/2024 chưa ghi nhận JunOS resolve TSB74336 nên phương án workaround là apply script cho thiết bị.

Hiện tại JTAC cung cấp 2 cách wordaround cho case như sau:

·         Add script cho từng FPC, sau khi add cần reboot linecard => sẽ mô tả ở phần (2.)

·         Add script cho cả thiết bị, sau khi add không cần reboot linecard => sẽ mô tả ở phần (3.)

Case ID trao đổi với hãng : 2023-1214-029565 - Viettel - SV TECHNOLOGIES JSC - HHT9603CRT09.PETH01.MX2020\_RE1 - VIETTEL || HHT9603CRT09.PETH01.MX2020 || MX2020 || REOPEN CASE "2023-1019-791831" : FPC14 MPC8E raise CPU\_CMERROR\_DDR\_CORRECTABLE\_MINOR alarm

# 2. Script add trực tiếp vào linecard, cần reboot FPC

## 2.1. Cách add script “disable-cstate-GRUB-MPC7\_01.sh” vào linecard MPC7E

- Chép script “disable-cstate-GRUB-MPC7\_01.sh” vào thư mục /var/tmp/

- Thực hiện add script theo quy trình sau:

|  |
| --- |
| **Login vào mức shell bằng account user root**  {master}  minh.le@MX480\_VietDan\_RE1> start shell user root  Password:                                                ### nhập password của account root    **Login vào FPC1 kiểm tra trạng thái của FPC**    root@MX480\_VietDan\_RE1:/var/home/SU # cty -1 -f fpc1    root@MX480\_VietDan\_RE1-fpc1:~# cat /sys/module/intel\_idle/parameters/max\_cstate  9                                                        ### card chưa được add script    Ctrl + C    **Add script vào FPC1 và reboot FPC1**    root@MX480\_VietDan\_RE1:/var/home/SU # sh /var/tmp/disable-cstate-GRUB-MPC7\_01.sh fpc1  logfile = /var/log/mcelog is added on /etc/mcelog/mcelog.conf .  C-state has been disabled in a new GRUB menu. Reboot FPC1 now.    root@MX480\_VietDan\_RE1:/var/home/SU # exit    root@MX480\_VietDan\_RE1-fpc1:~# cat /sys/module/intel\_idle/parameters/max\_cstate  9                                                ### cần reboot để script có tác dụng    Ctrl + C    MX480\_VietDan\_RE1>  request chassis fpc slot 1 restart      **Login vào FPC1 kiểm tra trạng thái của FPC sau khi đã add script và reboot**    root@MX480\_VietDan\_RE1:/var/home/SU # cty -1 -f fpc1    root@MX480\_VietDan\_RE1-fpc1:~# cat /sys/module/intel\_idle/parameters/max\_cstate  0                                                ### card đã được add script thành công |

## 2.2. Một số kịch bản đã test

|  |  |  |
| --- | --- | --- |
| **Kết quả test ghi nhận trên LegacyRE** | | |
| **Kịch bản test** | **Junos** | **Kết quả** |
| Add script vào khi thiết bị đã add sẵn | 20.4R3-S7.2 | Thiết bị báo ko cần chạy lại script :  /var/home/SU # sh /var/tmp/disable-cstate-GRUB-MPC7\_01.sh fpc1    /sys/module/intel\_idle/parameters/max\_cstate has the value of 0 already. |
| Add script vào card khác MPC7E | 20.4R3-S9.3 | Thiết bị sẽ kiểm tra không đúng HW FPC7 thì ko chạy:  NPC9(MX960-02 uart1)#  root@MX960-02:/var/home/lab # sh /var/tmp/disable-cstate-GRUB-MPC7\_01.sh fpc9    This script is only applicable to MPC7E. |
| Reboot card | 20.4R3-S7.2 | Không cần chạy lại script trên card |
| Reboot box | 20.4R3-S7.2 | Không cần chạy lại script trên card |
| Chuyển card sang slot khác cùng box    (test trên cả MX960 và 480) | 20.4R3-S7.2 | Không cần chạy lại script trên card |
| Switchover giữa 2 RE khác JUNOS | 18.4R3-S7->20.4R3-S7 | Cần chạy lại script trên card |
| Switchover giữa 2 RE cùng JUNOS | 20.4R3-S7.2 | Không cần chạy lại script trên card |
| Chuyển card sang thiết bị cùng JunOS | 20.4R3-S7 | Không cần chạy lại script trên card |
| Chuyển card sang thiết bị khác JunOS | 18.4R3-S7->20.4R3-S7 | Cần chạy lại script trên card |
| 22.2R3-S2 -> 21.2R3-S6 | Cần chạy lại script trên card |
| 21.2R3-S6 -> 21.4R3-S5 | Cần chạy lại script trên card |

# 3. Script apply vào event-option, không cần reboot FPC

## 3.1. Thêm script “fpc\_deep\_cstate\_avoidance.slax” vào event-option trên thiết bị

- Thêm script “fpc\_deep\_cstate\_avoidance.slax “ vào thư mục “/var/db/scripts/event/” trên thiết bị.

- Apply các cấu hình event-option sau:

|  |
| --- |
| > configure  # set event-options generate-event fpc\_deep\_cstate\_avoidance\_gen time-interval 600  # set event-options policy fpc\_deep\_cstate\_avoidance\_periodic events fpc\_deep\_cstate\_avoidance\_gen  # set event-options policy fpc\_deep\_cstate\_avoidance\_periodic then event-script fpc\_deep\_cstate\_avoidance.slax  # set event-options event-script file fpc\_deep\_cstate\_avoidance.slax  # commit |

- Sau khi apply cấu hình trên vào, ngay lập tức thiết bị sẽ apply script vào các card đang chạy trên thiết bị. Sau 1 khoảng tgian định kì (time-interval 600) thiết bị sẽ kiểm tra :

·         Nếu script đã được apply trên linecard: thiết bị sẽ giữ nguyên hiện trạng và không thay đổi.

·         Nếu script chưa được apply trên linecard: thiết bị sẽ apply vào linecard.

- Cách thức kiểm tra linecard đã được apply script chưa:

|  |
| --- |
| root@MX2K-PE2> start shell pfe network base-os fpc6  Last login: Thu Jan  4 09:37:01 ICT 2024 on ttyS1  root@-fpc6:~# ps aux|grep py  root        1000  0.0  0.0  30488  6288 ?        S    Jan04   0:00 /usr/bin/python2 /var/tmp/fpc\_deep\_cstate\_avoidance.py  è SCRIPT đã được apply  root       39305  0.0  0.0   4392   752 pts/0    S+ |

## 3.2. Xóa script “fpc\_deep\_cstate\_avoidance.slax” vào event-option trên thiết bị

- Để xóa script khỏi linecard, cần deactivate cấu hình liên quan đến script “fpc\_deep\_cstate\_avoidance\_periodic” trong config trước, sau đó kill process của script trên tất cả các linecard bằng lệnh sau:

|  |
| --- |
| > config  # deactivate event-options policy fpc\_deep\_cstate\_avoidance\_periodic  # commit      > op url /var/db/scripts/event/fpc\_deep\_cstate\_avoidance.slax kill true  FPC3: script has been killed  FPC6: script has been killed |

- ---

Note: cách check tính năng power saving đang enable hay disable: cat /sys/module/intel\_idle/parameters/max\_cstate
