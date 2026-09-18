# KB26261_[M/MX/T-series] Troubleshooting Checklist - Routing Engine High CPU

Description

This article provides a checklist that can be used to troubleshoot Routing Engine (RE) High CPU utilization related issues on M/MX/T routers.

Symptoms

A checklist that can be used to troubleshoot RE High CPU utilization related issues on M/MX/T routers.

Solution

Perform the following checks:

1. Check the CPU utilization on the Junos device with the command:    show chassis routing-engine

   > lab> show chassis routing-engine
   >
   > Routing Engine status:
   >
   > Slot 0:
   >
   > CPU utilization:
   >
   > User 0 percent
   >
   > Background 0 percent
   >
   > Kernel 5 percent
   >
   > Interrupt 0 percent
   >
   > Idle 95 percent
   >
   > Routing Engine status:
   >
   > Slot 1:
   >
   > CPU utilization:
   >
   > User 94 percent
   >
   > Background 0 percent
   >
   > Kernel 0 percent
   >
   > Interrupt 1 percent
   >
   > Idle 2 percent

   In the above output, the CPU utilization of the Routing Engines, as well as for various software components, are displayed.

- User : Percentage of CPU time being used by user processes. For example, RPD and various other daemons.
- Background : Percentage of CPU time being used by background processes.
- Kernel : Percentage of CPU time being used by kernel processes.
- Interrupt : Percentage of CPU time being used by interrupts.
- Idle : Percentage of CPU time that is idle.

  For more information about the output of the 'show chassis routing-engine' command, refer to the following link:

  <http://www.juniper.net/techpubs/en_US/junos/topics/reference/command-summary/show-chassis-routing-engine.html>

