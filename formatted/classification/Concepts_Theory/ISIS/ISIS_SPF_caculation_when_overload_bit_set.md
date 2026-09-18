# ISIS SPF caculation when overload bit set

![Attachment-6.png](image/Attachment-6.png)

- --

* *Part 1: Normal SPF Calculation Example**

- --

* *SPF Calculation Example: Part 1**

- In the following slides, an example SPF calculation is displayed. This graphic shows the beginning state of the network including the routers involved, the configured link metrics, and the LSDB. The network and the LSDB have recently converged and the local router, RTR-A, is running an SPF calculation to determine the shortest path to each node in the network.

```
root@R1_RTR-A> show log debug-isis
Jan 26 18:10:20.501174 L2 SPF trigger: Purging LSP R1_RTR-A.00-00
Jan 26 18:10:20.501234 SPF scheduled in 0.200000s    >>> delay (ms): minimum wait before the detection of an update and starting the SPF run (by default 200ms)
Jan 26 18:10:20.501299 SPF scheduled in 0.199933s
Jan 26 18:10:20.501310 SPF scheduled in 0.199921s
Jan 26 18:10:20.501319 SPF scheduled in 0.199912s
Jan 26 18:10:20.501931 SPF scheduled in 0.199912s
Jan 26 18:10:20.501938 SPF scheduled in 0.199912s
Jan 26 18:10:20.532733 SPF scheduled in 0.168511s
Jan 26 18:10:20.542114 SPF scheduled in 0.159126s
Jan 26 18:10:20.545474 SPF scheduled in 0.155764s
Jan 26 18:10:20.617032 SPF scheduled in 0.084216s
```

![Attachment-1.png](image/Attachment-1.png)

* *SPF Calculation Example: Part 2**

- RTR-A begins by moving its own local database tuple (A, A, 0) into the candidate database.
    - The total cost from the neighbor ID to the root is calculated, which results in a 0 value. In other words, RTR-A is directly connected to itself!
- The lowest, and only, tuple in the candidate database is moved to the tree database and RTR-A places itself on the network map.

```
Jan 26 18:10:20.712442 Running L2 Full SPF
Jan 26 18:10:20.712482   Initializing LSP R1_RTR-A.00-00
Jan 26 18:10:20.712487     Adding candidate, metric 0
Jan 26 18:10:20.712491   Initializing LSP R2_RTR-C.00-00
Jan 26 18:10:20.712495   Initializing LSP R3_RTR-D.00-00
Jan 26 18:10:20.712499   Initializing LSP R4_RTR-B.00-00
Jan 26 18:10:20.712508     Create direct next hops for neighbor R2_RTR-C
Jan 26 18:10:20.712513       Next hop with improved metric 2: R2_RTR-C.00-00
Jan 26 18:10:20.712553         numberred IFA 10.1.2.2 used as next hop for R2_RTR-C
Jan 26 18:10:20.712615         No matching IFA for next hop R2_RTR-C, count 0
Jan 26 18:10:20.712622     Create direct next hops for neighbor R4_RTR-B
Jan 26 18:10:20.712627       Next hop with improved metric 1: R4_RTR-B.00-00
Jan 26 18:10:20.712634         numberred IFA 10.1.4.4 used as next hop for R4_RTR-B
Jan 26 18:10:20.712639         No matching IFA for next hop R4_RTR-B, count 0
Jan 26 18:10:20.712658 L2 SPF initialization complete: 0.000196s
Jan 26 18:10:20.712666     Considering R1_RTR-A.00-00, metric 0, no next hop
```

![Attachment.png](image/Attachment.png)

* *SPF Calculation Example: Part 3**

- All tuples from the most recent node added to the tree database are now added to the candidate database.
    - Because RTR-A is the most recent entry to the tree database, all of RTR-A’s tuples are moved from the LSDB into the candidate database.
- All known nodes in the tree database are removed from the candidate, of which there are none.
    - (For example, if B were already in the tree database, the tuple (A, B,1) would be eliminated.)
- The cost to each neighbor ID from the root is then calculated.
    - It costs RTR-A 0 to reach itself and1to reach RTR-B, so the total cost to RTR-B is 1.
    - The same calculation is done for RTR-C, and the total cost of 2 is placed into the candidate database.

```
Jan 26 18:10:20.712670     Node R1_RTR-A.00-00 at metric 0
Jan 26 18:10:20.712674       Neighbor R4_RTR-B.00, metric 1
Jan 26 18:10:20.712677         Bidirectional adjacency, new metric 1
Jan 26 18:10:20.712681         Set candidate R4_RTR-B.00-00 metric to 1
Jan 26 18:10:20.712685       Neighbor R2_RTR-C.00, metric 2
Jan 26 18:10:20.712688         Bidirectional adjacency, new metric 2
Jan 26 18:10:20.712719         Set candidate R2_RTR-C.00-00 metric to 2
```

- The lowest cost tuple in the candidate database, (A, B,1), is now moved to the tree database, and RTR-B is placed on the network map.

```
Jan 26 18:10:20.712728     Considering R4_RTR-B.00-00, metric 1, with next hop
```

- The candidate database is not empty, so the algorithm continues.

![Attachment-4.png](image/Attachment-4.png)

* *SPF Calculation Example: Part 4**

- RTR-B is the most recent entry to the tree database, so all RTR-B’s tuples are moved from the LSDB into the candidate database.
- All known nodes in the tree database are then removed from the candidate.
    - Thus, the (B, A, 3) tuple is removed because RTR-A already has the shortest path to RTR-A.

```
Jan 26 18:10:20.712732     Node R4_RTR-B.00-00 at metric 1
Jan 26 18:10:20.712735       Neighbor R1_RTR-A.00, metric 3
Jan 26 18:10:20.712738         Suboptimal path, metric 4, current metric 0
```

- The cost to each neighbor ID from the root is then calculated.
    - It costs RTR-B 3 to reach RTR-D, and it costs 1 to reach RTR-B from the root.
    - So the total cost to reach RTR-D from the root through RTR-B is 4.

```
Jan 26 18:10:20.712742       Neighbor R3_RTR-D.00, metric 3
Jan 26 18:10:20.712745         Bidirectional adjacency, new metric 4
Jan 26 18:10:20.712748         Set candidate R3_RTR-D.00-00 metric to 4
```

- The lowest cost tuple in the candidate database, (A, C, 2), is now moved over to the tree database, and RTR-C is placed on the network map.

```
Jan 26 18:10:20.712752     Considering R2_RTR-C.00-00, metric 2, with next hop
```

