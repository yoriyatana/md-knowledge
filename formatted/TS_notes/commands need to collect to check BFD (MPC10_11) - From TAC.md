# commands need to collect to check BFD (MPC10/11) - From TAC

JTAC : Please share the below outputs.

```text
show ddos-protection protocols arp parameters
```

```text
show configuration system ddos-protection protocols | display set
```

```text
show ddos-protection protocols arp statistics terse
```

```text
show route forwarding-table destination 10.113.255.3  | match "Destination|ucst"
```

```text
show route forwarding-table destination 10.113.255.4  | match "Destination|ucst"
```

```text
show pfe statistics traffic | match drop
```

```text
show policer | match arp
```

```text
show class-of-service fabric statistics |  no-more
```

```text
show class-of-service fabric statistics summary | no-more
```

```text
show system connection |no-more
```

```text
show system connection extensive |no-more
```

start shell pfe network fpc < FPC no> --collect for fpc 0 and 5

```text
show interfaces
```

```text
show class-of-service interface queue-stats index  interface index based on the above output.
```

```text
show ddos policer violations arp
```

```text
show ddos policer arp configuration
```

```text
show system info
```

```text
show jnh exceptions level inst 0
```

```text
show jnh exceptions level inst 1
```

```text
show jnh exception-qdrops inst 0
```

```text
show jnh exception-qdrops inst 1
```

```text
show class-of-service interface scheduler brief
```

```text
show ppm adjacencies
```

```text
show ppm adjacencies protocol bfd detail
```

```text
show ppm statistics protocol bfd
```

```text
show ppm interfaces detail | no-more
```

```text
show ppm transmissions detail | no-more
```

```text
show ppm transmissions protocol bfd detail
```

```text
show pfe statistics traffic | no-more
```

```text
show ppm statistics protocol bfd
```

```text
show ppm distribution-statistics
```

```text
show ppm dfw-statistics
```

```text
show ppm packet-snapshot
```

```text
show ppm request-queue
```

```text
show ppm rpc-statistics
```

```text
show ppm info
```

```text
show ppm objects
```

```text
show ppm statistics detail
```

```text
show ttp statistics
```

```text
show system queue
```

```text
show threads
```

```text
show sched
```

```text
show host-path ports
```

```text
show host-path ports fp0
```

```text
show host-path ports fp1
```

```text
show host-path ports cp0
```

```text
show host-path ports punts
```

```text
show host-path ports io reassembly fp0
```

```text
show host-path ports io reassembly fp1
```

```text
show host-path ports punts fp0
```

```text
show host-path ports punts fp1
```

```text
show host-path packet-type
```

```text
show host-path network
```

```text
show host-path packets
```

```text
show host-path ports ppm0
```

```text
show filter pkt-log
```

```text
show firewall stats
```

```text
show host-path ddos all-policers nzero
```

```text
show ddos all-policers nzero
```

```text
show jnh ddos scfd global
```

```text
show jnh ddos policer statistics
```

```text
show jnh ddos policer statistics
```

```text
show jnh ddos policer configuration
```

```text
show pfe statistics reroute
```

```text
show pfe statistics traffic
```

```text
show pfe statistics error
```

```text
show pfe statistics notification
```

```text
show cda xqss statistics server api
```

```text
show host-path network layer2 ethernet
```

```text
show host-path app wedge-detect pfe-status
```

```text
show host-path app wedge-detect state
```

```text
show host-path app wedge-detect sm-stats
```

```text
show host-path app hw-notif statistics
```

```text
show host-path app icmp statistics
```

```text
show host-path app mlp statistics
```

```text
show host-path app ppm
```

```text
show host-path app resolve state
```

```text
show host-path app resolve statistics
```

```text
show host-path app rpc-statistics
```

```text
show host-path app twamp statistics
```

```text
show host-path app vxlanpkt statistics
```

```text
show host-path packets
```

```text
show jnh ucode-vars All inst 0
```

```text
show jnh ucode-vars All inst 1
```

```text
show jnh ucode-vars GeHost inst 0
```

```text
show jnh ucode-vars GeHost inst 1
```

```text
show interfaces statistics .punt
```
