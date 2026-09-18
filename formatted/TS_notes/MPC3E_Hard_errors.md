# MPC3E Hard errors

I understand from the case notes that you have observed the below FPC hard errors on the MX960 device:

_root@AGG-HUEHTY22> show chassis alarms no-forwarding_

_4 alarms currently active_

_Alarm time               Class  Description_

_2021-06-06 22:17:36 ICT  Major FPC 1 Hard errors_

_2021-06-06 22:17:04 ICT  Major FPC 1 offlined due to unreachable destinations_

_2021-06-06 22:16:54 ICT  Major FPC 1 has unreachable destinations_

Could you please provide me the below information to investigate:

- Were there any recent changes made to the software/hardware setup?
- Were there any troubleshooting steps already done? If yes, please describe and share any outputs that you might have (ex: putty sessions)
- The below command output from the CLI:

_show chassis fpc pic-status_

_show chassis fabric summary_

_show chassis fabric fpcs_

_show chassis fabric plane-location_

_show chassis fabric plane-degradation_

_>start shell pfe network fpc1_

_#show syslog messages_

_#show nvram_

_#show cmerror module_

_#show hsl2 statistics_

_#exit_
