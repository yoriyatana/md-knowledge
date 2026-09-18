# [M/MX] jnxFruOfflineReason

<https://kb.juniper.net/InfoCenter/index?page=content&id=KB29446&act=login>

* *SUMMARY:**

This article provides information about jnxFruOfflineReason.

* *SYMPTOMS:**

jnxFruOfflineReason appears in CHASSISD\_SNMP\_TRAP10 messages.

CHASSISD\_SNMP\_TRAP10 is an SNMP trap message. It is found in the chassisid file when a field-replaceable unit (FRU) goes offline.

jnxFruOfflineReason provides the reason why an FRU went offline.

* *CAUSE:**

When an FRU goes offline, for example, the following message is logged in the chassisd file:

Aug 26 08:52:45 CHASSISD\_SNMP\_TRAP10: SNMP trap generated: FRU power off

(jnxFruContentsIndex 8, jnxFruL1Index 7, jnxFruL2Index 2, jnxFruL3Index 0, jnxFruName PIC:

1x 10GE(LAN/WAN) IQ2 @ 6/1/\*, jnxFruType 11, jnxFruSlot 6, jnxFruOfflineReason 85,

jnxFruLastPowerOff 1332423971, jnxFruLastPowerOn 5231)

This FRU went offline because of jnxFruOfflineReason 85.

As defined in the **Solution** section below, jnxFruOfflineReason 85 means "PIC offlined on ecc errors cross certain limit."

The definitions of the various meanings of jnxFruOfflineReason are listed below.

* *SOLUTION:**

### jnxFruOfflineReason Definitions

unknown(1),                        -- unknown or other

none(2),                          -- none

error(3),                          -- error

noPower(4),                        -- no power

configPowerOff(5),                -- configured to power off

configHoldInReset(6),              -- configured to hold in reset

cliCommand(7),                    -- offlined by cli command

buttonPress(8),                    -- offlined by button press

cliRestart(9),                    -- restarted by cli command

overtempShutdown(10),              -- overtemperature shutdown

masterClockDown(11),              -- master clock down

singleSfmModeChange(12),          -- single SFM mode change

packetSchedulingModeChange(13),    -- packet scheduling mode change

physicalRemoval(14),              -- physical removal

unresponsiveRestart(15),          -- restarting unresponsive board

sonetClockAbsent(16),              -- sonet out clock absent

rddPowerOff(17),                  -- RDD power off

majorErrors(18),                  -- major errors

minorErrors(19),                  -- minor errors

lccHardRestart(20),                -- LCC hard restart

lccVersionMismatch(21),            -- LCC version mismatch

powerCycle(22),                    -- power cycle

reconnect(23),                    -- reconnect

overvoltage(24),                  -- overvoltage

pfeVersionMismatch(25),            -- PFE version mismatch

febRddCfgChange(26),              -- FEB redundancy cfg changed

fpcMisconfig(27),                  -- FPC is misconfigured

fruReconnectFail(28),              -- FRU did not reconnect

fruFwddReset(29),                  -- FWDD reset the fru

fruFebSwitch(30),                  -- FEB got switched

fruFebOffline(31),                -- FEB was offlined

fruInServSoftUpgradeError(32),    -- In Service Software Upgrade Error

fruChasdPowerRatingExceed(33),    -- Chassis power rating exceeded

fruConfigOffline(34),              -- Configured offline

fruServiceRestartRequest(35),      -- restarting request from a service

spuResetRequest(36),              -- SPU reset request

spuFlowdDown(37),                  -- SPU flowd down

spuSpi4Down(38),                  -- SPU SPI4 down

spuWatchdogTimeout(39),            -- SPU Watchdog timeout

spuCoreDump(40),                  -- SPU kernel core dump

fpgaSpi4LinkDown(41),              -- FPGA SPI4 link down

i3Spi4LinkDown(42),                -- I3 SPI4 link down

cppDisconnect(43),                -- CPP disconnect

cpuNotBoot(44),                    -- CPU not boot

spuCoreDumpComplete(45),          -- SPU kernel core dump complete

rstOnSpcSpuFailure(46),            -- Rst on SPC SPU failure

softRstOnSpcSpuFailure(47),        -- Soft Reset on SPC SPU failure

hwAuthenticationFailure(48),      -- HW authentication failure

reconnectFpcFail(49),              -- Reconnect FPC fail

fpcAppFailed(50),                  -- FPC app failed

fpcKernelCrash(51),                -- FPC kernel crash

spuFlowdDownNoCore(52),            -- SPU flowd down, no core dump

spuFlowdCoreDumpIncomplete(53),    -- SPU flowd crash with incomplete core dump

spuFlowdCoreDumpComplete(54),      -- SPU flowd crash with complete core dump