- The candidate database is not empty, so the algorithm continues.

![Attachment-5.png](image/Attachment-5.png)

* *SPF Calculation Example: Part 5**

- Because RTR-C is the most recent entry to the tree database, its tuples are moved from the LSDB into the candidate database.
- All known nodes in the tree database are then removed from the candidate.
    - Thus, the (C, A, 4) tuple is removed because RTR-A already has the shortest path to RTR-A.

```
Jan 26 18:10:20.712756     Node R2_RTR-C.00-00 at metric 2
Jan 26 18:10:20.712765       Neighbor R1_RTR-A.00, metric 4
Jan 26 18:10:20.712768         Suboptimal path, metric 6, current metric 0
```

- The cost to each neighbor ID from the root is then calculated.
    - It costs RTR-C 4 to reach RTR-D, and it costs 2 to reach RTR-C from the root.
    - So the total cost to reach RTR-D through RTR-C is 6.

```
Jan 26 18:10:20.712759       Neighbor R3_RTR-D.00, metric 4
Jan 26 18:10:20.712762         Suboptimal path, metric 6, current metric 4
```

- The lowest cost tuple in the candidate database, (B, D, 3), is moved to the tree database, and RTR-D is placed on the network map.

```
Jan 26 18:10:20.712772     Considering R3_RTR-D.00-00, metric 4, with next hop
```

- The candidate database is not empty, so the algorithm continues.

![Attachment-2.png](image/Attachment-2.png)

* *SPF Calculation Example: Part 6**

- RTR-D, through its link to RTR-B, is the most recent entry to the tree database. Therefore, its tuples are moved from the LSDB into the candidate database.
- All known nodes in the tree database are then removed from the candidate.
    - Thus, the (C, D, 4),(D, B,1), and (D, C, 2) tuples are removed because RTR-A already has paths to RTR-B, RTR-C, and RTR-D.
    - The candidate database is now empty of all tuples, so the algorithm stops.

```
Jan 26 18:10:20.712775     Node R3_RTR-D.00-00 at metric 4
Jan 26 18:10:20.712779       Neighbor R2_RTR-C.00, metric 2
Jan 26 18:10:20.712781         Suboptimal path, metric 6, current metric 2
Jan 26 18:10:20.712784       Neighbor R4_RTR-B.00, metric 1
Jan 26 18:10:20.712787         Suboptimal path, metric 5, current metric 1

Jan 26 18:10:20.712792 L2 SPF primary graph processing complete: 0.000135s
Jan 26 18:10:20.712799 L2 SPF multiarea postprocessing complete: 0.000007s
```

- RTR-A now has a complete network map built with the total cost to each node calculated. This information is then passed to the routing table for its use.

```
Jan 26 18:10:20.712823 Didn't alloc session id buf - count zero in spfinfo 0x964c17c!
Jan 26 18:10:20.712835   Cannot add route 10.1.1.1/32 in PPM msg (No sessid buffer)
Jan 26 18:10:20.712840   Cannot add route 10.1.2.0/24 in PPM msg (No sessid buffer)
Jan 26 18:10:20.712844   Cannot add route 10.1.4.0/24 in PPM msg (No sessid buffer)
Jan 26 18:10:20.712855   Cannot add route 2402:800::/32 in PPM msg (No sessid buffer)
Jan 26 18:10:20.712858 Enqueuing 0 session IDs in Session ID Down msg
Jan 26 18:10:20.712873 Not allocating Session ID Down msg (count=0, buffer=0x0)
Jan 26 18:10:20.712878 L2 SPF RIB postprocessing complete: 0.000079s
Jan 26 18:10:20.712884 Completed L2 Full SPF in 0.000422s cumulative time
Jan 26 18:10:20.712993 L2 SPF updated 0 routes (0 adds, 0 deletes, 0 changes, 0 fails) in 0.000090s
```

![Attachment-3.png](image/Attachment-3.png)

* *SPF traceoption on R1 - Full log**

