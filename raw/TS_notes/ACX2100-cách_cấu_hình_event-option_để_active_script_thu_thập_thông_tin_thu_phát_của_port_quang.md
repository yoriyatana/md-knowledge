# ACX2100 _ cách cấu hình event-option để active script thu thập thông tin thu phát của port quang

1. Mô tả:

Tạo event-script để generate OID giám sát thông tin tín hiệu thu của port quang. Có thể chỉnh sửa thời gian interval theo nhu cầu (5p, 10p...)

1. Các bước thực hiện:

Load file Optic.slax lên thiết bị vào thư mục: /var/db/scripts/event/

**lab@CSG-test-tool_v3# run file list /var/db/scripts/event/**

**/var/db/scripts/event/:**

**Optic.slax**

Cấu hình event-option interval để generate SNMP OID:

**lab@CSG-test-tool_v3# show event-options**

**max-policies 5;**

**generate-event {**

**    1_hours time-interval 3600;**

**}**

**policy record-Optic {**

**    events 1_hours;**

**    then {**

**        event-script Optic.slax;**

**    }**

**}**

**event-script {**

**    file Optic.slax;**

**}**

Trong đó:

                1_hours: name event

                Time-interval 3600: Sau 1 giờ script sẽ được kích hoạt.

            OID dùng để get thông tin : 1.3.6.1.4.1.2636.3.47.1.1.5.1.2

                **lab@CSG-test-tool_v3# run show snmp mib walk 1.3.6.1.4.1.2636.3.47.1.1.5.1.2       �**�

**jnxUtilStringValue.79.112.116.105.99.46.103.101.45.49.47.50.47.49 = test optics-;-OK/Rx:-5.11/Tx:-5.30/NMS-WarnThreshold:-21.09/NMS-AlarmThreshold:-24.09**
