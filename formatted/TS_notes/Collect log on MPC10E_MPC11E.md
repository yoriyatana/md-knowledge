# Collect log on MPC10E/MPC11E

Please upload the following logs to further investigate

a) request support information| save /var/tmp/rsiCURRENTDATE.txt

b) Get the var/log folder using command example: file archive compress source /var/log/\* destination /var/tmp/CURRENT-DATE.tgz

c) FPC10 shell logs

start shell pfe network fpc10.0

set syslog tty disable

show version

show nvram

show syslog messages

show hsl2 statistics crc  <

show hsl2 statistics         <

show pfe statistics error <

show cmerror module brief

exit

d) Collect the linux host logs of FPC10 using the procedure outlined below:

Login to the device using root credentials:

* start shell user root*

* rlogin -Ji fpc10*

* tar -zcvf /var/tmp/fpc10.tar.gz /var/log/\**

* *Copy /var/log from linux host of FPC to RE**

rcp /var/tmp/fpc10.tar.gz [128.0.0.1:/var/tmp](https://128.0.0.1:/var/tmp)

Dạ nhờ các anh @⁨Trực ca INOC2-KTM-VNPT Net⁩  lấy thêm giúp em /var/log dưới Linux host của card FPC10 này luôn ạ:

start shell user root command "set SLOT = 10 ; rsh -Ji fpc${SLOT} "find /var/log/ -type f | xargs tar -czvf - " > /var/tmp/fpc${SLOT}\_var\_log-HCM-GNIX.tgz"

=>>> Sau đó lấy file /var/tmp/fpc10\_var\_log-HCM-GNIX.tgz và đẩy lên FTP giúp em với ạ.
