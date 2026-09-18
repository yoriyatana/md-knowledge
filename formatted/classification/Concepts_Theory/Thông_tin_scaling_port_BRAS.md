# Thông tin scaling port BRAS

|Thông  tin scaling port BRAS                   |            |                                 |        |               |                                |                |
|-----------------------------------------------|------------|---------------------------------|--------|---------------|--------------------------------|----------------|
|Áp dụng  với thuê bao thường không sử dụng HQoS|            |                                 |        |               |                                |                |
|                                               |            |                                 |        |               |                                |                |
|**STT**                                        |**MPC type**|**Scaling MPC**                  |**PFE** |**Scaling PFE**|**Port**                        |**Scaling Port**|
|1                                              |**MPC2E-3D**|**32k dualstack**                |0       |16k            |xe-x/0/1

xe-x/1/0

xe-x/1/1
xe-x/0/0|16k             |
|1                                              |16k         |xe-x/2/1

xe-x/3/0

xe-x/3/1
xe-x/2/0 |16k     |               |                                |                |
|2                                              |**MPC5E**   |**64k dualstack**                |0       |64k            |xe-y/0/1

xe-y/2/0

xe-y/2/1
xe-y/0/0|64k             |
|et-y/3/0
et-y/1/0                               |64k         |                                 |        |               |                                |                |
|3                                              |**MPC7E**   |**64k dualstack**                |0       |32k            | et-z/0/5
et-z/0/2               |32k             |
|1                                              |32k         |et-z/1/5
et-z/1/2                 |32k     |               |                                |                |

                        Trong đó x,y,z là số slot mà các linecard cắm vào.
