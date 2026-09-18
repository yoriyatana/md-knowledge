# MAC move

{master}

juniper@MX2010-HDG00TBD-RE0> show configuration protocols l2-learning    

global-mac-move {

   threshold-time 1;

   threshold-count 50;

   cooloff-time 30;

   statistical-approach-wait-time 30;

   interface-recovery-time 3600;

   exclusive-mac 00:00:5e:00:01:00/40;

   exclusive-mac 00:00:0c:07:ac:00/40;

   exclusive-mac 00:07:b4:00:01:00/40;

   exclusive-mac 02:bf:00:00:00:00/16;

}

**![1d8b846eab97f3aed29cc9b271f68de1.png](image/1d8b846eab97f3aed29cc9b271f68de1.png)**
