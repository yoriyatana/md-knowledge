# SR-2021-1215-1608 - Hỗ trợ thử nghiệm IPv6 tĩnh cho KH CĐBR

Hi Linh,

Anh gửi thêm ID của Attribute nhé:

- IPv6 WAN

Attribute: Framed-IPv6-Prefix

Type: ipv6addr

```text
ID: 97
```

- IPv6 LAN

Attribute: Delegated-IPv6-Prefix

Type: ipv6addr

```text
ID: 123
```

Các attribute này anh đã test trên lab hoạt động bình thường nhé.

- --

Để cấp được IPv6 tĩnh cho khách hàng thì cần gán IPv6 cho khách hàng trên Radius. Cần sử dụng những Attribute sau để gán cho khách hàng.

- IPv6 WAN

Attribute: Framed-IPv6-Prefix

Type: ipv6addr

- IPv6 LAN

Attribute: Delegated-IPv6-Prefix

Type: ipv6addr

Anh gửi phần khai báo trên BRAS:

dynamic-profiles {

dualstack-PPPoE-Profile {

interfaces {

pp0 {

unit "$junos-interface-unit" {

no-traps;

ppp-options {

chap;

pap;

}

pppoe-options {

underlying-interface "$junos-underlying-interface";

server;

}

family inet {

unnumbered-address lo0.0;

}

family inet6 {

address $junos-ipv6-address;

}

}

}

}

protocols {

router-advertisement {

interface "$junos-interface-name" {

other-stateful-configuration;

prefix $junos-ipv6-ndra-prefix;

}

}

}

}

dualstack-single-vlan {

interfaces {

"$junos-interface-ifd-name" {

unit "$junos-interface-unit" {

no-traps;

vlan-id "$junos-vlan-id";

family pppoe {

dynamic-profile dualstack-PPPoE-Profile;

}

}

}

}

}

}
