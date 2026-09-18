# Kênh IPTV đứng hình khi xem

update kinh nghiệm 1 case multicast ftel:

- hiện tượng: iptv đứng hình khi đang xem, hoặc khi chuyển kênh có khi 10p sau kênh mới xem được, kênh bị ngẫu nhiên.

- đã add igmp static dưới switch nok.

- trên router: multicast route stats = 0 khi giựt hình hoặc ko xem được, pim join bị timeout

- troubleshoot: pim join extensive theo đường từ client đến server, có 1 router bị pim join timeout ngẫu nhiên==> có hiện tượng drop pim join ở vị trí router này

- nguyên nhân: do policer protect RE của pim
