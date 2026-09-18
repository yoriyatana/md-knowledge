# tính năng link-degrade để detect BER trên thiết bị Juniper

Em gửi lại cấu hình tính năng link-degrade để phát hiện BER đường trường với giá trị tốt hơn wanphy hiện tại:

```
set interfaces xe-3/0/0 link-degrade-monitor link-degrade-monitor-enable   /* enable tính năng trên interface vật lý */
set interfaces xe-3/0/0 link-degrade-monitor actions media-based     /* Action shutdown port khi BER đến ngưỡng set */
set interfaces xe-3/0/0 link-degrade-monitor recovery manual  /* Thực hiện recover lại trạng thái port bằng tay khi hoàn thành xử lý lỗi đường truyền */
set interfaces xe-3/0/0 link-degrade-monitor thresholds set 1e-8     /* Ngưỡng BER sẽ shutdown port */
set interfaces xe-3/0/0 link-degrade-monitor thresholds clear 1e-9   /* Ngưỡng BER clear trạng thái port về bình thường (có tác dụng khi sử dụng recovery auto */
set interfaces xe-3/0/0 link-degrade-monitor thresholds warning-set 1e-9   /* Ngưỡng BER thiết bị đẩy cảnh báo */
set interfaces xe-3/0/0 link-degrade-monitor thresholds warning-clear 1e-10 /* Ngưỡng BER clear cảnh báo */
set interfaces xe-3/0/0 link-degrade-monitor thresholds interval 1   /* 1 lần chạm ngưỡng BER set thì thực hiện shutdown port */
```

- SVTech đã thực hiện test LAB tính năng này với port 100G trên MPC7 và port 10G trên MPC4 để phát hiện BER trên đường truyền giữa 2 thiết bị truyền dẫn

+ Cách test:

Setup kênh truyền giữa 2 thiết bị truyền dẫn để nối 2 thiết bị MX Juniper

Kết nối thêm thiết bị OVA giữa link kết nối 2 thiết bị TD để tạo suy hao BER

Kiểm tra tính năng link-degrade trên MX Juniper

- > kết quả tính năng hoạt động đúng với các ngưỡng BER cấu hình

- Tính năng hoạt động được với các loại card:

|- MPC4E-3D-2CGE-8XGE
- MPC4E-3D-32XGE-SFPP
- MPC-3D-16XGE-SFP
- MPC3 with MIC3-3D-1X100GE-CFP
- MPC3 with MIC3-3D-2X40GE-QSFPP
- MPC3 with MIC-3D-2XGE-XFP
- MPC3 with 2x10GE XFP MIC
- MPC3 with 2x10GE XFP MIC
- MPC5 with following variants:
    - 2CGE + 4XGE
    - 24XGE + 6XLGE
- MPC6 with the following variants:
    - 2X100GE CFP2
    - 24X10GE SFPP
    - 24X10GE SFPP OTN
    - 4x100GE CXP
- MPC7E-MRATE
- MPC7E-10G (non-MACsec mode)
- MX2K-MPC8E with MIC-MRATE
- MX2K-MPC9E with MIC-MRATE

Note:

Link degrade monitoring is not supported on MACsec-enabled MPC7E-10G and MIC-MACSEC-MRATE.

- MPC10E-10C-MRATE (10G, 25G, 40G, 100G and 400G interfaces)
- MPC10E-15C-MRATE (10G, 25G, 40G, 100G and 400G interfaces)
- MX2K-MPC11E (10G, 40G, 100G, and 400G interfaces)

|
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

- Cách kiểm tra:

+ Kiểm tra trạng thái và các tham số:

