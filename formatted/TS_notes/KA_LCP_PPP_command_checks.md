# KA LCP PPP command checks

- --

* *KA LCP PPP command checks**

- --

* *KA LCP PPP command checks**

- Kiểm tra health check thiết bị
    - Cấu hình

```
user@host> show configuration interfaces ae104
user@host> show configuration interfaces ae104 | display inheritance
user@host> show configuration interfaces ae104 | display inheritance no-comments

user@host> show configuration dynamic-profiles
user@host> show configuration dynamic-profiles | display inheritance no-comments
user@host> show configuration dynamic-profiles | display inheritance no-comments | match dualstack-pppox-remote
user@host> show configuration dynamic-profiles | display inheritance no-comments | display set | match dualstack-pppox-remote
```

    - Thông tin tổng quan về thuê bao

```
tailc@QNI-PE4-MX960_RE0> show chassis hardware
tailc@QNI-PE4-MX960_RE0> show chassis hardware | match fpc

tailc@QNI-PE4-MX960_RE0> show chassis fpc detail

user@host> show subscribers summary port
user@host> show subscribers summary port
tailc@QNI-PE4-MX960_RE0> show subscribers summary port | refresh 1

user@host> show network-access aaa terminate-code summary
user@host> show network-access aaa terminate-code summary

tailc@QNI-PE4-MX960_RE0> show network-access aaa terminate-code brief
tailc@QNI-PE4-MX960_RE0> show network-access aaa terminate-code brief
tailc@QNI-PE4-MX960_RE0> show network-access aaa terminate-code brief

user@host> show subscribers summary port
user@host> show subscribers summary port

tailc@QNI-PE4-MX960_RE0> show system subscriber-management statistics all
tailc@QNI-PE4-MX960_RE0> show system subscriber-management statistics all extensive
tailc@QNI-PE4-MX960_RE0> show system subscriber-management statistics all extensive | match drop
tailc@QNI-PE4-MX960_RE0> show system subscriber-management statistics all extensive | match drop

tailc@QNI-PE4-MX960_RE0> show network-access aaa radius-servers brief
tailc@QNI-PE4-MX960_RE0> show network-access aaa radius-servers brief
tailc@QNI-PE4-MX960_RE0> show network-access aaa statistics radius queue-info
tailc@QNI-PE4-MX960_RE0> show network-access aaa statistics radius queue-info
tailc@QNI-PE4-MX960_RE0> show network-access aaa statistics authentication
tailc@QNI-PE4-MX960_RE0> show network-access aaa statistics authentication
tailc@QNI-PE4-MX960_RE0> show pppoe statistics
tailc@QNI-PE4-MX960_RE0> show pppoe statistics

tailc@QNI-PE4-MX960_RE0> show system resource-monitor summary

tailc@QNI-PE4-MX960_RE0> show ddos-protection protocols statistics terse
```

    - Reset counter terminal-code để dễ theo dõi

```
tailc@QNI-PE4-MX960_RE0> clear network-access aaa statistics terminate-code
```

    - Kiểm tra dưới linecard

```
tailc@QNI-PE4-MX960_RE0> start shell pfe network fpc3

NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh 0 exceptions terse

NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh inline-ka summary
NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh inline-ka summary

NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh inline-ka session 0 ppp global-stats
NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh inline-ka session 0 ppp global-stats

NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh inline-ka pfe 0 steering stats
NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh inline-ka pfe 0 steering stats

NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh inline-ka pfe 0 ae-info

NGMPC2(QNI-PE4-MX960_RE0 vty)# show jnh inline-ka mgmt

NGMPC2(QNI-PE4-MX960_RE0 vty)# show jnh inline-ka session 0 ppp host-outbound-info
```

    - Reset counter exceptions trên linecard để dễ theo dõi

```
NGMPC3(QNI-PE4-MX960_RE0 vty)# clear jnh 0 exceptions
```

```
NGMPC2(QNI-PE4-MX960_RE0 vty)# show vbf pfe-events
NGMPC3(QNI-PE4-MX960_RE0 vty)# show vbf flow summary
NGMPC2(QNI-PE4-MX960_RE0 vty)# show vbf ttp
NGMPC2(QNI-PE4-MX960_RE0 vty)# show jnh host-path-stats
```

