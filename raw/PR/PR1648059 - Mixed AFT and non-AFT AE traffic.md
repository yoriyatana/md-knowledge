# PR1648059 - Mixed AFT and non-AFT AE traffic

Việc bundle các port thuộc các loại chipset khác nhau AFT (MPC10E / MPC11E) và non-AFT (ví dụ Trio-Chip set: MPC2-3-4-5-6-7E) sẽ dẫn đến một số hành xử không mong muốn, đặc biệt là load-balance traffic.

# 1. PR1648059

This issue might be seen if the following conditions are met:

\* MX equipped with AFT FPC (e.g. MPC10E/11E) and non-AFT FPC (e.g. MPC5E)

\* AE configured with child links from both AFT and non-AFT FPCs

\* Traffic ingress via legacy cards

\* Traffic egress on the AE interface via IRB