```
svtech@TNN-BNG1_RE0> show interfaces et-10/0/5
Dec 14 15:08:33
Physical interface: et-10/0/5, Enabled, Physical link is Down
  Interface index: 217, SNMP ifIndex: 751
  Link-level type: Ethernet, MTU: 9192, MRU: 9200, Speed: 100Gbps, BPDU Error: None,
  Loop Detect PDU Error: None, Loopback: Disabled, Source filtering: Disabled,
  Flow control: Disabled
  Pad to minimum frame size: Disabled
  Device flags   : Present Running Down
  Interface flags: Hardware-Down SNMP-Traps Internal: 0x4000
  CoS queues     : 8 supported, 8 maximum usable queues
  Schedulers     : 0
  Current address: f0:1c:2d:7f:d4:c3, Hardware address: f0:1c:2d:7f:d3:86
  Last flapped   : 2021-12-14 15:08:24 ICT (00:00:09 ago)
  Input rate     : 0 bps (0 pps)
  Output rate    : 0 bps (0 pps)
  Active alarms  : LINK
  Active defects : LINK, LOCAL-FAULT
  PCS statistics                      Seconds
   Bit errors                             0
   Errored blocks                         1
  Ethernet FEC Mode  :                   NONE
  Ethernet FEC statistics              Errors
   FEC Corrected Errors                    0
   FEC Uncorrected Errors                  0
   FEC Corrected Errors Rate               0
   FEC Uncorrected Errors Rate             0
  Link Degrade :
   Link Monitoring                   :  Enable
   Link Degrade Set Threshold        :  1E-8
   Link Degrade Clear Threshold      :  1E-9
   Link Degrade War Set Threshold    :  1E-9
   Link Degrade War Clear Threshold  :  1E-10
   Estimated BER                     :  1E-8
   Link-degrade event                :  Seconds              Count                State
                                        9                    1                    Defect Active
  Interface transmit statistics: Disabled
```

+ Kiểm tra cảnh báo:

```
svtech@TNN-BNG1_RE0> show log messages | match degrade
Dec 14 15:08:24.667 2021  TNN-BNG1_RE0 fpc10 IFD: et-10/0/5 BER:1E-8, Link Degrade Warning SET threshold (1E-9) is crossed.
Dec 14 15:08:24.667 2021  TNN-BNG1_RE0 fpc10 IFD: et-10/0/5 BER:1E-8 Link Degrade SET threshold (1E-8) is crossed, ber_set_th_cross_event_cnt: 0 ifd_compare_cfg_thresholds.
Dec 14 15:08:24.669 2021  TNN-BNG1_RE0 fpc10 IFD: et-10/0/5 BER:1E-8 Link Degrade SET threshold (1E-8) cross event is observed 1 consecutive times, marking the IFD as Degraded ifd_compare_cfg_thresholds.
Dec 14 15:08:24.669 2021  TNN-BNG1_RE0 fpc10 IFD: et-10/0/5 *** Link Degrade Event:1 *** smic_link_degrade_action.
Dec 14 15:08:24.669 2021  TNN-BNG1_RE0 fpc10 et-10/0/5: Link Degrade is set, ifd_flags:0x8000 smic_link_degrade_action
Dec 14 15:09:20.288 2021  TNN-BNG1_RE0 mgd[55666]: UI_CMDLINE_READ_LINE: User 'svtech', command 'request interface link-degrade-recover et-1/0/5 '
Dec 14 15:09:30.241 2021  TNN-BNG1_RE0 mgd[55666]: UI_CMDLINE_READ_LINE: User 'svtech', command 'request interface link-degrade-recover et-10/0/5 '
Dec 14 15:09:30.844 2021  TNN-BNG1_RE0 fpc10 IFD: et-10/0/5 *** Link Degrade Event:2 *** smic_link_degrade_action.
Dec 14 15:09:30.845 2021  TNN-BNG1_RE0 fpc10 et-10/0/5: Link Degrade is Cleared, ifd_flags:0x8001
Dec 14 15:09:30.845 2021  TNN-BNG1_RE0 fpc10 smic_pic_cmd: PIC 0 Link degrade manual recovery OK
```

Nhờ các anh thử nghiệm trên 1 link riêng cho 2G và test lại trên mạng thật.

- --

Em gửi bổ sung lệnh để recover port, đưa port UP lại sau khi bị shutdown bởi đạt ngưỡng BER set:

```
request interface link-degrade-recover et-1/0/5
```
