# Command check user bras pppoe stuck

Kịch bản công việc xử lý lỗi một số thuê bao không cutout được trên BPC8003BRA01

###### ###############################

1. Thực hiện thu thập thông tin các user bị treo:

show subscribers physical-interface ae14 vlan-id 2036

show subscribers summary routing-instance

show subscribers username b651\_ipp\_hungcttxms extensive

show subscribers username b651\_ipp\_namcttcv1 extensive

show subscribers username b651\_gftth\_phuoccncttnmtv4 extensive

show subscribers username b651\_gftth\_doicnvbptdvtq90 extensive

show subscribers username b651\_gftth\_vietteltctcpbc16 extensive

show subscribers username b651\_gftth\_doivbpcntdcntq extensive

###### ###############################

2. Thực hiện thu thập baseline thiết bị:

set cli timestamp

set cli screen-width 300

/\* Lưu thông tin cấu hình và RSI \*/

request support information brief | no-more | save /var/log/rsi\_before\_BPC8003BRA01\_20210415

show configuration |  no-more | save /var/tmp/configuration\_BPC8003BRA01\_20210415

/\* Lưu thông tin alarm/core \*/

show version detail  | no-more

show version invoke-on all-routing-engines | no-more

show version invoke-on all-routing-engines | match "Junos:|RE" | no-more

show system core-dumps no-forwarding  | no-more

show chassis alarms no-forwarding  | no-more

show system processes extensive no-forwarding  | no-more

show pfe statistics error  | no-more

show chassis routing-engine no-forwarding  | no-more

show chassis environment no-forwarding  | no-more

show chassis fpc detail  | no-more

show chassis fabric summary  | no-more

show chassis fabric fpcs  | no-more

show chassis fabric plan  | no-more

/\* Lưu thông tin về OSPF  version 2 \*/

show ospf interface  | no-more

show ospf interface | count  | no-more

show ospf hostname | no-more

show ospf adjacency  | no-more

show ospf adjacency | count  | no-more

/\* Lưu thông tin về OSPF version 3 \*/

show ospf3 interface  | no-more

show ospf3 interface | count  | no-more

show ospf3 hostname | no-more

show ospf3 adjacency  | no-more

show ospf3 adjacency | count | no-more

/\* Lưu thông tin về MPLS/LDP/RSVP \*/ -> không chạy MPLS

/\* Lưu thông tin về BGP \*/

show bgp summary  | no-more

show bgp neighbor  | no-more

show route summary | no-more

/\* Lưu thông tin về Multicast \*/ -> không chạy Multicast

/\* Lưu thông tin LLDP/BFD \*/

show lldp neighbors  | no-more

show bfd session detail  | no-more

/\* Lưu thông tin hardware/fabric/fpc \*/

show chassis hardware  | no-more

show chassis fabric fpcs  | no-more

show chassis fabric summary extended  | no-more

show chassis fabric plane  | no-more

/\* Lưu thông tin đồng bộ GRES and NSR - KB32931  \*/

> Go to the Backup RE:

request routing-engine login backup

show system switchover | no-more

show task replication  | no-more

show database-replication summary | no-more

> Nhớ thoát để trở về RE master (RE0)

exit

show system switchover | no-more

show task replication  | no-more

show database-replication summary | no-more

request chassis routing-engine master switch check | no-more

show system subscriber-management summary | no-more

show chassis routing-engine | no-more

###### ###############################

3. Thực hiện thực hiện thu thập các thông tin liên quan đến user đang bị treo:

Debugging the stale pppoe sessions at the pfe.

1) > show subscribers user-name  extensive

2) > start shell

Important Note: use the fpc number on which the problematic subscriber is active. Based on the subscriber extensive output that you shared, it is on ae4 which uses xe-8/x/x i.e fpc8. However, please verify this once

% cprod -A fpc8 -c "show vbf flow" | grep ""

% cprod -A fpc8 -c "show vbf flow "

3) % cprod -A fpc8 -c "show jnh inline-ka session 0 ppp 1073751809" // thực hiện 10 lần

4) % cprod -A fpc8 -c "show jnh inline-ka session 1 ppp 1073751809" // thực hiện 10 lần

Repeat the commands 3) and 4) multiple times (say about 10 times) with a time gap of 10 seconds between each iteration.

Run Commands 1) to 4) for few of the problematic pppoe sessions and share it with us.

- ---------------------------------------------------------------

Also, run the following commands for 2 iterations and share it with us. These are not specific to per subscriber.

5) % cprod -A fpc8 -c "show jnh 0 exceptions terse"

