# Hỗ trợ giám sát bw cho term fb trên BRAS

Dear anh Minh,

 

Để giám sát được lưu lượng up/download của các term FACEBOOK mình sẽ thực hiện đẩy traffic của FB ở các term vào queue QoS riêng và sử dụng SNMP OID để giám sát BW các queue:

- **Cấu hình QoS:**

```
/* Cấu hình QoS đẩy traffic term Facebook vào FC riêng */
set   class-of-service forwarding-classes class CS6 queue-num 3
set   class-of-service forwarding-classes class FB_D queue-num 2
set   class-of-service forwarding-classes class FB_U queue-num 1
set   class-of-service forwarding-classes class BE queue-num 0
 
set   class-of-service scheduler-maps SCH_MAP forwarding-class CS6 scheduler S_CS6
set   class-of-service scheduler-maps SCH_MAP forwarding-class FB_D scheduler   S_FB_D
set   class-of-service scheduler-maps SCH_MAP forwarding-class FB_U scheduler   S_FB_U
set   class-of-service scheduler-maps SCH_MAP forwarding-class BE scheduler S_BE
		 
set   class-of-service schedulers S_CS6 transmit-rate percent 5
set   class-of-service schedulers S_CS6 buffer-size percent 5
set   class-of-service schedulers S_CS6 priority strict-high
set   class-of-service schedulers S_FB_D transmit-rate percent 10
set   class-of-service schedulers S_FB_D buffer-size percent 10
set   class-of-service schedulers S_FB_D priority low
set   class-of-service schedulers S_FB_U transmit-rate percent 10
set   class-of-service schedulers S_FB_U buffer-size percent 10
set   class-of-service schedulers S_FB_U priority low
set   class-of-service schedulers S_BE transmit-rate percent 75
set   class-of-service schedulers S_BE buffer-size percent 75
set   class-of-service schedulers S_BE priority low
		 
set   class-of-service host-outbound-traffic forwarding-class CS6
		 
set   class-of-service interfaces <interface up/down> scheduler-map SCH_MAP
		 
set   firewall family inet filter d-200m-fb term FACEBOOK then forwarding-class   FB_D
set firewall family inet filter u-200m-fb   term FACEBOOK then forwarding-class FB_U
```

 

- Tùy cấu hình thực tế trên từng BRAS để edit cấu hình trên:
    - Nếu BRAS chưa có cấu hình thì cấu hình full như trên
    - Nếu BRAS đang có cấu hình thì tùy cấu hình thực tế để edit cho phù hợp
- Như vậy FB upload sẽ thuộc queue 1, forwarding class FB_U
- FB download sẽ thuộc queue 2, forwarding class FB_D
- % BW cho FB anh cân đối thêm thực tế mình đẩy vào nhiều khách hàng không để điều chỉnh thêm cho phù hợp nhé.

 

- **IOD giám sát:**

**OID này sẽ giám sát được BW từng queue trên từng interface.**

 

|**snmp-object-name**              |**OID**  |                            |
|----------------------------------|---------|----------------------------|
|**Transmitted packet/byte  stats**|         |                            |
|jnxCosQstatTxedPkts               |Packets  |1.3.6.1.4.1.2636.3.15.4.1.7 |
|jnxCosQstatTxedPktRate            |Packets/s|1.3.6.1.4.1.2636.3.15.4.1.8 |
|                                  |         |                            |
|jnxCosQstatTxedBytes              |Bytes    |1.3.6.1.4.1.2636.3.15.4.1.9 |
|jnxCosQstatTxedByteRate           |Bytes/s  |1.3.6.1.4.1.2636.3.15.4.1.10|
|                                  |         |                            |
|**Tail-dropped**                  |         |                            |
|jnxCosQstatTailDropPkts           |Packets  |1.3.6.1.4.1.2636.3.15.4.1.11|
|jnxCosQstatTailDropPktRate        |Packets/s|1.3.6.1.4.1.2636.3.15.4.1.12|
|                                  |         |                            |
|**RED-dropped**                   |         |                            |
|jnxCosQstatTotalRedDropPkts       |Packets  |1.3.6.1.4.1.2636.3.15.4.1.13|
|jnxCosQstatTotalRedDropPktRate    |Packets/s|1.3.6.1.4.1.2636.3.15.4.1.14|
|                                  |         |                            |
|jnxCosQstatTotalRedDropBytes      |Bytes    |1.3.6.1.4.1.2636.3.15.4.1.23|
|jnxCosQstatTotalRedDropByteRate   |Bytes/s  |1.3.6.1.4.1.2636.3.15.4.1.24|
|**Rate Limit dropped**            |         |                            |
|jnxCosQstatRateLimitDropPkts      |Packets  |1.3.6.1.4.1.2636.3.15.4.1.49|
|jnxCosQstatRateLimitDropPktRate   |Packets/s|1.3.6.1.4.1.2636.3.15.4.1.50|
|                                  |         |                            |
|jnxCosQstatRateLimitDropBytes     |Bytes    |1.3.6.1.4.1.2636.3.15.4.1.51|
|jnxCosQstatRateLimitDropByteRate  |Bytes/s  |1.3.6.1.4.1.2636.3.15.4.1.52|
