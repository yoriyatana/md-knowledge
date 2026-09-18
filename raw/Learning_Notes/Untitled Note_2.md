# Untitled Note

as-path-expand vs as-path-prepend

as-path-prepend là nó thêm as vào trước khi thực hiện thêm as của nó, còn as-path-expand là ngược lại nó thêm as vào sau khi đã thêm as của nó vào cái AS-path.

local-as 123 prepend 234: 234 123 345 I

local-as 123 expand 234 : 123 234 345 I

- Route được quảng bá:

![](image/57c027dead16dbc2ac9b41bded59b51d.png)

- as-path-prepend: prepends given AS number after performing default own AS prepend. Recommended to use own AS only.

- Adverstise side: **local-AS 1**

![](image/39339a35cfd838d1ef2389165ed50372.png)

- Receive side:

![](image/2806ccffa77b1c8a241dbab4e195fd13.png)

- as-path-expand: prepends given AS number before performing default own AS prepend.

- Adverstise side:  local-AS 1

![](image/a231dfd34d4cc7c1434d14ba2c35605c.png)

- Receive side:

![](image/74cd80c4be57f1143d251e7624d2dc9e.png)
