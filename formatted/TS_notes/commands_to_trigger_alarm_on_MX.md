# commands to trigger alarm on MX

Juniper Case 2021-0617-0338

- --

There are commands to trigger this error. This only for testing and should not be tried in production.

```
NGMPC1(jtac-mx240-r2008-re0 vty)# show cmerror module
Module_id  Name  Error-id  PFE  Level Threshold Count Occurred Cleared Last-occurred(ms ago)  Description
- -------------------------------------------------------------------------------------------------------
<..>
   10  XL[0:0]
                  0x040008    0  Major     1       1       1     0      1231740ms              Declare wedge
```

Command to trigger this error:

```
# test cmerror trigger-error <error_id> <pfe_id> <string> <module>
```

In my lab I was able to trigger this error and it disable the links.

```
# test cmerror trigger-error 0x2e0006 0 test 10 /// 'PFE Disable'
```

```
NGMPC1(jtac-mx240-r2008-re0 vty)# ...ror 0x040008 0 test 10

NGMPC1(jtac-mx240-r2008-re0 vty)# [Jul  9 06:21:24.988 LOG: Debug] Cmerror: Draining ASIC error message queue
[Jul  9 06:21:24.988 LOG: Debug] cmerror_process_queue: module = XL[0:0]
[Jul  9 06:21:24.988 LOG: Debug] Cmerror: processing the task op_type 1 for level 1 level_count 0 occur_count 0 clear_count 0 level_threshold 1 level_action 0x44
 item errid 262152 item_threshold 1 item_count 0 item_sub_err_state 0 sub_item errid 0 sub_item_state 0 item_times[Jul  9 06:21:24.988 LOG: Debug] Cmerror: Level 1 count increment 1 occur_count 1 clear_count 0
[Jul  9 06:21:24.988 LOG: Info] Error (0x40008), module: XL[0:0], type: Declare wedge
[Jul  9 06:21:24.988 LOG: Debug] Cmerror: Level 1 count 1 (occur_count 1 clear_count 0)crossed threshold 1 action 0x44
[Jul  9 06:21:24.988 LOG: Debug] cmerror_take_action_helper: performing action 4 for level 1 err_id 262152 module id 10
[Jul  9 06:21:24.988 LOG: Debug] cmerror_take_action_helper: performing action 2 for level 1 err_id 262152 module id 10

NGMPC1(jtac-mx240-r2008-re0 vty)# exit
```

```
labroot@jtac-mx240-r2008-re0> show chassis alarms
1 alarms currently active
Alarm time               Class  Description
2021-07-09 11:51:25 IST  Major  FPC 1 Major Errors - Lkup Error code: 0x40008
```
