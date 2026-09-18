# Untitled Note

# Upgrading an MX960 to Use the SCBE2-MX

Consider the following scenarios when upgrading an MX960 SCB-MX or SCBE-MX to use the SCBE2-MX:

Scenario 1: SCBE2-MX; Routing Engine with Junos OS Release 13.3R1 or later installed.

- Replace the SCBs. Ensure you replace the Routing Engines at the same time.
- Ensure that Enhanced IP or Enhanced Ethernet Network Services mode is configured before you power on the router.

To upgrade the SCB-MX or SCBE-MX to SCBE2, perform the following steps:

NOTE: You cannot upgrade to SCBE2-MX without powering off the MX960 router.

## Prepare the MX960 Router for SCBE2-MX Upgrade

Verify that the system runs Junos OS Release 13.3 or later by issuing the show version command on the primary router.

```text
user@host> show version
```
Model: mx960

Junos Base OS Software Suite [13.3-yyyymmdd];

...

```text
> show chassis alarms
> show system alarms
> show system core-dumps
> show chassis network-services
> show version invoke-on all-routing-engines | match "re0|re1|Junos:"
> show chassis routing-engine | no-more
> show chassis routing-engine | match "Slot|State|Start"
show chassis environment cb | no-more
show chassis environment cb | match "CB|State"
> show chassis fabric summary | no-more
```
/\* Lưu thông tin hardware/fabric/fpc \*/

```text
> show chassis hardware | no-more
> show chassis fabric fpcs | no-more
> show chassis fabric summary extended | no-more
> show chassis fabric plane | no-more
```
/\* Lưu thông tin đồng bộ GRES and NSR - KB32931  \*/

```text
> show system switchover /\* Show on Backup RE – GRES Readiness Check\*/
> show task replication  /\* Show on Master RE – RPD Synchronization Check\*/
> show database-replication summary /\* Show on Master RE – For BNG only \*/
```
Verify that the system Configure Enhanced IP Network Services mode by issuing the  **show chassis network-services** command on the primary router.

```text
user@host> show chassis network-services
```
Network Services Mode: Enhanced-IP

NOTE: The SCBE2-MX is supported only on:

- Junos OS Release 13.3 or later
- Network Services Mode: Enhanced-IP

## Power Off the MX960 Router

NOTE: After turning off the power supply, wait at least 60 seconds before turning it back on.

1. Trên terminal kết nối đến thiết bị, dùng lệnh request system halt both-routing-engines để tắt RE một cách an toàn. (Nếu thiết bị chỉ có một RE thì dùng lệnh request system halt)

```text
user@host> request system halt both-routing-engines
Đợi đến khi thông báo xuất hiện xác nhận hệ thống đã tạm ngừng.
Chuyển công tác trên bộ nguồn AC hoặc DC sang vị trí off (O).
```
## Remove the MX960 Routing Engine

1. Đánh đấu và rút các cáp kết nối đến RE. Remove the cables connected to the Routing Engine.
2. Place an electrostatic bag or antistatic mat on a flat, stable surface.
3. Mang vòng tay tĩnh điện và kết nối đầy dây với điểm ESD trên chassis thiết bị.
4. Loosen the captive screws on the top and bottom of the Routing Engine.
5. Flip the ejector handles outward to unseat the Routing Engine.
6. Grasp the Routing Engine by the ejector handles, and slide it about halfway out of the chassis.
7. Place one hand underneath the Routing Engine to support it, and slide it completely out of the chassis.
8. Place the Routing Engine on the antistatic mat.

## Install the MX960 Routing Engine into the SCBE2-MX

1. Attach an electrostatic discharge (ESD) grounding strap to your bare wrist, and connect the strap to one of the ESD points on the chassis.
2. Ensure that the ejector handles are not in the locked position. If necessary, flip the ejector handles outward.
3. Place one hand underneath the Routing Engine to support it.
4. Carefully align the sides of the Routing Engine with the guides inside the opening on the SCBE2-MX.
5. Slide the Routing Engine into the SCBE2-MX until you feel resistance and then press the faceplate of the Routing Engine until it engages the connectors.
6. Press both of the ejector handles inward to seat the Routing Engine.
7. Tighten the captive screws on the top and bottom of the Routing Engine.
8. Connect the management device cables to the Routing Engine.

## Power On the MX960 Router

1. Verify that the power supplies are fully inserted in the chassis.
2. Verify that each AC power cord is securely inserted into its appliance inlet.
3. Verify that an external management device is connected to one of the Routing Engine ports (AUX, CONSOLE, or ETHERNET).
4. Turn on the power to the external management device.
5. Switch on the dedicated customer-site circuit breakers. Follow the ESD and safety instructions for your site.
6. Attach an ESD grounding strap to your bare wrist and connect the strap to one of the ESD points on the chassis.
7. Move the AC input switch on the chassis above the AC power supply or the DC circuit breaker on each DC power-supply faceplate to the off (—) position.
8. Check that the AC or the DC power supply is correctly installed and functioning normally. Verify that the AC OK and DC OK LEDs light steadily, and the PS FAIL LED is not lit.

```text
NOTE: After a power supply is powered on, it can take up to 60 seconds for status indicators—such as the status LEDs on the power supply and the show chassis command display—to indicate that the power supply is functioning normally. Ignore error indicators that appear during the first 60 seconds.
```
   If any of the status LEDs indicates that the power supply is not functioning normally, repeat the installation and cabling procedures.
9. On the external management device connected to the Routing Engine, monitor the startup process to verify that the system has booted properly.

   NOTE: If the system is completely powered off when you power on the power supply, the Routing Engine boots as the power supply completes its startup sequence. Normally, the router boots from the Junos OS on the CompactFlash card.

   After turning on a power supply, wait at least 60 seconds before turning it off.

## Complete the SCBE2-MX Upgrade

1. Verify that the installation is successful and the SCBE2-MX is online by issuing the show chassis environment cb command:

```text
user@host> show chassis environment cb 0
```
   CB 0 status

```text
State Online
```
   Temperature 30 degrees C / 86 degrees F

   ...

```text
user@host> show chassis environment cb 1
```
   CB 1 status

```text
State Online
```
   Temperature 30 degrees C / 86 degrees F

   ...

```text
Other details, such as, temperature, power, etc are also displayed along with the state.
Verify that the fabric planes come online correctly by issuing the show chassis fabric summary command:
user@host> show chassis fabric summary
Plane State Uptime
```
   0 Online 2 days, 19 hours, 10 minutes, 9 seconds

   1 Online 2 days, 19 hours, 10 minutes, 9 seconds

   ...
3. Verify that the backup Routing Engine is back online by issuing the show chassis routing-engine 1 command:

```text
user@host> show chassis routing-engine 1
```
   Routing Engine Status:

   Slot 1:

```text
Current State Backup
```
   ...
4. Verify the SCBE2-MXs before you finish by issuing the show chassis hardware command:

```text
user@host> show chassis hardware
```
   Hardware inventory:

   Item Version Part number Serial number Description

   CB 0 REV 08 750-048307 CABC9829 Enhanced MX SCB 2

   CB 1 REV 08 750-048307 CABC9828 Enhanced MX SCB 2

   ...

   As shown in the example, the MX960 now has SCBE2-MXs.
