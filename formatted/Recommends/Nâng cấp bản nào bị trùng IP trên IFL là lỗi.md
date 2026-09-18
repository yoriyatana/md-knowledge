# Nâng cấp bản nào bị trùng IP trên IFL là lỗi

em có nhớ 1 case là với các version 14. trở về trước cho phép cấu hình trùng địa chỉ IP (vô tình hoặc cố tình cấu hình trùng IP)

sau đó với version 15.x, 16.x không cho phép cấu hình trùng IP -> commit sẽ báo lỗi.

```text
do đó khi nâng cấp version từ 14. lên 15. phải bắt buộc nâng cấp mà no-validate cấu hình (do khác BSD)... sẽ xảy ra trường hợp là system nhận được version mới, nhưng sẽ stuck ở quá trình boot lên ( do quá trình boot sẽ load cấu hình -> trùng IP -> failed)
```

nên khi nâng cấp từ 14. lên 15., 16. phải lưu ý vụ trùng địa chỉ IP

hoặc phải nâng cấp bằng USB (install media)
