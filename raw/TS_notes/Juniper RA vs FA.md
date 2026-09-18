# Juniper RA vs FA

Khác biệt giữa FA (Failure Analysis) & RA (Repair Analysis) - ngoài đề cập ở JTAC User Guide đề cập thì hôm qua anh có hỏi thêm a.Đăng JuniperVN thì có thêm 1 số ý bổ sung thêm chỗ khác biệt giữa RA & FA để rõ hơn, cụ thể:

- Nếu RMA mà không có flag RA hoặc FA thì khi hàng lỗi gửi về nhà máy Juniper, họ sẽ sửa chữa và không báo kết quả sửa chữa cho mình biết. Như vậy trong trường hợp này mình chỉ biết 1 cách chung chung là FRU đó nó bị lỗi hardware - chứ không thể biết chính xác là component nào bên trong của FRU đó bị lỗi/hỏng. Nếu muốn biết chính xác FRU đó bị lỗi gì / ở thành phần nào/... thì khi mở RMA mọi nguoi cần nhờ JTAC là đánh dấu RA hoặc FA khi JTAC mở RMA ticket (flag RA/FA).

- Nếu RMA có flag RA thì hàng sau khi đc sửa chữa sẽ được ghi nhận lại sửa cái gì/thành phần nào và báo cáo lại việc sửa chữa này lại nguoi yêu cầu

- RMA có flag FA thì cũng tương tự như RA, tuy nhiên có một số khác biệt sau:

+ FA sẽ được phân tích sâu hơn bởi đội developing engineer - hw. Nếu thiết bị đã được sửa chữa trước đó rồi thì không process FA đc nữa.

+ FA sẽ phải đc approve bởi HQ do có nhiều điều kiện ràng buộc khác - cũng như chi phí cho FA lớn hơn nhiều so với RA.

+ FA sẽ không đc approve nếu sản phẩm đó đc ra mắt lần đầu cách đây 5 năm (Rule này là quy định chung - Một số truờng hợp nếu 1 sản phẩm ra đời đã quá 5 năm thì vẫn có ngoại lệ như case lỗi PEM trên MX960 thời gian qua ở dự án VNPT-NET PE/BNG & Mobifone MLMT)

Với lỗi xảy ra trên nhiều module:

- RA sẽ xác nhận là khớp với FA đã biết

- FA cho trường hợp chưa biết

Vậy khi mở nên flag RA hay FA? --> Tùy trường hợp, nếu tỉ lệ lỗi xảy ra nhiều thì cần báo các anh JuniperVN để quyết định sẽ RA hay FA. Trong trờng hợp yêu cầu RA thì cần note với JTAC là RA không có kết quả thì cần tự động chuyển qua FA để tránh trường hợp sau này khi nhận kết quả báo không có kết quả RA thì lúc đó mình muốn yêu cầu làm FA thì lại hiện trạng lỗi không còn đc giữ để thực hiện FA.

---> IMPORTANT NOTE: Khi RMA có flag RA/FA thì mình sẽ yêu cầu JTAC xem RA/FA đó đã đc approve chưa? Được Juniper approve rồi thì mình mới gửi hàng lỗi đi nhé.

---

• \*Repair Analysis\*—Routine repair correcting the cause

of a failure and verification of functionality. Repair

Analysis involves repair, test, and verification of a

reported failure, then repair data uploaded into

Juniper Networks Service Request tracking system. If

you and the JTAC engineer agree that RA is not

sufficient in providing an explanation of the failure, we

can perform Failure Analysis (FA) when required.

• \*Failure Analysis\*—Systematic analysis of a failure

symptom to identify the underlying root cause,

facilitating corrective action. FA involves simulation of

a symptom and reported environment, root cause

analysis of a failure, and corrective action

implementation. Root cause analysis involves

destructive testing of the hardware. Time frames for

analysis posting from date of receipt at Juniper Repair

Centers are:

- RA flagged: 30 calendar days

- FA interim results: 15 calendar days (with

further FA timelines to be determined

thereafter)