```
tailc@QNI-PE4-MX960_RE0> show subscribers user-name ngocduongqlat extensive
tailc@QNI-PE4-MX960_RE0> show interfaces demux0.3222222329
```

    - Kiểm tra KA cho user cụ thể
        - Mặc định inline-ka ppp Stats không được enabled trên từng session. Cần thực hiện bật thủ công cho từng session

```
tailc@QNI-PE4-MX960_RE0> show subscribers user-name ngocduongqlat extensive
tailc@QNI-PE4-MX960_RE0> show subscribers user-name ngocduongqlat extensive | match "PFE Flow ID:"

tailc@QNI-PE4-MX960_RE0> start shell pfe network fpc3

NGMPC3(QNI-PE4-MX960_RE0 vty)# show vbf flow 211683
Template   :
  .pp.124 1073741948 Single

NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh 0 inline-ka ppp 1073741948
NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh 0 inline-ka ppp 1073741948 stat
NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh 0 inline-ka ppp 1073741948 stat lcp-echo-req-rep stats

NGMPC3(QNI-PE4-MX960_RE0 vty)# test jnh inline-ka session change ppp 1073741948 debug stats

NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh 0 inline-ka

NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh inline-ka session ppp debug-stats
```

```
NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh 0 exceptions terse
NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh 0 exceptions terse

NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh 0 ucode-vars
NGMPC3(QNI-PE4-MX960_RE0 vty)# show jnh 0 ucode-vars
```

```
NGMPC3(QNI-PE4-MX960_RE0 vty)# show jspec cli
```

    - Dùng lệnh **request pfe execute command** để dễ thao tác và track được **set cli timestamp**

```
tailc@QNI-PE4-MX960_RE0> request pfe execute command "show jnh 0 ex ter" target fpc7
tailc@QNI-PE4-MX960_RE0> request pfe execute command "show jnh 0 ex ter" target fpc8
tailc@QNI-PE4-MX960_RE0> request pfe execute command "show jnh 0 ex ter" target fpc3
```

    - Dùng lệnh **shell mode** để thao tác và track **timestamp**

```
tailc@QNI-PE4-MX960_RE0> start shell

% cprod -A fpc7 -c "show jnh inline-ka session 0 ppp global-stats" ; date
% cprod -A fpc5 -c "show jnh inline-ka session 0 ppp global-stats" ; date
% cprod -A fpc3 -c "show jnh inline-ka session 0 ppp global-stats" ; date
```

    - Archive shmlog thành file

```
tailc@QNI-PE4-MX960_RE0> show shmlog statistics logname all | save /var/tmp/shmlog-stats0916a.txt
tailc@QNI-PE4-MX960_RE0> show shmlog entries logname all | save /var/tmp/shmlog-entries0916a.txt
```

- --

- CMD from Mr.Hưng

[ October 21, 2023 11:40 ] ⁨Hung Le⁩: nếu nghi ngờ là KA có vấn dề thì cần show các lệnh này trên các pfe có sub

```
show jnh <pfe> exception terse
show jnh <pfe> ucode-vars
show jnh inline-ka summary
show jnh inline-ka mgmt     Note:  This is before enqueue, if pkt validation failed stats are updated here.
show jnh inline-ka session <pfe> ppp global-stats
show jnh inline-ka session <pfe>  ppp host-outbound-info
show jnh inline-ka pfe <pfe>
show jnh inline-ka pfe <pfe> steering stats
show jnh inline-ka pfe <pfe> ae-info
show vbf pfe-events
show jnh host-path-stats
show vbf flow pppoe summary
```

