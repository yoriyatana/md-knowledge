# Command check user bras pppoe stuck

Kịch bản công việc xử lý lỗi một số thuê bao không cutout được trên BPC8003BRA01

###### ###############################

1. Thực hiện thu thập thông tin các user bị treo:

```text
show subscribers physical-interface ae14 vlan-id 2036
```

```text
show subscribers summary routing-instance
```

```text
show subscribers username b651\_ipp\_hungcttxms extensive
```

```text
show subscribers username b651\_ipp\_namcttcv1 extensive
```

```text
show subscribers username b651\_gftth\_phuoccncttnmtv4 extensive
```

```text
show subscribers username b651\_gftth\_doicnvbptdvtq90 extensive
```

```text
show subscribers username b651\_gftth\_vietteltctcpbc16 extensive
```

```text
show subscribers username b651\_gftth\_doivbpcntdcntq extensive
```

###### ###############################

2. Thực hiện thu thập baseline thiết bị:

```text
set cli timestamp
```

```text
set cli screen-width 300
```

/\* Lưu thông tin cấu hình và RSI \*/

```text
request support information brief | no-more | save /var/log/rsi\_before\_BPC8003BRA01\_20210415
```

```text
show configuration |  no-more | save /var/tmp/configuration\_BPC8003BRA01\_20210415
```

/\* Lưu thông tin alarm/core \*/

```text
show version detail  | no-more
```

```text
show version invoke-on all-routing-engines | no-more
```

```text
show version invoke-on all-routing-engines | match "Junos:|RE" | no-more
```

```text
show system core-dumps no-forwarding  | no-more
```

```text
show chassis alarms no-forwarding  | no-more
```

```text
show system processes extensive no-forwarding  | no-more
```

```text
show pfe statistics error  | no-more
```

```text
show chassis routing-engine no-forwarding  | no-more
```

```text
show chassis environment no-forwarding  | no-more
```

```text
show chassis fpc detail  | no-more
```

```text
show chassis fabric summary  | no-more
```

```text
show chassis fabric fpcs  | no-more
```

```text
show chassis fabric plan  | no-more
```

/\* Lưu thông tin về OSPF  version 2 \*/

```text
show ospf interface  | no-more
```

```text
show ospf interface | count  | no-more
```

```text
show ospf hostname | no-more
```

```text
show ospf adjacency  | no-more
```

```text
show ospf adjacency | count  | no-more
```

/\* Lưu thông tin về OSPF version 3 \*/

```text
show ospf3 interface  | no-more
```

```text
show ospf3 interface | count  | no-more
```

```text
show ospf3 hostname | no-more
```

```text
show ospf3 adjacency  | no-more
```

```text
show ospf3 adjacency | count | no-more
```

/\* Lưu thông tin về MPLS/LDP/RSVP \*/ -> không chạy MPLS

/\* Lưu thông tin về BGP \*/

```text
show bgp summary  | no-more
```

```text
show bgp neighbor  | no-more
```

```text
show route summary | no-more
```

/\* Lưu thông tin về Multicast \*/ -> không chạy Multicast

/\* Lưu thông tin LLDP/BFD \*/

```text
show lldp neighbors  | no-more
```

```text
show bfd session detail  | no-more
```

/\* Lưu thông tin hardware/fabric/fpc \*/

```text
show chassis hardware  | no-more
```

```text
show chassis fabric fpcs  | no-more
```

```text
show chassis fabric summary extended  | no-more
```

```text
show chassis fabric plane  | no-more
```

/\* Lưu thông tin đồng bộ GRES and NSR - KB32931  \*/

```text
> Go to the Backup RE:
```

```text
request routing-engine login backup
```

```text
show system switchover | no-more
```

```text
show task replication  | no-more
```

```text
show database-replication summary | no-more
```

```text
> Nhớ thoát để trở về RE master (RE0)
```

exit

```text
show system switchover | no-more
```

```text
show task replication  | no-more
```

```text
show database-replication summary | no-more
```

```text
request chassis routing-engine master switch check | no-more
```

```text
show system subscriber-management summary | no-more
```

```text
show chassis routing-engine | no-more
```

###### ###############################

3. Thực hiện thực hiện thu thập các thông tin liên quan đến user đang bị treo:

Debugging the stale pppoe sessions at the pfe.

```text
> show subscribers user-name  extensive
```

```text
> start shell
```

Important Note: use the fpc number on which the problematic subscriber is active. Based on the subscriber extensive output that you shared, it is on ae4 which uses xe-8/x/x i.e fpc8. However, please verify this once

```text
% cprod -A fpc8 -c "show vbf flow" | grep ""
```

```text
% cprod -A fpc8 -c "show vbf flow "
```

```text
% cprod -A fpc8 -c "show jnh inline-ka session 0 ppp 1073751809" // thực hiện 10 lần
```

```text
% cprod -A fpc8 -c "show jnh inline-ka session 1 ppp 1073751809" // thực hiện 10 lần
```

Repeat the commands 3) and 4) multiple times (say about 10 times) with a time gap of 10 seconds between each iteration.

```text
Run Commands 1) to 4) for few of the problematic pppoe sessions and share it with us.
```

- ---------------------------------------------------------------

