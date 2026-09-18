# SR#01219162/Viettel/SLA/NFE/Viettel || MPC5E-2CGE-4XGE cao tải CPU

Dear Tú, Trường, cùng các anh chị Viettel!

Qua log thu thập trên thiết bị trong mạng Viettel cùng việc thực hiện replicate lỗi lại trên hệ thông la, bên anh và đã phối hợp với Advance TAC và engineer của Juniper để phân tích tìm nguyên nhân gây CPU cao tải trên linecard MPC5E. Anh xin gửi lại tổng hợp thông tin phân tích của ATAC như sau:

1. **Hiệ****n tư****ợng CPU cao tải trên MPC5E trên mạng Viettel chỉ là expected behavior �**�không ảnh hưởng đến dịch vụ đang chạy trên thiết bị. Hiện tại mình đang dùng OID/MIB lấy giá trị realtime CPU của linecard để giám sát CPU của linecard qua gragh giám sát CPU của linecard. Tuy nhiên từ version 15.1 trở đi có thay đổi về kiến trúc SNMP lấy CPU của linecard nên OID/MIB giám sát realtime không còn đúng nữa:

As per the discussion with engineering, what we are observing is sub second CPU spikes which is expected with any production box-line cards which is harmless. It doesn’t indicate any problem, rather it is trying to complete  some bulk tasks with in short period of time as it could find free CPU cycles. Which is expected behavior.

There are significant changes in MIB/OID structures between 13.1 and 15.1 and above ( Like average CPU utilization for 1,10- and 15-minutes figures introduced ) and to make sure whether you are using the correct  NMS polling technique / MIB OID to poll average CPU usage data.

1. **Nguyên nhân CPU cao thấ****t thư****ờng trên MPC5E**: do từ version 15.1R5 trở đi PPE rebalance service trên linecard được enab và khi nó xử lý sẽ làm CPU của linecard tăng cao, tuy nhiên đây chỉ là harmless và **expected behavior �**�

After 15.1R5, 16.1R3 or later, **Packet Process Engine UCODE Re-balancing (LKUP ASIC UCODE Rebalance Service ) feature is getting enabled by default to improve forwarding performance**. Prior to these versions, it was disabled by default. A noticeable behavior due to this microcode re-balance mechanism is that, MPC CPU spikes may be observed on regular intervals on MX series routers with MPCs installed which is **harmless in nature**.

This mechanism increases overall packet forwarding performance or better throughput.

1. **Advance TAC khuyến nghị giám sát CPU của linecard thông qua OID/MIB lấy giá trị trung bình**. **Thông tin OID/MIB giám sát giá trị trung bình:**

In another words, If the customer is polling for real time CPU usage of FPC, not the average CPU Usage value , then the graph won’t look correct. Because, the NMS graph will show that real time usage value  of that particular milli-second till the next polling happens where only it gets the next value. So, suppose if the MIB polling for FPC CPU is happening every 1 minute, then the same value will be shown for that 1 minute till the next polling happens. Even  if they do some average-math with the next data with the previous real time one, it won’t be accurate.

For example, NMS server is sending a MIB polling request with OID requesting real time CPU Usage. Router responds with the real time CPU value for that particular moment. For example, 80%. Then, the next polling  is scheduled after 5 minutes from the NMS server, then, the NMS server will plot the value of 80% for the next 5 minutes. Even if it’s done some average math with the next polling value the graph will not look correct. So, the graph will show that inaccurate  value even the CPU actually dropped off in next second or some milli seconds !

As customer is using the real time CPU utilization OID instead of Average CPU OID, sub second CPU spikes are getting highlighted in the graph.

We would like to suggest your customer to use average CPU utilization OID instead of real time OID to fetch a genuine CPU utilization graph

Correct OID’s for FPC average CPU from 15.1 and above

|**No**|**Name**               |**Name mib**          |**OID**                                |
|------|-----------------------|----------------------|---------------------------------------|
|1     |
* *1 Minute average**  |jnxOperating1MinAvgCPU|
* *1.3.6.1.4.1.2636.3.1.13.1.23.7.x.0**|
|2     |
* *5 Minute average**  |jnxOperating1MinAvgCPU|**1.3.6.1.4.1.2636.3.1.13.1.24.7.x.0** |
|3     |
* *15 Minutes average**|jnxOperating1MinAvgCPU|**1.3.6.1.4.1.2636.3.1.13.1.25.7.x.0** |

Whereas ‘x’= FPC Number + 1

Example: To poll FPC0 , the value of x should be 1. For FPC1, the value for x will be 2. All other octets in the OID remains the same.

Note: They must set the polling interval according to these average intervals depends on what they are going to choose. In another words, they have to match the average interval and their polling interval  from NMS ( 1 minute, 5 minutes or 15 minutes) to get the accurate data plotted on to their graphs. 5 Minutes average shows optimum results with less intense polling.

Vậy em cập nhật thông tin để các anh chị nắm rõ tình hình.

Trân trọng cám ơn!
