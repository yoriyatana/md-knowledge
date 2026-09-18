# triển khai apply term Block_CTH_POLYCOM vào filter block-frag-in của Inside CGNAT

Dear Dũng, Vũ!

Sau khi triển khai apply term Block_CTH_POLYCOM vào filter block-frag-in của Inside CGNAT và giám sát firewall counter của term Block_CTH_POLYCOM từ tháng 11/2022 đến nay. Qua giám sát không xuất hiện hiện tượng cao CPU lại. Hiện tại thiết bị hoạt động ổn định.

Để tăng tính an toàn cho CGNAT, bên anh khuyến nghị bổ sung thêm term chỉ cho chỉ phép các gói tin có source là các dải Private đã qui hoạch được phép đi vào inside của card NAT để bảo vệ cho các NAT:

|set firewall family inet filter block-frag-in **term ALLOW_PRIVATE from source-prefix-list PRIVATE_IP_INTERNET**

set firewall family inet filter block-frag-in term ALLOW_PRIVATE then count allow_nat

set firewall family inet filter block-frag-in **term ALLOW_PRIVATE then accept**

set firewall family inet filter block-frag-in **term FINAL then discard**
delelte firewall family inet filter block-frag-in term 2|
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

Hiện tại trên thiết bị CGNAT cũng đã apply filter với các subinterface inside trong VRF_CGAT:

|

 * *unit 4052 {**

            description VRF_CGNAT;

            vlan-id 4052;

            family inet {

                filter {

                    * *input IP_PRIVATE_USER;**

                }

                address 172.16.146.33/30;

            }

        }

…

        filter IP_PRIVATE_USER {

            term ACCEPT_IP_PRIVATE_USER {

                from {

                    source-prefix-list {

                        CONNECTED_IP;

                        * *PRIVATE_IP_INTERNET**;

                    }

                }

                then accept;

            }

            term FINAL {

                then {

                    discard;

                }

            }

        }

...

    * *prefix-list PRIVATE_IP_INTERNET** {

        10. 0.0.0/8;

        100. 64.0.0/10;

    }
Ae…|
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

Vì vậy việc bổ sung thêm term **ALLOW_PRIVATE** trong filter block-frag-in không ảnh hưởng đến traffic CGNAT và tăng khả tính an toàn cho CGNAT.

Vậy cập nhật thông tin để các anh chị nắm rõ.

Trân trọng cám ơn!