```
root@R1_RTR-A> show log debug-isis
Jan 26 18:10:09 R1_RTR-A clear-log[3827]: logfile cleared
Jan 26 18:10:20.501174 L2 SPF trigger: Purging LSP R1_RTR-A.00-00
Jan 26 18:10:20.501234 SPF scheduled in 0.200000s
Jan 26 18:10:20.501299 SPF scheduled in 0.199933s
Jan 26 18:10:20.501310 SPF scheduled in 0.199921s
Jan 26 18:10:20.501319 SPF scheduled in 0.199912s
Jan 26 18:10:20.501931 SPF scheduled in 0.199912s
Jan 26 18:10:20.501938 SPF scheduled in 0.199912s
Jan 26 18:10:20.532733 SPF scheduled in 0.168511s
Jan 26 18:10:20.542114 SPF scheduled in 0.159126s
Jan 26 18:10:20.545474 SPF scheduled in 0.155764s
Jan 26 18:10:20.617032 SPF scheduled in 0.084216s
Jan 26 18:10:20.712442 Running L2 Full SPF
Jan 26 18:10:20.712482   Initializing LSP R1_RTR-A.00-00
Jan 26 18:10:20.712487     Adding candidate, metric 0
Jan 26 18:10:20.712491   Initializing LSP R2_RTR-C.00-00
Jan 26 18:10:20.712495   Initializing LSP R3_RTR-D.00-00
Jan 26 18:10:20.712499   Initializing LSP R4_RTR-B.00-00
Jan 26 18:10:20.712508     Create direct next hops for neighbor R2_RTR-C
Jan 26 18:10:20.712513       Next hop with improved metric 2: R2_RTR-C.00-00
Jan 26 18:10:20.712553         numberred IFA 10.1.2.2 used as next hop for R2_RTR-C
Jan 26 18:10:20.712615         No matching IFA for next hop R2_RTR-C, count 0
Jan 26 18:10:20.712622     Create direct next hops for neighbor R4_RTR-B
Jan 26 18:10:20.712627       Next hop with improved metric 1: R4_RTR-B.00-00
Jan 26 18:10:20.712634         numberred IFA 10.1.4.4 used as next hop for R4_RTR-B
Jan 26 18:10:20.712639         No matching IFA for next hop R4_RTR-B, count 0
Jan 26 18:10:20.712658 L2 SPF initialization complete: 0.000196s
Jan 26 18:10:20.712666     Considering R1_RTR-A.00-00, metric 0, no next hop
Jan 26 18:10:20.712670     Node R1_RTR-A.00-00 at metric 0
Jan 26 18:10:20.712674       Neighbor R4_RTR-B.00, metric 1
Jan 26 18:10:20.712677         Bidirectional adjacency, new metric 1
Jan 26 18:10:20.712681         Set candidate R4_RTR-B.00-00 metric to 1
Jan 26 18:10:20.712685       Neighbor R2_RTR-C.00, metric 2
Jan 26 18:10:20.712688         Bidirectional adjacency, new metric 2
Jan 26 18:10:20.712719         Set candidate R2_RTR-C.00-00 metric to 2
Jan 26 18:10:20.712728     Considering R4_RTR-B.00-00, metric 1, with next hop
Jan 26 18:10:20.712732     Node R4_RTR-B.00-00 at metric 1
Jan 26 18:10:20.712735       Neighbor R1_RTR-A.00, metric 3
Jan 26 18:10:20.712738         Suboptimal path, metric 4, current metric 0
Jan 26 18:10:20.712742       Neighbor R3_RTR-D.00, metric 3
Jan 26 18:10:20.712745         Bidirectional adjacency, new metric 4
Jan 26 18:10:20.712748         Set candidate R3_RTR-D.00-00 metric to 4
Jan 26 18:10:20.712752     Considering R2_RTR-C.00-00, metric 2, with next hop
Jan 26 18:10:20.712756     Node R2_RTR-C.00-00 at metric 2
Jan 26 18:10:20.712759       Neighbor R3_RTR-D.00, metric 4
Jan 26 18:10:20.712762         Suboptimal path, metric 6, current metric 4
Jan 26 18:10:20.712765       Neighbor R1_RTR-A.00, metric 4
Jan 26 18:10:20.712768         Suboptimal path, metric 6, current metric 0
Jan 26 18:10:20.712772     Considering R3_RTR-D.00-00, metric 4, with next hop
Jan 26 18:10:20.712775     Node R3_RTR-D.00-00 at metric 4
Jan 26 18:10:20.712779       Neighbor R2_RTR-C.00, metric 2
Jan 26 18:10:20.712781         Suboptimal path, metric 6, current metric 2
Jan 26 18:10:20.712784       Neighbor R4_RTR-B.00, metric 1
Jan 26 18:10:20.712787         Suboptimal path, metric 5, current metric 1
Jan 26 18:10:20.712792 L2 SPF primary graph processing complete: 0.000135s
Jan 26 18:10:20.712799 L2 SPF multiarea postprocessing complete: 0.000007s
Jan 26 18:10:20.712823 Didn't alloc session id buf - count zero in spfinfo 0x964c17c!
Jan 26 18:10:20.712835   Cannot add route 10.1.1.1/32 in PPM msg (No sessid buffer)
Jan 26 18:10:20.712840   Cannot add route 10.1.2.0/24 in PPM msg (No sessid buffer)
Jan 26 18:10:20.712844   Cannot add route 10.1.4.0/24 in PPM msg (No sessid buffer)
Jan 26 18:10:20.712855   Cannot add route 2402:800::/32 in PPM msg (No sessid buffer)
Jan 26 18:10:20.712858 Enqueuing 0 session IDs in Session ID Down msg
Jan 26 18:10:20.712873 Not allocating Session ID Down msg (count=0, buffer=0x0)
Jan 26 18:10:20.712878 L2 SPF RIB postprocessing complete: 0.000079s
Jan 26 18:10:20.712884 Completed L2 Full SPF in 0.000422s cumulative time
Jan 26 18:10:20.712993 L2 SPF updated 0 routes (0 adds, 0 deletes, 0 changes, 0 fails) in 0.000090s
```

- --

* *Part 2: SPF Calculation Example when RTR-B set overload-bit**

- --

* *SPF Calculation Example: Part 1**

- In the following slides, an example SPF calculation is displayed. This graphic shows the beginning state of the network including the routers involved, the configured link metrics, and the LSDB. The network and the LSDB have recently converged and the local router, RTR-A, is running an SPF calculation to determine the shortest path to each node in the network.

```
root@R1_RTR-A> show log debug-isis
Jan 26 18:42:01 R1_RTR-A clear-log[4055]: logfile cleared
Jan 26 18:42:01.406113 L2 SPF trigger: Purging LSP R1_RTR-A.00-00
Jan 26 18:42:01.406154 SPF scheduled in 0.200000s    >>> delay (ms): minimum wait before the detection of an update and starting the SPF run (by default 200ms)
Jan 26 18:42:01.406223 SPF scheduled in 0.199929s
Jan 26 18:42:01.406234 SPF scheduled in 0.199916s
Jan 26 18:42:01.406246 SPF scheduled in 0.199905s
Jan 26 18:42:01.406257 SPF scheduled in 0.199905s
Jan 26 18:42:01.406261 SPF scheduled in 0.199905s
Jan 26 18:42:01.427240 SPF scheduled in 0.178915s
Jan 26 18:42:01.458430 SPF scheduled in 0.147739s
Jan 26 18:42:01.458725 SPF scheduled in 0.147432s
Jan 26 18:42:01.532778 SPF scheduled in 0.073390s
```

![Attachment-7.png](image/Attachment-7.png)

* *SPF Calculation Example: Part 2**

- RTR-A begins by moving its own local database tuple (A, A, 0) into the candidate database.
    - The total cost from the neighbor ID to the root is calculated, which results in a 0 value. In other words, RTR-A is directly connected to itself!
- The lowest, and only, tuple in the candidate database is moved to the tree database and RTR-A places itself on the network map.

```
Jan 26 18:42:01.624493 Running L2 Full SPF
Jan 26 18:42:01.624555   Initializing LSP R1_RTR-A.00-00
Jan 26 18:42:01.624566     Adding candidate, metric 0
Jan 26 18:42:01.624582   Initializing LSP R2_RTR-C.00-00
Jan 26 18:42:01.624593   Initializing LSP R3_RTR-D.00-00
Jan 26 18:42:01.624602   Initializing LSP R4_RTR-B.00-00
Jan 26 18:42:01.624620     Create direct next hops for neighbor R2_RTR-C
Jan 26 18:42:01.624632       Next hop with improved metric 2: R2_RTR-C.00-00
Jan 26 18:42:01.624698         numberred IFA 10.1.2.2 used as next hop for R2_RTR-C
Jan 26 18:42:01.624733         No matching IFA for next hop R2_RTR-C, count 0
Jan 26 18:42:01.624750     Create direct next hops for neighbor R4_RTR-B
Jan 26 18:42:01.624762       Next hop with improved metric 1: R4_RTR-B.00-00
Jan 26 18:42:01.624780         numberred IFA 10.1.4.4 used as next hop for R4_RTR-B
Jan 26 18:42:01.624793         No matching IFA for next hop R4_RTR-B, count 0
Jan 26 18:42:01.624840 L2 SPF initialization complete: 0.000310s
Jan 26 18:42:01.624859     Considering R1_RTR-A.00-00, metric 0, no next hop
```

