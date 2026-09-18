# multiple Junos-cli commands at the same time

Please try this construct - it works for me:

start shell command "cli -c 'show interfaces et-0/0/[0-1] extensive | match \"physical|bytes  :\" | no-more; show interfaces et-0/0/3[2-5] extensive | match \"physical|bytes  :\"| no-more; show interfaces ae\* extensive | match \"physical|bytes  :\"| no-more'"
