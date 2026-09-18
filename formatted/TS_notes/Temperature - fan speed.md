# Temperature - fan speed

Here is the final answer from dev is with the fix of both the PR’s 1199447 and 1316192

For MPC1/2/3/4 & MPC2/3-NG - fan speed control algorithms are based on intake/exhaust A/B temperature

For MPC5/6/7/8/9- fan speed control algorithms are based on the XL,MX, XQ Temperature sensors along with intake/exhaust A/B.

Above is applied for all MX- MX240/MX480/MX960/MX2008/MX2010/MX2020.

- --

t: Max temperature {intake sensor, exhaust sensor} for MPC type-1/2/3/4.

Max Temperature of {intake Sensor, exhaust Sensor, ASIC sensors} for MPC5/6/7/8/9

- --

![](image/8a2965d00fb02e82b9268e8856cb4422)![](image/141998593efc1a2ee6770a007371c981)![](image/ee15a22f1dac51c03ceec1187d96239e)

{master}

pmgatepro@HHT9602BRA27\_RE0> show chassis pic fpc-slot 8 pic-slot 1

FPC slot 8, PIC slot 1 information:

Type                            1X100GE CFP2 OTN

```text
State                            Online
```

PIC version                  0.0

Uptime                        96 days, 9 hours, 30 minutes, 51 seconds

PIC port information:

Fiber                    Xcvr vendor      Wave-    Xcvr        JNPR

Port Cable type        type  Xcvr vendor        part number      length  Firmware    Rev

0    100GBASE LR4      SM    FINISAR CORP.      FTLC1121RDNL-J3  1310 nm  1.5          REV 01

NPC2(vty)# show max6697 addresses

max6697\_count = 2

I2C Device Name                : Group  Device

- ---------------------------------------------

WSURF XL\_XQ                    : 0x49  0x4d

WSURF XM                      : 0x48  0x1c

max6697\_count = 2

I2C Device Name                : Group  Device

- ---------------------------------------------

WSURF XL\_XQ                    : 0x49  0x4d

WSURF XM                      : 0x48  0x1c

NPC2(vty)# show max6697 0x48  0x1c

WSURF XM (group 0x48, device 0x1c(sad)

Channel(Chip)    Int Temp/Thresh(IH)  Ext Temp/Thresh(EH)/Thresh(EO)  Config(1/2/3)      Status(1/2/3)

1  XM 0                48/75                  64/100/115              0x28/0x00/0x00    0x00/0x00/0x70

2  XM 1                48/75                  47/100/N/A              0x28/0x00/0x00    0x00/0x00/0x70

3  PLX PCIe Switch      48/75                  91/100/N/A              0x28/0x00/0x00    0x00/0x00/0x70
