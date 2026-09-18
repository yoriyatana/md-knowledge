# SCB

MX240, MX480, MX960:

- SCB

- SCBE

- SCBE2

- SCBE3

MX240 & MX480:

- Dùng tối đa 2 card SCB trên mỗi box. Về mặt logical, mỗi SCB sẽ có 4 fabric plane.

- Redundancy:

+ SCB/SCBE/SCBE2: 1+1 (4 plane active - 4 plane spare)

+ SCBE3: <https://www.juniper.net/documentation/us/en/hardware/mx960/topics/concept/scbe3-desc.html>

MX960: (SCB/SCBE/SCBE2/SCBE3)

- Dùng tối đa 3 card SCB trên mỗi box. Về mặt logical, mỗi SCB sẽ có 2 fabric plane.

```text
Redundancy: 2+1 hoặc 3+0
```