![Attachment.png](image/Attachment.png)

* *SPF Calculation Example: Part 3**

- All tuples from the most recent node added to the tree database are now added to the candidate database.
    - Because RTR-A is the most recent entry to the tree database, all of RTR-A’s tuples are moved from the LSDB into the candidate database.
- All known nodes in the tree database are removed from the candidate, of which there are none.
    - (For example, if B were already in the tree database, the tuple (A, B,1) would be eliminated.)
- The cost to each neighbor ID from the root is then calculated.
    - It costs RTR-A 0 to reach itself and1to reach RTR-B, so the total cost to RTR-B is1.
    - The same calculation is done for RTR-C, and the total cost of 2 is placed into the candidate database.

```
Jan 26 18:42:01.624870     Node R1_RTR-A.00-00 at metric 0
Jan 26 18:42:01.624880       Neighbor R4_RTR-B.00, metric 1
Jan 26 18:42:01.624889         Bidirectional adjacency, new metric 1
Jan 26 18:42:01.624899         Set candidate R4_RTR-B.00-00 metric to 1
Jan 26 18:42:01.624910       Neighbor R2_RTR-C.00, metric 2
Jan 26 18:42:01.624917         Bidirectional adjacency, new metric 2
Jan 26 18:42:01.624949         Set candidate R2_RTR-C.00-00 metric to 2
```

- The lowest cost tuple in the candidate database, (A, B,1), is now moved to the tree database, and RTR-B is placed on the network map.

```
Jan 26 18:42:01.624970     Considering R4_RTR-B.00-00, metric 1, with next hop
```

- The LSDB is not empty, so the algorithm continues.

![Attachment-4.png](image/Attachment-4.png)

* *SPF Calculation Example: Part 4**

- RTR-B is the most recent entry to the tree database and is overloaded, so all RTR-B’s tuples are removed from the LSDB.

```
Jan 26 18:42:01.624980     Node R4_RTR-B.00-00 at metric 1
Jan 26 18:42:01.624988         Leaf is overloaded, ignoring neighbors
```

- The lowest cost tuple in the candidate database, (A, C, 2), is now moved over to the tree database, and RTR-C is placed on the network map.

```
Jan 26 18:42:01.625000     Considering R2_RTR-C.00-00, metric 2, with next hop
```

- The LSDB  is not empty, so the algorithm continues.

![Attachment-8.png](image/Attachment-8.png)

* *SPF Calculation Example: Part 5**

- Because RTR-C is the most recent entry to the tree database, its tuples are moved from the LSDB into the candidate database.
- All known nodes in the tree database are then removed from the candidate.
    - Thus, the (C, A, 4) tuple is removed because RTR-A already has the shortest path to RTR-A.

```
Jan 26 18:42:01.625009     Node R2_RTR-C.00-00 at metric 2
Jan 26 18:42:01.625046       Neighbor R1_RTR-A.00, metric 4
Jan 26 18:42:01.625054         Suboptimal path, metric 6, current metric 0
```

- The cost to each neighbor ID from the root is then calculated.
    - It costs RTR-C 4 to reach RTR-D, and it costs 2 to reach RTR-C from the root.
    - So the total cost to reach RTR-D through RTR-C is 6.

```
Jan 26 18:42:01.625019       Neighbor R3_RTR-D.00, metric 4
Jan 26 18:42:01.625027         Bidirectional adjacency, new metric 6
Jan 26 18:42:01.625037         Set candidate R3_RTR-D.00-00 metric to 6
```

- The lowest cost tuple in the candidate database, (C, D, 4), is moved to the tree database, and RTR-D is placed on the network map.

```
Jan 26 18:42:01.625065     Considering R3_RTR-D.00-00, metric 6, with next hop
```

- The LSDB is not empty, so the algorithm continues.

![Attachment-9.png](image/Attachment-9.png)

* *SPF Calculation Example: Part 6**

- RTR-D, through its link to RTR-C, is the most recent entry to the tree database. Therefore, its tuples are moved from the LSDB into the candidate database.
- All known nodes in the tree database are then removed from the candidate.
    - Thus, the (D, B,1), and (D, C, 2) tuples are removed because RTR-A already has paths to RTR-B and RTR-C.
    - The LSDB is now empty of all tuples, so the algorithm stops.

```
Jan 26 18:42:01.625074     Node R3_RTR-D.00-00 at metric 6
Jan 26 18:42:01.625083       Neighbor R2_RTR-C.00, metric 2
Jan 26 18:42:01.625091         Suboptimal path, metric 8, current metric 2
Jan 26 18:42:01.625100       Neighbor R4_RTR-B.00, metric 1
Jan 26 18:42:01.625108         Suboptimal path, metric 7, current metric 1

Jan 26 18:42:01.625122 L2 SPF primary graph processing complete: 0.000283s
Jan 26 18:42:01.625140 L2 SPF multiarea postprocessing complete: 0.000019s
```

- RTR-A now has a complete network map built with the total cost to each node calculated. This information is then passed to the routing table for its use.

```
Jan 26 18:42:01.625186 Didn't alloc session id buf - count zero in spfinfo 0x964c17c!
Jan 26 18:42:01.625215   Cannot add route 10.1.1.1/32 in PPM msg (No sessid buffer)
Jan 26 18:42:01.625228   Cannot add route 10.1.2.0/24 in PPM msg (No sessid buffer)
Jan 26 18:42:01.625241   Cannot add route 10.1.4.0/24 in PPM msg (No sessid buffer)
Jan 26 18:42:01.625267   Cannot add route 2402:800::/32 in PPM msg (No sessid buffer)
Jan 26 18:42:01.625276 Enqueuing 0 session IDs in Session ID Down msg
Jan 26 18:42:01.625290 Not allocating Session ID Down msg (count=0, buffer=0x0)
Jan 26 18:42:01.625302 L2 SPF RIB postprocessing complete: 0.000163s
Jan 26 18:42:01.625317 Completed L2 Full SPF in 0.000789s cumulative time
Jan 26 18:42:01.625540 L2 SPF updated 0 routes (0 adds, 0 deletes, 0 changes, 0 fails) in 0.000163s
```

