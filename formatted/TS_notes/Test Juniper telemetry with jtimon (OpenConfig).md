# Test Juniper telemetry with jtimon (OpenConfig)

<https://iosonounrouter.wordpress.com/2021/12/20/test-juniper-telemetry-in-two-seconds/>

Install jtimon

$ yum install golang -y

$ git clone https://github.com/Juniper/jtimon.git

$ cd jtimon

$ make linux

$ ./jtimon-linux-amd64 --help or jtimon-darwin-amd64 --help

Make a config file in json format:

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

"file": "test\_MX204.log"

}

}

Last, we enable telemetry on the device:

[edit system services]

+ extension-service {

```text
request-response {
```

+ grpc {

```text
clear-text {
```

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

We start jtimon:

./jtimon-linux-amd64  --config test\_MX204\_1.json --print

or

./jtimon-linux-amd64  --config test\_MX204\_1.json --print >> test\_MX204\_1.ouput.log

and data arrives:

Receiving telemetry data from 192.168.3.241:32767

system\_id: SGP001IGR04

```text
component\_id: 65535
```

```text
sub\_component\_id: 0
```

path: sensor\_1004:/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/:/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/:rpd

```text
sequence\_number: 0
```

```text
timestamp: 1695289069640
```

sync\_response: false

key: \_\_timestamp\_\_

```text
uint\_value: 1695289069641
```

key: \_\_junos\_re\_stream\_creation\_timestamp\_\_

```text
uint\_value: 1695289069611
```

key: \_\_junos\_re\_payload\_get\_timestamp\_\_

```text
uint\_value: 1695289069611
```

key: \_\_prefix\_\_

str\_value: /network-instances/network-instance[name='master']/protocols/protocol/bgp/neighbors/neighbor[neighbor-address='27.111.228.1']/

key: snmp-peer-index

```text
uint\_value: 172
```

```text
key: state/peer-as
```

```text
uint\_value: 42
```

```text
key: state/local-as
```

```text
uint\_value: 45903
```

```text
key: state/peer-type
```

str\_value: EXTERNAL

```text
key: state/auth-password
```

str\_value: (null)

```text
key: state/route-flap-damping
```

bool\_value: false

```text
key: state/description
```

str\_value: Peer-PCH-AS42

```text
key: state/session-state
```

str\_value: IDLE

```text
key: state/last-established
```

```text
uint\_value: 1694967381
```

```text
key: state/established-transitions
```

```text
uint\_value: 0
```

```text
key: state/messages/sent/UPDATE
```

```text
uint\_value: 0
```

```text
key: state/messages/sent/NOTIFICATION
```

```text
uint\_value: 0
```

```text
key: state/messages/sent/last-notification-time
```

```text
uint\_value: 0
```

```text
key: state/messages/sent/last-notification-error-subcode
```

str\_value: UNSPECIFIC

```text
key: state/messages/received/UPDATE
```

```text
uint\_value: 0
```

```text
key: state/messages/received/NOTIFICATION
```

```text
uint\_value: 0
```

```text
key: state/messages/received/last-notification-time
```

```text
uint\_value: 0
```

```text
key: state/messages/received/last-notification-error-code
```

str\_value: NONE

```text
key: state/messages/received/last-notification-error-subcode
```

str\_value: UNSPECIFIC

```text
key: state/queues/input
```

```text
uint\_value: 0
```

```text
key: state/queues/output
```

```text
uint\_value: 0
```

```text
key: state/dynamically-configured
```

bool\_value: false

```text
key: state/session-status
```

str\_value: HALTED

```text
key: state/session-admin-status
```

str\_value: STOP

```text
key: state/interface-error
```

bool\_value: true

```text
key: state/import-eval-pending
```

bool\_value: false

```text
key: state/import-eval
```

bool\_value: false

```text
key: state/peer-group
```

str\_value: Equinix

```text
key: state/neighbor-address
```

```text
str\_value: 27.111.228.1
```

```text
key: state/enabled
```

bool\_value: true

```text
key: timers/state/connect-retry
```

```text
str\_value: 0.00
```

```text
key: timers/state/hold-time
```

```text
str\_value: 90.00
```

```text
key: timers/state/keepalive-interval
```

```text
str\_value: 30.00
```

```text
key: timers/state/minimum-advertisement-interval
```

```text
str\_value: 0.00
```

```text
key: timers/state/negotiated-hold-time
```

```text
str\_value: 0.00
```

```text
key: transport/state/tcp-mss
```

```text
uint\_value: 0
```

```text
key: transport/state/mtu-discovery
```

bool\_value: false

```text
key: transport/state/passive-mode
```

bool\_value: false

```text
key: transport/state/local-address
```

```text
str\_value: 27.111.228.152
```

```text
key: transport/state/local-port
```

```text
uint\_value: 0
```

```text
key: transport/state/remote-address
```

```text
str\_value: 27.111.228.1
```

```text
key: transport/state/remote-port
```

```text
uint\_value: 0
```

```text
key: error-handling/state/treat-as-withdraw
```

bool\_value: true

```text
key: error-handling/state/erroneous-update-messages
```

```text
uint\_value: 0
```

```text
key: logging-options/state/log-neighbor-state-changes
```

bool\_value: false

```text
key: ebgp-multihop/state/enabled
```

bool\_value: false

```text
key: ebgp-multihop/state/multihop-ttl
```

```text
uint\_value: 0
```

```text
key: route-reflector/state/route-reflector-cluster-id
```

str\_value: zero-len

```text
key: route-reflector/state/route-reflector-client
```

bool\_value: false

```text
key: as-path-options/state/allow-own-as
```

```text
uint\_value: 0
```

```text
key: as-path-options/state/replace-peer-as
```

bool\_value: false

```text
key: as-path-options/state/disable-peer-as-filter
```

bool\_value: false

```text
key: use-multiple-paths/state/enabled
```

bool\_value: false

```text
key: use-multiple-paths/ebgp/state/allow-multiple-as
```

bool\_value: false

```text
key: graceful-restart/state/enabled
```

bool\_value: false

```text
key: graceful-restart/state/restart-time
```

```text
uint\_value: 120
```

```text
key: graceful-restart/state/stale-routes-time
```

```text
str\_value: 300.00
```

```text
key: graceful-restart/state/helper-only
```

bool\_value: true

```text
key: graceful-restart/state/peer-restarting
```

bool\_value: false

```text
key: graceful-restart/state/local-restarting
```

bool\_value: false

```text
key: graceful-restart/state/mode
```

str\_value: HELPER\_ONLY

```text
key: apply-policy/state/import-policy
```

leaf\_list\_value: element:

```text
key: apply-policy/state/export-policy
```

leaf\_list\_value: element:

![](image/96eee75dd90796be25cf4f07821d284a.log)![](image/ec13c0e06c1ded86e5451328bfc87709.pcap)
