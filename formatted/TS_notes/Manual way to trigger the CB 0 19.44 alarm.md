# Manual way to trigger the CB 0 19.44 alarm

Here's a manual way to trigger the CB 0 19.44 alarm.

```text
labroot@jtac-mx480-r2014-re0> show chassis alarms
```
3 alarms currently active

Alarm time        Class Description

2022-02-26 10:56:30 IST Minor Loss of communication with Backup RE

2022-02-26 10:56:05 IST Minor CB 1 Fabric Chip 1 Not Online

2022-02-26 10:56:04 IST Minor CB 1 Fabric Chip 0 Not Online

{master}

```text
labroot@jtac-mx480-r2014-re0> start shell user root
```
Password:

```text
root@jtac-mx480-r2014-re0% cli
```
{master}

```text
labroot@jtac-mx480-r2014-re0> start shell user root
root@jtac-mx480-r2014-re0% spc -w 0 0 0x38 0x85 ; spc -w 0 0 0x39 0xa
root@jtac-mx480-r2014-re0% cli
```
{master}

```text
labroot@jtac-mx480-r2014-re0> show log messages |grep "CB 0 19"
```
Mar 3 18:07:36.171 jtac-mx480-r2014-re0 alarmd[2030]: Alarm set: CB color=RED, class=CHASSIS, reason=CB 0 19.44 MHz clock failure

Mar 3 18:07:36.171 jtac-mx480-r2014-re0 craftd[1765]: Major alarm set, CB 0 19.44 MHz clock failure

{master}

```text
labroot@jtac-mx480-r2014-re0> show chassis alarms
```
4 alarms currently active

Alarm time        Class Description

2022-03-03 18:07:36 IST Major CB 0 19.44 MHz clock failure

2022-02-26 10:56:30 IST Minor Loss of communication with Backup RE

2022-02-26 10:56:05 IST Minor CB 1 Fabric Chip 1 Not Online

2022-02-26 10:56:04 IST Minor CB 1 Fabric Chip 0 Not Online

Please note that it is highly not recommended to test this in a production setup.
