# KB31811_[MX] How to check if Enhanced Subscriber Management (bbe-smgd) is enabled and working

* *Desciption**

This article describes how a system administrator can check if a system has been rebooted after enabling Enhanced Subscriber Management.

* *Symptoms**

On a fresh install of the Junos Subscriber Management build, the system must be rebooted according to Juniper's documentation on [Configuring Junos OS Enhanced Subscriber Management](http://www.juniper.net/documentation/en_US/junos/topics/task/configuration/subscriber-management-enhanced-initial-setup.html).

```text
Operating a system without a reboot may result in unexpected system behavior. How can a system administrator verify if the chassis rebooted or not at a later state?
```

* *Solution**

Configured Enhanced Subscriber Management  without system Reboot:

From Cli:

```text
user@host> show system subscriber-management statistics
```

```text
subscriber-management not enabled <-- System reports that Subscriber Management is "not enabled"
```

```text
command not supported
```

From RE Shell:

```text
% sysctl -a | grep enhance
```

```text
net.enhanced\_rpf\_debug: 0
```

```text
net.pfe.debug\_ae\_count\_lag\_enhanced: -1
```

```text
net.pfe.debug\_force\_lag\_enhanced: 0
```

```text
net.disable\_lag\_enhanced: 0
```

```text
net.enhanced\_bbe\_support: 2 <-- “2” indicates the system is not running Enhanced Subscriber Management
```

...

After System Reboot:

From Cli:

```text
user@host> show system subscriber-management statistics
```

Session Manager started @ Thu Jun 1 09:59:32 2017

Session Manager cleared @ Thu Jun 1 09:59:32 2017

- -------------------------------------------------------------

Packet Statistics

- -------------------------------------------------------------

I/O Statistics: <-- I/O statistics displayed means that Subscriber Management has been "enabled"

- -------------------------------------------------------------

Rx Statistics

packets : 0

Tx Statistics

packets : 0

Layer 3 Statistics

Rx Statistics

packets : 0

Tx Statistics

packets : 0

From RE Shell:

```text
% sysctl -a | grep enhance
```

```text
net.enhanced\_rpf\_debug: 0
```

```text
net.pfe.debug\_ae\_count\_lag\_enhanced: -1
```

```text
net.pfe.debug\_force\_lag\_enhanced: 0
```

```text
net.disable\_lag\_enhanced: 0
```

```text
net.enhanced\_bbe\_support: 1 <-- “1” Indicates the system is enabled with Enhanced Subscriber Management
```

...

##
