# How to collect vmhost coredumps from Next Generation Routing Engine (NG-RE)

In NG-RE, there are two levels of coredumps to be collected for JTAC analysis:

1. Junos OS VM
2. Linux based host (VMHost)

#### Steps for collecting 'vmhost' coredumps:

1. Check if any crashes occurred on the vmhost:

```text
user@host> show vmhost crash
```
Compute cluster: cluster1-re-cc

Compute node: cluster1-re-cn

Crash Info

==========

total 0  <<< 0 means there is no crashes in vmhost

2. If there are any vmhost coredumps, copy them from /var/crash on the vmhost to Junos OS VM /var/tmp:

```text
request vmhost file-copy crash from-jnode  to-vjunos /var/tmp/
```
Now the files can be directly copied from the Routing Engine to any local host by using FTP, SCP, JWEB, or mounted USB.

* *Note:** FTP, SSH and HTTP are configured under the system services stanza.
