# PFE disable script

- Why?
    - Lỗi xảy ra trên các block trên PFE:
        - Blackhole traffic trên PFE
        - Blackhole traffic cả box
    - Giảm thời gian ảnh hưởng dịch vụ
    - Nếu khách hàng không chấp nhận sử dụng
        - -> có thể tham khảo để có dấu hiệu nhận biết các lỗi thường gặp ảnh hưởng dịch vụ
    - Yêu cầu khi dùng script:
        - Có dự phòng link, node, PFE
- What for?
    - Log classification
        - Transient hardware ~ one time issue: don't have trigger event, no symptom, no predictable
            - Parity Error
            - Thường có KB
            - Đánh giá được mức độ nghiêm trọng
        - Hardware
        - Software
        - Software or hardware
    - Phù hợp nhất với MPC dùng XM chip
    - Lỗi DDRIF không restart
    - Tình trạng Host loopback Wek: lỗi thoáng qua
- How?
- How efficient?

1 LUCHIP có 16 block PPE

- Head: header
- Tail: payload

MPC block diagram

action do script hay do JunOS thực hiện

KB31893

BOUNCING:

RESEAT: cli + physical action

RESET/RESTART: by cli

Action script disable port

show system commit | match script

delete inteface <int> disable

Action script offline PFE

request chassis fabric pfe fpc <> pic <>

request chassis fpc (offline | online | restart) slot slot-number

<all-members>

<local>

<member member-id>

set chassis fpc 0 error major action <>

show chassis fpc errors

show chassis fpc errors

show interface ext

show configure | di s set | match syslog

show log  mess

show start shell pfe  network

show hsl2 statistics crc

show hsl2 statistics

show cmerror module

show cmerror module <slot> error <mã lỗi>

show pfe traffic statistics | match "Hardware.*|Farbric drops"

Normal discard: discard do FF,...

show class-of-service fabric static ## check drop statistics

show chassis ethernet statistics
