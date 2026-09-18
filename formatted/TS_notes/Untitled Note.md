# Untitled Note

Sorry for delay in responding

I could understand that your question is that the temperature threshold to high fan speed is 60,but why do many components of FPC have a temperature over 60 but fan speed is still normal?

Please be informed that the health of the FPC is defined by the below mentioned command .Which provide the overall detail about the FPC as below.

```text
user@switch> show chassis fpc detail
```

Slot 0 information:

```text
State                Online
```

Temperature           28 degrees C / 82 degrees F

Total CPU DRAM         2820 MB

Total SRAM            0 MB

Total SDRAM            0 MB

Start time             2010-09-20 01:34:13 PDT

Uptime               3 days, 3 hours, 31 minutes, 48 seconds

The speed of the FAN is determined by the FPC temperature values as mentioned above.

When ever the FPC is reached its threshold values then the fan speed will be changed accordingly.

As you mentioned the values in the below mentioned output

```text
Show chassis environment | no-more
```

It define the chip level temperature values its wont have any impact on the fan speed .Only the overall FPC temperature values define the fan speed.

Temperature (PMB)—Temperature of the air passing by the Processor Mezzanine Board (PMB) at the bottom of the FPC.

Temperature (Intake)—Temperature of the air flowing into the chassis.

Temperature (Exhaust)—Exhaust temperatures for multiple zones (Exhaust A and Exhaust B).

Temperature (TLn)-–Temperature of the specified Lookup ASIC (TL) of the packet forwarding engine on the FPC.

Temperature (TQn)-–Temperature of the specified Queuing and Memory Interface ASIC (TQ) of the packet forwarding engine on the FPC.

Please free to ask incase if you have any further question from the clarification.
