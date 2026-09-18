# cách upgrade/downgrade JunOS cho physical device on Jlab/vlab

login vào máy VMhelper

# yum install -y  ftp

# ftp ftp.cloudlabs.juniper.net

```text
12:28:27.740 220 Welcome to JCL service ftp!
```

```text
12:28:45.175 Name (ftp.cloudlabs.juniper.net:root): anonymous
```

```text
12:28:45.187 331 Please specify the password.
```

```text
12:28:46.905 Password:                                              <<<~~~  No pass
```

```text
12:28:46.923 230 Login successful.
```

```text
12:28:46.923 Remote system type is UNIX.
```

```text
12:28:46.923 Using binary mode to transfer files.
```

```text
12:29:00.571 ftp> cd /pub/junos
```

```text
12:29:00.591 250 Directory successfully changed.
```

```text
12:29:04.506 ftp> ls
```

```text
12:29:04.506 ftp> ls junos-evo-install-acx-f-x86-64
```

Lấy đường dẫn đến file junos

vào thiết bị Juniper để thực hiện lệnh file copy kéo file về máy

```text
12:35:01.709 jcluser@ACX7100-A1> file copy ftp://ftp.cloudlabs.juniper.net/pub/junos/junos-evo-install-acx-f-x86-64/junos-evo-install-acx-f-x86-64-22.4R2.11-EVO.iso /var/tmp/
```

thực hiện nâng cấp

```text
jcluser@ACX7100-A1> request system software add /var/tmp/junos-evo-install-acx-f-x86-64-22.4R2.11-EVO.iso no-validate reboot
```

upgrade/downgrade JunOS-EVO on ACX7100

re0: Run 'show system software list' to get all installed software versions

re0: To enable this image, do 'request system software rollback reboot'.

re0: To uninstall this image, do 'request system software delete junos-evo-install-acx-f-x86-64-22.4R2.11-EVO force'.
