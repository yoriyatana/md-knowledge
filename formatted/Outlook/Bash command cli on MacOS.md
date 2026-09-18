# Bash command cli on MacOS

* *Display disk usage on macOS with du command**

```text
% du -d 1 -h /Users/tungnt/Library/\* | grep -e "\dG\s"
```

- --

* *Set a Static IP Address in macOS Using Command Line**

```text
% networksetup -listallnetworkservices
```

An asterisk (\*) denotes that a network service is disabled.

Apple USB Ethernet Adapter

USB 10/100/1000 LAN

Wi-Fi

Bluetooth PAN

Thunderbolt Bridge

```text
% networksetup -setmanual Wi-Fi 192.168.1.2 255.255.255.0 192.168.1.1
```

Setting it back to DHCP

```text
% networksetup -setdhcp SERVICE
```

Keep DHCP with a manual IP

```text
% networksetup -setmanualwithdhcprouter SERVICE IP
```

- --

* *Upload file to remote host via scp**

```text
% scp host\_varlog\_RE0.tar root@192.168.1.2:/var/tmp/
```

- --

* *Download file from remote host via scp**

```text
% scp lab@192.168.3.181:/var/tmp/config\_test\_RPM\_80\_probes.config "/Users/tungnt/Downloads"
```
