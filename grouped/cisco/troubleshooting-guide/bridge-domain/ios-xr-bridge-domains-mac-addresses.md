# Cisco IOS-XR Bridge Domains and MAC Addresses

## Source: `formatted/TS_notes/IOS-XR Bridge Domains _ MAC Addresses.md`

**BD Overview**

Even though bridge domains are children of bridge groups, the show command on the CLI requires one to specify the bridge domain name first, then the bridge group (i.e., specifying from bottom and going up up the heirarchy, rather than the top down, which feels weird):

```cisco
show l2vpn bridge-domain bd-name ZTP group ZTP
```
**MAC Addresses**

Why type `show mac address VLAN foo` when you can type:

```cisco
show l2vpn forwarding bridge-domain ZTP:ZTP mac-address location 0/0/CPU0
```
**MAC Addresses**

```cisco
show l2vpn forwarding bridge-domain ZTP:ZTP mac-address location 0/0/CPU0
```
- --

## 1.    Kiểm tra học MAC trên Metro AGG, SRT

|  |  |  |
| --- | --- | --- |
| **Thiết bị** | **Câu lệnh** | **Ý nghĩa** |
| Metro AGG ASR903 | Kiểm tra học MAC trong bride-domain | |
| show mac-address-table bdomain | kiểm tra học MAC trong bridge-domain  đảm bảo có MAC trên port downlink và qua PW |
| Clear MAC trong bridge-domain | |
| clear mac-address-table bdomain | xóa MAC trong bridge-domain để kiểm tra MAC có học lại không |

## 2.    Kiểm tra học MAC trên Metro Core

|  |  |  |
| --- | --- | --- |
| **Thiết bị** | **Câu lệnh** | **Ý nghĩa** |
| Metro Core ASR9010 | Kiểm tra học MAC trong bride-domain | |
| show l2vpn forwarding bridge-domain :  mac-address location 0/0/CPU0 | kiểm tra học MAC trong bridge-domain  đảm bảo có MAC trên port downlink và qua PW |
| Clear MAC trong bridge-domain | |
| clear l2vpn forwarding mac-address-table bridge-domain : location 0/0/CPU0 | xóa MAC trong bridge-domain để kiểm tra MAC có học lại không |

## 3.    Kiểm tra các member thuộc bridge-domain

|  |  |  |
| --- | --- | --- |
| **Thiết bị** | **Câu lệnh** | **Ý nghĩa** |
| Metro AGG ASR903 | Kiểm tra các member thuộc bridge-domain | |
| show bridge-domain | kiểm tra các member thuộc brigde-domain  phải đảm bảo chứa service-instance, có PW nối đến các MA khác |

Output câu lệnh
```cisco
HCM100.MA01#show bridge-domain 3649

Bridge-domain 3649 (7 ports in all)


State: UP                    Mac learning: Enabled
Aging-Timer: 300 second(s)

Maximum address limit: 16000

Port-channel3 service instance 3649

Port-channel4 service instance 3649

Port-channel18 service instance 3649

vfi VMS-3649 neighbor 172.20.96.22 26048

vfi VMS-3649 neighbor 172.20.96.23 26048

vfi VMS-3649 neighbor 172.20.96.34 26048

vfi VMS-3649 neighbor 172.20.96.28 26048
```
## 4.    Kiểm tra PW trong VFI MA, SRT

|  |  |  |
| --- | --- | --- |
| Thiết bị | Câu lệnh | Ý nghĩa |
| Metro AGG ASR903 | Kiểm tra trạng thái PW trong VFI | |
| show l2vpn vfi name | kiểm tra PW trong vfi  yêu cầu vfi phải UP  yêu cầu các PW phải báo hiệu được local label, remote label  kiểm tra giá trị ve-id |

```cisco
HCM100.MA01#show l2vpn vfi name VMS-3649

Legend: RT=Route-target, S=Split-horizon, Y=Yes, N=No


VFI name: VMS-3649, state: up, type: multipoint, signaling: BGP

VPN ID: 26048, VE-ID: 22, VE-SIZE: 100


RD: 172.20.96.24:26048, RT: 45903:26048, 45903:26048,

Bridge-Domain 3649 attachment circuits:

Pseudo-port interface: pseudowire100502

Interface          Peer Address    VE-ID  Local Label  Remote Label    S

pseudowire102552   172.20.96.28    26     26827        4153            Y

pseudowire102340   172.20.96.34    54     26855        26684           Y

pseudowire102198   172.20.96.23    21     26822        7417            Y

pseudowire101928   172.20.96.22    27     26828        288340          Y
```
## 5.    Kiểm tra PW trong bridge-domain MC

|  |  |  |
| --- | --- | --- |
| Thiết bị | Câu lệnh | Ý nghĩa |
| ASR9010 | Kiểm tra trạng thái PW | |
| show l2vpn bridge-domain bd-name | hiển thị trạng thái PW trong bridge-domain |

