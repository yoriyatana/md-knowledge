# Cisco template pppoe DHCPv6 NA (PPPoE IPv6)

pppoe\_client#show run

Building configuration...

Current configuration : 1799 bytes

!

! Last configuration change at 18:31:34 ICT Mon Jul 11 2022

!

version 15.4

service timestamps debug datetime msec

service timestamps log datetime msec

no service password-encryption

!

hostname pppoe\_client

!

boot-start-marker

boot-end-marker

!

!

!

no aaa new-model

clock timezone ICT 7 0

mmi polling-interval 60

no mmi auto-configure

no mmi pvc

mmi snmp-timeout 180

!

!

!

!

!

!

!

!

!

ip dhcp excluded-address 192.168.88.1

!

ip dhcp pool LAN\_POOL

network 192.168.88.0 255.255.255.0

default-router 192.168.88.1

!

!

!

no ip domain lookup

ip cef

ipv6 unicast-routing

ipv6 cef

!

multilink bundle-name authenticated

!

!

!

!

!

!

!

!

!

redundancy

!

!

!

!

!

!

!

!

!

!

!

!

!

!

!

interface Ethernet0/0

no ip address

!

interface Ethernet0/0.4003

encapsulation dot1Q 4003

```text
pppoe enable group global
```

pppoe-client dial-pool-number 1

!

interface Ethernet0/1

ip address 192.168.88.1 255.255.255.0

ip nat inside

ip virtual-reassembly in

ipv6 address FE80::2000:1 link-local

ipv6 address PREFIX\_FROM\_ISP ::1/64

ipv6 enable

!

interface Ethernet0/2

no ip address

shutdown

!

interface Ethernet0/3

no ip address

shutdown

!

interface Dialer1

mtu 1492

ip address negotiated

ip nat outside

ip virtual-reassembly in

encapsulation ppp

dialer pool 1

dialer-group 1

ipv6 address dhcp

ipv6 address FE80::10 link-local

ipv6 enable

ppp authentication pap chap callin

ppp chap hostname lab1

ppp chap password 0 lab123

ppp pap sent-username lab1 password 0 lab123

ppp ipcp route default

!

ip forward-protocol nd

!

!

no ip http server

no ip http secure-server

ip nat inside source list NAT\_ACL interface Dialer1 overload

!

ip access-list standard NAT\_ACL

permit any

!

!

!

!

control-plane

!

!

!

!

!

!

!

!

line con 0

logging synchronous

line aux 0

line vty 0 4

login

transport input none

!

!

end
