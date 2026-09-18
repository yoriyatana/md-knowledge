# OID Alarm count

em gửi SNMP OID để theo dõi số lượng alarm phát sinh trên thiết bị nhé

RedAlarm ~ Major

YellowAlarm ~ Minor

```text
>>> Nếu thiết bị không có alarm thì 2 OID này sẽ có giá trị 0, khi phát sinh alarm thì tuỳ mức độ mà alarm tương ứng sẽ thay đổi # 0 ạ
```
{master}

```text
lab@HCM-ASBR5-RE0> show chassis alarms
```
4 alarms currently active

Alarm time               Class  Description

2022-12-17 11:39:56 ICT  Major  FPC 8 Major Errors

2022-12-17 11:39:50 ICT  Minor  FPC 8 Minor Errors

2022-12-09 22:04:45 ICT  Major  PEM 3 Not OK

2022-12-09 22:04:45 ICT  Major  PEM 3 Input Failure

{master}

```text
lab@HCM-ASBR5-RE0> show snmp mib walk 1.3.6.1.4.1.2636.3.4.2.2.2
```
jnxYellowAlarmCount.0 = 1

{master}

```text
lab@HCM-ASBR5-RE0> show snmp mib walk 1.3.6.1.4.1.2636.3.4.2.3.2
```
jnxRedAlarmCount.0 = 3

```text
lab@PE1-MX960-02-RE0> show chassis alarms
```
No alarms currently active

{master}

```text
lab@PE1-MX960-02-RE0> show chassis alarms
```
No alarms currently active

{master}

```text
lab@PE1-MX960-02-RE0> show snmp mib walk 1.3.6.1.4.1.2636.3.4.2.2.2
```
jnxYellowAlarmCount.0 = 0

{master}

```text
lab@PE1-MX960-02-RE0> show snmp mib walk 1.3.6.1.4.1.2636.3.4.2.3.2
```
jnxRedAlarmCount.0 = 0

{master}

```text
lab@PE1-MX960-02-RE0>
```
