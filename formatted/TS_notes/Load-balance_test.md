# Load-balance test

![Attachment.png](image/Attachment.png)

```
show forwarding-options load-balance family inet6 ingress-interface xe-5/0/3 transport-protocol tcp source-address 2201::2 destination-address 2202::2 source-port 1617 destination-port 1640 tos 224
```

jsim tài liệu packetWalkthrough
