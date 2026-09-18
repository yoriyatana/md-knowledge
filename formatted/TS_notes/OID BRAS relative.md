# OID BRAS relative

[ June 30, 2023 15:43 ] ⁨SVT.Dũng.TQ⁩: + Giám sát IP Pool (cung cấp bảng MIB)

1. 3.6.1.4.1.2636.3.51.1.1.4.1.1.1    name jnxUserAAAAccessPoolGeneral

[ June 30, 2023 15:43 ] ⁨SVT.Dũng.TQ⁩: + Giám sát license key :

OID

```text
show snmp mib walk  : 1.3.6.1.4.1.2636.3.63
```
[ June 30, 2023 15:44 ] ⁨SVT.Dũng.TQ⁩: juniper@BRAS\_RE0> show snmp mib walk 1.3.6.1.4.1.2636.3.63.1.1.1.2.1 check license key

[ June 30, 2023 15:45 ] ⁨SVT.Dũng.TQ⁩: Giam sat ipv6:

```text
>show snmp mib walk .1.3.6.1.2.1.55
> show snmp mib walk 1.3.6.1.4.1.2636.3.11.1.3.1.1
> show snmp mib walk 1.3.6.1.4.1.2636.3.62.62.2.1.1
```
From <<https://iphostmonitor.com/mib/oids/JUNIPER-JDHCPV6-MIB/jnxJdhcpv6LocalServerTotalDropped.html>>

Juniper Jdhcpv6 Local Server Total Lease Count

1. 3.6.1.4.1.2636.3.62.62.2.1.23

[ June 30, 2023 15:45 ] ⁨SVT.Dũng.TQ⁩: juniper@HNI-BNG01RE0# run show snmp mib walk jnxSubscriberTotalCount

jnxSubscriberTotalCount.0 = 48990

{master}[edit groups BNG routing-instances]

```text
juniper@HNI-BNG01RE0# run show snmp mib walk 1.3.6.1.4.1.2636.3.64.1.1.1.1
```
jnxSubscriberTotalCount.0 = 49386

```text
juniper@HNI-BNG01RE0# run show snmp mib walk 1.3.6.1.4.1.2636.3.62.62.2.1.23
```
jnxJdhcpv6LocalServerTotalLeaseCount.0 = 16057
