# MX960_MS-MPC_CGNAT SNMP OID monitor CPU, MEM of NPUs on MS-MPC

Please see the below SNMP OID’s are which are nearly matching your requirements: 

 

Name: jnxSpSvcSetIfMemoryUsage64

OID:  1.3.6.1.4.1.2636.3.32.1.3.1.9

Description: The amount of memory used by this Service PIC, expressed in bytes, represented by 64 bit integer

 

Name: jnxJsIdpSessionsUsage

OID: 1.3.6.1.4.1.2636.3.39.1.11.1.1.2.0

Description: Currently allocated sessions by IDP in percentage

 

Name: dot1xAuthSessionStatsTable

OID: 1.0.8802.1.1.1.1.2.4

Description: A table that contains the session statistics objects for the Authenticator PAE associated with each Port. An entry appears in this table for each port that may authenticate access to itself.

 

Name: jnxMbgPgwCPUUtilization

OID: 1.3.6.1.4.1.2636.3.66.1.1.1.2.4.0

Description: Current CPU Utilization.

 

Name: jnxJsSPUMonitoringCurrentCPSession

OID: 1.3.6.1.4.1.2636.3.39.1.12.1.1.1.8

Description: Current CP session number of SPU.

 

Name: jnxJsSPUMonitoringCurrentFlowSession

OID: 1.3.6.1.4.1.2636.3.39.1.12.1.1.1.6

Description: Current flow session number of SPU.

 

Name: jnxJsSPUMonitoringMaxFlowSession

OID: 1.3.6.1.4.1.2636.3.39.1.12.1.1.1.7

Description: Max flow session number of SPU.

 

Name: jnxJsSPUMonitoringMemoryUsage

OID: 1.3.6.1.4.1.2636.3.39.1.12.1.1.1.5

Description: Current memory usage of SPU(CPU) in percentage.

 

Name: jnxJsSPUMonitoringCPUUsage

OID: 1.3.6.1.4.1.2636.3.39.1.12.1.1.1.4

Description: Current SPU(CPU) Utilization in percentage.

If you would like to do more searches or find more relevant OID’s according to your requirement, please use the below links: 

[https://apps.juniper.net/mib-explorer/search.jsp#object=jnxMbgPgwCPUUtilization&product=Junos%20OS&release=17.4R3](https://apps.juniper.net/mib-explorer/search.jsp#object=jnxMbgPgwCPUUtilization&product=Junos%20OS&release=17.4R3)

[https://www.juniper.net/documentation/us/en/software/junos/interfaces-next-gen-services/topics/concept/usf-snmp-mibs-traps.html#id-snmp-mibs-and-traps__d18842e663](https://www.juniper.net/documentation/us/en/software/junos/interfaces-next-gen-services/topics/concept/usf-snmp-mibs-traps.html#id-snmp-mibs-and-traps__d18842e663)
