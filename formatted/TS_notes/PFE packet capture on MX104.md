# PFE packet capture on MX104

```text
% ssh test2nqe31.dk|tee output.txt
```

```text
fisakytt@test2nqe31-re1.dk> start shell pfe network afeb0
```

AFEB platform (1000Mhz QorIQ P2020 processor, 2048MB memory, 512KB flash)

MX104-ABB-0(test2nqe31-re1.dk vty)# test jnh 0 packet-via-dmem enable

MX104-ABB-0(test2nqe31-re1.dk vty)# test jnh 0 packet-via-dmem capture 0x3 0x0a0b0c0d

MX104-ABB-0(test2nqe31-re1.dk vty)# test jnh 0 packet-via-dmem capture 0x0

MX104-ABB-0(test2nqe31-re1.dk vty)# test jnh 0 packet-via-dmem dump

MX104-ABB-0(test2nqe31-re1.dk vty)# test jnh 0 packet-via-dmem disable
