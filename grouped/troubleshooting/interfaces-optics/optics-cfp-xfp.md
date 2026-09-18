# Optics CFP and XFP

> Generated deterministically from the approved grouping manifest.


## Source: `formatted/TS_notes/CFP.md`

# CFP

[ Tuesday, June 15, 2021 2:03 PM ] ⁨SVT.Thái.NĐ⁩: mấy case module quang, ví dụ như CFP ở đây: bình thường mình sẽ yêu cầu khách hàng làm hard-loop, soft-loop, đấu thẳng.

[ Tuesday, June 15, 2021 2:03 PM ] ⁨SVT.Thái.NĐ⁩: trong quá trình đó thu thập thông tin sau nhé anh chị em:

[ Tuesday, June 15, 2021 2:03 PM ] ⁨SVT.Thái.NĐ⁩: > start shell pfe network fpc#

# show syslog messages

# show cfp list ### get the cfp id from here and below outputs

# show cfp  alarms

# show cfp  diagnostics

# show cfp  identifier

# show cfp  info

# show cfp  mdio-bus-error-count

# show cmic 0 info

# show cmic 0 interrupts

# show nvram

>> Thử laser on/ laser off CFP bằng câu lệnh:

test cfp  laser  off

test cfp  laser  on

>> Thu thập rsi, var/log:

request support information | save /var/log/rsi-after

file archive compress source /var/log/\* destination /var/tmp/varlogs-jtac.tgz

[ Tuesday, June 15, 2021 2:06 PM ] ⁨SVT.Thái.NĐ⁩: hard-loop là lấy 1 sợi dây đơn -> 1 đầu cắm vào port Tx (transmit), 1 đầu còn lại cắm vào port Rx (receive)

[ Tuesday, June 15, 2021 2:07 PM ] ⁨SVT.Thái.NĐ⁩: soft-loop là dùng câu lệnh để set interface đó Up (không cắm quang)

## Source: `formatted/TS_notes/Xử lý CFP, XFP bị lõi.md`

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

# show mtip-cgpcs summary

# show mtip-cgpcs  registers

# show mtip-cgpcs  errors

# show mtip-cgpcs  error-count

# show mtip-cgpcs  block-lock

# show mtip-cgpcs  fault-condition

# show mtip-cgpcs  high-BER

# show mtip-cgpcs  link-status

* *Note đối với module** ***SFP+*** ***10Gig*:**

# show sfp list ### get the cfp id from here and below outputs

# show sfp  alarms

# show sfp  diagnostics

# show sfp  identifier

# show sfp  info

# show sfp  mdio-bus-error-count

# show mic 0 info

# show mic 0 interrupts

* *Note đối với module** ***XFP 10Gig*:**

# show xfp list ### get the xfp id from here and below outputs

# show xfp  alarms

# show xfp  diagnostics

# show xfp  identifier

# show xfp  info

# show xfp  mdio-bus-error-count

# Check với QSFP 100G:

1. Thực hiện soft-loop, hard-loop (local loop):

> show chassis hardware

> show interfaces diagnostics optics (et-… / xe-…)

> show interfaces (et-… / xe-…)

2. Thu thập RSI, var/log.

3. Gửi hình ảnh của moudule đang bị lỗi.

4. Thu thập các tập lệnh output sau trong trường hợp hard-loop:

- --

The 'PCI Fatal' errors seen above do not represent an actual hardware issue with the MIC or router. The following commands may help identify the presence of any faulty SFPs:

|  |
| --- |
| > start shell pfe network afeb0  # show sfp list  # show sfp  info  Check i2c failure count on each SFP. If the SFP shows a non-zero i2c failure count, replace that specific SFP.  # show sfp 3 info  show sfp 3 info  index: 0x03  sfp name: MIC(0/1)  pic context: 0x4CD44248  id mem scanned: false  linkstate: Up  sfp\_present: false  sfp\_changed: false  i2c failure count: 0x3C <<<--- non-zero  diag polling count: 0x8D42  no diag polling from RE:0x1  run\_periodic: false |

## Source: `formatted/TS_notes/SNMP interface jnxDom (laser) MIB OID.md`

# SNMP interface jnxDom (laser) MIB OID

show snmp mib walk [1.3.6.1.4.1.2636.3.60.1.2.1.1](http://1.3.6.1.4.1.2636.3.60.1.2.1.1)

jnxDomCurrentLaneTxLaserOutputPower - 1.3.6.1.4.1.2636.3.60.1.2.1.1.8

jnxDomCurrentLaneRxLaserPower - 1.3.6.1.4.1.2636.3.60.1.2.1.1.6
