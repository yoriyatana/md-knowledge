# Adaptive SPF Timers in JUNOS

[https://networker.technolabs.org/?p=129](https://networker.technolabs.org/?p=129)

Juniper Networks uses a linear fast/slow algorithm for adaptive SPF timers. So, it introduced the SPF delay timer which is the minimum delay in the time between the detection of a topology change and when the SPF algorithm actually runs. This period is 200ms by default. The period is configurable with the **spf-delay** command to between 50 and 8000ms.

Secondly, they introduce a second parameter which is **rapid-runs**.  If three (the default) SPF runs are triggered in quick succession, indicating instability in the network, the router will enter the “slow mode” and a third parameter called the **hold-down** timer will start. Any subsequent SPF calculation is not run until the hold-down timer expires. The routers remain in this “slow mode” until the hold-down period have passed since the last SPF run—indicating that the network has converged—and then switches back to “fast mode”, and the system reverts to the configured values for the delay and rapid-runs statements.

The default values for SPF calculations in JUNOS can be seen below:

|**Default SPF timers values in JUNOS**                                                                                           |
|---------------------------------------------------------------------------------------------------------------------------------|
|Full SPF runs: 280SPF delay: **0.200000**sec, SPF holddown: **5** sec, SPF rapid runs: **3**
r2@r2> show ospf overview | match SPF|

Now we are going to play with the timers and run the debugs, and examine the behavior. We will set the delay to 1 sec and the hold-down timer to 20 sec while keeping the rapid-runs as default.
![JUNOS-diagram1.png](image/JUNOS-diagram1.png)
