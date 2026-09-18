# MPC3E Hard errors

I understand from the case notes that you have observed the below FPC hard errors on the MX960 device:

```text
root@AGG-HUEHTY22> show chassis alarms no-forwarding*
```

* 4 alarms currently active*

* Alarm time               Class  Description*

* 2021-06-06 22:17:36 ICT  Major FPC 1 Hard errors*

* 2021-06-06 22:17:04 ICT  Major FPC 1 offlined due to unreachable destinations*

* 2021-06-06 22:16:54 ICT  Major FPC 1 has unreachable destinations*

Could you please provide me the below information to investigate:

- Were there any recent changes made to the software/hardware setup?
- Were there any troubleshooting steps already done? If yes, please describe and share any outputs that you might have (ex: putty sessions)
- The below command output from the CLI:

```text
show chassis fpc pic-status*
```

```text
show chassis fabric summary*
```

```text
show chassis fabric fpcs*
```

```text
show chassis fabric plane-location*
```

```text
show chassis fabric plane-degradation*
```

```text
>start shell pfe network fpc1*
```

* #show syslog messages*

* #show nvram*

* #show cmerror module*

* #show hsl2 statistics*

* #exit*
