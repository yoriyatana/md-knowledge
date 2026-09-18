# DDoS Protection và RE Protection trên MX

- Gói tin đi vào linecard sẽ đi qua các thành phần:
    - Đi vào cổng vật lý
    - Chuyển đến khối Forwarding: bao gồm cả header và payload
        - Tách biệt phần header và payload -> băm nhỏ header ra thành parcel
            - gói tin có kích thước nhở hơn 320B thì không tách ra
    - Chuyển parcell đến khối Routing: xác định outgoing interface theo bảng FIB
        - Nếu outgoing interface cùng PFE: 
        - Nếu outgoing interface không cùng PFE: băm gói tin thành j-cell 64B và đẩy gói tin sang fabric 
- Trio Chipset gồm:
    - Routing ASIC: chứa thông tin FIB (gồm destination và NH để tiết kiệm Memory)
    - Forwarding ASIC: 
    - Enhanced CoS
- Linecard CPU:
    - giám sát và quản lý thông tin các component trên FPC
- Khi chạy các protol sử dụng multicast, khi enable protocol đó thì multicast address của protocol sẽ được thêm vào bảng inet.0 để biết được gói tin này nó sẽ xử lý