![Attachment-10.png](image/Attachment-10.png)

* *SPF traceoption on R1 - Full log when overload-bit set**

```
root@R1_RTR-A> show log debug-isis
Jan 26 18:42:01 R1_RTR-A clear-log[4055]: logfile cleared
Jan 26 18:42:01.406113 L2 SPF trigger: Purging LSP R1_RTR-A.00-00
Jan 26 18:42:01.406154 SPF scheduled in 0.200000s
Jan 26 18:42:01.406223 SPF scheduled in 0.199929s
Jan 26 18:42:01.406234 SPF scheduled in 0.199916s
Jan 26 18:42:01.406246 SPF scheduled in 0.199905s
Jan 26 18:42:01.406257 SPF scheduled in 0.199905s
Jan 26 18:42:01.406261 SPF scheduled in 0.199905s
Jan 26 18:42:01.427240 SPF scheduled in 0.178915s
Jan 26 18:42:01.458430 SPF scheduled in 0.147739s
Jan 26 18:42:01.458725 SPF scheduled in 0.147432s
Jan 26 18:42:01.532778 SPF scheduled in 0.073390s
Jan 26 18:42:01.624493 Running L2 Full SPF
Jan 26 18:42:01.624555   Initializing LSP R1_RTR-A.00-00
Jan 26 18:42:01.624566     Adding candidate, metric 0
Jan 26 18:42:01.624582   Initializing LSP R2_RTR-C.00-00
Jan 26 18:42:01.624593   Initializing LSP R3_RTR-D.00-00
Jan 26 18:42:01.624602   Initializing LSP R4_RTR-B.00-00
Jan 26 18:42:01.624620     Create direct next hops for neighbor R2_RTR-C
Jan 26 18:42:01.624632       Next hop with improved metric 2: R2_RTR-C.00-00
Jan 26 18:42:01.624698         numberred IFA 10.1.2.2 used as next hop for R2_RTR-C
Jan 26 18:42:01.624733         No matching IFA for next hop R2_RTR-C, count 0
Jan 26 18:42:01.624750     Create direct next hops for neighbor R4_RTR-B
Jan 26 18:42:01.624762       Next hop with improved metric 1: R4_RTR-B.00-00
Jan 26 18:42:01.624780         numberred IFA 10.1.4.4 used as next hop for R4_RTR-B
Jan 26 18:42:01.624793         No matching IFA for next hop R4_RTR-B, count 0
Jan 26 18:42:01.624840 L2 SPF initialization complete: 0.000310s
Jan 26 18:42:01.624859     Considering R1_RTR-A.00-00, metric 0, no next hop
Jan 26 18:42:01.624870     Node R1_RTR-A.00-00 at metric 0
Jan 26 18:42:01.624880       Neighbor R4_RTR-B.00, metric 1
Jan 26 18:42:01.624889         Bidirectional adjacency, new metric 1
Jan 26 18:42:01.624899         Set candidate R4_RTR-B.00-00 metric to 1
Jan 26 18:42:01.624910       Neighbor R2_RTR-C.00, metric 2
Jan 26 18:42:01.624917         Bidirectional adjacency, new metric 2
Jan 26 18:42:01.624949         Set candidate R2_RTR-C.00-00 metric to 2
Jan 26 18:42:01.624970     Considering R4_RTR-B.00-00, metric 1, with next hop
Jan 26 18:42:01.624980     Node R4_RTR-B.00-00 at metric 1
Jan 26 18:42:01.624988         Leaf is overloaded, ignoring neighbors
Jan 26 18:42:01.625000     Considering R2_RTR-C.00-00, metric 2, with next hop
Jan 26 18:42:01.625009     Node R2_RTR-C.00-00 at metric 2
Jan 26 18:42:01.625019       Neighbor R3_RTR-D.00, metric 4
Jan 26 18:42:01.625027         Bidirectional adjacency, new metric 6
Jan 26 18:42:01.625037         Set candidate R3_RTR-D.00-00 metric to 6
Jan 26 18:42:01.625046       Neighbor R1_RTR-A.00, metric 4
Jan 26 18:42:01.625054         Suboptimal path, metric 6, current metric 0
Jan 26 18:42:01.625065     Considering R3_RTR-D.00-00, metric 6, with next hop
Jan 26 18:42:01.625074     Node R3_RTR-D.00-00 at metric 6
Jan 26 18:42:01.625083       Neighbor R2_RTR-C.00, metric 2
Jan 26 18:42:01.625091         Suboptimal path, metric 8, current metric 2
Jan 26 18:42:01.625100       Neighbor R4_RTR-B.00, metric 1
Jan 26 18:42:01.625108         Suboptimal path, metric 7, current metric 1
Jan 26 18:42:01.625122 L2 SPF primary graph processing complete: 0.000283s
Jan 26 18:42:01.625140 L2 SPF multiarea postprocessing complete: 0.000019s
Jan 26 18:42:01.625186 Didn't alloc session id buf - count zero in spfinfo 0x964c17c!
Jan 26 18:42:01.625215   Cannot add route 10.1.1.1/32 in PPM msg (No sessid buffer)
Jan 26 18:42:01.625228   Cannot add route 10.1.2.0/24 in PPM msg (No sessid buffer)
Jan 26 18:42:01.625241   Cannot add route 10.1.4.0/24 in PPM msg (No sessid buffer)
Jan 26 18:42:01.625267   Cannot add route 2402:800::/32 in PPM msg (No sessid buffer)
Jan 26 18:42:01.625276 Enqueuing 0 session IDs in Session ID Down msg
Jan 26 18:42:01.625290 Not allocating Session ID Down msg (count=0, buffer=0x0)
Jan 26 18:42:01.625302 L2 SPF RIB postprocessing complete: 0.000163s
Jan 26 18:42:01.625317 Completed L2 Full SPF in 0.000789s cumulative time
Jan 26 18:42:01.625540 L2 SPF updated 0 routes (0 adds, 0 deletes, 0 changes, 0 fails) in 0.000163s
```

- --

* *Part 3: SPF Calculation Example when RTR-B set overload-bit with�**�**advertise-high-metrics option**

- --

* *SPF traceoption on R1 - Full log when overload-bit set�**�**with advertise-high-metrics option**

```
[edit]
root@R4_RTR-B# set protocols isis overload advertise-high-metrics

[edit]
root@R4_RTR-B# commit
commit complete
```

