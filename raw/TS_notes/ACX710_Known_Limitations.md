# ACX710 Known Limitations

ACX5448, ACX710 and ACX7100 series routers do not support **log**, **syslog**, **reject**, **forwarding-class**, and **loss-priority** in the egress direction. In the ingress and egress direction, the routers support interface specific semantics only.

[https://www.juniper.net/documentation/us/en/software/junos/routing-policy/topics/topic-map/firewall-filter-match-conditions-and-actions-acx.html](https://www.juniper.net/documentation/us/en/software/junos/routing-policy/topics/topic-map/firewall-filter-match-conditions-and-actions-acx.html)

- On the ACX710 router, VRRP over aggregated Ethernet interface is not supported. [PR1483594](http://prsearch.juniper.net/PR1483594)
- When you add or delete a configuration or a LAG member link flaps, configuration updates happen for all other members of the LAG too. This results in transient traffic drop on the ACX710 devices. [PR1486997](http://prsearch.juniper.net/PR1486997)
- The maximum FIB route scale supported in an ACX710 router are as below:
    - FIB IPv6 route scale - 80,000
    - FIB IPv4 route scale - 170,000
- If routes are added above this scale, an error indicating lpm route add failure is reported. [PR1515545](http://prsearch.juniper.net/PR1515545)

- On ACX710 routers, VRRP over dual tagged interface is not supported. [PR1483759](http://prsearch.juniper.net/PR1483759)

[https://www.juniper.net/documentation/en_US/junos/information-products/topic-collections/release-notes/20.2/jd0e135.html](https://www.juniper.net/documentation/en_US/junos/information-products/topic-collections/release-notes/20.2/jd0e135.html)
