# Hỗ trợ giám sát bw cho term fb trên BRAS

Dear anh Minh,

Để giám sát được lưu lượng up/download của các term FACEBOOK mình sẽ thực hiện đẩy traffic của FB ở các term vào queue QoS riêng và sử dụng SNMP OID để giám sát BW các queue:

- **Cấu hình QoS:**

/\* Cấu hình QoS đẩy traffic term Facebook vào FC riêng \*/

```text
set  class-of-service forwarding-classes class CS6 queue-num 3
```

```text
set  class-of-service forwarding-classes class FB\_D queue-num 2
```

```text
set  class-of-service forwarding-classes class FB\_U queue-num 1
```

```text
set  class-of-service forwarding-classes class BE queue-num 0
```

```text
set  class-of-service scheduler-maps SCH\_MAP forwarding-class CS6 scheduler S\_CS6
```

```text
set  class-of-service scheduler-maps SCH\_MAP forwarding-class FB\_D scheduler  S\_FB\_D
```

```text
set  class-of-service scheduler-maps SCH\_MAP forwarding-class FB\_U scheduler  S\_FB\_U
```

```text
set  class-of-service scheduler-maps SCH\_MAP forwarding-class BE scheduler S\_BE
```

```text
set  class-of-service schedulers S\_CS6 transmit-rate percent 5
```

```text
set  class-of-service schedulers S\_CS6 buffer-size percent 5
```

```text
set  class-of-service schedulers S\_CS6 priority strict-high
```

```text
set  class-of-service schedulers S\_FB\_D transmit-rate percent 10
```

```text
set  class-of-service schedulers S\_FB\_D buffer-size percent 10
```

```text
set  class-of-service schedulers S\_FB\_D priority low
```

```text
set  class-of-service schedulers S\_FB\_U transmit-rate percent 10
```

```text
set  class-of-service schedulers S\_FB\_U buffer-size percent 10
```

```text
set  class-of-service schedulers S\_FB\_U priority low
```

```text
set  class-of-service schedulers S\_BE transmit-rate percent 75
```

```text
set  class-of-service schedulers S\_BE buffer-size percent 75
```

```text
set  class-of-service schedulers S\_BE priority low
```

```text
set  class-of-service host-outbound-traffic forwarding-class CS6
```

```text
set  class-of-service interfaces  scheduler-map SCH\_MAP
```

```text
set  firewall family inet filter d-200m-fb term FACEBOOK then forwarding-class  FB\_D
```

```text
set firewall family inet filter u-200m-fb  term FACEBOOK then forwarding-class FB\_U
```

- Tùy cấu hình thực tế trên từng BRAS để edit cấu hình trên:

- Nếu BRAS chưa có cấu hình thì cấu hình full như trên
- Nếu BRAS đang có cấu hình thì tùy cấu hình thực tế để edit cho phù hợp

```text
Như vậy FB upload sẽ thuộc queue 1, forwarding class FB\_U
FB download sẽ thuộc queue 2, forwarding class FB\_D
% BW cho FB anh cân đối thêm thực tế mình đẩy vào nhiều khách hàng không để điều chỉnh thêm cho phù hợp nhé.
```

- **IOD giám sát:**

* *OID này sẽ giám sát được BW từng queue trên từng interface.**

|  |  |  |
| --- | --- | --- |
| **snmp-object-name** | | **OID** |
| **Transmitted packet/byte  stats** | |  |
| jnxCosQstatTxedPkts | Packets | 1.3.6.1.4.1.2636.3.15.4.1.7 |
| jnxCosQstatTxedPktRate | Packets/s | 1.3.6.1.4.1.2636.3.15.4.1.8 |
|  |  |  |
| jnxCosQstatTxedBytes | Bytes | 1.3.6.1.4.1.2636.3.15.4.1.9 |
| jnxCosQstatTxedByteRate | Bytes/s | 1.3.6.1.4.1.2636.3.15.4.1.10 |
|  |  |  |
| **Tail-dropped** | |  |
| jnxCosQstatTailDropPkts | Packets | 1.3.6.1.4.1.2636.3.15.4.1.11 |
| jnxCosQstatTailDropPktRate | Packets/s | 1.3.6.1.4.1.2636.3.15.4.1.12 |
|  |  |  |
| **RED-dropped** | |  |
| jnxCosQstatTotalRedDropPkts | Packets | 1.3.6.1.4.1.2636.3.15.4.1.13 |
| jnxCosQstatTotalRedDropPktRate | Packets/s | 1.3.6.1.4.1.2636.3.15.4.1.14 |
|  |  |  |
| jnxCosQstatTotalRedDropBytes | Bytes | 1.3.6.1.4.1.2636.3.15.4.1.23 |
| jnxCosQstatTotalRedDropByteRate | Bytes/s | 1.3.6.1.4.1.2636.3.15.4.1.24 |
| **Rate Limit dropped** | |  |
| jnxCosQstatRateLimitDropPkts | Packets | 1.3.6.1.4.1.2636.3.15.4.1.49 |
| jnxCosQstatRateLimitDropPktRate | Packets/s | 1.3.6.1.4.1.2636.3.15.4.1.50 |
|  |  |  |
| jnxCosQstatRateLimitDropBytes | Bytes | 1.3.6.1.4.1.2636.3.15.4.1.51 |
| jnxCosQstatRateLimitDropByteRate | Bytes/s | 1.3.6.1.4.1.2636.3.15.4.1.52 |
