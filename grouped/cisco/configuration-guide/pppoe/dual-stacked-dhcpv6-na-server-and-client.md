# Cisco PPPoE Dual-Stack DHCPv6-NA Client

## Source: `formatted/PR/Cisco template pppoe DHCPv6 NA (PPPoE IPv6).md`
```cisco
pppoe_client#show run
Building configuration...

Current configuration : 1876 bytes
!
! Last configuration change at 16:16:34 ICT Fri Sep 18 2026
!
version 15.5
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname pppoe_client
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
!
!
!
bsd-client server url https://cloudsso.cisco.com/as/token.oauth2
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
!
!
!
!


!
ip dhcp excluded-address 192.168.88.1
!
ip dhcp pool LAN_POOL
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
cts logging verbose
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
 shutdown
!
interface Ethernet0/0.4003
 encapsulation dot1Q 4003
 pppoe enable group global
 pppoe-client dial-pool-number 1
!
interface Ethernet0/1
 ip address 192.168.88.1 255.255.255.0
 ip nat inside
 ip virtual-reassembly in
 shutdown
 ipv6 address FE80::2000:1 link-local
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
ip nat inside source list NAT_ACL interface Dialer1 overload
!
ip access-list standard NAT_ACL
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
```
