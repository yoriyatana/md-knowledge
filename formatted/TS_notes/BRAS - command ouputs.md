# BRAS - command ouputs

Dạ anh Tú,

Em xin summary case này như sau:

+ khoảng chục thuê bao có hiện trạng online chậm, ghi nhận vào thời điểm 20h-21h

Nhờ anh Tú gửi thêm giúp em các thông tin dưới đây anh nhé:

+ Các output: (thực hiện trước khi lấy varlog)

```text
show shmlog entries logname all | save  /var/log/shmentries1.txt
show shmlog statistics logname all | save /var/log/shmstatistics1.txt
```
+ RSI brief, varlog của box.

+ Graph CPU, memory của RE, linecard 1 ngày trở lại đây.

Bên em có thể sẽ cần onsite **vào thời điểm lỗi** này ngày mai để lấy thông tin, các thông tin cần lấy theo các bước dưới đây:

1. **Xác định thuê bao lỗi.**

2. **Traceoptions of authd/pppoe/ppp/smgd trong vòng 10 phút**

```text
set system processes general-authentication-service traceoptions file trace\_general-authentication
set system processes general-authentication-service traceoptions file size 50m
set system processes general-authentication-service traceoptions file files 10
set system processes general-authentication-service traceoptions flag all
set system processes smg-service traceoptions file trace\_smg-service
set system processes smg-service traceoptions file size 100m
set system processes smg-service traceoptions file files 10
set system processes smg-service traceoptions level all
set system processes smg-service traceoptions flag all
set protocols ppp-service traceoptions file trace\_ppp-service
set protocols ppp-service traceoptions file size 50m
set protocols ppp-service traceoptions file files 10
set protocols ppp-service traceoptions flag all
set protocols ppp-service traceoptions level all
set protocols pppoe traceoptions file trace\_pppoe
set protocols pppoe traceoptions file size 50m
set protocols pppoe traceoptions file files 10
set protocols pppoe traceoptions flag all
set protocols pppoe traceoptions level all
```
3. **Monitor traffic**

```text
monitor traffic interface *interface\_name* matching "ether host *subscriber\_mac*" extensive
```
4. **Các log dưới shell, linecard nếu cần thiết**

5. **Shmlogs atleast for 2 iterations.**

Command to collect shmlogs :

```text
show shmlog entries logname all | save  /var/tmp/shmentries1.txt
show shmlog statistics logname all | save /var/tmp/shmstatistics1.txt
```
wait for a 2 minutes and collect

```text
show shmlog entries logname all | save  /var/tmp/shmentries2.txt
show shmlog statistics logname all | save /var/tmp/shmstatistics2.txt
```
6. **CLI logs :  ( the logging could change based on the issue) here are logs to start with.**

```text
set cli timestamp
show subscribers summary | no-more
show subscribers summary port | no-more
show subscribers summary slot | no-more
show subscribers summary all | no-more
show system alarms | no-more
show chassis fpc |no-more
show chassis fpc detail | no-more
show chassis alarms | no-more
show chassis routing-engine | no-more
show system subscriber-management info  | no-more
show system subscriber-management summary | no-more
show system subscriber-management detail | no-more
show system subscriber-management statistics all extensive | no-more
show system configuration database usage | no-more
show shm-ipc statistics | no-more
show shmlog statistics logname all | match fail | no-more
show shmlog statistics logname all | match err | no-more
show system resource-monitor summary | no-more
show system process extensive |no-more
show pppoe statistics | no-more
show pppoe statistics | no-more
show ddos-protection protocols violations | no-more
show ddos-protection protocols statistics terse | no-more
show ddos-protection protocols pppoe padi | no-more
show ddos-protection protocols pppoe | no-more
clear pppoe statistics
show pppoe statistics | no-more
show pppoe statistics | no-more
show subscribers summary | no-more
show subscribers summary port | no-more
show subscribers summary slot | no-more
show subscribers summary | no-more
show system subscriber-management statistics all extensive | no-more
show shm-ipc statistics | no-more
```
start shell csh command "vty -c 'show smd throttle' -s 7208 128.0.0.1"

```text
show system subscriber-management statistics all extensive | no-more
show network-access aaa terminate-code brief | no-more
show network-access aaa terminate-code detail | no-more
show network-access aaa statistics address-assignment pool ftth\_private routing-instance VRF\_CGNAT | no-more
show network-access aaa statistics authentication detail | no-more
show network-access aaa statistics radius queue-info | no-more
show network-access aaa statistics radius detail | no-more
show network-access aaa statistics accounting detail | no-more
show network-access aaa statistics authentication detail | no-more
show network-access memory-pools | no-more
show subscribers summary | no-more
show pppoe statistics | no-more
show ppp statistics detail | no-more
show pppoe statistics | no-more
show ppp statistics detail | no-more
show shmlog statistics logname all | match fail | no-more
show shmlog statistics logname all | match err | no-more
show subscribers summary | no-more
show subscribers summary port | no-more
show subscribers summary slot | no-more
show subscribers summary | no-more
show system subscriber-management statistics all extensive | no-more
show shm-ipc statistics | no-more
show system process extensive |no-more
show ddos-protection protocols statistics terse | no-more
```
start shell csh command "vty -c 'show smd throttle' -s 7208 128.0.0.1"

```text
show network-access aaa statistics address-assignment pool ftth\_private routing-instance VRF\_CGNAT | no-more
show network-access aaa statistics authentication detail | no-more
show network-access aaa statistics radius queue-info | no-more
show network-access aaa statistics radius detail | no-more
show network-access aaa statistics accounting detail | no-more
show network-access aaa statistics authentication detail | no-more
show accounting pending-accounting-stops brief | no-more
```
* *Clear the stats and collect again for 2 iterations.**

```text
clear shmlog entries logname all
clear shmlog statistics logname all
clear network-access aaa statistics radius
clear network-access aaa statistics accounting
clear network-access aaa statistics authentication
clear network-access aaa statistics terminate-code
clear ppp statistics
clear pppoe statistics
```
