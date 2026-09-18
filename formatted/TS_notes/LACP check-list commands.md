# LACP check-list commands

Phía MX:

1. Apply traceoptions LACP và PPM trên cả 4 thiết bị QFX & MX.

2. Thu thập thông tin và enable event-options để MX tự động thu thập log khi có trigger liên quan đến event lacpd\_timeout và lacp\_intf\_down.

3. Thu thập thông tin dưới shell mode và kernel

[ Thursday, January 13, 2022 11:13 AM ] ⁨SVT.Thái.NĐ⁩: 1. Enable cli timestamp

set cli timestamp

2. Enable lacp traceoptions and reproduce the issue

set protocols lacp traceoptions file lacpd.log size 1g world-readable

set protocols lacp traceoptions flag all

set routing-options ppm traceoptions flag al

set routing-options ppm traceoptions file ppmd.log size 1g

3. Take multiple output of below commands in RE.

show lacp interfaces extensive

show lacp statistics interfaces

show interfaces ae | match flap

show lacp timeouts (multiple times)

show ppm adjacencies protocol lacp detail

show ppm transmissions protocol lacp detail

show ppm adjacencies protocol lacp

show ppm transmissions protocol lacp

4. Go to PFE shell using any of the below-mentioned methods

a. While at the CLI prompt

start shell pfe network fpc

OR

b. While at the FreeBSD prompt of RE

vty fpc

clear ppm statistics first before collecting any data.

set ppm utrace protocol lacp

set ppm utrace protocol lacp

set ppm utrace tcpdump

debug ppm protocol lacp level 3

set ppm utrace proto

set ppm utrace protocol lacp

set ppm utrace all

debug ppm protocol lacp level 3

show ukern\_trace handles <<<<

search for PPM handle <<<<

set ukern\_trace  level extensive

set ukern\_trace  logging enable

set ukern\_trace  buffer 100000000

set ukern\_trace  printf enable

Above debugs will be coming continuously. keep separate console and collect the above debugs running on both DUT and PEER device through out the logs collection.

Take multiple output of below commands in while in PFE shell?. Take these commands without timedelay

Collect these clis using cprod.

at the start of the logs collection on both sides on PFEs. >> clear ppm statistics

show ppm statistics protocol lacp

show ppm adjacencies protocol lacp

show ppm transmits protocol lacp

show ppm statistics detail

freebsd promt:

copy paste the clis continuously for few times.

date

cprod -A fpc -c "show sched"

date

cprod -A fpc -c "show threads cpu"

date

cprod -A fpc -c "show ttp statistics"

date

cprod -A fpc -c " show ppm statistics"

date

PFE BCM commands to Collect.

HW( "show c cpu" & "show c") -> ("show halp-pkt pkt-stats") ->  "show ttp statistics" -> use tcp-dump etc.

Below are the commands.

VTY: Both Device.

show halp-pkt asic-queues

show dcbcm ifd all

show halp-pkt hostpath-cfgs

show halp-pkt pkt-stats    << Multiple outputs.

If drop is seen on PFE-SHIM/HALP, there are commands to enable debug. "debug halp-pkt tx/rx".

Output of "debug halp tx/rx" can be seen in as below

FPC0(PE-3 vty)# show ukern\_trace handles

FPC0(PE-3 vty)# show ukern\_trace 13

[Tue Oct 13 10:42:24.314] [9430] brcm\_rx\_init:408 (init) rx init done

[Tue Oct 13 10:42:24.314] [9431] brcm\_tx\_init:441 (init) tx init done

[Tue Oct 13 10:42:24.317] [9432] brcm\_pkt\_fastpath\_init:754 (init) pkt fp thread started

[Fri Oct 23 04:04:02.702] [13917] brcm\_pkt\_debug\_tx:1827 (tx\_api\_entry) pkt 0xaf5f0178  ifd  idx 656 len 74

proto 0 ifl\_inp 0 hint 40009001 msec 840115082

18 2a d3 9c d8 35 78 4f 9b eb fc d1 08 00 45 c0 00 3c d2 51 00 00 01 2e 8e 61 ab 0a 01 06 ab 0a

01 07 11 14 bc 3d 01 00 00 28 00 0c 16 01 1b d7 9c 5e e6 ab 73 68 00 0c 83 01 00 00 00 00 00 00

[Fri Oct 23 04:04:02.867] [13918] brcm\_pkt\_debug\_tx:1827 (tx\_api\_entry) pkt 0xaf5f0178  ifd  idx 656 len 85

proto 0 ifl\_inp 0 hint 9001 msec 840115247

However if drop is in HW/BCM then need to check why HW is dropping.

BCM(sad)Both Device)

Show c

Show c cpu

tcpdump -ni

Lấy giúp em các output dưới đây (ở mức shell) vào giờ thấp điểm, và chạy từng lệnh một:

set cli screen-length 0

## Check linecard shell-mode

request pfe execute command "show syslog messages" target fpc2

request pfe execute command "show nvram" target fpc2

request pfe execute command "show cmerror module" target fpc2

request pfe execute command "show hsl2 statistics" target fpc2

request pfe execute command "show hsl2 statistics crc" target fpc2

request pfe execute command "show threads cpu" target fpc2

request pfe execute command "show sched" target fpc2

>>>> take this output 3 times in the interval of 30secs

request pfe execute command "show ppm transmits protocol lacp" target fpc2

request pfe execute command "show ppm adjacencies protocol lacp" target fpc2

request pfe execute command "show ppm statistics protocol lacp" target fpc2

## Check linecard shell-mode

request pfe execute command "show syslog messages" target fpc4

request pfe execute command "show nvram" target fpc4

request pfe execute command "show cmerror module" target fpc4

request pfe execute command "show hsl2 statistics" target fpc4

request pfe execute command "show hsl2 statistics crc" target fpc4

request pfe execute command "show threads cpu" target fpc4

request pfe execute command "show sched" target fpc4

>>>> take this output 3 times in the interval of 30secs

request pfe execute command "show ppm transmits protocol lacp" target fpc4

request pfe execute command "show ppm adjacencies protocol lacp" target fpc4

request pfe execute command "show ppm statistics protocol lacp" target fpc4

# ------------------------

set cli screen-length 30
