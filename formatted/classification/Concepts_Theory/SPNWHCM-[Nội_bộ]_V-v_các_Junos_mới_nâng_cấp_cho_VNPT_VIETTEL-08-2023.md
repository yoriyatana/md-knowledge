# SPNWHCM - [Nội bộ] V/v các Junos mới nâng cấp cho VNPT VIETTEL - 08/2023

Hi ACE

Chiều qua mấy ae có ngồi discuss về các junos đã/đang test cho Vtel và VnPT và xem có sử dụng dc chung kq cho đỡ mất công sức test POC

Em gửi note sau buổi discuss chiều qua nhé

|             |**VnPT**           |**Team Test**|**Viettel**|**Team Test**|**Notes**            |      |                                                                                              |
|-------------|-------------------|-------------|-----------|-------------|---------------------|------|----------------------------------------------------------------------------------------------|
|             |**Current**        |**Target**   |           |**Current**  |**Target**           |      |                                                                                              |
|MANE/METRO   |14.2/15.1/17.3/18.4|20.4R3-S8    |HN         |             |20.4R3-S8            |HN    |                                                                                              |
|PE           |17.3/18.4          |20.4R3-S8    |HCM        |             |21.2R3-Sx            |HCM   |TBD                                                                                           |
|BNG          |17.3/18.4          |20.4R3-S8    |HCM        |18.4         |20.4R3-S8 or21.2R3-Sx|HN    |                                                                                              |
|CGNAT MS-MPC |15.1               |21.2R3-S6    |HN         |18.4R3       |21.2R3-S6            |HN    |Trao đổi VnPT có nâng cấp đợt này hay ko vì đg nâng cấp toàn mạng VN2, MANE không có nguồn lực|
|CGNAT MX-SPC3|19.4               |21.4R3-S4.9  |           |NA           |21.4R3-S4.9          |HN+HCM|                                                                                              |
|             |                   |             |           |             |                     |      |                                                                                              |
|             |                   |             |           |             |                     |      |                                                                                              |
|             |Done               |             |           |             |                     |      |                                                                                              |
|             |low pri            |             |           |             |                     |      |                                                                                              |
|             |high pri           |             |           |             |                     |      |                                                                                              |
|             |TBD                |             |           |             |                     |      |                                                                                              |
