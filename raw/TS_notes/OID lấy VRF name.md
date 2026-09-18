# OID lấy VRF name

Subject: RE: Ticket được tạo mới: SR-2022-1024-0929 - Viettel- SLA- Hỗ trợ cung cấp OID lấy VRF name trên thiết bị router của Juniper- SN: NK0216180128

Dear Sơn,

Hiện tại thiết bị Juniper chưa có OID nào chính xác để bắt được thông tin VRF name trên thiết bị.

Hiện chỉ có OID lấy thông tin description của VRF: 1.3.6.1.3.118.1.2.2.1.3

juniper@MX960\_UPE02\_RE0> show snmp mib walk 1.3.6.1.3.118.1.2.2.1.3

mplsVpnVrfDescription.8.76.51.86.80.78.45.51.71 = L3VPN-3G

mplsVpnVrfDescription.8.76.51.86.80.78.45.52.71 = L3VPN-4G

mplsVpnVrfDescription.9.76.51.86.80.78.45.66.73.90 = L3VPN-BIZ

mplsVpnVrfDescription.9.76.51.86.80.78.45.86.79.68 = L3VPN-VOD

- Trường hợp VRF không cấu hình description thì description lấy trùng VRF name -> OID này có thể lấy đúng VRF name
- Trường hợp VRF có cấu hình description thì OID này lấy theo thông tin description đã cấu hình, có thể ko trùng VRF name.

Hoặc có thể phần mềm thực hiện convert decimal thành string để lấy giá trị VRF name:

juniper@MX960\_UPE02\_RE0> show snmp mib walk 1.3.6.1.3.118.1.2.2.1.3 ascii

mplsVpnVrfDescription."L3VPN-3G" = L3VPN-3G

mplsVpnVrfDescription."L3VPN-4G" = L3VPN-4G

mplsVpnVrfDescription."L3VPN-BIZ" = L3VPN-BIZ

mplsVpnVrfDescription."L3VPN-VOD" = L3VPN-VOD

như 2 output show trên mình có thể dùng phần mềm convert giá trị 8.76.51.86.80.78.45.51.71 thành L3VPN-3G
