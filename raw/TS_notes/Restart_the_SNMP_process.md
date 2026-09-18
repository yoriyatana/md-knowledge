# Restart the SNMP process

**Step 1:Take the PID for reference,**

show system processes extensive | match "mib|snmp"          

 1320 root        1  96    0 20464K  8312K select   0:35  0.00% mib2d

 1321 root        1  96    0 15248K  9900K select   0:14  0.00% snmpd

 

**Step 2: Restart the process**

 

restart snmp immediately

restart mib-process immediately

 

**Step 3: confirm the process are up with the new PID**

show system processes extensive | match "mib|snmp"  

71731 root        1  96    0 15228K  9684K select   0:00  0.00% snmpd

71705 root        1  96    0 20432K  8344K select   0:00  0.00% mib2d
