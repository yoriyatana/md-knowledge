# Track specific packet sizes or specific MAC

Start shell pfe network fpc4

show mtip-cge summary

show mtip-cge 2 statistics

clear mtip-cge 2 statistics

MX204 - mtip

SMPC0(BDG-MP-01-07 vty)# show mtip-chmac summary    

 ID mtip_chmac name        FPC PIC Port Chan ASIC inst link ifd            (ptr)

--- ---------------------- --- --- ---- ---- ---- ---- ---- -------------- --------

  1 mtip_chmac.0.0.60:0    0  0  60    0    0    0  0                  eb612570

  2 mtip_chmac.0.0.2:0      0  0    2    0    0    0  0  et-0/0/2      eb612270

  3 mtip_chmac.0.0.3:0      0  0    3    0    0    0  0  et-0/0/3      eb6121b0

SMPC0(BDG-MP-01-07 vty)# show mtip-cmac summary                          

 ID mtip_cmac name        FPC PIC Port Chan ASIC Inst ifd                  (ptr)

--- ---------------------- --- --- ---- ---- ---- ---- ------------------ --------

  1 mtip_cmac.0.0.60        0  0  60  0    0  0                    eb6124b0

  2 mtip_cmac.0.0.0        0  0    0  0    0  0    et-0/0/0        eb6123f0

  3 mtip_cmac.0.0.1        0  0    1  0    0  0    et-0/0/1        eb612330

SMPC0(BDG-MP-01-07 vty)# show mtip-chmac 2 statistics

SMPC0(BDG-MP-01-07 vty)# show mtip-cmac 1 statistics

show mtip-chmac summary    

show mtip-cmac summary                          

show mtip-chmac 2 statistics

show mtip-cmac 1 statistics
