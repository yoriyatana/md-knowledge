# How to collect /var/log files from Next Generation Routing Engine (NG-RE)

In NGRE, there are two levels of /var/log to be collected for JTAC analysis:

1. Junos OS VM
2. Linux based host (VMHost)

### Steps to collect /var/log:

1. Junos OS VM

   Use the following command to zip all files under /var/log and dump it as /var/tmp/re-0-var-log.tgz
2. Linux based host (VMHost)

a. Log in to shell.

labroot> start shell% su

Password:

b. Log in to host.

root@:/var/home/lab # vhclient -s

Last login: Wed Mar  1 19:34:22 CST 2017 from local-node on pts/1

c. Zip the content.

root@local-node:~# tar -cf ~/host\_varlog\_RE0.tar -C /var/log/\*

tar: Removing leading `/' from member names

root@local-node:~# ls -l | grep varlog

- rw-r--r--. 1 root root 75509760 Jun 22 02:55 host\_varlog\_RE0.tar

d. Copy the file to VM Routing Engine /var/tmp.

- - PTX10K systems --

root@ptx10008-re0-node:~# scp host\_varlog\_RE0.tar root@192.168.1.2:/var/tmp/

Password:

host\_varlog\_RE0.tar                            100%   54MB  26.8MB/s   00:02

- - MX systems & PTX5K systems --

root@mx2008-re0-node:~# scp host\_varlog\_RE0.tar root@192.168.1.1:/var/tmp/

Password:

host\_varlog\_RE0.tar                            100%   73MB  36.5MB/s   00:02

e. You can also directly copy the host logs, collected in step (c) above, from the CLI by using the following commands:

```text
> request vmhost file-copy from-jnode host-logs.tar to-vjunos /var/tmp/host\_varlog\_RE0.tar log
```

* *Note:** In order perform the file copy operation from VMHOST to Junos (Step 2d) possible, users should be allowed to log in to the router via SSH as "root":

[edit]

+ system {

+ services {

```text
ssh {
```

+ root-login allow;

+ }

+ }

+ }

Now the files can be directly copied from Routing Engine to any local host using FTP, SCP, J-Web, or mounted USB.

* *Note:** FTP, SSH and HTTP are configured under the system services stanza.