3. If the User or Background process is high, continue to step 2 for further analysis.
5. If the Interrupt process is high, jump to [Interrupt process consuming High CPU](https://supportportal.juniper.net/s/article/M-MX-T-series-Troubleshooting-Checklist-Routing-Engine-High-CPU?language=en_US#interrupt).

If the Kernel process is high, jump to [Kernel process consuming High CPU](https://supportportal.juniper.net/s/article/M-MX-T-series-Troubleshooting-Checklist-Routing-Engine-High-CPU?language=en_US#kernel).

7. If the Cscript process is high, jump to [CSCRIPT\_process\_consuming\_High\_CPU](https://supportportal.juniper.net/s/article/M-MX-T-series-Troubleshooting-Checklist-Routing-Engine-High-CPU?language=en_US#CSCRIPT_process_consuming_High_CPU).

   If the NTPD process is high, jump to [NTPD\_process\_consuming\_High\_CPU](https://supportportal.juniper.net/s/article/M-MX-T-series-Troubleshooting-Checklist-Routing-Engine-High-CPU?language=en_US#NTPD_process_consuming_High_CPU).

   - --
8. Check the CPU utilization consumed by each software process with the command:    show system process extensive

   lab > show system processes extensive

   last pid: 7920; load averages: 0.00, 0.02, 0.00 up 0+07:11:16 21:10:07

   203 processes: 4 running, 182 sleeping, 17 waiting

   Mem: 461M Active, 71M Inact, 106M Wired, 860M Cache, 69M Buf, 2009M Free

   Swap: 3584M Total, 3584M Free

   PID USERNAME THR PRI NICE SIZE RES STATE TIME WCPU COMMAND

   11 root 1 171 52 0K 12K RUN 412:13 1.07% idle

   1351 root 2 8 -88 38592K 14076K nanslp 15:14 2.98% chassisd

   2307 root 1 4 0 42156K 19240K kqread 8:11 93.05% rpd <---------------

   12 root 1 -20 -139 0K 12K RUN 0:31 0.00% swi7: clock sio

   20 root 1 -68 -187 0K 12K WAIT 0:24 0.00% irq10: em0 em1+++\*

   1184 root 1 76 0 0K 12K 0:23 0.00% bcmLINK.0

   80 root 1 -8 0 0K 12K mdwait 0:11 0.00% md1

   14 root 1 -40 -159 0K 12K WAIT 0:06 0.00% swi2: net

   142 root 1 -8 0 0K 12K mdwait 0:06 0.00% md4

   1413 root 3 20 0 64764K 37628K sigwai 0:05 0.00% jpppd

   9 root 1 171 52 0K 12K pgzero 0:03 0.00% pagezero

   1373 root 1 96 0 3232K 1460K select 0:03 0.00% license-check

   1416 root 1 96 0 9528K 4932K select 0:02 0.00% jdiameterd

   1183 root 1 76 0 0K 12K 0:02 0.00% bcmXGS3AsyncTX

   1392 root 1 96 0 11232K 7024K select 0:02 0.00% l2ald

   5632 root 1 96 0 44200K 35340K select 0:02 0.00% mgd

   1422 root 2 96 0 15012K 6092K select 0:02 0.00% pfed

   1419 root 1 96 0 27924K 24816K select 0:02 0.00% snmpd

   1182 root 1 76 0 0K 12K 0:02 0.00% bcmTX

   15 root 1 -16 0 0K 12K - 0:02 0.00% yarrow

   1391 root 1 4 0 40488K 13644K kqread 0:02 0.00% rpd

   1348 root 1 96 0 1608K 1080K select 0:01 0.00% bslockd

   1352 root 1 96 0 4572K 2964K select 0:01 0.00% alarmd

   49 root 1 -16 0 0K 12K - 0:01 0.00% schedcpu

   1418 root 1 96 0 30320K 8096K select 0:01 0.00% dcd

   Look for which process is consuming WCPU (Weighted CPU). Also observe the STATE of the process.  From the output above, you can see that RPD is at 93% utilization and is in the kqread (kernel queue read) state. Also, look for TIME (number of system and user CPU seconds that the process has used) and RES (current amount of resident memory, in kilobytes which should be less than SIZE allocated to it).

   If the RPD process is high, jump to [RPD consuming high CPU](https://supportportal.juniper.net/s/article/M-MX-T-series-Troubleshooting-Checklist-Routing-Engine-High-CPU?language=en_US#rpd).

   For more information about the output of the above command, refer to the following link:

   <http://www.juniper.net/techpubs/en_US/junos/topics/reference/command-summary/show-system-processes.html>
9. Check the output of the following commands around the time of the High CPU utilization event for any additional clues:

- show system virtual-memory | no-more

  For more information on the above command output please refer to the following:

  <https://www.juniper.net/techpubs/en_US/junos/topics/reference/command-summary/show-system-virtual-memory.html>
- show task memory detail | no-more

  For more information on the above command output please refer to the following:

  <http://www.juniper.net/techpubs/en_US/junos/topics/reference/command-summary/show-task-memory.html>
- show log messages | no-more

10. If you need to open a case with your technical support representative, collect the output specified in the 'High CPU' section of the Data Collection Checklist:

    [KB22637 - Data Collection Checklist - Logs/data to collect for troubleshooting](https://supportportal.juniper.net/s/article/M-MX-PTX-T-Data-Collection-Checklist-Logs-data-to-collect-for-troubleshooting).

- --

####

####

#### RPD consuming high CPU

If RPD is consuming high CPU, then perform the following checks and verify the following parameters:

1. Check the interfaces: Check if any interfaces are flapping on the router. This can be verified by looking at the output of the show log messages and show interfaces ge-x/y/z extensive commands. Find out why they are flapping; if possible you can consider enabling the hold-time for link up and link down.
2. Check if there any Traceoptions configured.
3. Check if there are syslog error messages related to interfaces or any FPC/PIC, by looking at the output of show log messages .
4. Check the routes:  Verify the total number of routes that are learned by the router by looking at the output of show route summary . Check if it has reached the maximum limit.
5. Check the RPD tasks: Identify what is keeping the process busy. This can be checked by first enabling set task accounting on .   Important:  This might increase the load on the CPU and its utilization; so do not forget to turn it off when you are finished with the required output collection.  Then run show task accounting and look for the thread with the high CPU time:

   user@router> show task accounting

   Task Started User Time System Time Longest Run

   Scheduler 146051 1.085 0.090 0.000

   Memory 1 0.000 0 0.000

   BGP.128.0.0.4+179 268 13.975 0.087 0.328

   BGP.0.0.0.0+179 18375163 1w5d 23:16:57.823 48:52.877 0.142

   BGP RT Background 134 8.826 0.023 0.099

   Find out why a thread, which is related to a particular prefix or a protocol, is taking high CPU.

   You can also verify if routes are oscillating (or route churns) by looking at the output of the shell command:

   % rtsockmon –t

   sender flag type op

   [12:12:24] rpd P route delete inet 110.159.206.28 tid=0 plen=30 type=user flags=0x180 nh=indr nhflags=0x4 nhidx=1051574 altfwdnhidx=0 filtidx=0

   [12:12:24] rpd P route change inet 87.255.194.0 tid=0 plen=24 type=user flags=0x0 nh=indr nhflags=0x4 nhidx=1048903 altfwdnhidx=0 filtidx=0

   [12:12:26] rpd P route delete inet 219.94.62.120 tid=0 plen=29 type=user flags=0x180 nh=indr nhflags=0x4 nhidx=1051583 altfwdnhidx=0 filtidx=0

   Pay attention to the timestamp, behavior, and prefix. If a massive routing update can be found with the same prefix or protocol, then there could be route oscillation or interface bouncing.
6. Check RPD Memory. Some times High memory utilization might indirectly lead to high CPU, to interpret RPD memory utilization in Junos, refer to

   <http://www.juniper.net/techpubs/en_US/junos/topics/reference/general/rpd-memory-faq.html>.
7. If still the rpd is consuming high cpu then collect the logs from data collection checklist

   [KB22637 - Data Collection Checklist - Logs/data to collect for troubleshooting](https://supportportal.juniper.net/s/article/M-MX-PTX-T-Data-Collection-Checklist-Logs-data-to-collect-for-troubleshooting)and open a case with your technical support representative.

Another way to check the rtsockmon output is as follows:

> start shell

% rtsockmon -t > /var/tmp/rtsockmon.txt

(wait 1 minute)

Press CTRL+C

Then in a Unix-like OS which is not Junos OS, issue:

% cat rtsockmon.txt | grep inet | grep add | grep route | cut -c 50- | awk '{print $1 " " $2}' | sort | uniq -c | rev |cut -b 7-| rev |sort

The output will look something like this:

3    10.51.11.66

151  10.51.145.116

2    10.51.147.28

The first column will be the number of times the route was added. The second column is the prefix. So in the above example, 10.51.145.116 flappe: 151 times!

- --

####

####

#### Interrupt process consuming High CPU

As per the output of the show chassis routing-engine command, Interrupt may be consuming a lot of CPU resources.

> CPU utilization:
>
> User 0 percent
>
> Background 0 percent
>
> Kernel 11 percent
>
> Interrupt 47 percent
>
> Idle 42 percent

Collect the output of the following commands:

- show chassis routing-engine
- show system process extensive | no-more
- show system virtual-memory | no-more
- show task memory detail | no-more
- show log messages | no-more

Some of the reasons for high interrupt CPU are as follows:

- The first possibility is duplicated via IP/ARP flooding on one of the device's ports. For this case, high CPU utilization may even cause the connection to be lost between both of the REs. Massive ARP duplicating error logs can be found:

  Apr 23 17:12:37.666 2010 igw02.brf-re0 /kernel: %KERN-3-KERN\_ARP\_DUPLICATE\_ADDR:

  duplicate IP address 10.55.1.219! sent from address: 00:a0:a5:64:2d:6c (error count = 3672452574)

  Apr 23 17:13:37.632 2010 igw02.brf-re0 /kernel: %KERN-3-KERN\_ARP\_DUPLICATE\_ADDR:

  duplicate IP address 10.55.1.219! sent from address: 00:a0:a5:64:2d:6c (error count = 3675570687)

  Apr 23 17:14:37.598 2010 igw02.brf-re0 /kernel: %KERN-3-KERN\_ARP\_DUPLICATE\_ADDR:

  duplicate IP address 10.55.1.219! sent from address: 00:a0:a5:64:2d:6c (error count = 3678688551)

  After addressing the ARP problem, the issue was resolved.
- Another trigger is due to out of band (OOB) devices. You can identify this by looking at the output of show system process extensive :

  PID USERNAME THR PRI NICE SIZE RES STATE TIME WCPU COMMAND

  27 root 1 -48 -167 0K 12K RUN 223:30 48.19% swi0: sio

  Some particular logs from chassisd and log messages:

  Feb 7 00:55:53 I2CS write cmd to FPM#0 [0x0], reg 0x44, cmd 0x11

  Feb 7 00:55:54 I2CS write cmd to FPM#0 [0x0], reg 0x44, cmd 0x11

  Dec 22 01:19:59.261 2009 igw01.ash.re1 /kernel: %KERN-3: sio1:

  164 more interrupt-level buffer overflows (total 450)

  Dec 22 01:20:00.847 2009 igw01.ash.re1 /kernel: %KERN-3: sio1: 315 more interrupt-level buffer overflows

  (total 765)

  Dec 28 17:37:09.835 2009 igw01.ash.re1 getty[3917]: %AUTH-3: getty exiting due to excessive running time

  Dec 28 17:38:17.154 2009 igw01.ash.re1 getty[3918]: %AUTH-3: getty exiting due to excessive running time

  This issue can be resolved by changing the console cable.

- --

####

####

#### Kernel process consuming High CPU

As per the output of the show chassis routing-engine command, kernel  may be consuming a lot of CPU resources.

> CPU utilization:
>
> User 0 percent
>
> Background 0 percent
>
> Kernel 87 percent
>
> Interrupt 11 percent
>
> Idle 2 percent

Collect the output of the following commands:

- show chassis routing-engine
- show system process extensive | no-more
- show system virtual-memory | no-more
- show system processes memory
- From Shell:  /sbin/sysctl -a | grep vm.kmem (to verify if kernel has high memory untilization)

One of the symptoms that occur with high kernel CPU usage are messages with RPD\_SCHED\_SLIP in the logs.

show log messages | match RPD\_SCHED\_SLIP

Jul 30 12:24:11 m10i-a-re0 rpd[1304]: RPD\_SCHED\_SLIP: 7 sec scheduler slip, user: 1 sec 339119 usec, system: 0 sec, 0 usec Jul 30 12:25:29 m10i-a-re0 rpd[1304]: RPD\_SCHED\_SLIP: 4 sec scheduler slip, user: 1 sec 431622 usec, system: 0 sec, 0 usec Jul 30 12:25:37 m10i-a-re0 rpd[1304]: RPD\_SCHED\_SLIP: 4 sec scheduler slip, user: 1 sec 528918 usec, system: 0 sec, 74784 usec Jul 30 17:47:55 m10i-a-re0 rpd[1304]: RPD\_SCHED\_SLIP: 4 sec scheduler slip, user: 0 sec 526784 usec, system: 0 sec, 4608 usec Jul 30 17:48:03 m10i-a-re0 rpd[1304]: RPD\_SCHED\_SLIP: 4 sec scheduler slip, user: 1 sec 285283 usec, system: 0 sec, 19077 usec

Some of the reasons for high kernel CPU are as follows:

- CLI sessions are not closed gracefully on the router.  In this case, one would see mgd running high on CPU, starving the kernel of CPU cycles.

  1059 root 1 132 0 24344K 18936K RUN 405.0H 43.75% mgd

  26275 root 1 132 0 24344K 18936K RUN 353.5H 43.75% mgd

  CPU utilization:

  User 12 percent

  Kernel 87 percent

  Interrupt 0 percent

  Idle 0 percent

  One way to address this issue is to kill the mgd processes eating up the CPU.

- 'Sampling' is enabled on the router.  This sometimes leads to high kernel CPU; to address this, reduce the rate at which you are sampling on the router.

- --

#### [Cscript process consuming High CPU](https://supportportal.juniper.net/s/article/M-MX-T-series-Troubleshooting-Checklist-Routing-Engine-High-CPU?language=en_US)

- Collect the output of the following commands:

root@JTAC> show system process extensive | no-more

PID USERNAME THR PRI NICE SIZE RES STATE TIME WCPU COMMAND

41037 root 1 8 0 125M 122M nanslp 0:48 52.84% cscrip t

root@JTAC> show log messages | match cscript

Event message: Process (41037,cscript) has exceeded 85% of RLIMIT\_DATA:

root@JTAC> show system core-dumps no-forwarding

- rw-rw---- 1 root wheel 18450069 Nov 12 18:52 /var/tmp/cscript.core.0.gz

If there are any core dumps also upload to them to the FTP server to be decoded

- Display logging data associated with all script processing using show log cscript.log . Check which scripts are running and consuming the HIGH CPU. For example:

root@JTAC> show log cscript.log | last

Jan 24 19:12:44 no errors from jais-SN-activate-scripts.slax

Jan 24 19:16:28 no errors from jais-SN-activate-scripts.slax

Jan 24 19:31:22 no errors from jais-SN-activate-scripts.slax

This can be resolved by :

- The log messages Event message: Process (41037,cscript) has exceeded 85% of RLIMIT\_DATA may refer to PR722161:

[https://prsearch.juniper.net/InfoCenter/index?page=prcontent&id=PR722161](https://prsearch.juniper.net/problemreport/PR722161)

- Killing the CSCRIPT process via the PID will be a temporary fix until the script starts again. The PID can be found via show sys proc exten . Example:

% kill -9 41037 (from shell)

- Dampening script execution:

Please refer to the following:

<http://www.juniper.net/techpubs/en_US/junos14.1/topics/task/configuration/script-dampening-configuration.html>

- If the CSCRIPT is still high then the script may containCPU-intensive remote procedure call. To fix this the running scripts must be deactivated from configuration. Deactivate the running scripts checked from previous command show log cscript.log | last, example below:

disable juniper-ais system scripts commit file jais-SN-activate-scripts.slax

- --

#### [NTPD process consuming High CPU](https://supportportal.juniper.net/s/article/M-MX-T-series-Troubleshooting-Checklist-Routing-Engine-High-CPU?language=en_US)

Collect the output of the following commands:

show system process extensive | no-more

PID USERNAME THR PRI NICE SIZE RES STATE TIME WCPU COMMAND

1615 root 1 129 0 2640K 2664K RUN 150:07 69.19% ntpd

If unwanted NTP requests come into a Junos device, the NTP process will occupy resources such as memory and CPU, slowing down other processes and affecting overall system functionality. In extreme cases, the situation could result in traffic loss or protocol flaps. The most effective mitigation is to apply a firewall filter to allow only trusted addresses and networks, plus the router's loopback address, access to the NTP service on the device, rejecting all other requests. For example:

term allow-ntp {

from {

source-address {

;

;

}

protocol udp;

port ntp;

}

then accept;

}

term block-ntp {

from {

protocol udp;

port ntp;

}

then {

discard;

}

}

Apply the firewall filter to the lo0 interface.

Modification History

2020-06-08: Under 'RPD consuming high CPU' section, added check Traceoptions configured.

2020-02-03: Article reviewed for accuracy. Article is correct and complete.

##
