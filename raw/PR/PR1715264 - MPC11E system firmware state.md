# PR1715264 - MPC11E system firmware state

[ March 6, 2023 10:34 ] ⁨SVT.Tùng.NT⁩: Hi anh ‪⁨Ju.a.Đăng⁩, anh ‪⁨Hung Le⁩, anh ‪⁨Ju.a.Cương⁩ , khách hàng FTEL đang có hỏi về TSB này ạ. Nhờ các anh cho em hỏi số lượng MPC11 được report với TSB này với ạ?

[ March 6, 2023 11:05 ] ⁨Hung Le⁩: sao lai hỏi sl card bi em nhỉ?

[ March 6, 2023 11:12 ] ⁨SVT.Tùng.NT⁩: dạ tại trong TSB đề cập là case report với MPC11E là ít hơn. Nên tụi em muốn biết số lượng để xem mức độ có phổ biến không ạ

[ March 6, 2023 11:13 ] ⁨SVT.Tùng.NT⁩: Hiện FTEL em check thì đang dùng ~ 14 card MPC11E ạ

[ March 7, 2023 14:36 ] ⁨Hung Le⁩: Hi em, voi MPC11 chi ghi nhan:

```text
show system firmware' for MPC11E may go bad after RE SWO or chassisd restart. Unable to proceed firmware upgrade.
```
[ March 7, 2023 14:36 ] ⁨Hung Le⁩: khong co ghi nhan bi reboot

[ March 7, 2023 14:37 ] ⁨Hung Le⁩: mac du cung 1 TSB

[ March 7, 2023 14:37 ] ⁨Hung Le⁩: trong TSB cung co de cap ne e

```text
[ March 7, 2023 14:37 ] ⁨Hung Le⁩: MPC11E with 21.3 and earlier Junos has a known issue that 'show system firmware' output would become an unexpected state and prevents firmware upgrade. rebooting the MPC11E board resolves the issue and makes firmware upgrade available.
```
PR1715264 is tracking this. Pelase refer external-tab on the PR for detail.

[ March 7, 2023 14:54 ] ⁨SVT.Tùng.NT⁩: Dạ, vậy em xin trình bày lại ý em đang hiểu về TSB này cho MPC11 xem em đã hiểu đúng chưa các anh ạ:

- Hiện chưa ghi nhận card MPC11 bị slient reboot như TSB này mô tả

- MPC11 với JunOS từ 21.3 sẽ hit với PR1715264

[ March 7, 2023 15:01 ] ⁨Hung Le⁩: Ban đầu sẽ là :

[ March 7, 2023 15:01 ] ⁨Hung Le⁩: In rare situations, MPC10E, EX9200-15C, and MPC11E line cards may get silently restarted without any trigger or external event. No core dump is observed during the event.

This problem might be caused by CPU ucode eratta and can be resolved by upgrading MPC BIOS by installing the optional jfirmware package.

```text
The failed device will become online after the silent restarted.
```
Juniper Networks is aware of multiple production cases for MPC10E and EX9200-15C.

MPC11E potentially has the same problem but less number of cases have been reported so far.

[ March 7, 2023 15:01 ] ⁨Hung Le⁩: sau các lần cập nhật và ghi nhận thực tế thì bổ sung thêm:

```text
> MPC11E with 21.3 and earlier Junos has a known issue that 'show system firmware' output would become an unexpected state and prevents firmware upgrade. rebooting the MPC11E board resolves the issue and makes firmware upgrade available.
```
PR1715264 is tracking this. Pelase refer external-tab on the PR for detail.
