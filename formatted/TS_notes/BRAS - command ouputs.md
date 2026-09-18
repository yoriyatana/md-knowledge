# BRAS - command ouputs

Dạ anh Tú,

Em xin summary case này như sau:

+ khoảng chục thuê bao có hiện trạng online chậm, ghi nhận vào thời điểm 20h-21h

Nhờ anh Tú gửi thêm giúp em các thông tin dưới đây anh nhé:

+ Các output: (thực hiện trước khi lấy varlog)

```text
show shmlog entries logname all | save  /var/log/shmentries1.txt
```

```text
show shmlog statistics logname all | save /var/log/shmstatistics1.txt
```

+ RSI brief, varlog của box.

+ Graph CPU, memory của RE, linecard 1 ngày trở lại đây.

Bên em có thể sẽ cần onsite **vào thời điểm lỗi** này ngày mai để lấy thông tin, các thông tin cần lấy theo các bước dưới đây:

1. **Xác định thuê bao lỗi.**

2. **Traceoptions of authd/pppoe/ppp/smgd trong vòng 10 phút**

```text
set system processes general-authentication-service traceoptions file trace\_general-authentication
```

```text
set system processes general-authentication-service traceoptions file size 50m
```

```text
set system processes general-authentication-service traceoptions file files 10
```

```text
set system processes general-authentication-service traceoptions flag all
```

```text
set system processes smg-service traceoptions file trace\_smg-service
```

```text
set system processes smg-service traceoptions file size 100m
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
set protocols ppp-service traceoptions file trace\_ppp-service
```

```text
set protocols ppp-service traceoptions file size 50m
```

```text
set protocols ppp-service traceoptions file files 10
```

```text
set protocols ppp-service traceoptions flag all
```

```text
set protocols ppp-service traceoptions level all
```

```text
set protocols pppoe traceoptions file trace\_pppoe
```

```text
set protocols pppoe traceoptions file size 50m
```

```text
set protocols pppoe traceoptions file files 10
```

```text
set protocols pppoe traceoptions flag all
```

```text
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
```

```text
show shmlog statistics logname all | save /var/tmp/shmstatistics1.txt
```

wait for a 2 minutes and collect

```text
show shmlog entries logname all | save  /var/tmp/shmentries2.txt
```

```text
show shmlog statistics logname all | save /var/tmp/shmstatistics2.txt
```

6. **CLI logs :  ( the logging could change based on the issue) here are logs to start with.**

```text
set cli timestamp
```

```text
show subscribers summary | no-more
```

```text
show subscribers summary port | no-more
```

```text
show subscribers summary slot | no-more
```

```text
show subscribers summary all | no-more
```

```text
show system alarms | no-more
```

```text
show chassis fpc |no-more
```

```text
show chassis fpc detail | no-more
```

```text
show chassis alarms | no-more
```

```text
show chassis routing-engine | no-more
```

```text
show system subscriber-management info  | no-more
```

```text
show system subscriber-management summary | no-more
```

```text
show system subscriber-management detail | no-more
```

```text
show system subscriber-management statistics all extensive | no-more
```

```text
show system configuration database usage | no-more
```

```text
show shm-ipc statistics | no-more
```

```text
show shmlog statistics logname all | match fail | no-more
```

```text
show shmlog statistics logname all | match err | no-more
```

```text
show system resource-monitor summary | no-more
```

```text
show system process extensive |no-more
```

```text
show pppoe statistics | no-more
```

```text
show pppoe statistics | no-more
```

```text
show ddos-protection protocols violations | no-more
```

```text
show ddos-protection protocols statistics terse | no-more
```

```text
show ddos-protection protocols pppoe padi | no-more
```

```text
show ddos-protection protocols pppoe | no-more
```

```text
clear pppoe statistics
```

```text
show pppoe statistics | no-more
```

```text
show pppoe statistics | no-more
```

```text
show subscribers summary | no-more
```

```text
show subscribers summary port | no-more
```

```text
show subscribers summary slot | no-more
```

```text
show subscribers summary | no-more
```

```text
show system subscriber-management statistics all extensive | no-more
```

```text
show shm-ipc statistics | no-more
```

start shell csh command "vty -c 'show smd throttle' -s 7208 128.0.0.1"

```text
show system subscriber-management statistics all extensive | no-more
```

```text
show network-access aaa terminate-code brief | no-more
```

```text
show network-access aaa terminate-code detail | no-more
```

```text
show network-access aaa statistics address-assignment pool ftth\_private routing-instance VRF\_CGNAT | no-more
```

```text
show network-access aaa statistics authentication detail | no-more
```

```text
show network-access aaa statistics radius queue-info | no-more
```

```text
show network-access aaa statistics radius detail | no-more
```

```text
show network-access aaa statistics accounting detail | no-more
```

```text
show network-access aaa statistics authentication detail | no-more
```

```text
show network-access memory-pools | no-more
```

```text
show subscribers summary | no-more
```

```text
show pppoe statistics | no-more
```

```text
show ppp statistics detail | no-more
```

```text
show pppoe statistics | no-more
```

```text
show ppp statistics detail | no-more
```

```text
show shmlog statistics logname all | match fail | no-more
```

```text
show shmlog statistics logname all | match err | no-more
```

```text
show subscribers summary | no-more
```

```text
show subscribers summary port | no-more
```

```text
show subscribers summary slot | no-more
```

```text
show subscribers summary | no-more
```

```text
show system subscriber-management statistics all extensive | no-more
```

```text
show shm-ipc statistics | no-more
```

```text
show system process extensive |no-more
```

```text
show ddos-protection protocols statistics terse | no-more
```

start shell csh command "vty -c 'show smd throttle' -s 7208 128.0.0.1"

```text
show network-access aaa statistics address-assignment pool ftth\_private routing-instance VRF\_CGNAT | no-more
```

```text
show network-access aaa statistics authentication detail | no-more
```

```text
show network-access aaa statistics radius queue-info | no-more
```

```text
show network-access aaa statistics radius detail | no-more
```

```text
show network-access aaa statistics accounting detail | no-more
```

```text
show network-access aaa statistics authentication detail | no-more
```

```text
show accounting pending-accounting-stops brief | no-more
```

* *Clear the stats and collect again for 2 iterations.**

```text
clear shmlog entries logname all
```

```text
clear shmlog statistics logname all
```

```text
clear network-access aaa statistics radius
```

```text
clear network-access aaa statistics accounting
```

```text
clear network-access aaa statistics authentication
```

```text
clear network-access aaa statistics terminate-code
```

```text
clear ppp statistics
```

```text
clear pppoe statistics
```