```
[edit]
root@R1_RTR-A# run clear log debug-isis

[edit]
root@R1_RTR-A# run clear isis database purge

root@R1_RTR-A# run show log debug-isis
Jan 27 03:27:53 R1_RTR-A clear-log[7766]: logfile cleared
Jan 27 03:27:53.875975 L2 SPF trigger: Purging LSP R1_RTR-A.00-00
Jan 27 03:27:53.876063 SPF scheduled in 0.200000s
Jan 27 03:27:53.876200 SPF scheduled in 0.199856s
Jan 27 03:27:53.876231 SPF scheduled in 0.199824s
Jan 27 03:27:53.876259 SPF scheduled in 0.199796s
Jan 27 03:27:53.876283 SPF scheduled in 0.199796s
Jan 27 03:27:53.876293 SPF scheduled in 0.199796s
Jan 27 03:27:53.909914 SPF scheduled in 0.166144s
Jan 27 03:27:53.919083 SPF scheduled in 0.156975s
Jan 27 03:27:53.937391 SPF scheduled in 0.138669s
Jan 27 03:27:53.956006 SPF scheduled in 0.120053s
Jan 27 03:27:54.089823 Running L2 Full SPF
Jan 27 03:27:54.089900   Initializing LSP R1_RTR-A.00-00
Jan 27 03:27:54.089911     Adding candidate, metric 0
Jan 27 03:27:54.089926   Initializing LSP R2_RTR-C.00-00
Jan 27 03:27:54.089935   Initializing LSP R3_RTR-D.00-00
Jan 27 03:27:54.089944   Initializing LSP R4_RTR-B.00-00
Jan 27 03:27:54.089962     Create direct next hops for neighbor R2_RTR-C
Jan 27 03:27:54.089974       Next hop with improved metric 2: R2_RTR-C.00-00
Jan 27 03:27:54.090041         numberred IFA 10.1.2.2 used as next hop for R2_RTR-C
Jan 27 03:27:54.090075         No matching IFA for next hop R2_RTR-C, count 0
Jan 27 03:27:54.090091     Create direct next hops for neighbor R4_RTR-B
Jan 27 03:27:54.090101       Next hop with improved metric 1: R4_RTR-B.00-00
Jan 27 03:27:54.090118         numberred IFA 10.1.4.4 used as next hop for R4_RTR-B
Jan 27 03:27:54.090135         No matching IFA for next hop R4_RTR-B, count 0
Jan 27 03:27:54.090188 L2 SPF initialization complete: 0.000314s
Jan 27 03:27:54.090208     Considering R1_RTR-A.00-00, metric 0, no next hop
Jan 27 03:27:54.090218     Node R1_RTR-A.00-00 at metric 0
Jan 27 03:27:54.090229       Neighbor R4_RTR-B.00, metric 1
Jan 27 03:27:54.090236         Bidirectional adjacency, new metric 1
Jan 27 03:27:54.090246         Set candidate R4_RTR-B.00-00 metric to 1
Jan 27 03:27:54.090256       Neighbor R2_RTR-C.00, metric 2
Jan 27 03:27:54.090263         Bidirectional adjacency, new metric 2
Jan 27 03:27:54.090293         Set candidate R2_RTR-C.00-00 metric to 2
Jan 27 03:27:54.090313     Considering R4_RTR-B.00-00, metric 1, with next hop
Jan 27 03:27:54.090322     Node R4_RTR-B.00-00 at metric 1
Jan 27 03:27:54.090331       Neighbor R1_RTR-A.00, metric 63
Jan 27 03:27:54.090339         Suboptimal path, metric 64, current metric 0
Jan 27 03:27:54.090348       Neighbor R3_RTR-D.00, metric 63
Jan 27 03:27:54.090355         Bidirectional adjacency, new metric 64
Jan 27 03:27:54.090365         Set candidate R3_RTR-D.00-00 metric to 64
Jan 27 03:27:54.090375     Considering R2_RTR-C.00-00, metric 2, with next hop
Jan 27 03:27:54.090384     Node R2_RTR-C.00-00 at metric 2
Jan 27 03:27:54.090393       Neighbor R3_RTR-D.00, metric 4
Jan 27 03:27:54.090400         Bidirectional adjacency, new metric 6
Jan 27 03:27:54.090409         Set candidate R3_RTR-D.00-00 metric to 6
Jan 27 03:27:54.090418       Neighbor R1_RTR-A.00, metric 4
Jan 27 03:27:54.090425         Suboptimal path, metric 6, current metric 0
Jan 27 03:27:54.090435     Considering R3_RTR-D.00-00, metric 6, with next hop
Jan 27 03:27:54.090444     Node R3_RTR-D.00-00 at metric 6
Jan 27 03:27:54.090452       Neighbor R2_RTR-C.00, metric 2
Jan 27 03:27:54.090460         Suboptimal path, metric 8, current metric 2
Jan 27 03:27:54.090468       Neighbor R4_RTR-B.00, metric 1
Jan 27 03:27:54.090475         Suboptimal path, metric 7, current metric 1
Jan 27 03:27:54.090488 L2 SPF primary graph processing complete: 0.000302s
Jan 27 03:27:54.090505 L2 SPF multiarea postprocessing complete: 0.000017s
Jan 27 03:27:54.090551 Didn't alloc session id buf - count zero in spfinfo 0x964c17c!
Jan 27 03:27:54.090579   Cannot add route 10.1.1.1/32 in PPM msg (No sessid buffer)
Jan 27 03:27:54.090591   Cannot add route 10.1.2.0/24 in PPM msg (No sessid buffer)
Jan 27 03:27:54.090602   Cannot add route 10.1.4.0/24 in PPM msg (No sessid buffer)
Jan 27 03:27:54.090627   Cannot add route 2402:800::/32 in PPM msg (No sessid buffer)
Jan 27 03:27:54.090647 Enqueuing 0 session IDs in Session ID Down msg
Jan 27 03:27:54.090661 Not allocating Session ID Down msg (count=0, buffer=0x0)
Jan 27 03:27:54.090673 L2 SPF RIB postprocessing complete: 0.000169s
Jan 27 03:27:54.090687 Completed L2 Full SPF in 0.000816s cumulative time
Jan 27 03:27:54.090925 L2 SPF updated 0 routes (0 adds, 0 deletes, 0 changes, 0 fails) in 0.000189s
```

