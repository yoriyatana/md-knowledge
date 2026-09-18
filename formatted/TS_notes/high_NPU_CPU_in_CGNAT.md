# high NPU CPU in CGNAT

show interfaces mams-* | match "mams-|rate"

- --

> start shell

cli -c 'show services sessions interface mams-8/3/0' | grep Forward | awk '{if (int($7) > 1000000) print}'

cli -c 'show services sessions interface mams-8/3/0' | grep Forward | awk '{if (int($7) > 100000) print}'

cli -c 'show services sessions interface mams-8/0/0' | grep Forward | awk '{if (int($7) > 1000000) print}'

cli -c 'show services sessions interface mams-8/0/0' | grep Forward | awk '{if (int($7) > 100000) print}'
