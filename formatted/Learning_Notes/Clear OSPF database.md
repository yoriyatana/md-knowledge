# Clear OSPF database

<https://packetcorner.wordpress.com/2012/08/30/clear-ospf-database/>

## Difference between “none” and “purge”

In Junos, “clear OSPF database” will reset the neighbor relationship, while the same command with “purge” option only refresh the database by timeout the maxage timer, and get the latest LSA updates from neighbors.