```
[edit]
root@R1_RTR-A# run show isis database detail
IS-IS level 1 link-state database:

IS-IS level 2 link-state database:

R1_RTR-A.00-00 Sequence: 0x34, Checksum: 0xb8c7, Lifetime: 563 secs
   IS neighbor: R2_RTR-C.00                   Metric:        2
   IS neighbor: R4_RTR-B.00                   Metric:        1
   IP prefix: 10.1.1.1/32                     Metric:        0 Internal Up
   IP prefix: 10.1.2.0/24                     Metric:        2 Internal Up
   IP prefix: 10.1.4.0/24                     Metric:        1 Internal Up

R2_RTR-C.00-00 Sequence: 0x35, Checksum: 0x1039, Lifetime: 561 secs
   IS neighbor: R1_RTR-A.00                   Metric:        4
   IS neighbor: R3_RTR-D.00                   Metric:        4
   IP prefix: 10.1.2.0/24                     Metric:        4 Internal Up
   IP prefix: 10.2.2.2/32                     Metric:        0 Internal Up
   IP prefix: 10.2.3.0/24                     Metric:        4 Internal Up
   V6 prefix: 2402:800::/32                   Metric:        4 Internal Up

R3_RTR-D.00-00 Sequence: 0x33, Checksum: 0x73b8, Lifetime: 560 secs
   IS neighbor: R2_RTR-C.00                   Metric:        2
   IS neighbor: R4_RTR-B.00                   Metric:        1
   IP prefix: 10.2.3.0/24                     Metric:        2 Internal Up
   IP prefix: 10.3.3.3/32                     Metric:        0 Internal Up
   IP prefix: 10.3.4.0/24                     Metric:        1 Internal Up

R4_RTR-B.00-00 Sequence: 0x36, Checksum: 0x4413, Lifetime: 561 secs
   IS neighbor: R1_RTR-A.00                   Metric:       63
   IS neighbor: R3_RTR-D.00                   Metric:       63
   IP prefix: 10.1.4.0/24                     Metric:        3 Internal Up
   IP prefix: 10.3.4.0/24                     Metric:        3 Internal Up
   IP prefix: 10.4.4.4/32                     Metric:        0 Internal Up
```

```
[edit]
root@R1_RTR-A# run show isis spf results
IS-IS level 1 SPF results:
  0 nodes

IS-IS level 2 SPF results:
Node             Metric     Interface        NH   Via             SNPA
R3_RTR-D.00      6          ge-0/0/0.0       IPV4 R2_RTR-C        0:5:86:71:d6:0
                 8          10.2.3.0/24
                 6          10.3.3.3/32
                 7          10.3.4.0/24
R2_RTR-C.00      2          ge-0/0/0.0       IPV4 R2_RTR-C        0:5:86:71:d6:0
                 6          10.1.2.0/24
                 2          10.2.2.2/32
                 6          10.2.3.0/24
                 6          2402:800::/32
R4_RTR-B.00      1          ge-0/0/1.0       IPV4 R4_RTR-B        0:5:86:71:72:1
                 4          10.1.4.0/24
                 4          10.3.4.0/24
                 1          10.4.4.4/32
R1_RTR-A.00      0
                 0          10.1.1.1/32
                 2          10.1.2.0/24
                 1          10.1.4.0/24
  4 nodes
```

- --

* *Part 4: SPF Calculation Example when RTR-B set overload-bit with�**�**advertise-high-metrics option and wide-metrics-only**

- --

* *SPF traceoption on R1 - Full log when overload-bit set�**�**with advertise-high-metrics option�**�**and wide-metrics-only**

