# SNMP interface rate MIB OID

show snmp mib walk ifDescr | match <int name>

For example:

ifIn1SecRate - .1.3.6.1.4.1.2636.3.3.1.1.1

Input rate on interface ge-0/0/0 of Step 1:  .1.3.6.1.4.1.2636.3.3.1.1.1.508

ifOut1SecRate - .1.3.6.1.4.1.2636.3.3.1.1.4

Output rate of interface ge-0/0/0 of Step 1: .1.3.6.1.4.1.2636.3.3.1.1.4.508

ifHCOut1SecRate -  1.3.6.1.4.1.2636.3.3.1.1.8

ifHCIn1SecRate -  1.3.6.1.4.1.2636.3.3.1.1.7
