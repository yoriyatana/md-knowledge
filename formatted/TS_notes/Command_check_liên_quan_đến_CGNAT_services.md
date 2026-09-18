# Command check liên quan đến CGNAT services

@ 1 số lệnh check liên quan đến CGNAT services:

- Card MS-MPC:

* *## === NAT Services ===**

show services stateful-firewall flows count | no-more

show services nat pool detail | no-more

show services nat mappings summary | no-more

show services service-sets memory-usage | no-more

show services service-sets cpu-usage | no-more

show services service-set summary | no-more

show service sessions count | no-more

show services nat mappings address-pooling-paired private _21.81.226.73_

# -------------

show service sessions analysis | no-more

show services sessions utilization | no-more

show services service-sets cpu-usage | no-more

show services service-sets summary | no-more

show log messages | last 100 | match "cpu zone" | no-more

> show interface mams-* | match rate

> monitor interface ams0 no-resolve

# ==========================

- Check more with **MX-SPC3**:

* *## === NAT Services ===**

show services stateful-firewall flows count | no-more

show services nat source pool all | no-more

show services nat source mappings summary | no-more

show services service-sets memory-usage | no-more

show services service-sets cpu-usage | no-more

show services service-set summary | no-more

show service sessions count | no-more

# -------------

show service sessions analysis | no-more

show services sessions utilization | no-more

show services service-sets cpu-usage | no-more

show services service-sets summary | no-more

show log messages | last 100 | match "cpu zone" | no-more

show interface mams-* | match rate

# --------------

Case lỗi điển hình bên INOC2:

- Delay cao đột biến.

[ Thursday, January 6, 2022 11:39 PM ] ⁨INOC2-Phuoc [Trinh Van]⁩: show services sessions interface mams-7/1/0 service-set 3G

[ Thursday, January 6, 2022 11:40 PM ] ⁨INOC2-Phuoc [Trinh Van]⁩: anh show cái này thấy thuê bao bên trong request tới cái IP **113.185.56.173**

[ Thursday, January 6, 2022 11:40 PM ] ⁨INOC2-Phuoc [Trinh Van]⁩: route discard 113.185.56.160/27 trong vrf VR-NAT thì giảm
![bda04bb85ab4b616932be5eb1b1e3cf0.png](image/bda04bb85ab4b616932be5eb1b1e3cf0.png)

![3f76e9ff0232893810c2153a04b7497c.png](image/3f76e9ff0232893810c2153a04b7497c.png)

* *show services sessions source-prefix 14.172.216.224 �**�
![3cd9b6c5c80792070bc1b8bfdc457bfe.png](image/3cd9b6c5c80792070bc1b8bfdc457bfe.png)

* *OID:**
![e7159429b13d3b23b07930758e318980.png](image/e7159429b13d3b23b07930758e318980.png)

![07d62a12387ca567daf5dfc555b70cbf.png](image/07d62a12387ca567daf5dfc555b70cbf.png)

