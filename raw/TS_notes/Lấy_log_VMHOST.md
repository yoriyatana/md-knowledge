# Lấy log VMHOST

1. **Các thông tin log sau:**

| // Remote login to a FPC2 //

 root@QFX10008-re0:RE:0% rlogin -Ji fpc2

 // Compress /var/log using the command "tar" //

 root@fpc2:~# tar -zcvf /var/tmp/varlog-fpc2.tar.gz /var/log/* 

 // Verify the compressed file is created //

 root@fpc2:~# ls -l /var/tmp/varlog-fpc2.tar.gz 

 -rw-r--r-- 1 root root 205933 Sep 16 01:10 /var/tmp/varlog-fpc2.tar.gz

 // Copy the file from FPC to JUNOS //

 root@fpc0:~# rcp /var/tmp/varlog-fpc2.tar.gz 128.0.0.1:/var/tmp

 // Use the command "exit" to exit from FPC2 //

 root@fpc0:~# exit

**  //download file “****varlog-fpc2.tar.gz”** **trong thư mục var/tmp về //**

 
user@QFX10008-re0> start shell user root|
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
