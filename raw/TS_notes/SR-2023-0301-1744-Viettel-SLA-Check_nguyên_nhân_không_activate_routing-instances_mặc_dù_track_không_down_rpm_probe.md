# SR-2023-0301-1744 - Viettel- SLA- Check nguyên nhân không activate routing-instances mặc dù track không down rpm probe

Em xin update lại case này như sau ah:

 

**1/ Trước tiên em xin phép giải thích các tham số hiện tại mình đang cấu hình**

 

|**Cấu hình hiện tại**                                                                                                                                                                                                                                                                                                                 |**Ý nghĩa**                                                                                                                                                                                                                                                                                       |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   probe TRACK_GW_VDTC {

       test TRACK_GW_VRF {

           probe-type icmp-ping;

           target address 10.254.255.19;

           probe-count 3;

          probe-interval 1;

          test-interval 1;

           routing-instance own_namctcpgtsv1;

           thresholds {

               total-loss 3;

           }

       }

   }

}
rpm {|>> Điều này có nghĩa rằng cứ khoảng hơn 3s RPM sẽ report một kết quả TEST FAILED hoặc TEST COMPLETED.
Mỗi lần TEST thực hiện send probe 3 gói ICMP, mỗi gói cách nhau 1s. Nếu loss cả 3 gói thì kết luận PING_TEST_FAILED, còn lại kết luận PING_TEST_COMPLETED. Mỗi lần TEST cách nhau 1s.        |
|   events ping_test_completed;

   within 30 {

       trigger on 1;

       events ping_test_failed;

   }

   then {

       ..actions..

   }

}
policy VDTC_UP {                                                                                                                                                                                   |>> Điều này tương đương rằng PING_TEST_FAILED phải xảy ra liên tục ít nhất 30s trước khi xuất hiện PING_TEST_COMPLETED thì policy mới được kích hoạt.
Nếu kết quả PING_TEST_COMPLETED xuất hiện duy nhất 1 lần trong 30s và trong 30s đó có cả PING_TEST_FAILED, thì policy này mới được kích hoạt.|
|   events ping_test_failed;

   within 30 {

       trigger on 1;

       events ping_test_completed;

   }

   then {

       ..actions..

   }

}
policy VDTC_DOWN {                                                                                                                                                                                 |>> Điều này tương đương rằng PING_TEST_COMPLETED phải xảy ra liên tục ít nhất 30s trước khi xuất hiện PING_TEST_FAILED thì policy mới được kích hoạt.
Nếu kết quả PING_TEST_FAILED xuất hiện duy nhất 1 lần trong 30s và trong 30s đó có cả PING_TEST_COMPLETED, thì policy này mới được kích hoạt.|

 

**2/ Trở lại issue**

 

Quan sát một đoạn log nhỏ bên dưới ta sẽ thấy rằng:

 

- Tại thời điểm 14:44:25 có xuất hiện PING FAILED, và trước đó có kết quả PING COMPLETED đã xảy ra liên tục hơn 30s → Nên thỏa mãn điều kiện kích hoạt policy, do vậy ta có thể thấy action deactivate vẫn hoạt động bình thường.
- Đến thời điểm 14:44:33 có xuất hiện PING COMPLETED, tuy nhiên trước đó kết quả PING_FAILED chưa đủ 30s  (từ 14:44:25 đến 14:44:33 mới được khoảng 8s), (hay nói cách khác trong 30s đó có nhiều hơn 1 lần PING COMPLETED) → Nên không thỏa mãn điều kiện kích hoạt policy và dẫn đến không có action activate nào được thực hiện.

 

<30>1 2023-03-01T14:41:53.976+07:00 QNH0422SRT03 rmopd 4022 PING_TEST_COMPLETED [junos@2636.1.1.1.2.116 test-owner="TRACK_GW_VDTC" test-name="TRACK_GW_VRF"]

<30>1 2023-03-01T14:42:11.994+07:00 QNH0422SRT03 - - - - last message repeated 6 times

<30>1 2023-03-01T14:42:33.016+07:00 QNH0422SRT03 - - - - last message repeated 7 times

<30>1 2023-03-01T14:42:36.020+07:00 QNH0422SRT03 rmopd 4022 PING_TEST_COMPLETED [junos@2636.1.1.1.2.116 test-owner="TRACK_GW_VDTC" test-name="TRACK_GW_VRF"]

<30>1 2023-03-01T14:42:42.026+07:00 QNH0422SRT03 - - - - last message repeated 2 times

<30>1 2023-03-01T14:44:21.130+07:00 QNH0422SRT03 - - - - last message repeated 33 times

<30>1 2023-03-01T14:44:25.135+07:00 QNH0422SRT03 rmopd 4022 PING_TEST_FAILED [junos@2636.1.1.1.2.116 test-owner="TRACK_GW_VDTC" test-name="TRACK_GW_VRF"]

<182>1 2023-03-01T14:44:27.015+07:00 QNH0422SRT03 mgd 95976 UI_CFG_AUDIT_OTHER [junos@2636.1.1.1.2.116 username="root" action="deactivate" pathname="[routing-instances own_namctcpgtsv1 routing-options static route 10.12.5.0/25\]" delimiter="" value=""]

<182>1 2023-03-01T14:44:27.038+07:00 QNH0422SRT03 mgd 95976 UI_CFG_AUDIT_OTHER [junos@2636.1.1.1.2.116 username="root" action="deactivate" pathname="[routing-instances own_namctcpgtsv1 routing-options static route 10.12.5.128/25\]" delimiter="" value=""]

<30>1 2023-03-01T14:44:28.389+07:00 QNH0422SRT03 rmopd 4022 PING_TEST_FAILED [junos@2636.1.1.1.2.116 test-owner="TRACK_GW_VDTC" test-name="TRACK_GW_VRF"]

<30>1 2023-03-01T14:44:31.644+07:00 QNH0422SRT03 - - - - last message repeated 2 times

<30>1 2023-03-01T14:44:31.644+07:00 QNH0422SRT03 rmopd 4022 PING_TEST_FAILED [junos@2636.1.1.1.2.116 test-owner="TRACK_GW_VDTC" test-name="TRACK_GW_VRF"]

<30>1 2023-03-01T14:44:33.905+07:00 QNH0422SRT03 rmopd 4022 PING_TEST_COMPLETED [junos@2636.1.1.1.2.116 test-owner="TRACK_GW_VDTC" test-name="TRACK_GW_VRF"]

<30>1 2023-03-01T14:44:36.910+07:00 QNH0422SRT03 rmopd 4022 PING_TEST_COMPLETED [junos@2636.1.1.1.2.116 test-owner="TRACK_GW_VDTC" test-name="TRACK_GW_VRF"]

<30>1 2023-03-01T14:44:39.913+07:00 QNH0422SRT03 rmopd 4022 PING_TEST_COMPLETED [junos@2636.1.1.1.2.116 test-owner="TRACK_GW_VDTC" test-name="TRACK_GW_VRF"]

 

Như vậy ở đây có thể kết luận do thời gian flapping từ ping FAILED sang ping COMPLETED quá nhanh (< 30s), nên không thể kích hoạt được policy action.

 

**3/ Khuyến nghị**

 

Do vậy để giải quyết vấn đề này, nhờ các anh cân nhắc việc chuyển cấu hình thời gian within từ 30s sang 5s ah.
