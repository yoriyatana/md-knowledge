# RPD mode 64-bit

Basically, the health status of the router is stable; however, regarding the core-dump file, I have checked internally and I could find the below information.

From core file it looks like router was running @ 77%+ memory during the issue time.

```text
Core happened when RPD (BGP) requested for additional memory and kernel returned ENOMEM (Error - 12)
```

# define ENOMEM      12  /\* Out of memory \*/

Could you please provide the below output to proceed further?

```text
>show system processes | no more
```

Also, could you please confirm if the logical systems are configured and utilized in your router as I could notice that the configuration is inactive.

- --

```text
As per my previous email, Core file was generated when RPD (BGP) requested for additional memory and kernel returned ENOMEM (Error - 12) due to memory exhaustion during the issue time.
```

# define ENOMEM      12  /\* Out of memory \*/

- --

Have checked internally and I could notice that based on the below output, the number routes learnt in Logical system HCM-RR02 is near to 1 million routes now and during the issue time there should have been more routes seen in the logical system which has led to RPD crash in the logical system HCM-RR02 due memory exhaustion.

Logical system: HCM-RR02

Routing table: default.inet

Internet:

Enabled protocols: Bridging, Dual VLAN,

```text
user:         852573 routes
```

```text
perm:          5 routes
```

```text
intf:          5 routes
```

```text
dest:          8 routes
```

root@HCM001PRT02\_RE0> show system core-dumps no-forwarding

/var/crash/\*core\*: No such file or directory

- rw-rw----  1 root  wheel  738680996 Jun 4  05:37 /var/tmp/rpd\_HCM-RR02.core-tarball.0.tgz

Checked the below output that you have shared and we could notice that only main instance is using 64 bit rpd; however, logical system is using 32-bit.

cuong.hv1@HCM001PRT02\_RE0> show system processes | no-more

14051  -  S       391:40.41 /usr/libexec64/rpd -N

35980  -  S       952:24.63 /usr/sbin/rpd -N -JLHCM-RR02

/usr/libexec64/rpd -N      -->        Master Logical System, 64-bit mode

/usr/sbin/rpd -N -JLxxx    -->        Logical System 'xxx', 32-bit mode

As per the core dump decode, RPD was crashed due to high memory utilization.

In 32 bit mode, RPD will be allowed only to use 3.2 GB of memory.

Next action:

Could you please change the RPD in logical system to 64bit mode? Changing these settings will implicitly cause a 'restart routing' operation, hence, I would request you to perform this activity during the MW.

logical-systems {

{

system {

processes {

routing {

force-64-bit

}

}

}

}

}

Please check and let me know if you have any concern.

- --

1/ Applying the 64-bit mode, RPD will be restart, Besides that, is there anything else we need to pay attention to? Since we are forcing rpd from 32-bit to 64-bit or 64-bit-to 32-bit, it will restart the rpd process, which can impact the routing protocols only.

2/ What bugs related to convert from 32bit mode -> 64bit-mode? If have, please give me refer to the solutions to prevent also the PR related to them. -  Based on this issue dealt with other customers I am providing this solution to avoid rpd memory exhaustion issue.

3/ Why the Junos don't use RPD default into Logical-system in 64bit-mode? I saw that the Logical-system is 32bit, if I want to set default 64bit, how can I do it? Basically, for logical system we cannot set “auto-64-bit” rpd mode as per the below document; however, we can enable “force-64-bit” in the logical systems to always use 64-bit mode.

Please refer - <https://www.juniper.net/documentation/us/en/software/junos/junos-overview/topics/ref/statement/routing-edit-system-processes.html>