Also, run the following commands for 2 iterations and share it with us. These are not specific to per subscriber.

```text
% cprod -A fpc8 -c "show jnh 0 exceptions terse"
```

```text
% cprod -A fpc8 -c "show jnh 1 exceptions terse"
```

```text
% cprod -A fpc8 -c "show jnh 0 ucode-vars"
```

```text
% cprod -A fpc8 -c "show jnh 1 ucode-vars"
```

```text
% cprod -A fpc8 -c "show jnh inline-ka summary"
```

```text
% cprod -A fpc8 -c "show jnh inline-ka mgmt"
```

```text
% cprod -A fpc8 -c "show jnh inline-ka session 0 ppp global-stats"
```

```text
% cprod -A fpc8 -c "show jnh inline-ka session 1 ppp global-stats"
```

```text
% cprod -A fpc8 -c "show jnh inline-ka session 0 ppp host-outbound-info"
```

```text
% cprod -A fpc8 -c "show jnh inline-ka session 1 ppp host-outbound-info"
```

```text
% cprod -A fpc8 -c "show jnh inline-ka pfe 0 steering stats”
```

```text
% cprod -A fpc8 -c "show jnh inline-ka pfe 1 steering stats”
```

```text
% cprod -A fpc8 -c "show jnh inline-ka pfe 0 ae-info”
```

```text
% cprod -A fpc8 -c "show jnh inline-ka pfe 1 ae-info”
```

```text
% cprod -A fpc8 -c "show vbf pfe-events"
```

```text
% cprod -A fpc8 -c "show jnh host-path-stats"
```

```text
% cprod -A fpc8 -c "show vbf flow pppoe summary"
```

###### ###############################

4. Bật traceoptions để thu thập log của các tiến trình liên quan:

```text
set system processes smg-service traceoptions file trace\_bbesmgd
```

```text
set system processes smg-service traceoptions file size 10m
```

```text
set system processes smg-service traceoptions file files 10
```

```text
set system processes smg-service traceoptions level all
```

```text
set system processes smg-service traceoptions flag all
```

```text
set system processes general-authentication-service traceoptions file trace\_gauthd
```

```text
set system processes general-authentication-service traceoptions file size 10m
```

```text
set system processes general-authentication-service traceoptions file files 10
```

```text
set system processes general-authentication-service traceoptions flag all
```

## set system processes general-authentication-service traceoptions filter user b651\_ipp\_namcttcv1

```text
set protocols ppp-service traceoptions file trace\_ppp-service
```

```text
set protocols ppp-service traceoptions file size 10m
```

```text
set protocols ppp-service traceoptions file files 10
```

```text
set protocols ppp-service traceoptions flag all
```

## set protocols ppp-service traceoptions filter user b651\_ipp\_namcttcv1

```text
set protocols ppp traceoptions file trace\_ppp
```

```text
set protocols ppp traceoptions file size 10m
```

```text
set protocols ppp traceoptions file files 10
```

```text
set protocols ppp traceoptions flag all
```

```text
set protocols pppoe traceoptions file trace\_pppoe
```

```text
set protocols pppoe traceoptions file size 10m
```

```text
set protocols pppoe traceoptions file files 10
```

```text
set protocols pppoe traceoptions flag all
```

## set protocols pppoe traceoptions filter user b651\_ipp\_namcttcv1

###### ###############################

5. Thực hiện cutout user bị treo bằng lệnh ẩn sau:

```text
request system subscriber-management release-session id
```

## kiểm tra thông tin user

```text
show subscribers extensive username b651\_ipp\_namcttcv1
```

###### ###############################

6. Nếu bước trên không cutout được thuê bao, tiếp tục thực hiện khởi động lại tiến trình quản lý thuê bao trên thiết bị:

6. 1 Thực thi lệnh khởi động lại tiến trình:

```text
restart smg-service immediately
```

6. 2 Kiểm tra thông tin log để xác định việc restart có phát sinh bất thường:

```text
show log messages | find "restarting.\*Enhanced.\*Management"
```

6. 3 Thực thi lệnh cutout user bị treo:

```text
clear network-access aaa subscriber username
```

```text
clear network-access aaa subscriber session-id
```

```text
request system subscriber-management release-session id
```

## kiểm tra thông tin user

```text
show subscribers extensive username b651\_ipp\_namcttcv1
```

###### ###############################

8. Thu thập các session output và thông tin log trên thiết bị để phục vụ cho công việc phân tích về sau:

```text
show shmlog entries logname all | save /var/log/shmlog\_BPC8003BRA01\_20210415
```

```text
request support information brief | no-more | save /var/log/rsi\_after\_BPC8003BRA01\_20210415
```

```text
file archive source /var/log/\* destination /tmp/LOG\_BPC8003BRA01\_20210415
```

###### ###############################

9. Tắt các traceoption đã bật trên thiết bị:

```text
deactivate system processes smg-service traceoptions
```

```text
deactivate system processes general-authentication-service traceoptions
```

```text
deactivate protocols ppp-service traceoptions
```

```text
deactivate protocols ppp traceoptions
```

```text
deactivate protocols pppoe traceoptions
```

###### ###############################

###### ####################################################################

![](image/5991025a4eaf2c511ed17481167f44b3.docx)
