# PR1561855 - Continuous bbe-smgd cores are generated after restarting the smgd

https://prsearch.juniper.net/InfoCenter/index?page=prcontent&id=PR1561855

| **Problem Report​** | |
| --- | --- |
| **Number** | PR1561855 |
| **Title** | Continuous bbe-smgd cores are generated after restarting the smgd |
| **Release Note​** | |  | | --- | | After executing the command 'restart smg-service', because of a timing issue continuous bbe-smgd cores are generated and lead to service impact on subscribers. | |
| **Severity** | Major |
| **Status** | Closed |
| **Last Modified​** | 2021-07-14 23:32:12 EDT |
| **Resolved In​** | |  |  | | --- | --- | | **Release** | **junos** | | **19.1R3-S5** | x | | **18.4R3-S7** | x | | **19.3R3-S2** | x | | **19.2R3-S2** | x | | **20.3R3** | x | | **20.4R2** | x | | **21.2R1** | x | | **21.1R1** | x | | **20.1R3** | x | | **19.4R3-S2** | x | | **20.2R3** | x | | **20.3R2** | x | |
| **Product** | MX-series |
| **Functional Area​** | software |
| **Problem** | |  | | --- | | Continuous bbe-smgd cores are generated. The problem state could be found with the following commands:  user@device> show system core-dumps no-forwarding  -rw-rw----  ​1 root  ​wheel   ​<>  ​16:02 /var/tmp/bbe-smgd.core-tarball.0.tgz  -rw-rw----  ​1 root  ​wheel   ​<>  ​16:04 /var/tmp/bbe-smgd.core-tarball.1.tgz  -rw-rw----  ​1 root  ​wheel   ​<>  ​16:15 /var/tmp/bbe-smgd.core-tarball.2.tgz  <> ​ | |
| **Triggers** | |  | | --- | | This issue might be seen if the following conditions are met:  \* On MX platforms  \* In subscriber scenario  \* Restart daemon 'Enhanced Session Management process' by command 'restart smg-service' | |
