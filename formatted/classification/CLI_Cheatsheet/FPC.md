# FPC

- RSI và var/log thiết bị
- Core-dump nếu có
- Output các câu lệnh sau:

show log messages | no-more

show log messages.0.gz  | no-more

show log messages.1.gz | no-more

show log messages.2.gz | no-more

show log messages.3.gz | no-more

show log chassisd | no-more

show log chassisd .0.gz | no-more

show log chassisd.1.gz | no-more

show log chassisd.2.gz | no-more

show log chassisd.3.gz | no-more

- --

## Regarding to FPC

show chassis hardware | no-more

show chassis alarm | no-more

show version | no-more

show chassis fpc | no-more

show chassis fpc pic-status | no-more

show chassis fpc errors | no-more

show chassis fabric fpcs  | no-more

show chassis fabric plane  | no-more

show chassis fabric summary  | no-more

show chassis fabric map | no-more

show chassis fabric plane-location | no-more

show chassis fabric destinations | no-more

show system resource-monitor fpc | no-more

show pfe statistics traffic  | no-more

show pfe statistics traffic detail  | no-more

show pfe statistics error | no-more

- --

### PFE level information

request pfe execute command "show syslog messages" target fpc0 | no-more

request pfe execute command "show nvram" target fpc0 | no-more

request pfe execute command "show ttp statistics" target fpc0 | no-more

request pfe execute command "show hsl2 statistics" target fpc0 | no-more

request pfe execute command "show hsl2 statistics crc" target fpc0 | no-more

request pfe execute command "show cmerror module" target fpc0 | no-more

request pfe execute command "show sched" target fpc0 | no-more

request pfe execute command "show threads cpu" target fpc0 | no-more

request pfe execute command "show jnh 0 exceptions" target fpc0 | no-more

- --

>start shell pfe network fpc8

### show hsl2 statistics

# show cmerror level

# show cmerror module brief

# show cmerror module <id> <<<< replace with the id collected from above command where you see the errors

# show cmerror statistics

### show syslog messages

### show nvram

- --

@⁨SVT.Tung.NT⁩ cái log lỗi chỗ Viettel, chắc em nhờ họ kiểm tra và lấy thêm mấy file ppe trap, nếu có phát sinh.

Fru

jnxFruOfflineReason 2: N/A

jnxFruOfflineReason 7 người tác động

- --

Như trao đổi meeting, anh gửi list command collect thông tin về memory firewall đang sử dụng trên các thiết bị mình định apply sampling:

|1. operation command collect

show chassis fpc

show system resource-monitor fpc

show system resource-monitor summary

1. Pfe shell commands to collect thông tin trên các linecard của thiết bị:

show jnh 0 pool

show jnh 0 pool detail

show jnh 0 pool usage

show jnh 0 pool composition

show jnh 0 pool layout

show heap 0

show heap 0 accounting pc size

show heap 0 accounting rates

show route summary

show nhdb management all

show route manager statistics

show piles

show packet

show packet statistics

show heap 1

show syslog messages
|
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

- --

Overall health check:

show chassis fabric summary

show chassis fabric plane

show system coredump

cpu RE/FPC/process

memory: RE/FPC

interface:

- thu/phát quang

- show interface ge/xe/et/ae/... extensive - at least 2 times

- traffic rate: pps & bps uplink interfaces

- traffic rate: pps & bps downlink interfaces

error fpc: enable/disable & counter

bổ sung dịch vụ multicast

vpls:

- check mac learning per interface

- check mac learning per instance

L3VPN

- Arp per interface & per instance
