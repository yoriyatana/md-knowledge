# vpn-apply-export and advertise-from-main-vpn-tables

#

---

chỗ ý 4 thì không biết khi nào thì sẽ cần apply ạ? em chưa hình dung case study cụ thể để dùng ạ?

Changing an RR to a non-RR or the reverse (by adding or removing the cluster statement) causes the table advertisement change. Also, configuring the first EBGP session or removing the EBGP session from the configuration in the master instance for a VPN NLRI family causes the table advertisement change.

<https://www.juniper.net/documentation/us/en/software/junos/bgp/topics/topic-map/bgp-session-flaps.html#jd0e161>

---> đây là 1 lý do/cách để workaround cho hành xử đã biết trên Junos (như mô tả chi tiết ở link trên) bằng cách ép cứng luôn luôn quảng bá vpn route từ main global table, ví dụ: bgp.l3vpn.0

lý do thứ 2 theo anh biết là: 1 số lý do cần phải thực hiện policy ở mức global khi quảng bá route vpn (có thể quảng bá export trực tiếp ở vrf có 1 số giới hạn về tinh chỉnh thuộc tính bgp,...)
