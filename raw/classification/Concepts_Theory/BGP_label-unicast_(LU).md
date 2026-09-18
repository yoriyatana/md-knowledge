# BGP label-unicast (LU)

# BGP LU

- family label-unicast:

    - Router sẽ gán label 3 cho route trên nó (connected)
    - Còn route từ protocol khác mà có next-hop là một ip trên router khác thì sẽ sinh **label khác 3**
- family label-unicast **explicit-null**
    - Gói tin sẽ được lookup lần 2 theo IPv4 hoặc IPv6 nên sẽ gán **label 2 với IPv6** hoặc **label 0 với IPv4**