[https://apps.juniper.net/mib-explorer/search.jsp#object=jnxJsNatIfSrcPoolTotalSinglePorts&product=Junos](https://apps.juniper.net/mib-explorer/search.jsp%20%5Cl%20object=jnxJsNatIfSrcPoolTotalSinglePorts&product=Junos) OS&release=19.4R3
![3cd9b6c5c80792070bc1b8bfdc457bfe.png](image/3cd9b6c5c80792070bc1b8bfdc457bfe.png)

Case liên quan:

RE: Case Updated - P2 - High - 2022-0117-398960 - SV TECHNOLOGIES JSC - [VNPT] MX-SPC3 can not NAT with 2nd services-set
![3cd9b6c5c80792070bc1b8bfdc457bfe.png](image/3cd9b6c5c80792070bc1b8bfdc457bfe.png)

![131c0a66e023fede9f88f41641be5bbd.png](image/131c0a66e023fede9f88f41641be5bbd.png)

show snmp mib walk 1.3.6.1.4.1.2636.3.59.1.1.1.1.8

show snmp mib walk 1.3.6.1.4.1.2636.3.59.1.1.1.1.6

show snmp mib walk 1.3.6.1.4.1.2636.3.59.1.1.3.1.3

show snmp mib walk **jnxSpSvcSetSessCount**

show snmp mib walk **jnxJsNatRuleTable**

* *_svtech-tool@DNG-CGNAT-MX480_RE0> show services sessions count_**

Interface   Service set                        Valid      Invalid      Pending  Other state

mams-1/0/0  CGNAT                             359160            0            0            0

mams-1/1/0  CGNAT                             354534            0            0            0

mams-3/0/0  CGNAT                             358151            0            0            0

mams-3/1/0  CGNAT                             359261            0            0            0

{master}

* *_svtech-tool@DNG-CGNAT-MX480_RE0> show snmp mib walk_** **_1.3.6.1.4.1.2636.3.32.1.1.1.16  �_**�

jnxSpSvcSetSessCount.5.67.71.78.65.84 = 1432309

* *_svtech-tool@DNG-CGNAT-01_RE0> show snmp mib walk_** **jnxFWCounterByteCount** **_| display xml  �_**�

<rpc-reply xmlns:junos="[http://xml.juniper.net/junos/19.4R0/junos](http://xml.juniper.net/junos/19.4R0/junos)">

    <snmp-object-information xmlns="[http://xml.juniper.net/junos/19.4R0/junos-snmp](http://xml.juniper.net/junos/19.4R0/junos-snmp)">

        <snmp-object>

            <name>jnxFWCounterByteCount.2.51.48.13.66.68.72.45.67.71.78.65.84.45.73.88.80.2</name>

            <index>

                <index-name>jnxFWCounterFilterName</index-name>

                <index-value>30</index-value>

            </index>

            <index>

                <index-name>jnxFWCounterName</index-name>

                <index-value>BDH-CGNAT-IXP</index-value>

            </index>

            <index>

                <index-name>jnxFWCounterType</index-name>

                <index-value>2</index-value>

            </index>

            <object-value-type>counter64</object-value-type>

            <object-value>11660040352</object-value>

            <oid>1.3.6.1.4.1.2636.3.5.2.1.5.2.51.48.13.66.68.72.45.67.71.78.65.84.45.73.88.80.2</oid>

        </snmp-object>

        <snmp-object>

            <name>jnxFWCounterByteCount.2.51.48.13.66.68.72.45.67.71.78.65.84.45.78.73.88.2</name>

            <index>

                <index-name>jnxFWCounterFilterName</index-name>

                <index-value>30</index-value>

            </index>

            <index>

                <index-name>jnxFWCounterName</index-name>

                <index-value>BDH-CGNAT-NIX</index-value>

            </index>

            <index>

                <index-name>jnxFWCounterType</index-name>

                <index-value>2</index-value>

            </index>

            <object-value-type>counter64</object-value-type>

            <object-value>416057986093</object-value>

            <oid>1.3.6.1.4.1.2636.3.5.2.1.5.2.51.48.13.66.68.72.45.67.71.78.65.84.45.78.73.88.2</oid>

        </snmp-object>

[https://apps.juniper.net/mib-explorer/search.jsp#object=jnxFWCounterByteCount&product=Junos%20OS&release=19.4R3](https://apps.juniper.net/mib-explorer/search.jsp%20%5Cl%20object=jnxFWCounterByteCount&product=Junos%20OS&release=19.4R3)
![3cd9b6c5c80792070bc1b8bfdc457bfe.png](image/3cd9b6c5c80792070bc1b8bfdc457bfe.png)

* *# Lỗi chập chờn CGNAT (case HNI)**:

- Liên quan phần cứng của MX-SPC3
- Fabric drop của MPC7E

Một số lệnh để check:

show log messages | match mqss

show snmp mib walk 1.3.6.1.4.1.2636.3.81.1.1.1.1.1.11 | match 65535

show snmp mib walk 1.3.6.1.4.1.2636.3.81.1.1.1.1.1.15 | match 65535

và lệnh này để show trafic Fabric in/out card

đơn vị Bps, lấy giá trị kia x8 = bps

xem có over **170Gbps** ko nhé? --> MPC7E oversubscription

show pfe statistics traffic | match fabric

1. 3.6.1.4.1.2636.3.81.1.1.1.1.1.10 mib này check pps

1. 3.6.1.4.1.2636.3.81.1.1.1.1.1.15 check packet drop

INOC3 FTP vào 123.29.0.59 lấy file nhé

   * *guest/svtech@123**
