# traceoptions for specific RSVP

Như có trao đổi, anh gửi lại đoạn cấu hình để capture các log có liên quan đến giao thức RSPV, và capture only LSP mình cần. Có một số lưu ý như sau

|  |
| --- |
| set protocols rsvp lsp-set MY\_LSP\_SET match-criteria lsp-name TO\_PE\_01\_NEW  //Thay thế TO\_PE\_01\_NEW bằng các LSP mà mình muốn capture log khi có issue  set protocols rsvp lsp-set MY\_LSP\_SET traceoptions file RSVP\_LSP\_SPECIFIC  set protocols rsvp lsp-set MY\_LSP\_SET traceoptions file size 10m  set protocols rsvp lsp-set MY\_LSP\_SET traceoptions flag path detail  set protocols rsvp lsp-set MY\_LSP\_SET traceoptions flag pathtear detail  set protocols rsvp lsp-set MY\_LSP\_SET traceoptions flag resv detail  set protocols rsvp lsp-set MY\_LSP\_SET traceoptions flag resvtear detail  set protocols rsvp lsp-set MY\_LSP\_SET traceoptions flag error detail |

- Cấu hình này cần bật trên các box dọc theo tuyến đường của LSP (Transit/Egress/Ingress).
- Nếu muốn bắt nhiều LSP, có thể tạo ra nhiều lsp-set và cấu hình tương ứng.

- --

1) Rsvp logging that is enabled. Want to add in all the pathErr seen on P1 and P2 systems.

Next commannd is hidden..please type out full command.

1) show rsvp transport interface | no-more

2) show rsvp transport queues -- 3 times 10 second intervals

3) show rsvp transport task - 3 times 10 second intervals

4) show rsvp transport neighbor | no-more -- 3 times 10 second interval
