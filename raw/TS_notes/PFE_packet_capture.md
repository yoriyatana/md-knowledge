# PFE packet capture

# sh ttrace

# bringup ttrace 0 delete

# test lkup-asic rebalance periodic disable

##############worked##########

# sh ttrace

# test lkup-asic rebalance disable

# bringup ttrace 0 delete

# bringup ttrace 1 delete    

# bringup ttrace 2 delete    

# bringup ttrace 3 delete    

# test lkup-asic rebalance reenable

# sh ttrace    

# test jnh 0 packet-via-dmem enable 

# test jnh 0 packet-via-dmem capture 0x3 0xc0a80303c0a80403 32     

# test jnh 0 packet-via-dmem capture 0

# test jnh 0 packet-via-dmem dump

# test jnh 0 packet-via-dmem capture 0x3 0xc0a80303c0a80403 40     

# test jnh 0 packet-via-dmem capture 0

# test jnh 0 packet-via-dmem dump

# test jnh 0 packet-via-dmem capture 0x3 0xc0a80303 32             

# test jnh 0 packet-via-dmem capture 0

# test jnh 0 packet-via-dmem dump

# test jnh 0 packet-via-dmem capture 0x3 0xc0a80303c0a80403 60     

# test jnh 0 packet-via-dmem capture 0

# test jnh 0 packet-via-dmem dump

# test jnh 0 packet-via-dmem capture 0x3 0xc0a80303c0a80403 60     

# test jnh 0 packet-via-dmem capture 0

# test jnh 0 packet-via-dmem disable 

# exit

######################

# show jnh exceptions-trace

########################

# test jnh 0 packet-via-dmem inject trace
