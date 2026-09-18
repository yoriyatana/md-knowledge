# BGP AS 4-bytes

**![](image/21ff5a283ddd7d617bb33e5e9f13b632.png)**

**![](image/1fdc4f39897578df1027e973696cb238.png)**

**Khi build gói update cho neighbor không support AS4, BGP tự động send cả 2 loại attribute AS Path (bao gồm cả thông tin AS2 và AS4) nên gói tin mới bị too big (>4096 bytes)**

**![](image/bc1e687bdf47c5f0e6d908168513f506.png)**
