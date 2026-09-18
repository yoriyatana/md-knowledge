# Subscriber scale MX204 vs MX304

* *MX204 vs MX304 BNG SCALE**

|                    |**Chassis Scale**|                         |                         |                         |
|--------------------|-----------------|-------------------------|-------------------------|-------------------------|
|**Deployment Model**|Family           |Access Model             |MX204                    |MX304                    |
|**1:1 CVLAN**       |100% V4          |DHCP                     |32K                      |32K w 2LMICs/48K w 3LMICs|
|PPPoE               |32K              |32K w 2LMICs/48K w 3LMICs|                         |                         |
|100% Dual Stack     |DHCP             |32K                      |32K w 2LMICs/48K w 3LMICs|                         |
|PPPoE               |32K              |32K w 2LMICs/48K w 3LMICs|                         |                         |
|**N:1 Service VLAN**|100% V4          |DHCP                     |32K                      |32K w 2LMICs/48K w 3LMICs|
|PPPoE               |32K              |32K w 2LMICs/48K w 3LMICs|                         |                         |
|100% Dual Stack     |DHCP             |32K                      |32K w 2LMICs/48K w 3LMICs|                         |
|PPPoE               |32K              |32K w 2LMICs/48K w 3LMICs|                         |                         |
|**L2TP LAC**        |100% V4          |PPP/LAC                  |32K                      |32K w 2LMICs/48K w 3LMICs|
|**L2TP LNS**        |100% V4          |PPP/LNS                  |32K                      |32K w 2LMICs/48K w 3LMICs|
|100% Dual Stack     |32K              |32K w 2LMICs/48K w 3LMICs|                         |                         |
|**IP/MPLS PWEs**    |100% V4          |DHCP                     |32K                      |32K w 2LMICs/48K w 3LMICs|
|PPPoE               |32K              |32K w 2LMICs/48K w 3LMICs|                         |                         |
|100% Dual Stack     |DHCP             |32K                      |32K w 2LMICs/48K w 3LMICs|                         |
|PPPoE               |32K              |32K w 2LMICs/48K w 3LMICs|                         |                         |

- --

# **Platforms and Scale**

This subscriber QOS model is available first on [MX304](https://community.juniper.net/blogs/reema-ray/2023/03/28/mx304-deepdive "MX304 Deepdive"), enabling 32,000 subscriber sessions per LMIC, up to 96,000 session per chassis, assuming no Routing Engine redundancy and 64,000 sessions otherwise. Assuming full capacity on an LMIC, the model enables up to 50 Mbps per subscriber.

[https://community.juniper.net/blogs/horia-miclea/2023/04/04/new-subscriber-qos-for-next-generation-broadband?CommunityKey=44efd17a-81a6-4306-b5f3-e5f82402d8d3](https://community.juniper.net/blogs/horia-miclea/2023/04/04/new-subscriber-qos-for-next-generation-broadband?CommunityKey=44efd17a-81a6-4306-b5f3-e5f82402d8d3)
