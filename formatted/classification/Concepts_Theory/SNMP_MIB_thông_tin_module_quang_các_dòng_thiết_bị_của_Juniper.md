# SNMP MIB thông tin module quang các dòng thiết bị của Juniper

Anh gửi thông tin MIB collect thông tin trên các thiết bị MXs mà bên em đang quan tâm:

1. Thực hiện collect với Junos 17.3R3 trên MX2010 và MX2020, MX960, mx240 thì có thể collect các thông tin module trên MX240,MX960,MX2010,MX2020. MX2008 hỗ trợ từ 20.1R3. TXP không hỗ trợ.

|**STT**|**ascii MIB**         |**OID MIB**              |**desciption**                                             |**Note**                                                                                                                                                                                    |**Thông tin mẫu  collect**                           |
|-------|----------------------|-------------------------|-----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
|1      |entPhysicalDescr      |1.3.6.1.2.1.47.1.1.1.1.2 |Mib mô tả các  thành phần hardware bao gồm part chữ        |Hỗ trợ trên MX960, MX2010(Junos kiểm tra  17.3R3), MX2020( Junos kiểm tra 17.3R3). **Riêng MX2008 hỗ trợ từ các junos 20.1R3, 20.3R3,  20.4R2, 21.1R2 trở đi. TXP không hỗ trợ các mib này**|entPhysicalDescr.444  = **CFP-100G-LR4** @ 1/1/0     |
|2      |entPhysicalSoftwareRev|1.3.6.1.2.1.47.1.1.1.1.10|Mib hiển thị  Junos version mà các thành phần đang sử dụng |entPhysicalSoftwareRev.444  = **17.3R3-S10.1**                                                                                                                                              |                                                     |
|3      |entPhysicalSerialNum  |1.3.6.1.2.1.47.1.1.1.1.11|Mib hiển thị  Serial Number của thành phần hardware        |entPhysicalSerialNum.444  = **U2QASLU**                                                                                                                                                     |                                                     |
|4      |entPhysicalMfgName    |1.3.6.1.2.1.47.1.1.1.1.12|Mib hiển thị  vendor cung cấp thành phần hardware          |entPhysicalMfgName.444  = **FINISAR CORP**.                                                                                                                                                 |                                                     |
|5      |entPhysicalModelName  |1.3.6.1.2.1.47.1.1.1.1.13|Mib hiển thị  Part số của thành phần hardware              |entPhysicalModelName.444  = **740-047682**                                                                                                                                                  |                                                     |
|6      |ifTable               |1.3.6.1.2.1.2.2          |Mib hiển thị  thông tin về interfaces                      |                                                                                                                                                                                            |ifDescr.622    = et-2/1/0  ifSpeed.622   = 4294967295|
|       |                      |                         |                                                           |                                                                                                                                                                                            |                                                     |

1. Trên MX2010,MX2020 sử dụng junos 15.1F6 đang chạy trên MANE chưa hỗ trợ các mibs collect thông tin trên.

* *Hướng xử lý:**

- Ngoài việc collect thông tin module trên MXs qua SNMP, chúng ta có thể collect thông tin module và hardware thông qua hardware inventory trên Automation tool mà Svtech đã thử nghiệm.
