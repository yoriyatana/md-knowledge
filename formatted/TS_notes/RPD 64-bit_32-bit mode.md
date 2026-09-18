# RPD 64-bit/32-bit mode

Dear Anh Cường,

Em xin tổng hợp lại case của bên mình đang gặp như sau:

- Lỗi: Nháy hàng loạt phiên BGP.

- Nguyên nhân:

+ Core-dump xuất hiện khi tiến trình RPD(BGP) yêu cầu cung cấp thêm memory xử lý.

Tại thời điểm lỗi memory sử dụng 77%

# define ENOMEM      12  /\* Out of memory \*/

Logical system: HCM-RR02

Routing table: default.inet

Internet:

Enabled protocols: Bridging, Dual VLAN,

user:         852573 routes

perm:          5 routes

intf:          5 routes

dest:          8 routes

root@HCM001PRT02\_RE0> show system core-dumps no-forwarding

/var/crash/\*core\*: No such file or directory

- rw-rw----  1 root  wheel  738680996 Jun 4  05:37 /var/tmp/rpd\_HCM-RR02.core-tarball.0.tgz

Hiện tại HCM-RR02 đang học tầm 852573 routes -> trong quá trình xảy ra lỗi, đã có số lượng routes được thêm vào.

- > RPD bị crashed trong logical system HCM-RR02 do cạn kiệt memory.

+ RPD đang chạy ở 32-bit mode

cuong.hv1@HCM001PRT02\_RE0> show system processes | no-more

14051  -  S       391:40.41 /usr/libexec64/rpd -N  -> RPD master đang chạy chính là 64-bit mode

35980  -  S       952:24.63 /usr/sbin/rpd -N -JLHCM-RR02  -> ở LS HCM-RR02 đang chạy 32-bit mode

- Giải pháp:

Thay đổi value 64bit trong logical-system

logical-systems {

HCM-RR02 {

system {

processes {

routing {

force-64-bit

}

}

}

}

}

Lưu ý: Thực hiện vào giờ thấp điểm vì có khả năng restart routing.

Anh Cường nắm thông tin, chưa rõ đoạn nào thì báo em biết nhé.

Em cảm ơn ạ

HCM001PRT02\_RE0> show system processes | no-more | match rpd

14051  -  S       454:58.01 /usr/libexec64/rpd -N

35980  -  S      3895:01.23 /usr/libexec64/rpd -N -JLHCM-RR02

HCM001PRT02\_RE0> show task memory logical-system HCM-RR02

Memory                 Size (kB)  Percentage  When

Currently In Use:      4497732         13%  now

Maximum Ever Used:     4525031         13%  21/06/16 16:20:12

Available:            34281107        100%  now
