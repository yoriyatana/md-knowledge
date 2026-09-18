# set system debugger-on-panic  and set system debugger-on-break

From JTAC support’s suggestion, there is one option to enable kernel debug when crash happened:

```text
configure following two commands into your SRX system:**set system debugger-on-panic**  and **set system debugger-on-break**
```
This will enable the box to fall into debugger when kernel crashes/panic happens ( please note that until you type reset on console, it will not boot upto give you cli access)When box falls to db>, we can collect the following information.**db> btdb> show regdb> show msgbufdb> x/s versiondb> psdb> show pagedb> show intrcntdb> x/x ticksdb> x/x softticksdb> show tlbdb> show pcpudb> show allpcpudb> show allvmsdb> show threadsdb> show files**
