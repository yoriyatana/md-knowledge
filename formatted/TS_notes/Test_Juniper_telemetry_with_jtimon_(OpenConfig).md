# Test Juniper telemetry with jtimon (OpenConfig)

[https://iosonounrouter.wordpress.com/2021/12/20/test-juniper-telemetry-in-two-seconds/](https://iosonounrouter.wordpress.com/2021/12/20/test-juniper-telemetry-in-two-seconds/)

Install jtimon

```
$ yum install golang -y
$ git clone https://github.com/Juniper/jtimon.git
$ cd jtimon
$ make linux
$ ./jtimon-linux-amd64 --help or jtimon-darwin-amd64 --help
```

Make a config file in json format:

```
{
    "host": "192.168.3.241",
    "port": 32767,
    "user": "lab",
    "password": "lab123",
    "cid": "cid",
    "grpc" : {
        "ws" : 1048576
    },
    "paths": [{
        "path": "/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor",
        "freq": 5000
    }],
    "log": {
        "file": "test_MX204.log"
    }
}
```

Last, we enable telemetry on the device:

```
[edit system services]
+ extension-service {
+ request-response {
+ grpc {
+ clear-text {
+ port 32767;
+ }
+ skip-authentication;
+ }
+ }
+ notification {
+ allow-clients {
+ address 192.168.3.0/24;
+ }
+ }
+ }
```

We start jtimon:

```
./jtimon-linux-amd64  --config test_MX204_1.json --print

or

./jtimon-linux-amd64  --config test_MX204_1.json --print >> test_MX204_1.ouput.log
```

and data arrives:

```
Receiving telemetry data from 192.168.3.241:32767
system_id: SGP001IGR04
component_id: 65535
sub_component_id: 0
path: sensor_1004:/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/:/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/:rpd
sequence_number: 0
timestamp: 1695289069640
sync_response: false
  key: __timestamp__
  uint_value: 1695289069641
  key: __junos_re_stream_creation_timestamp__
  uint_value: 1695289069611
  key: __junos_re_payload_get_timestamp__
  uint_value: 1695289069611
  key: __prefix__
  str_value: /network-instances/network-instance[name='master']/protocols/protocol/bgp/neighbors/neighbor[neighbor-address='27.111.228.1']/
  key: snmp-peer-index
  uint_value: 172
  key: state/peer-as
  uint_value: 42
  key: state/local-as
  uint_value: 45903
  key: state/peer-type
  str_value: EXTERNAL
  key: state/auth-password
  str_value: (null)
  key: state/route-flap-damping
  bool_value: false
  key: state/description
  str_value: Peer-PCH-AS42
  key: state/session-state
  str_value: IDLE
  key: state/last-established
  uint_value: 1694967381
  key: state/established-transitions
  uint_value: 0
  key: state/messages/sent/UPDATE
  uint_value: 0
  key: state/messages/sent/NOTIFICATION
  uint_value: 0
  key: state/messages/sent/last-notification-time
  uint_value: 0
  key: state/messages/sent/last-notification-error-subcode
  str_value: UNSPECIFIC
  key: state/messages/received/UPDATE
  uint_value: 0
  key: state/messages/received/NOTIFICATION
  uint_value: 0
  key: state/messages/received/last-notification-time
  uint_value: 0
  key: state/messages/received/last-notification-error-code
  str_value: NONE
  key: state/messages/received/last-notification-error-subcode
  str_value: UNSPECIFIC
  key: state/queues/input
  uint_value: 0
  key: state/queues/output
  uint_value: 0
  key: state/dynamically-configured
  bool_value: false
  key: state/session-status
  str_value: HALTED
  key: state/session-admin-status
  str_value: STOP
  key: state/interface-error
  bool_value: true
  key: state/import-eval-pending
  bool_value: false
  key: state/import-eval
  bool_value: false
  key: state/peer-group
  str_value: Equinix
  key: state/neighbor-address
  str_value: 27.111.228.1
  key: state/enabled
  bool_value: true
  key: timers/state/connect-retry
  str_value: 0.00
  key: timers/state/hold-time
  str_value: 90.00
  key: timers/state/keepalive-interval
  str_value: 30.00
  key: timers/state/minimum-advertisement-interval
  str_value: 0.00
  key: timers/state/negotiated-hold-time
  str_value: 0.00
  key: transport/state/tcp-mss
  uint_value: 0
  key: transport/state/mtu-discovery
  bool_value: false
  key: transport/state/passive-mode
  bool_value: false
  key: transport/state/local-address
  str_value: 27.111.228.152
  key: transport/state/local-port
  uint_value: 0
  key: transport/state/remote-address
  str_value: 27.111.228.1
  key: transport/state/remote-port
  uint_value: 0
  key: error-handling/state/treat-as-withdraw
  bool_value: true
  key: error-handling/state/erroneous-update-messages
  uint_value: 0
  key: logging-options/state/log-neighbor-state-changes
  bool_value: false
  key: ebgp-multihop/state/enabled
  bool_value: false
  key: ebgp-multihop/state/multihop-ttl
  uint_value: 0
  key: route-reflector/state/route-reflector-cluster-id
  str_value: zero-len
  key: route-reflector/state/route-reflector-client
  bool_value: false
  key: as-path-options/state/allow-own-as
  uint_value: 0
  key: as-path-options/state/replace-peer-as
  bool_value: false
  key: as-path-options/state/disable-peer-as-filter
  bool_value: false
  key: use-multiple-paths/state/enabled
  bool_value: false
  key: use-multiple-paths/ebgp/state/allow-multiple-as
  bool_value: false
  key: graceful-restart/state/enabled
  bool_value: false
  key: graceful-restart/state/restart-time
  uint_value: 120
  key: graceful-restart/state/stale-routes-time
  str_value: 300.00
  key: graceful-restart/state/helper-only
  bool_value: true
  key: graceful-restart/state/peer-restarting
  bool_value: false
  key: graceful-restart/state/local-restarting
  bool_value: false
  key: graceful-restart/state/mode
  str_value: HELPER_ONLY
  key: apply-policy/state/import-policy
  leaf_list_value: element:<leaflist_str_value:"RX-FROM-EQUINIX" >
  key: apply-policy/state/export-policy
  leaf_list_value: element:<leaflist_str_value:"ADV-TO-EQUINIX" >
```

[test_MX204_1-ouput.log](./file/test_MX204_1-ouput.log)

[telemetry.pcap](./file/telemetry.pcap)
