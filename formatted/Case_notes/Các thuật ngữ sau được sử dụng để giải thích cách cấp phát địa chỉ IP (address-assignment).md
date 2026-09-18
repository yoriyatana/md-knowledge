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