spuIdpdDownNoCore(55),            -- SPU idpd down, no core dump

spuIdpdCoreDumpIncomplete(56),    -- SPU idpd crash with incomplete core dump

spuIdpdCoreDumpComplete(57),      -- SPU idpd crash with complete core dump

spuCoreDumpIncomplete(58),        -- SPU kernel crash with incomplete core dump

spuIdpdDown(59),                  -- SPU idpd down

fruPfeReset(60),                  -- PFE reset

fruReconnectNotReady(61),          -- FPC not ready to reconnect

fruSfLinkDown(62),                -- FE - Fabric links down

fruFabricDown(63),                -- Fabric transitioned from up to down

fruAntiCounterfeitRetry(64),      -- FPC offlined due to Anti Counterfeit Retry

fruFPCChassisClusterDisable(65),  -- FPC offlined due to Chassis Cluster Disable

spuFipsError(66),                  -- SPU fips error

fruFPCFabricDownOffline(67),      -- FPC offlined due to Fabric down

febCfgChange(68),                  -- FEB config change

routeLocalizationRoleChange(69),  -- Route localization role change

fruFpcUnsupported(70),            -- FPC unsupported

psdVersionMismatch(71),            -- PSD version mismatch

fruResetThresholdExceeded(72),    -- FRU Reset Threshold Exceeded

picBounce(73),                    -- PIC Bounce

badVoltage(74),                    -- bad voltage

fruFPCReducedFabricBW(75),        -- FPC offlined due to Reduced Fabric Bandwidth

fruAutoheal(76),                  -- FRU offlined due to software autoheal action

builtinPicBounce(77),              -- Builtin PIC Bounce

fruFabricDegraded(78),            -- Fabric running in degraded state

fruFPCFabricDegradedOffline(79),  -- FPC offlined due to degraded fabric action

fruUnsupportedSlot(80),            -- FRU unsupported in the current slot

fruRouteLocalizationMisCfg(81),    -- Route Localization - FPC Misconfiguration

fruTypeConfigMismatch(82),        -- FRU Type configuration mismatch

lccModeChanged(83),                -- LCC mode changed on the SFC

hwFault(84),                      -- Hardware fault

fruPICOfflineOnEccErrors(85),      -- PIC offlined on ecc errors cross ceratins limit.

fruFpcIncompatible(86),            -- FPC imcompatible with other FPCs

fruFpcFanTrayPEMIncompatible(87),  -- FPC incompatible with FAN-TRAYs ,PEMs

fruUnsupportedFirmware(88),        -- Firmware on this FRU not supported

openflowConfigChange(89),          -- Openflow config change offlines FPC

fruFpcScbIncompatible(90),        -- FPC incompatible with SCB

fruReUnresponsive(91),            -- Corresponding slot RE unresponsive

hwError(92),                      -- Hardware error

fruErrorManagerReqFPCReset(93),    -- Error manager requested FPC reset.

fruIncompatibleWithPEM(94),        -- FRU incompatible with power supply

fruIncompatibleWithSIB(95),        -- FRU incompatible with SIB

sibIncompatibleWithOtherSIB(96),  -- FRU incompatible with other SIB

fruPfeErrors(97),                  -- PIC offlined on PFE Errors cross limit.

vpnLocalizationRoleChange(98),    -- VPN localization core-facing-FPC role change

fruFpcFanTrayIncompatible(99),    -- FPC incompatible with FAN-TRAYs

fruFpcPEMIncompatible(100),        -- FPC incompatible with PEMs

mixedSwitchFabric(101),            -- Mixed Switch Fabric error

unsupportedFabric(102),            -- unsupported Fabric error

jamConfigError(103),              -- JAM configuration error

fruFpcHFanTrayIncompatible(104),  -- FPC incompatible with Horizontal FAN-TRAYs

gnfIsOffline(105),                -- GNF is Offline

gnfdisconnected(106),              -- GNF disconnected

fruIncompatibleWithVersion(107),  -- Incompatibile with BSYS

fruInvalidConfig(108),            -- FRU invalid configuration

katsPostError(109),                -- KATS post error

katsRuntimeError(110),            -- KATS run time error

gnfInitRestart(111),              -- GNF has initiated FPC restart

gnfOverlapMac(112),                -- MAC address overlap detected between GNFs

fruOfflinedonFipsConstraints(113), -- FRU offlined due to FIPS constraints

fpcUnsupportedMode(114),          -- FPC Unsupported Mode

fpcFtrayNotVerified(115),          -- FPC Ftray not verified

fpcPemNotVerified(116),            -- FPC PEM not verified

fabricAsicFault(117)              -- Fabric ASIC Fault
