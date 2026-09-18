# BRAS Address Assignment Pools

> Generated deterministically from the approved grouping manifest.


## Source: `formatted/Case_notes/Các thuật ngữ sau được sử dụng để giải thích cách cấp phát địa chỉ IP (address-assignment).md`

# Các thuật ngữ sau được sử dụng để giải thích cách cấp phát địa chỉ IP (address-assignment)

Các thuật ngữ sau được sử dụng để giải thích cách cấp phát địa chỉ IP:

- lowAddress — Địa chỉ thấp nhất trong đoạn địa chỉ
- highAddress — Địa chỉ cao nhất trong đoạn địa chỉ
- nextAddress — Địa chỉ tiếp theo sau địa chỉ vừa được cấp phát.

Ví dụ dãy A có chỉ có 1 đoạn IP gồm 192.0.2.1, 192.0.2.2, 192.0.2.3, 192.0.2.4. Khi đó:

```text
lowAddress: 192.0.2.1
highAddress: 190.0.2.4
Nếu 192.0.2.2 là địa chỉ vừa được cấp phát, thì nextAddress: 192.0.2.3
```

Cách cấp phát liên tục (mặc định) để tìm ra IP address trống dùng cấp cho thuê bao:

- Ví dụ: dãy địa chỉ IP đang được cấu hình gồm 4 dãy là A, B, C, và D. Dãy địa chỉ vừa được cấp phát là C.

- Mỗi dãy chia thành 3 đoạn địa chỉ IP là r1, r2, r3. Đoạn địa chỉ vừa được sử dụng là r2.

Tiến trình tìm địa chỉ IP trong để cấp phát sẽ diễn ra như sau:

1. Tìm trong dãy địa chỉ C, từ nextAddress đến highAddress ở đoạn r2.

2. Tìm trong dãy địa chỉ C, từ lowAddress đến nextAddress ở đoạn r2.

3. Tìm trong dãy địa chỉ C, từ nextAddress đến highAddress ở đoạn r3.

4. Tìm trong dãy địa chỉ C, từ lowAddress đến nextAddress ở đoạn r3.

5. Tìm trong dãy địa chỉ C, từ nextAddress đến highAddress ở đoạn r1.

6. Tìm trong dãy địa chỉ C, từ lowAddress đến nextAddress ở đoạn r1.

Sau khi tìm trong dãy địa chỉ C, việc tìm kiếm tiếp tục diễn ra với dãy đầu tiên là A.

7. Tìm trong dãy địa chỉ A, từ nextAddress đến highAddress ở đoạn r2.

8. Tìm trong dãy địa chỉ A, từ lowAddress đến nextAddress ở đoạn r2.

9. Tìm trong dãy địa chỉ A, từ nextAddress đến highAddress ở đoạn r3.

10. Tìm trong dãy địa chỉ A, từ lowAddress đến nextAddress ở đoạn r3.

11. Tìm trong dãy địa chỉ A, từ nextAddress đến highAddress ở đoạn r1.

12. Tìm trong dãy địa chỉ A, từ lowAddress đến nextAddress ở đoạn r1.

Sau khi tìm trong dãy địa chỉ A, việc tìm kiếm tiếp tục diễn ra với dãy kế tiếp là B

Tiến trình tìm kiếm sẽ diễn ra cho tất cả các dãy. Thứ tự thực hiện sẽ là C > A > B > C > D, và kết thúc.

## Source: `formatted/TS_notes/BRAS check address-assignment.md`

# BRAS check address-assignment

```text
> show ddos-protection protocols dhcpv6 statistics brief
```

```text
> show ddos-protection protocols pppoe statistics brief
```

```text
> show ddos-protection protocols ndpv6 statistics brief
```

```text
> show configuration system ddos-protection | display inheritance
```

```text
> show configuration system
```

```text
> show ddos-protection protocols culprit-flows
```

```text
> show chassis routing-engine
```

```text
> show chassis fpc
```

```text
> show pppoe statistics
```

```text
> show network-access aaa terminate-code
```

```text
> show network-access aaa terminate-code brief
```

```text
> show subscribers |match glfdl-161031
```

```text
> show subscribers |match -161031
```

```text
> show subscribers mac-address a4:81:7a:d9:12:06
```

```text
> show subscribers | last
```

```text
> show subscribers user-name bifl-161220-008
```

```text
> show subscribers user-name bifdl-161220-008
```

```text
> show subscribers user-name bifdl-161220-008 extensive
```

```text
> show interfaces pp0.3221619975 extensive
```

```text
> show configuration dynamic-profiles PPPoE-FF-IPv6-2-nonQoS
```

```text
> show configuration access
```

```text
> show configuration routing-instances NAT
```

```text
> show subscribers interface pp0.3221619975 extensive
```

```text
> show system subscriber-management route prefix 2405:4800:4180:5513::/64
```

```text
> show system subscriber-management route prefix 2405:4800:4186:f769::/64
```

```text
> show dhcpv6 server binding
```

```text
> show dhcpv6 server binding 2405:4800:4186:f769::/64
```

```text
> show dhcpv6 server binding 2405:4800:4180:5513::/64
```

```text
> show configuration | display set | match 2405:4800:4186
```

```text
> show configuration | display set | match 2405:4800:418
```

```text
> show network-access address-assignment pool IPv6-MegaYou routing-instance NAT
```

```text
> show network-access address-assignment pool IPv6-MegaYou routing-instance NAT | match 2405:4800:4186:f769::/64
```

```text
> show network-access aaa statistics address-assignment pool IPv6-MegaYou
```

```text
> show configuration | display set | match 2405:4800:4180:551
```

```text
> show network-access aaa statistics address-assignment pool IPv6-Front
```
