# commands need to collect to check BFD (MPC10/11) - From TAC

JTAC : Please share the below outputs.

show ddos-protection protocols arp parameters

show configuration system ddos-protection protocols | display set

show ddos-protection protocols arp statistics terse

show route forwarding-table destination 10.113.255.3  | match "Destination|ucst"

show route forwarding-table destination 10.113.255.4  | match "Destination|ucst"

show pfe statistics traffic | match drop

show policer | match arp

show class-of-service fabric statistics |  no-more

show class-of-service fabric statistics summary | no-more

show system connection |no-more

show system connection extensive |no-more

start shell pfe network fpc < FPC no> --collect for fpc 0 and 5

show interfaces

show class-of-service interface queue-stats index  interface index based on the above output.

show ddos policer violations arp

show ddos policer arp configuration

show system info

show jnh exceptions level inst 0

show jnh exceptions level inst 1

show jnh exception-qdrops inst 0

show jnh exception-qdrops inst 1

show class-of-service interface scheduler brief

show ppm adjacencies

show ppm adjacencies protocol bfd detail

show ppm statistics protocol bfd

show ppm interfaces detail | no-more

show ppm transmissions detail | no-more

show ppm transmissions protocol bfd detail

show pfe statistics traffic | no-more

show ppm statistics protocol bfd

show ppm distribution-statistics

show ppm dfw-statistics

show ppm packet-snapshot

show ppm request-queue

show ppm rpc-statistics

show ppm info

show ppm objects

show ppm statistics detail

show ttp statistics

show system queue

show threads

show sched

show host-path ports

show host-path ports fp0

show host-path ports fp1

show host-path ports cp0

show host-path ports punts

show host-path ports io reassembly fp0

show host-path ports io reassembly fp1

show host-path ports punts fp0

show host-path ports punts fp1

show host-path packet-type

show host-path network

show host-path packets

show host-path ports ppm0

show filter pkt-log

show firewall stats

show host-path ddos all-policers nzero

show ddos all-policers nzero

show jnh ddos scfd global

show jnh ddos policer statistics

show jnh ddos policer statistics

show jnh ddos policer configuration

show pfe statistics reroute

show pfe statistics traffic

show pfe statistics error

show pfe statistics notification

show cda xqss statistics server api

show host-path network layer2 ethernet

show host-path app wedge-detect pfe-status

show host-path app wedge-detect state

show host-path app wedge-detect sm-stats

show host-path app hw-notif statistics

show host-path app icmp statistics

show host-path app mlp statistics

show host-path app ppm

show host-path app resolve state

show host-path app resolve statistics

show host-path app rpc-statistics

show host-path app twamp statistics

show host-path app vxlanpkt statistics

show host-path packets

show jnh ucode-vars All inst 0

show jnh ucode-vars All inst 1

show jnh ucode-vars GeHost inst 0

show jnh ucode-vars GeHost inst 1

show interfaces statistics .punt