6) % cprod -A fpc8 -c "show jnh 1 exceptions terse"

7) % cprod -A fpc8 -c "show jnh 0 ucode-vars"

8) % cprod -A fpc8 -c "show jnh 1 ucode-vars"

9) % cprod -A fpc8 -c "show jnh inline-ka summary"

10) % cprod -A fpc8 -c "show jnh inline-ka mgmt"

11) % cprod -A fpc8 -c "show jnh inline-ka session 0 ppp global-stats"

12) % cprod -A fpc8 -c "show jnh inline-ka session 1 ppp global-stats"

13) % cprod -A fpc8 -c "show jnh inline-ka session 0 ppp host-outbound-info"

14) % cprod -A fpc8 -c "show jnh inline-ka session 1 ppp host-outbound-info"

15) % cprod -A fpc8 -c "show jnh inline-ka pfe 0 steering stats”

16) % cprod -A fpc8 -c "show jnh inline-ka pfe 1 steering stats”

17) % cprod -A fpc8 -c "show jnh inline-ka pfe 0 ae-info”

18) % cprod -A fpc8 -c "show jnh inline-ka pfe 1 ae-info”

19) % cprod -A fpc8 -c "show vbf pfe-events"

20) % cprod -A fpc8 -c "show jnh host-path-stats"

21) % cprod -A fpc8 -c "show vbf flow pppoe summary"

###### ###############################

4. Bật traceoptions để thu thập log của các tiến trình liên quan:

set system processes smg-service traceoptions file trace\_bbesmgd

set system processes smg-service traceoptions file size 10m

set system processes smg-service traceoptions file files 10

set system processes smg-service traceoptions level all

set system processes smg-service traceoptions flag all

set system processes general-authentication-service traceoptions file trace\_gauthd

set system processes general-authentication-service traceoptions file size 10m

set system processes general-authentication-service traceoptions file files 10

set system processes general-authentication-service traceoptions flag all

## set system processes general-authentication-service traceoptions filter user b651\_ipp\_namcttcv1

set protocols ppp-service traceoptions file trace\_ppp-service

set protocols ppp-service traceoptions file size 10m

set protocols ppp-service traceoptions file files 10

set protocols ppp-service traceoptions flag all

## set protocols ppp-service traceoptions filter user b651\_ipp\_namcttcv1

set protocols ppp traceoptions file trace\_ppp

set protocols ppp traceoptions file size 10m

set protocols ppp traceoptions file files 10

set protocols ppp traceoptions flag all

set protocols pppoe traceoptions file trace\_pppoe

set protocols pppoe traceoptions file size 10m

set protocols pppoe traceoptions file files 10

set protocols pppoe traceoptions flag all

## set protocols pppoe traceoptions filter user b651\_ipp\_namcttcv1

###### ###############################

5. Thực hiện cutout user bị treo bằng lệnh ẩn sau:

request system subscriber-management release-session id

## kiểm tra thông tin user

show subscribers extensive username b651\_ipp\_namcttcv1

###### ###############################

6. Nếu bước trên không cutout được thuê bao, tiếp tục thực hiện khởi động lại tiến trình quản lý thuê bao trên thiết bị:

6. 1 Thực thi lệnh khởi động lại tiến trình:

restart smg-service immediately

6. 2 Kiểm tra thông tin log để xác định việc restart có phát sinh bất thường:

show log messages | find "restarting.\*Enhanced.\*Management"

6. 3 Thực thi lệnh cutout user bị treo:

clear network-access aaa subscriber username

clear network-access aaa subscriber session-id

request system subscriber-management release-session id

## kiểm tra thông tin user

show subscribers extensive username b651\_ipp\_namcttcv1

###### ###############################

8. Thu thập các session output và thông tin log trên thiết bị để phục vụ cho công việc phân tích về sau:

show shmlog entries logname all | save /var/log/shmlog\_BPC8003BRA01\_20210415

request support information brief | no-more | save /var/log/rsi\_after\_BPC8003BRA01\_20210415

file archive source /var/log/\* destination /tmp/LOG\_BPC8003BRA01\_20210415

###### ###############################

9. Tắt các traceoption đã bật trên thiết bị:

deactivate system processes smg-service traceoptions

deactivate system processes general-authentication-service traceoptions

deactivate protocols ppp-service traceoptions

deactivate protocols ppp traceoptions

deactivate protocols pppoe traceoptions

###### ###############################

###### ####################################################################

![](image/5991025a4eaf2c511ed17481167f44b3.docx)
