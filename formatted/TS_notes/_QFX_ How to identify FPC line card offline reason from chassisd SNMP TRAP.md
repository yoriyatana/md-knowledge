# [QFX] How to identify FPC line card offline reason from chassisd SNMP TRAP

<https://kb.juniper.net/InfoCenter/index?page=content&id=KB36874&actp=METADATA>

* *SUMMARY:**

When a modular chassis FPC line card goes online or offline, the chassisd process generates a SNMP trap message to record FRU power on / power off events, with FRU slot number, FRU type, FRU model name and offline reason code. By checking the offline reason code in the SNMP trap message, we can identify the actual reason that triggered the specific FRU to go offline. This information can be useful for troubleshooting FRU related issues.

* *SOLUTION:**

Syslog message example:

Apr  1 13:19:21.126  QFX10008 chassisd[7236]: %DAEMON-5-CHASSISD\_SNMP\_TRAP10: SNMP trap generated: FRU power off (jnxFruContentsIndex 7, jnxFruL1Index 7, jnxFruL2Index 0, jnxFruL3Index 0, jnxFruName FPC: ULC-36Q-12Q28 @ 6/\*/\*, jnxFruType 3, jnxFruSlot 6, jnxFruOfflineReason 7, jnxFruLastPowerOff 67219028, jnxFruLastPowerOn 6088

The following table can be used as a reference to identify the actual reason why a specific FRU went offline. For instance, the offline reason in the above example, the SNMP trap is code 7. By checking the following table, we know the offline reason is "offlined by cli command".

Code#  Reason                      Explanation

1      unknown                      unknown or other

2      none                        none

```text
3      error                        error
```
4      noPower                      no power

5      configPowerOff              configured to power off

6      configHoldInReset            configured to hold in reset

7      cliCommand                  offlined by cli command

8      buttonPress                  offlined by button press

9      cliRestart                  restarted by cli command

10    overtempShutdown            overtemperature shutdown

11    masterClockDown              master clock down

12    singleSfmModeChange          single SFM mode change

13    packetSchedulingModeChange  packet scheduling mode change

14    physicalRemoval              physical removal

15    unresponsiveRestart          restarting unresponsive board

16    sonetClockAbsent            sonet out clock absent

17    rddPowerOff                  RDD power off

18    majorErrors                  major errors

19    minorErrors                  minor errors

20    lccHardRestart              LCC hard restart

21    lccVersionMismatch          LCC version mismatch

22    powerCycle                  power cycle

23    reconnect                    reconnect

24    overvoltage                  overvoltage

25    pfeVersionMismatch          PFE version mismatch

26    febRddCfgChange              FEB redundancy cfg changed

27    fpcMisconfig                FPC is misconfigured

28    fruReconnectFail            FRU did not reconnect

29    fruFwddReset                FWDD reset the fru

30    fruFebSwitch                FEB got switched

31    fruFebOffline                FEB was offlined

```text
32    fruInServSoftUpgradeError    In Service Software Upgrade Error
```
33    fruChasdPowerRatingExceed    Chassis power rating exceeded

34    fruConfigOffline            Configured offline

35    fruServiceRestartRequest    restarting request from a service

36    spuResetRequest              SPU reset request

37    spuFlowdDown                SPU flowd down

38    spuSpi4Down                  SPU SPI4 down

39    spuWatchdogTimeout          SPU Watchdog timeout

40    spuCoreDump                  SPU kernel core dump

41    fpgaSpi4LinkDown            FPGA SPI4 link down

42    i3Spi4LinkDown              I3 SPI4 link down

43    cppDisconnect                CPP disconnect

44    cpuNotBoot                  CPU not boot

45    spuCoreDumpComplete          SPU kernel core dump complete

46    rstOnSpcSpuFailure          Rst on SPC SPU failure

47    softRstOnSpcSpuFailure      Soft Reset on SPC SPU failure

48    hwAuthenticationFailure      HW authentication failure

49    reconnectFpcFail            Reconnect FPC fail

```text
50    fpcAppFailed                FPC app failed
```
51    fpcKernelCrash              FPC kernel crash

52    spuFlowdDownNoCore          SPU flowd down no core dump

53    spuFlowdCoreDumpIncomplete  SPU flowd crash with incomplete core dump

54    spuFlowdCoreDumpComplete    SPU flowd crash with complete core dump

55    spuIdpdDownNoCore            SPU idpd down no core dump

56    spuIdpdCoreDumpIncomplete    SPU idpd crash with incomplete core dump

57    spuIdpdCoreDumpComplete      SPU idpd crash with complete core dump

58    spuCoreDumpIncomplete        SPU kernel crash with incomplete core dump

59    spuIdpdDown                  SPU idpd down

60    fruPfeReset                  PFE reset

61    fruReconnectNotReady        FPC not ready to reconnect

62    fruSfLinkDown                FE - Fabric links down

63    fruFabricDown                Fabric transitioned from up to down

64    fruAntiCounterfeitRetry      FPC offlined due to Anti Counterfeit Retry

65    fruFPCChassisClusterDisable  FPC offlined due to Chassis Cluster Disable

```text
66    spuFipsError                  SPU fips error
```
67    fruFPCFabricDownOffline      FPC offlined due to Fabric down

68    febCfgChange                  FEB config change

69    routeLocalizationRoleChange  Route localization role change

70    fruFpcUnsupported            FPC unsupported

71    psdVersionMismatch            PSD version mismatch

72    fruResetThresholdExceeded    FRU Reset Threshold Exceeded

73    picBounce                    PIC Bounce

74    badVoltage                    bad voltage

75    fruFPCReducedFabricBW        FPC offlined due to Reduced Fabric Bandwidth

76    fruAutoheal                  FRU offlined due to software autoheal action

77    builtinPicBounce              Builtin PIC Bounce

```text
78    fruFabricDegraded            Fabric running in degraded state
```
79    fruFPCFabricDegradedOffline  FPC offlined due to degraded fabric action

80    fruUnsupportedSlot            FRU unsupported in the current slot

81    fruRouteLocalizationMisCfg    Route Localization - FPC Misconfiguration

82    fruTypeConfigMismatch        FRU Type configuration mismatch

83    lccModeChanged                LCC mode changed on the SFC

84    hwFault                      Hardware fault

85    fruPICOfflineOnEccErrors      PIC offlined on ecc errors cross ceratins limit.

86    fruFpcIncompatible            FPC imcompatible with other FPCs

87    fruFpcFanTrayPEMIncompatible  FPC incompatible with FAN-TRAYs PEMs

```text
88    fruUnsupportedFirmware        Firmware on this FRU not supported
```
89    openflowConfigChange          Openflow config change offlines FPC

90    fruFpcScbIncompatible        FPC incompatible with SCB

91    fruReUnresponsive            Corresponding slot RE unresponsive

```text
92    hwError                      Hardware error
93    fruErrorManagerReqFPCReset    Error manager requested FPC reset.
```
94    fruIncompatibleWithPEM        FRU incompatible with power supply

95    fruIncompatibleWithSIB        FRU incompatible with SIB

96    sibIncompatibleWithOtherSIB  FRU incompatible with other SIB

97    fruPfeErrors                  PIC offlined on PFE Errors cross limit.

98    vpnLocalizationRoleChange    VPN localization core-facing-FPC role change

99    fruFpcFanTrayIncompatible    FPC incompatible with FAN-TRAYs

100    fruFpcPEMIncompatible        FPC incompatible with PEMs

```text
101    mixedSwitchFabric            Mixed Switch Fabric error
102    unsupportedFabric            unsupported Fabric error
103    jamConfigError              JAM configuration error
```
104    fruFpcHFanTrayIncompatible  FPC incompatible with Horizontal FAN-TRAYs

105    gnfIsOffline                GNF is Offline

106    gnfdisconnected              GNF disconnected

107    fruIncompatibleWithVersion  Incompatibile with BSYS