```
[ October 21, 2023 22:23 ] ⁨Hung Le⁩: bngss@BRMJ00> show subscribers id 6067970
Nov 10 11:20:19
Total subscribers: 0, Active Subscribers: 0

{master}
bngss@BRMJ00> show subscribers id 7911013
Nov 10 11:20:22
Interface             IP Address/VLAN ID                      User Name LS:RI
ge-2/1/2.3221261020    138 L2BSA@dt.net default:L2RIID-4
[ October 21, 2023 22:23 ] ⁨Hung Le⁩: đây là 2 session của 1 user
[ October 21, 2023 22:23 ] ⁨Hung Le⁩: 1 cũ trước khi sw và 1 mới sau khi kết nối lại
[ October 21, 2023 22:23 ] ⁨Hung Le⁩: 02:57:56 Uhr: ServiceStop für jnpr ge-2/1/2:6067970:6067971-1603943628 -> AcctResponse
02:57:56 Uhr: ServiceStart für jnpr ge-2/1/2:6067970:7819259-1604973426 -> AcctResponse
[ October 21, 2023 22:24 ] ⁨Hung Le⁩: session cũ vẫn gửi acct sau khi sw
[ October 21, 2023 22:24 ] ⁨Hung Le⁩: bngss@BRMJ00> show network-access aaa subscribers session-id 6067970
Nov 10 11:17:34
Logical system/Routing instance   Client type    Session-ID     Session uptime    Accounting
default:L2RIID-4                  vlan-oob       6067970        1w5d 06:23        on/volume+time
Service name               Service type   Quota           Accounting
L2BSA_QOS(0,0,L2-Voice,low,Voice,low,L2-Voice,low,Voice,low) -na- -na- on/volume+time
L2BSA_QOS(0,0,L2-LowLoss,low,LowLoss,low,L2-LowLoss,low,LowLoss,low) -na- -na- on/volume+time
L2BSA_QOS(0,0,L2-LowDelay,low,LowDelay,low,L2-LowDelay,low,LowDelay,low) -na- -na- on/volume+time
L2BSA_SRL(10305,32587)     -na-           -na-            on/volume+time
[ October 21, 2023 22:24 ] ⁨Hung Le⁩: show lệnh này vẫn thấy thông tin session cũ
[ October 21, 2023 22:26 ] ⁨Hung Le⁩: Checked the authd core, for sub 6067970 state is active (AUTH_DONE_STATE) and logout is not triggered from client.
This is the reason AST has the entry, and with this SDB entry should not have been deleted either. Client (autoconf plugin) should delete SDB entry only after logout/terminate ACK from authd, and clearly is misbehavior from client as earlier mentioned
[ October 21, 2023 22:27 ] ⁨Hung Le⁩: bật traceoption authen mới thấy lỗi
[ October 21, 2023 22:27 ] ⁨Hung Le⁩: Nov 10 12:21:25.510 2020  BRMJ00 mgd[53913]: UI_CMDLINE_READ_LINE: User 'J-apnbng', command 'set system processes general-authentication-service traceoptions file jtac-authd.log '
 Nov 10 12:21:32.033 2020  BRMJ00 authd[20689]: ../../../../../../../src/junos/usr.sbin/authd/plugin/radius/authd_plugin_radius_module.cc:2332 Failed to get SDB snapshot for session-id:6709955
 Nov 10 12:21:51.505 2020  BRMJ00 authd[20689]: NACK received for profile request with id=0x17fd3c58 from bbe-smgd daemon: No more resources retry FALSE result 0x00000020
 Nov 10 12:21:51.505 2020  BRMJ00 authd[20689]: NACK received for profile request with id=0x17fd3c74 from bbe-smgd daemon: No more resources retry FALSE result 0x00000020
 Nov 10 12:21:51.505 2020  BRMJ00 authd[20689]: NACK received for profile request with id=0x17fd3c90 from bbe-smgd daemon: No more resources retry FALSE result 0x00000020
 Nov 10 12:21:51.506 2020  BRMJ00 authd[20689]: NACK received for profile request with id=0x17fd3cac from bbe-smgd daemon: No more resources retry FALSE result 0x00000020
[ October 21, 2023 22:29 ] ⁨Hung Le⁩: ======Thử với user stuck==== gửi CoA activate 1 cái service gì đó
[ October 21, 2023 22:29 ] ⁨Hung Le⁩: ./BRMJ00-var-log-shmlog.txt:bbe-ljbase-hi        1755903 Nov 10 03:54:41.499135 jauthd: rx: trap                                             session_id=6067970 trap-type=2 req-id=0x00000946 ch=0x00000002
./BRMJ00-var-log-shmlog.txt:bbe-autoconf-info    1755904 Nov 10 03:54:41.499138 BBE_AUTOCONF_I_RX_AUTH_TRAP                                  auth trap 2 received for session session_id=6067970
./BRMJ00-var-log-shmlog.txt:bbe-ljbase-hi        1755905 Nov 10 03:54:41.499166 jauthd: tx: trap response queued                             session_id=6067970 trap-type=2 req-id=0x00000946 result=ifd-1 ch=0x00000002 >>>>> Result=1 indicates autoconf could not find client session

jtac-bbesmgd.log.7.gz:Nov 10 12:54:41 couldn't find client from auth dynamic request  6067970
[ October 21, 2023 22:29 ] ⁨Hung Le⁩: thì trong shmlog sẽ có như vậy=> để chứng minh là phần autoconffig ko có gì
```
