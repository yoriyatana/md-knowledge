# Alarm on FPC

Juniper Case 2021-0712-0231

---

With respect to the FPC error handling and default action:

- Starting from 17.3 release onwards, the default action for major alarms on FPC is pfe-disable.
- Starting from 17.4, the default action can be modified per error.

<-- Default action on each alarm severity:

labroot@mx> show chassis fpc errors

FPC  Level Occurred Cleared Threshold Action-Taken Action

0   Minor      0      0      1      0 LOG|CM ALARM|

Major      0      0      1      0 CM ALARM|DISABLE PFE

Fatal      0      0      1      0  RESET

<-- Change the default action:

# set chassis fpc 0 error minor action log

labroot@mx> show chassis fpc errors

FPC  Level Occurred Cleared Threshold Action-Taken Action

0   Minor      0      0      1      0   LOG|                    <<<<<<

Major      0      0      1      0 CM ALARM|DISABLE PFE

Fatal      0      0      1      0  RESET

The above one is to modify the action for complete FPC. You can change the major error action to “reset” the FPC which will restart the FPC and gr-\* interface can switch to another line. There are no risk when you modify this default action. If the links are having redundancy, modify the major error action to reset FPC which will restart the FPC to recover the error state instead of disable PFE which requires manual intervention to restart the FPC to recover from error state.

You can also modify the action for each error code.

Here is an example. This just for your knowledge and do not modify unless you get any recommendation from JTAC.

If I have to change the error code(XM Chip Error code: 0x7032c), check how many XMCHIPs are there in the line card.

labroot@jtac-mx480-r2055-re0> request pfe execute command "show jspec client" target fpc0 | grep XM

8       XMCHIP[0]

9       XMCHIP[1]

There are two XMCHIPs on both MPC5 and MPC4.

labroot@jtac-mx480-r2055-re0> show chassis hardware detail | match FPC

FPC 0            REV 56   750-046005   CAMP7081          MPC5E 3D Q 2CGE+4XGE

FPC 1            REV 09   750-062865   CAJG9690          MPC4E 3D 32XGE

abroot@jtac-mx480-r2055-re0> request pfe execute command "show jspec client" target fpc0 | grep XM

8       XMCHIP[0]

9       XMCHIP[1]

labroot@jtac-mx480-r2055-re0> request pfe execute command "show jspec client" target fpc1 | grep XM

3       XMCHIP[0]

6       XMCHIP[1]

Check the CMERROR module for XMCHIP:

labroot@jtac-mx480-r2055-re0> request pfe execute command "show cmerror module brief" target fpc0 | grep XMCHIP

21      XMCHIP(0)         0              No        0x00000000  0x170d4240

23      XMCHIP(1)         0              No        0x00000000  0x1bd53698

labroot@jtac-mx480-r2055-re0> request pfe execute command "show cmerror module brief" target fpc1 | grep XMCHIP

9       XMCHIP(0)         0              No        0x00000000  0x46445dd0

15      XMCHIP(1)         0              No        0x00000000  0x49b58370

<-- Pick the identifier of the error for each XMCHIP:

labroot@jtac-mx480-r2055-re0> request pfe execute command "show cmerror module 21 error 0x7032c" target fpc0

SENT: Ukern command: show cmerror module 21 error 0x7032c

Error-id              : 0x7032c

Error Name            : XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Identifier            : /fpc/0/pfe/0/cm/0/XMCHIP(0)/0/XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Description           : WI\_PROTECT: Detected: Parity error for wicpq free pointer SRAM

State                 : enabled

Scope                 : fpc

Category              : default

PFE                   : 0

Configured Level      : Major

Default Level         : Major

Count                 : 0

Threshold             : 1

Error Limit           : 0

Occur Count           : 0

Clear Count           : 0

Last-occurred(ms ago) : 0

Logs:

----------------------------------------------------------

Index  Time                 Sub-Err   State    Description

----------------------------------------------------------

labroot@jtac-mx480-r2055-re0> request pfe execute command "show cmerror module 23 error 0x7032c" target fpc0

SENT: Ukern command: show cmerror module 23 error 0x7032c

Error-id              : 0x7032c

Error Name            : XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Identifier            : /fpc/0/pfe/0/cm/0/XMCHIP(1)/1/XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Description           : WI\_PROTECT: Detected: Parity error for wicpq free pointer SRAM

State                 : enabled

Scope                 : fpc

Category              : default

PFE                   : 1

Configured Level      : Major

Default Level         : Major

Count                 : 0

Threshold             : 1

Error Limit           : 0

Occur Count           : 0

Clear Count           : 0

Last-occurred(ms ago) : 0

Logs:

----------------------------------------------------------

Index  Time                 Sub-Err   State    Description

----------------------------------------------------------

labroot@jtac-mx480-r2055-re0> request pfe execute command "show cmerror module 9 error 0x7032c" target fpc1

SENT: Ukern command: show cmerror module 9 error 0x7032c

Error-id              : 0x7032c

Error Name            : XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Identifier            : /fpc/1/pfe/0/cm/0/XMCHIP(0)/0/XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Description           : WI\_PROTECT: Detected: Parity error for wicpq free pointer SRAM

State                 : enabled

Scope                 : fpc

Category              : default

PFE                   : 0

Configured Level      : Major

Default Level         : Major

Count                 : 0

Threshold             : 1

Error Limit           : 0

Occur Count           : 0

Clear Count           : 0

Last-occurred(ms ago) : 0

Logs:

----------------------------------------------------------

Index  Time                 Sub-Err   State    Description

----------------------------------------------------------

labroot@jtac-mx480-r2055-re0> request pfe execute command "show cmerror module 15 error 0x7032c" target fpc1