```
root@R1_RTR-A> show log debug-isis
Jan 27 04:20:41 R1_RTR-A clear-log[8253]: logfile cleared
Jan 27 04:20:42.012600 L2 SPF trigger: Purging LSP R1_RTR-A.00-00
Jan 27 04:20:42.012657 SPF scheduled in 0.200000s
Jan 27 04:20:42.012787 SPF scheduled in 0.199862s
Jan 27 04:20:42.012814 SPF scheduled in 0.199834s
Jan 27 04:20:42.012846 SPF scheduled in 0.199803s
Jan 27 04:20:42.012867 SPF scheduled in 0.199803s
Jan 27 04:20:42.012878 SPF scheduled in 0.199803s
Jan 27 04:20:42.046832 SPF scheduled in 0.165824s
Jan 27 04:20:42.063424 SPF scheduled in 0.149230s
Jan 27 04:20:42.066400 SPF scheduled in 0.146254s
Jan 27 04:20:42.079886 SPF scheduled in 0.132773s
Jan 27 04:20:42.226524 Running L2 Full SPF
Jan 27 04:20:42.226589   Initializing LSP R1_RTR-A.00-00
Jan 27 04:20:42.226601     Adding candidate, metric 0
Jan 27 04:20:42.226619   Initializing LSP R2_RTR-C.00-00
Jan 27 04:20:42.226637   Initializing LSP R3_RTR-D.00-00
Jan 27 04:20:42.226656   Initializing LSP R4_RTR-B.00-00
Jan 27 04:20:42.226684     Create direct next hops for neighbor R2_RTR-C
Jan 27 04:20:42.226716       Next hop with improved metric 2: R2_RTR-C.00-00
Jan 27 04:20:42.226830         numberred IFA 10.1.2.2 used as next hop for R2_RTR-C
Jan 27 04:20:42.226870         No matching IFA for next hop R2_RTR-C, count 0
Jan 27 04:20:42.226894     Create direct next hops for neighbor R4_RTR-B
Jan 27 04:20:42.226908       Next hop with improved metric 1: R4_RTR-B.00-00
Jan 27 04:20:42.226929         numberred IFA 10.1.4.4 used as next hop for R4_RTR-B
Jan 27 04:20:42.226940         No matching IFA for next hop R4_RTR-B, count 0
Jan 27 04:20:42.226970 L2 SPF initialization complete: 0.000415s
Jan 27 04:20:42.226989     Considering R1_RTR-A.00-00, metric 0, no next hop
Jan 27 04:20:42.226997     Node R1_RTR-A.00-00 at metric 0
Jan 27 04:20:42.227006       Neighbor R4_RTR-B.00, metric 1
Jan 27 04:20:42.227012         Bidirectional adjacency, new metric 1
Jan 27 04:20:42.227021         Set candidate R4_RTR-B.00-00 metric to 1
Jan 27 04:20:42.227029       Neighbor R2_RTR-C.00, metric 2
Jan 27 04:20:42.227035         Bidirectional adjacency, new metric 2
Jan 27 04:20:42.227064         Set candidate R2_RTR-C.00-00 metric to 2
Jan 27 04:20:42.227075     Considering R4_RTR-B.00-00, metric 1, with next hop
Jan 27 04:20:42.227082     Node R4_RTR-B.00-00 at metric 1
Jan 27 04:20:42.227090       Neighbor R1_RTR-A.00, metric 16777214
Jan 27 04:20:42.227097         Suboptimal path, metric 16777215, current metric 0
Jan 27 04:20:42.227104       Neighbor R3_RTR-D.00, metric 16777214
Jan 27 04:20:42.227110         Bidirectional adjacency, new metric 16777215
Jan 27 04:20:42.227118         Set candidate R3_RTR-D.00-00 metric to 16777215
Jan 27 04:20:42.227127     Considering R2_RTR-C.00-00, metric 2, with next hop
Jan 27 04:20:42.227134     Node R2_RTR-C.00-00 at metric 2
Jan 27 04:20:42.227142       Neighbor R3_RTR-D.00, metric 4
Jan 27 04:20:42.227148         Bidirectional adjacency, new metric 6
Jan 27 04:20:42.227155         Set candidate R3_RTR-D.00-00 metric to 6
Jan 27 04:20:42.227163       Neighbor R1_RTR-A.00, metric 4
Jan 27 04:20:42.227169         Suboptimal path, metric 6, current metric 0
Jan 27 04:20:42.227177     Considering R3_RTR-D.00-00, metric 6, with next hop
Jan 27 04:20:42.227185     Node R3_RTR-D.00-00 at metric 6
Jan 27 04:20:42.227192       Neighbor R2_RTR-C.00, metric 2
Jan 27 04:20:42.227198         Suboptimal path, metric 8, current metric 2
Jan 27 04:20:42.227205       Neighbor R4_RTR-B.00, metric 1
Jan 27 04:20:42.227212         Suboptimal path, metric 7, current metric 1
Jan 27 04:20:42.227228 L2 SPF primary graph processing complete: 0.000255s
Jan 27 04:20:42.227242 L2 SPF multiarea postprocessing complete: 0.000015s
Jan 27 04:20:42.227279 Didn't alloc session id buf - count zero in spfinfo 0x964c17c!
Jan 27 04:20:42.227294   Cannot add route 10.1.1.1/32 in PPM msg (No sessid buffer)
Jan 27 04:20:42.227304   Cannot add route 10.1.2.0/24 in PPM msg (No sessid buffer)
Jan 27 04:20:42.227313   Cannot add route 10.1.4.0/24 in PPM msg (No sessid buffer)
Jan 27 04:20:42.227335   Cannot add route 2402:800::/32 in PPM msg (No sessid buffer)
Jan 27 04:20:42.227352 Enqueuing 0 session IDs in Session ID Down msg
Jan 27 04:20:42.227360 Not allocating Session ID Down msg (count=0, buffer=0x0)
Jan 27 04:20:42.227370 L2 SPF RIB postprocessing complete: 0.000129s
Jan 27 04:20:42.227381 Completed L2 Full SPF in 0.000828s cumulative time
Jan 27 04:20:42.227510 L2 SPF updated 0 routes (0 adds, 0 deletes, 0 changes, 0 fails) in 0.000098s
```

```
root@R1_RTR-A> show isis database detail
IS-IS level 1 link-state database:

IS-IS level 2 link-state database:

R1_RTR-A.00-00 Sequence: 0x3c, Checksum: 0xf367, Lifetime: 325 secs
   IS neighbor: R2_RTR-C.00                   Metric:        2
   IS neighbor: R4_RTR-B.00                   Metric:        1
   IP prefix: 10.1.1.1/32                     Metric:        0 Internal Up
   IP prefix: 10.1.2.0/24                     Metric:        2 Internal Up
   IP prefix: 10.1.4.0/24                     Metric:        1 Internal Up

R2_RTR-C.00-00 Sequence: 0x3e, Checksum: 0x67a4, Lifetime: 1164 secs
   IS neighbor: R1_RTR-A.00                   Metric:        4
   IS neighbor: R3_RTR-D.00                   Metric:        4
   IP prefix: 10.1.2.0/24                     Metric:        4 Internal Up
   IP prefix: 10.2.2.2/32                     Metric:        0 Internal Up
   IP prefix: 10.2.3.0/24                     Metric:        4 Internal Up
   V6 prefix: 2402:800::/32                   Metric:        4 Internal Up

R3_RTR-D.00-00 Sequence: 0x3c, Checksum: 0x7c93, Lifetime: 914 secs
   IS neighbor: R2_RTR-C.00                   Metric:        2
   IS neighbor: R4_RTR-B.00                   Metric:        1
   IP prefix: 10.2.3.0/24                     Metric:        2 Internal Up
   IP prefix: 10.3.3.3/32                     Metric:        0 Internal Up
   IP prefix: 10.3.4.0/24                     Metric:        1 Internal Up

R4_RTR-B.00-00 Sequence: 0x3e, Checksum: 0x2aef, Lifetime: 1051 secs
   IS neighbor: R1_RTR-A.00                   Metric: 16777214
   IS neighbor: R3_RTR-D.00                   Metric: 16777214
   IP prefix: 10.1.4.0/24                     Metric:        3 Internal Up
   IP prefix: 10.3.4.0/24                     Metric:        3 Internal Up
   IP prefix: 10.4.4.4/32                     Metric:        0 Internal Up
```

```
root@R1_RTR-A> show isis spf results
IS-IS level 1 SPF results:
  0 nodes

IS-IS level 2 SPF results:
Node             Metric     Interface        NH   Via             SNPA
R3_RTR-D.00      6          ge-0/0/0.0       IPV4 R2_RTR-C        0:5:86:71:d6:0
                 8          10.2.3.0/24
                 6          10.3.3.3/32
                 7          10.3.4.0/24
R2_RTR-C.00      2          ge-0/0/0.0       IPV4 R2_RTR-C        0:5:86:71:d6:0
                 6          10.1.2.0/24
                 2          10.2.2.2/32
                 6          10.2.3.0/24
                 6          2402:800::/32
R4_RTR-B.00      1          ge-0/0/1.0       IPV4 R4_RTR-B        0:5:86:71:72:1
                 4          10.1.4.0/24
                 4          10.3.4.0/24
                 1          10.4.4.4/32
R1_RTR-A.00      0
                 0          10.1.1.1/32
                 2          10.1.2.0/24
                 1          10.1.4.0/24
  4 nodes
```
