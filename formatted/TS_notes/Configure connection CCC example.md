# Configure connection CCC example

lab@MX204-01> show configuration | compare

[edit interfaces xe-0/1/5]

+ unit 2000 {

+ encapsulation vlan-ccc;

+ vlan-id-list [ 2000-2100 4000 ];

+ }

[edit interfaces ae100]

+ unit 2000 {

+ encapsulation vlan-ccc;

+ vlan-id-list [ 2000-2100 4000 ];

+ }

[edit protocols]

+ mpls {

+ interface xe-0/1/5.2000;

+ interface ae100.2000;

+ }

+ connections {

+ interface-switch EndUser\_to\_SRT {

+ interface xe-0/1/5.2000;

+ interface ae100.2000;

+ }

+ }

[edit interfaces xe-0/1/0]

+ description To-MX104\_01-ge-0/0/3;

+ mtu 9192;

+ encapsulation ethernet-ccc;

+ unit 0 {

+ family ccc;

+ }

[edit interfaces xe-0/1/1]

+ description To-MX104\_01-ge-0/0/4;

+ mtu 9192;

+ encapsulation ethernet-ccc;

+ unit 0 {

+ family ccc;

+ }

[edit protocols mpls]

+ interface xe-0/1/0.0;

+ interface xe-0/1/1.0;

[edit protocols connections]

+ interface-switch LOOP\_MX960\_02 {

+ interface xe-0/1/0.0;

+ interface xe-0/1/1.0;

+ }
