# Optics, CFP, XFP & Physical Layer Diagnostics

> Generated deterministically from the approved grouping manifest.


## Source: `formatted/TS_notes/10GbE LAN-PHY_40GbE_100GbE LFS (Link fault signalling).md`

# 10GbE LAN-PHY/40GbE/100GbE LFS (Link fault signalling)

```text
10GbE LAN-PHY/40GbE/100GbE LFS operates between remote Reconciliation Sublayers (RS) and local RS. Link faults detected between remote RSs and local RSs are received by local RSs. Only the RS originates Remote Fault signals. When this Local Fault status reaches an RS, the RS stops sending MAC data, and continuously generates a Remote Fault status on the transmit data path. When Remote Fault status is received by an RS, the RS stops sending MAC data, and continuously generates Idle control characters. When the RS no longer receives fault status messages, it returns to normal operation, sending MAC data
```
![](../../../assets/optics-physical/c5fe9577fa-a29c8b33b3303696d0641b4e0f996313)

![](../../../assets/optics-physical/b775079e65-56fd4a9d253fc2834603fafb0e64d8e5)

![](../../../assets/optics-physical/cba69894db-1c9c67fbaf70d67ac3e2bdd28d79c141)

![](../../../assets/optics-physical/b7c73abdac-4fb016033ce3685396eacd9e69017339)

## Source: `formatted/TS_notes/BUG Hold-time down không hoạt động được nếu cấu hình nhỏ hơn 1s trên interface chạy WANPHY.md`

# BUG Hold-time down không hoạt động được nếu cấu hình nhỏ hơn 1s trên interface chạy WANPHY

Hi Team,

Junos từ 18 đến 20.4R3-S4 đang có bug với các interface đang bật WANPHY đồng thời cấu hình hold-time down với thời gian nhỏ hơn 1 giây thì sẽ gây flap interface nếu nháy truyền dẫn, tức là hold-time down không hoạt động đúng mong đợi. Hiện tại, lỗi này chưa biết được trigger nên chưa có kế hoạch để có thể fix trên Junos.

Hiện tại ghi nhận được bug không gặp trong các trường hợp sau:

- Ở Junos 17.x

- Interface chạy mode LANPHY

- Chạy WANPHY nhưng không cấu hình hold-time down hoặc có cấu hình nhưng thời gian tầm 2 giây trở lên.

Workaround cho lỗi này thì có thể cân nhắc 2 option bên dưới:

1/. Thay đổi thành interface từ mode WANPHY -> LANPHY. giải pháp này cần kiểm tra thêm đầu truyền dẫn xem có hỗ trợ mode này hay không

2/. Tăng hold-time down lên khoảng 2s: giải pháp này thì có thể sẽ gây blackhole traffic trong khoảng thời gian hold-time down. (thực tế test ở lab, theo Hoàng NWHNI kiểm tra thì khi set hold-time down tầm 1,5 giây thì vẫn gây flap).

Chi tiết về case này, Hoàng NWHNI có làm việc với JTAC qua case 2022-0731-520372 - đồng thời thực hiện test Lab với kết quả rất chi tiết ở mail dưới. AE xem thêm để nắm bug của lỗi này để tránh/hạn chế gặp trên các Junos hiện tại.

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

```text
>> Thử laser on/ laser off CFP bằng câu lệnh:
test cfp  laser  off
test cfp  laser  on
>> Thu thập rsi, var/log:
request support information | save /var/log/rsi-after
file archive compress source /var/log/\* destination /var/tmp/varlogs-jtac.tgz
```
[ Tuesday, June 15, 2021 2:06 PM ] ⁨SVT.Thái.NĐ⁩: hard-loop là lấy 1 sợi dây đơn -> 1 đầu cắm vào port Tx (transmit), 1 đầu còn lại cắm vào port Rx (receive)

[ Tuesday, June 15, 2021 2:07 PM ] ⁨SVT.Thái.NĐ⁩: soft-loop là dùng câu lệnh để set interface đó Up (không cắm quang)

## Source: `formatted/TS_notes/SNMP interface jnxDom (laser) MIB OID.md`

# SNMP interface jnxDom (laser) MIB OID

```text
show snmp mib walk [1.3.6.1.4.1.2636.3.60.1.2.1.1](http://1.3.6.1.4.1.2636.3.60.1.2.1.1)
```
jnxDomCurrentLaneTxLaserOutputPower - 1.3.6.1.4.1.2636.3.60.1.2.1.1.8

jnxDomCurrentLaneRxLaserPower - 1.3.6.1.4.1.2636.3.60.1.2.1.1.6

## Source: `formatted/TS_notes/Xử lý CFP, XFP bị lõi.md`

# Xử lý CFP, XFP bị lõi

* *1. Thực hiện soft-loop & hard-loop (loop local), thu thập thông tin sau:**

```text
show chassis hardware
show interfaces diagnostics optics (et-… / xe-…)
show interfaces (et-… / xe-…)
```
- Note câu lệnh soft-loop:

```text
set interfaces  gigether-options loopback
```
* *2. Thu thập tập lệnh output sau trong 2 trường hợp** **soft-loop** **và** **hard-loop**

* *Note đối với module** ***CFP 100Gig*:**

```text
> start shell pfe network fpc#
```
# show syslog messages

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

```text
> start shell pfe network fpc#
```
# show xfp list ### get the xfp id from here and below outputs

# show xfp  alarms

# show xfp  diagnostics

# show xfp  identifier

# show xfp  info

# show xfp  mdio-bus-error-count

# Check với QSFP 100G:

1. Thực hiện soft-loop, hard-loop (local loop):

```text
> show chassis hardware
> show interfaces diagnostics optics (et-… / xe-…)
> show interfaces (et-… / xe-…)
```
2. Thu thập RSI, var/log.

3. Gửi hình ảnh của moudule đang bị lỗi.

4. Thu thập các tập lệnh output sau trong trường hợp hard-loop:

- --

The 'PCI Fatal' errors seen above do not represent an actual hardware issue with the MIC or router. The following commands may help identify the presence of any faulty SFPs:

|  |
| --- |
| > start shell pfe network afeb0  # show sfp list  # show sfp  info  Check i2c failure count on each SFP. If the SFP shows a non-zero i2c failure count, replace that specific SFP.  # show sfp 3 info  show sfp 3 info  index: 0x03  sfp name: MIC(0/1)  pic context: 0x4CD44248  id mem scanned: false  linkstate: Up  sfp\_present: false  sfp\_changed: false  i2c failure count: 0x3C <<<--- non-zero  diag polling count: 0x8D42  no diag polling from RE:0x1  run\_periodic: false |

## Source: `formatted/TS_notes/interfaces diagnostics optics.md`

# interfaces diagnostics optics

######

```text
Show cfp :
```
MX2010-ADV-NPE-01:

```text
> show interfaces extensive et-6/0/0 | no-more
> show interfaces diagnostics optics et-6/0/0 | no-more
> start shell pfe network fpc6
```
# show cfp list

# exit

###### #########

MX2010-GDI-P-01:

```text
> show interfaces extensive et-3/0/1 | no-more
> show interfaces diagnostics optics et-3/0/1 | no-more
> start shell pfe network fpc3
```
# show cfp list

## Source: `formatted/TS_notes/set link-speed 100G cho interface ae với et-8 interface.md`

# set link-speed 100G cho interface ae với et-8 interface

![](../../../assets/optics-physical/5cc96a11cc-8978cf3f97651ac41f377624e9931b65.png)
