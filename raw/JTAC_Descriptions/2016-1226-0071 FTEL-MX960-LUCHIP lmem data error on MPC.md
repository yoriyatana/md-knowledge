# 2016-1226-0071 FTEL-MX960-LUCHIP lmem data error on MPC

2016-1226-0071 FTEL-MX960-LUCHIP lmem data error on MPC

The fixed release of PR614054 is 11.4R1, does it mean release 12.3R8.7 is also fixed too?

JTAC:-correct

and if errors are repeated within a zone, it is taken offline  Can you explain it more detail? What is a zone? How impact if taking a zone offline suddenly and how can we prevent this situation might happen?

JTAC:-Zone is internal to the Card, Inside the fpc for LU there are multiple PPE(packet processing Engines ) which has different threads ,these threads are allocated to  a zone.

Zone is the part where one packet will be there until its processing is complete.

As there are multiple zones usually offline one zone does not cause impact And further analysis can be done form logs.
