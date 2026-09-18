# Xử lý CFP, XFP bị lõi

* *1. Thực hiện soft-loop & hard-loop (loop local), thu thập thông tin sau:**

show chassis hardware

show interfaces diagnostics optics (et-… / xe-…)

show interfaces (et-… / xe-…)

- Note câu lệnh soft-loop:

set interfaces  gigether-options loopback

* *2. Thu thập tập lệnh output sau trong 2 trường hợp** **soft-loop** **và** **hard-loop**

* *Note đối với module** ***CFP 100Gig*:**

> start shell pfe network fpc#

# show syslog messages

# show cfp list                ### get the cfp id from here and below outputs

# show cfp  alarms

# show cfp  diagnostics

# show cfp  identifier

# show cfp  info

# show cfp  mdio-bus-error-count

# show cmic 0 info

# show cmic 0 interrupts

# show mtip-cgpcs summary

# show mtip-cgpcs  registers

# show mtip-cgpcs  errors

# show mtip-cgpcs  error-count

# show mtip-cgpcs  block-lock

# show mtip-cgpcs  fault-condition

# show mtip-cgpcs  high-BER

# show mtip-cgpcs  link-status

# show syslog messages

# show nvram

* *Note đối với module** ***SFP+*** ***10Gig*:**

> start shell pfe network fpc#

# show syslog messages

# show sfp list ### get the cfp id from here and below outputs

# show sfp  alarms

# show sfp  diagnostics

# show sfp  identifier

# show sfp  info

# show sfp  mdio-bus-error-count

# show mic 0 info

# show mic 0 interrupts

# show mtip-cgpcs summary

# show mtip-cgpcs  registers

# show mtip-cgpcs  errors

# show mtip-cgpcs  error-count

# show mtip-cgpcs  block-lock

# show mtip-cgpcs  fault-condition

# show mtip-cgpcs  high-BER

# show mtip-cgpcs  link-status

# show syslog messages

# show nvram

* *Note đối với module** ***XFP 10Gig*:**

> start shell pfe network fpc#

# show xfp list ### get the xfp id from here and below outputs

# show xfp  alarms

# show xfp  diagnostics

# show xfp  identifier

# show xfp  info

# show xfp  mdio-bus-error-count

# show mic 0 info

# show mic 0 interrupts

# show mtip-cgpcs summary

# show mtip-cgpcs  registers

# show mtip-cgpcs  errors

# show mtip-cgpcs  error-count

# show mtip-cgpcs  block-lock

# show mtip-cgpcs  fault-condition

# show mtip-cgpcs  high-BER

# show mtip-cgpcs  link-status

# show syslog messages

# show nvram

# Check với QSFP 100G:

1. Thực hiện soft-loop, hard-loop (local loop):

> show chassis hardware

> show interfaces diagnostics optics (et-… / xe-…)

> show interfaces (et-… / xe-…)

2. Thu thập RSI, var/log.

3. Gửi hình ảnh của moudule đang bị lỗi.

4. Thu thập các tập lệnh output sau trong trường hợp hard-loop:

> start shell pfe network fpc#

# show syslog messages

# show cfp list ### get the cfp id from here and below outputs

# show cfp  alarms

# show cfp  diagnostics

# show cfp  identifier

# show cfp  info

# show cfp  mdio-bus-error-count

# show cmic 0 info

# show cmic 0 interrupts

# show mtip-cgpcs summary

# show mtip-cgpcs  registers

# show mtip-cgpcs  errors

# show mtip-cgpcs  error-count

# show mtip-cgpcs  block-lock

# show mtip-cgpcs  fault-condition

# show mtip-cgpcs  high-BER

# show mtip-cgpcs  link-status

# show syslog messages

# show nvram

- --

The 'PCI Fatal' errors seen above do not represent an actual hardware issue with the MIC or router. The following commands may help identify the presence of any faulty SFPs:

|  |
| --- |
| > start shell pfe network afeb0  # show sfp list  # show sfp  info  Check i2c failure count on each SFP. If the SFP shows a non-zero i2c failure count, replace that specific SFP.  # show sfp 3 info  show sfp 3 info  index: 0x03  sfp name: MIC(0/1)  pic context: 0x4CD44248  id mem scanned: false  linkstate: Up  sfp\_present: false  sfp\_changed: false  i2c failure count: 0x3C <<<--- non-zero  diag polling count: 0x8D42  no diag polling from RE:0x1  run\_periodic: false |
