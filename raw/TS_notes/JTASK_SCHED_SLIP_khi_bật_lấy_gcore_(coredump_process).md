# JTASK_SCHED_SLIP khi bật lấy gcore (coredump process)

Thank you for your detailed information about FPCs crashed. I agree with you that the trigger of the FPC crashed was changing ARP on interface irb.3913 but that is not the root cause of this issue. You don't touch any previous events like JTASK_SCHED_SLIP  logs or LDP sessions down,...

 

As I mentioned before, the first gcore taking was between 23:21:07 and 23:22:24. During that time, the JTASK_SCHED_SLIP [duration="28"] log was raised at 23:21:59. Due to high kernel CPU usage for 28 seconds, T-LDP sessions went down and trafic was switched between PECD.01 and PECD.02. Next, the devices hit the PR as mentioned and some FPCs rebooted.

 

<27>1 2021-08-07T23:21:59.055+07:00 HHT9402.PECD.MX2020.02_RE0 rpd 4625 JTASK_SCHED_SLIP [junos@2636.1.1.1.2.93 duration="28" user-seconds="0" user-microseconds="0" system-seconds="0" system-microseconds="0"]

 

Today, when taking the gcore in the lab, I also observed the JTASK_SCHED_SLIP log each time the gcore command was executed. Can you explain about JTASK_SCHED_SLIP log in this situation and continue to analyze the root cause of ldp sesions down?