SENT: Ukern command: show cmerror module 15 error 0x7032c

Error-id              : 0x7032c

Error Name            : XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Identifier            : /fpc/1/pfe/0/cm/0/XMCHIP(1)/1/XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Description           : WI\_PROTECT: Detected: Parity error for wicpq free pointer SRAM

State                 : enabled

Scope                 : fpc

Category              : default

PFE                   : 1

Configured Level      : Major

Default Level         : Major

Count                 : 0

Threshold             : 1

Error Limit           : 0

Occur Count           : 0

Clear Count           : 0

Last-occurred(ms ago) : 0

Logs:

----------------------------------------------------------

Index  Time                 Sub-Err   State    Description

----------------------------------------------------------

From the identifier of each CHIP, apply the commands to the respective line cards:

set chassis fpc 0 error "/fpc/0/pfe/0/cm/0/XMCHIP(0)/0/XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM" severity minor

set chassis fpc 0 error "/fpc/0/pfe/0/cm/0/XMCHIP(1)/1/XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM" severity minor

set chassis fpc 1 error "/fpc/1/pfe/0/cm/0/XMCHIP(0)/0/XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM" severity minor

set chassis fpc 1 error "/fpc/1/pfe/0/cm/0/XMCHIP(1)/1/XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM" severity minor

After modifying the severity, check again on each FPC:

labroot@jtac-mx480-r2055-re0> request pfe execute command "show cmerror module 21 error 0x7032c" target fpc0

SENT: Ukern command: show cmerror module 21 error 0x7032c

Error-id              : 0x7032c

Error Name            : XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Identifier            : /fpc/0/pfe/0/cm/0/XMCHIP(0)/0/XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Description           : WI\_PROTECT: Detected: Parity error for wicpq free pointer SRAM

State                 : enabled

Scope                 : fpc

Category              : default

PFE                   : 0

Configured Level      : Minor

Default Level         : Major

Count                 : 0

Threshold             : 1

Error Limit           : 0

Occur Count           : 0

Clear Count           : 0

Last-occurred(ms ago) : 0

Logs:

----------------------------------------------------------

Index  Time                 Sub-Err   State    Description

----------------------------------------------------------

labroot@jtac-mx480-r2055-re0> request pfe execute command "show cmerror module 23 error 0x7032c" target fpc0

SENT: Ukern command: show cmerror module 23 error 0x7032c

Error-id              : 0x7032c

Error Name            : XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Identifier            : /fpc/0/pfe/0/cm/0/XMCHIP(1)/1/XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Description           : WI\_PROTECT: Detected: Parity error for wicpq free pointer SRAM

State                 : enabled

Scope                 : fpc

Category              : default

PFE                   : 1

Configured Level      : Minor

Default Level         : Major

Count                 : 0

Threshold             : 1

Error Limit           : 0

Occur Count           : 0

Clear Count           : 0

Last-occurred(ms ago) : 0

Logs:

----------------------------------------------------------

Index  Time                 Sub-Err   State    Description

----------------------------------------------------------

labroot@jtac-mx480-r2055-re0> request pfe execute command "show cmerror module 9 error 0x7032c" target fpc1

SENT: Ukern command: show cmerror module 9 error 0x7032c

Error-id              : 0x7032c

Error Name            : XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Identifier            : /fpc/1/pfe/0/cm/0/XMCHIP(0)/0/XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Description           : WI\_PROTECT: Detected: Parity error for wicpq free pointer SRAM

State                 : enabled

Scope                 : fpc

Category              : default

PFE                   : 0

Configured Level      : Minor

Default Level         : Major

Count                 : 0

Threshold             : 1

Error Limit           : 0

Occur Count           : 0

Clear Count           : 0

Last-occurred(ms ago) : 0

Logs:

----------------------------------------------------------

Index  Time                 Sub-Err   State    Description

----------------------------------------------------------

labroot@jtac-mx480-r2055-re0> request pfe execute command "show cmerror module 15 error 0x7032c" target fpc1

SENT: Ukern command: show cmerror module 15 error 0x7032c

Error-id              : 0x7032c

Error Name            : XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Identifier            : /fpc/1/pfe/0/cm/0/XMCHIP(1)/1/XMCHIP\_CMERROR\_WI\_WICPQ\_FREEPTR\_SRAM\_PAR\_PROTECT\_FSET\_REG\_DETECTED\_WICPQ\_FREEPTR\_SRAM

Description           : WI\_PROTECT: Detected: Parity error for wicpq free pointer SRAM

State                 : enabled

Scope                 : fpc

Category              : default

PFE                   : 1

Configured Level      : Minor

Default Level         : Major

Count                 : 0

Threshold             : 1

Error Limit           : 0

Occur Count           : 0

Clear Count           : 0

Last-occurred(ms ago) : 0

Logs:

----------------------------------------------------------

Index  Time                 Sub-Err   State    Description

----------------------------------------------------------

---

As I understand it, version 17.3 and earlier, we can only change the default action for each alarm level. is it right? Can you explain about board vs PFE scope?

---

[Tung.NT] At the moment, is it the only way to failover gr-\*? Is there a roadmap for redundant groups that support the gr-\*?

[siva] There is no way to failover gr-\* and I do not find any roadmap for it.

As I understand it, version 17.3 and earlier, we can only change the default action for each alarm level. is it right?

[siva] Yes, you are right.

Board means for the errors on the FPC and PFE means the errors on the PFE. There may be more than one PFE on line cards.

> board                Board level scope

> pfe                  Forwarding engine scope

---

Yes, the major alarm on board might not affect all the ASIC/PFE which is why no default action is taken and just raise alarm so that user takes action.

In case of errors on PFE/ASIC which might cause impact to other PFE. Hence, they are disabled to minimize the impact.