```cisco
RP/0/RSP1/CPU0:HCM.MC02#show l2vpn bridge-domain bd-name L2VPN-TAKEDA-VL890

Tue Jan 23 10:56:15.761 HaNoi

Legend: pp = Partially Programmed.


Bridge group: L2VPN, bridge-domain: L2VPN-TAKEDA-VL890, id: 610, state: up, ShgId: 0, MSTi: 0
Aging: 300 s, MAC limit: 4000, Action: none, Notification: syslog

Filter MAC addresses: 0


ACs: 1 (1 up), VFIs: 0, PWs: 2 (2 up), PBBs: 0 (0 up)

List of ACs:


BE5.890, state: up, Static MAC addresses: 0

List of Access PWs:


Neighbor 172.20.96.24 pw-id 30312, state: up, Static MAC addresses: 0
Neighbor 172.20.98.35 pw-id 30312, state: up, Static MAC addresses: 0

List of VFIs:
```
## 6.    Kiểm tra cấu hình khai báo trên Switch AGG, MA, SRT

|  |  |  |
| --- | --- | --- |
| Thiết bị | Câu lệnh | Ý nghĩa |
| ASR903,  ASR920 | Kiểm tra cấu hình service-instance, bridge-domain | |
| show run |  section | hiển thị tất cả cấu hình liên quan đến vlan dịch vụ  hiện thị được khai báo service-instance, bridge-domain vì quy hoạch bằng giá trị vlan |
| Kiểm tra cấu hình VFI | |
| show run |  section | hiển thị cấu hình liên quan đến vfi |

```cisco
HCM100.SRT01#show running-config | section 2607

l2vpn vfi context L2VPN-ISHCMC-VL2607

vpn id 27508

mtu 9000

autodiscovery bgp signaling bgp

ve id 72

ve range 100

rd 172.20.98.33:27508

route-target export 45903:27508

route-target import 45903:27508

bridge-domain 2607

member GigabitEthernet0/0/1 service-instance 2607

member vfi L2VPN-ISHCMC-VL2607

description "[L2VPN][ISHHCM][VL2607][92-Nguyen-Huu-Canh]

service instance 2607 ethernet

encapsulation untagged

HCM100.SRT01#show running-config | section L2VPN-ISHCMC-VL2607
```

## 7.    Kiểm tra ping từ MA, SRT đến IP khách hàng

|  |  |  |
| --- | --- | --- |
| Thiết bị | Câu lệnh | Ý nghĩa |
| ASR903,  ASR920 | Khai báo IP trên interface BDI, lưu ý: chỉ ping được từ BDI đến IP khách hàng khi có khai rewrite trong service-instance MA | |
| interface | khai báo IP trên interface BDI  giá trị BDI-ID trùng vói bridge-domain |
| ip address | khai báo địa chỉ IP thuộc subnet LAN khách hàng |
| no shut | bật interface BDI, default sau khai báo thiết bị shutdown interface BDI |
| ping đến IP khách hàng | |
| ping |  |

- --

```cisco
show mpls l2transport vc vcid 27188
show l2vpn vfi name
show ethernet service instance interface be17
show l2vpn atom vc
```
- --

<https://www.cisco.com/c/en/us/support/docs/routers/asr-9000-series-aggregation-services-routers/116453-technote-ios-xr-l2vpn-00.html>
```cisco
sh int gig 0/1/0/1

sh l2vpn xconnect group test

sh l2vpn xconnect group test det

sh l2vpn forwarding interface gigabitEthernet 0/1/0/1 hardware ingress detail location 0/1/CPU0

sh l2vpn forwarding interface Te 0/0/0/3 hardware egress detail location 0/0/CPU0

sh run int gig 0/0/0/1

sh run l2vpn xconnect group test

sh l2vpn xconnect detail

sh run interface GigabitEthernet0/1/0/1.1

sh l2vpn xconnect group test xc-name p2p4 detail

sh mpls forwarding labels 16026

show l2vpn bridge-domain group customer1 bd-name engineering

show l2vpn bridge-domain group customer1 bd-name engineering det

show l2vpn forwarding bridge-domain customer1:engineering mac-address location 0/1/CPU0

show l2vpn forwarding bridge-domain customer1:engineering mac-address detail location 0/1/CPU0

show l2vpn forwarding bridge-domain customer1:engineering mac-address hardware ingress location 0/1/CPU0

show l2vpn forwarding bridge-domain customer1:engineering mac-address hardware egress location 0/2/CPU0

sh l2vpn forwarding bridge-domain customer1: engineering mac-address location 0/1/CPU0

sh mpls forwarding prefix 10.0.0.11/32

sh bundle bundle-ether 222

sh etherchannel summary

sh run l2vpn bridge group customer1

sh l2vpn bridge-domain bd-name engineering detail

sh l2vpn bridge-domain bd-name engineering detail | i "PW:|PW type”

show run formal | inc 1479
```
