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

We start jtimon:

./jtimon-linux-amd64  --config test\_MX204\_1.json --print

or

./jtimon-linux-amd64  --config test\_MX204\_1.json --print >> test\_MX204\_1.ouput.log

and data arrives:

Receiving telemetry data from 192.168.3.241:32767

system\_id: SGP001IGR04

component\_id: 65535

sub\_component\_id: 0

path: sensor\_1004:/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/:/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/:rpd

sequence\_number: 0

timestamp: 1695289069640

sync\_response: false

key: \_\_timestamp\_\_

uint\_value: 1695289069641

key: \_\_junos\_re\_stream\_creation\_timestamp\_\_

uint\_value: 1695289069611

key: \_\_junos\_re\_payload\_get\_timestamp\_\_

uint\_value: 1695289069611

key: \_\_prefix\_\_

str\_value: /network-instances/network-instance[name='master']/protocols/protocol/bgp/neighbors/neighbor[neighbor-address='27.111.228.1']/

key: snmp-peer-index

uint\_value: 172

key: state/peer-as

uint\_value: 42

key: state/local-as

uint\_value: 45903

key: state/peer-type

str\_value: EXTERNAL

key: state/auth-password

str\_value: (null)

key: state/route-flap-damping

bool\_value: false

key: state/description

str\_value: Peer-PCH-AS42

key: state/session-state

str\_value: IDLE

key: state/last-established

uint\_value: 1694967381

key: state/established-transitions

uint\_value: 0

key: state/messages/sent/UPDATE

uint\_value: 0

key: state/messages/sent/NOTIFICATION

uint\_value: 0

key: state/messages/sent/last-notification-time

uint\_value: 0

key: state/messages/sent/last-notification-error-subcode

str\_value: UNSPECIFIC

key: state/messages/received/UPDATE

uint\_value: 0

key: state/messages/received/NOTIFICATION

uint\_value: 0

key: state/messages/received/last-notification-time

uint\_value: 0

key: state/messages/received/last-notification-error-code

str\_value: NONE

key: state/messages/received/last-notification-error-subcode

str\_value: UNSPECIFIC

key: state/queues/input

uint\_value: 0

key: state/queues/output

uint\_value: 0

key: state/dynamically-configured

bool\_value: false

key: state/session-status

str\_value: HALTED

key: state/session-admin-status

str\_value: STOP

key: state/interface-error

bool\_value: true

key: state/import-eval-pending

bool\_value: false

key: state/import-eval

bool\_value: false

key: state/peer-group

str\_value: Equinix

key: state/neighbor-address

str\_value: 27.111.228.1

key: state/enabled

bool\_value: true

key: timers/state/connect-retry

str\_value: 0.00

key: timers/state/hold-time

str\_value: 90.00

key: timers/state/keepalive-interval

str\_value: 30.00

key: timers/state/minimum-advertisement-interval

str\_value: 0.00

key: timers/state/negotiated-hold-time

str\_value: 0.00

key: transport/state/tcp-mss

uint\_value: 0

key: transport/state/mtu-discovery

bool\_value: false

key: transport/state/passive-mode

bool\_value: false

key: transport/state/local-address

str\_value: 27.111.228.152

key: transport/state/local-port

uint\_value: 0

key: transport/state/remote-address

str\_value: 27.111.228.1

key: transport/state/remote-port

uint\_value: 0

key: error-handling/state/treat-as-withdraw

bool\_value: true

key: error-handling/state/erroneous-update-messages

uint\_value: 0

key: logging-options/state/log-neighbor-state-changes

bool\_value: false

key: ebgp-multihop/state/enabled

bool\_value: false

key: ebgp-multihop/state/multihop-ttl

uint\_value: 0

key: route-reflector/state/route-reflector-cluster-id

str\_value: zero-len

key: route-reflector/state/route-reflector-client

bool\_value: false

key: as-path-options/state/allow-own-as

uint\_value: 0

key: as-path-options/state/replace-peer-as

bool\_value: false

key: as-path-options/state/disable-peer-as-filter

bool\_value: false

key: use-multiple-paths/state/enabled

bool\_value: false

key: use-multiple-paths/ebgp/state/allow-multiple-as

bool\_value: false

key: graceful-restart/state/enabled

bool\_value: false

key: graceful-restart/state/restart-time

uint\_value: 120

key: graceful-restart/state/stale-routes-time

str\_value: 300.00

key: graceful-restart/state/helper-only

bool\_value: true

key: graceful-restart/state/peer-restarting

bool\_value: false

key: graceful-restart/state/local-restarting

bool\_value: false

key: graceful-restart/state/mode

str\_value: HELPER\_ONLY

key: apply-policy/state/import-policy

leaf\_list\_value: element:

key: apply-policy/state/export-policy

leaf\_list\_value: element:

![](image/96eee75dd90796be25cf4f07821d284a.log)![](image/ec13c0e06c1ded86e5451328bfc87709.pcap)
