# Lệnh off laser mode shell <<< dùng flap link

xe-1/0/1 {

description looped-2;

hold-time up 2000 down 300 alternative;

framing {

wan-phy;

}

sonet-options {

trigger {

ber-sd {

hold-time up 3000 down 1000;

}

}

}

}

[ February 24, 2023 16:56 ] ⁨Hung Le⁩: test ifd xe-1/0/0 laser off 50

Dec  4 20:35:06.652 LOG: Debug] xe-1/0/0: turn off laser for 50 msec, then turn on laser

RMPC1(jtac-mx240-r2036-re0 vty)#  test ifd xe-1/0/0 laser off 50

Kết quả test trên lab

SMPC platform (1750Mhz Intel(R) Atom(TM) CPU processor, 3168MB memory, 8192KB flash)

SMPC4(MX960-01\_RE1 vty)# test ifd xe-4/1/1 laser off 5000

[Jul  5 08:58:36.115 LOG: Debug] xe-4/1/1: turn off laser for 5000 msec, then turn on laser

[Jul  5 08:58:36.619 LOG: Info] ifp xe-4/1/1 ifd\_mdown: 186954054 ms

[Jul  5 08:58:40.955 LOG: Notice] SMIC(4/1) link 1 SFP laser bias current low  alarm set

[Jul  5 08:58:40.955 LOG: Notice] SMIC(4/1) link 1 SFP output power low  alarm set

[Jul  5 08:58:40.955 LOG: Notice] SMIC(4/1) link 1 SFP laser bias current low  warning set

[Jul  5 08:58:40.955 LOG: Notice] SMIC(4/1) link 1 SFP output power low  warning set

[Jul  5 08:58:47.014 LOG: Notice] SMIC(4/1) link 1 SFP laser bias current low  alarm cleared

[Jul  5 08:58:47.014 LOG: Notice] SMIC(4/1) link 1 SFP output power low  alarm cleared

[Jul  5 08:58:47.014 LOG: Notice] SMIC(4/1) link 1 SFP laser bias current low  warning cleared

[Jul  5 08:58:47.014 LOG: Notice] SMIC(4/1) link 1 SFP output power low  warning cleared

test cfp  laser  off

test cfp  laser  on

[ July 5, 2023 16:01 ] ⁨SVT.Anh.VT⁩: lệnh để up down cổng ngay lập tức dưới shell anh em nhé

ifconfig ge-0/0/3 down

ifconfig ge-0/0/3 up
