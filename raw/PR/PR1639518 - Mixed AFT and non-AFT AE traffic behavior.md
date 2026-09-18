# PR1639518 - Mixed AFT and non-AFT AE traffic behavior

# 2. PR1639518

This issue might be seen if the following conditions are met:

\* MX equipped with AFT FPC (e.g. MPC10E/11E) and non-AFT FPC (e.g. MPC5E)

\* Traffic ingressing on a non-AFT line card and destined to go via IRB over AE with member links hosted on both AFT and non-AFT line cards

Khuyến nghị các Anh/Chị FTEL: trong điều kiện cho phép, đừng thực hiện bundle các Interfaces thuộc các loại MPC type khác nhau để tránh các hành xử về traffic không mong muốn.


## Related investigation notes

[ May 5, 2022 10:37 ] ⁨SVT.Anh.VT⁩: Dạ anh Đăng, anh Hưng ơi, bọn em đang rà soát lại mấy case FPC11 vừa rồi bên FTEL thì có vẻ mỗi lần lỗi thì bọn em có quan sát thấy có cái log matching với PR này

[ May 5, 2022 10:38 ] ⁨SVT.Anh.VT⁩: <https://prsearch.juniper.net/problemreport/PR1639518>

[ May 5, 2022 10:38 ] ⁨SVT.Anh.VT⁩: Anh cho bọn em xin thêm thông tin chi tiết hơn của PR được ko anh :D

[ May 5, 2022 10:38 ] ⁨SVT.Anh.VT⁩: Em cám ơn ạ.

[ May 9, 2022 14:30 ] ⁨Hung Le⁩: PR này mở ra để track viec sua lỗi của PR 1601049

[ May 9, 2022 14:32 ] ⁨SVT.Anh.VT⁩: Dạ, PR này thì em thấy nói MPC11E ko hit phải anh ạ

[ May 9, 2022 14:32 ] ⁨SVT.Anh.VT⁩: On all Junos platforms with MPC10E line-cards, repeated 100GE interface link flaps may result in loss of traffic going out of the interface. Each 100GE interface down event might not flush the stream and triggers a major alarm causing disable-pfe action. This is specific to interfaces configured with high priority scheduler. MPC11E card is not exposed.

[ May 9, 2022 14:34 ] ⁨SVT.Anh.VT⁩: tuy nhiên check log của PR1639518 thì em thấy log giống PR đó, còn PR1601049 thì ko thấy log anh ạ

[ May 9, 2022 14:35 ] ⁨SVT.Anh.VT⁩: Em đang đợi hãng confirm xem MPC11E có hit vào PR1639518 hay không và có workaround nào ko anh ạ !

[ May 9, 2022 14:38 ] ⁨Hung Le⁩: 1639518: This PR is to track the cosd related changes from Rajesh which was added in the context of the PR#1601049 for interface flap leading to pfe-disable and wedge condition.

[ May 9, 2022 15:02 ] ⁨Hung Le⁩: (interface not able to send/receive any packet after flapping on MPC10E card)1560772 vi fix loi cho PR nay nen gay ra loi dc mô tả trong PR 1601049(Changes to ensure that COSD does not respond immediately to link flaps

)=>PR1639518 will be used to port the change to all other throttles as original PR tracks

[ May 9, 2022 15:02 ] ⁨Hung Le⁩: zt chip đều bị hit 1560772, nhung lỗi chỉ mới thấy ở mpc10

[ May 9, 2022 15:02 ] ⁨Hung Le⁩: chưa thấy ở mpc11 chứ ko phải ko bị ở mpc11

[ May 9, 2022 15:09 ] ⁨Ju.a.Đăng⁩: Như thường lệ, PR chỉ focus vào data có ở thời điểm đó & cho khách hàng ở thời điểm đó thôi chứ ko bao quát tất cả các trường hợp.

