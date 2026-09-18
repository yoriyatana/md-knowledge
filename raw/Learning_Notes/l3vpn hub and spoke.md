# l3vpn hub and spoke

Interface routes

# In my case I only advertised a single loopback address from each spoke. In the JNCIE lab, you will need to advertise a lot more. Be sure to read their instructions carefully, and pay special attention to the interface routes. Even if they don’t specifically tell you to advertise them, you would always do well to include them when constructing your routing policies.

Note: I recommend that you only **use vrf import/export policies** for the JNCIE lab and avoid the vrf-target command for layer 3 VPN.

**L3VPN hub-and-spoke**

Overview

To summarize this article:

\* Hub and Spoke MPLS VPN routes traffic through a hub site instead of directly between spokes.

\* To achieve this, the control plane (i.e. routing) also follows a hub and spoke model.

\* The spoke routers import and export from different hub PE VRFs.

\* The hub PE has two VRFs, one for sending routes to the hub CE and one for receiving them.

BGP between CE <> PE

To wrap-up:

• We configured basic BGP as our PE-CE protocol on the hub and spokes, and defined basic VRFs on the PEs.

• On the spoke PE’s, we defined special import/export policies such that the hubs import routes tagged with the hub community but export with the spoke policy.

• We configured two VRFs on the hub PE router, one of which imported spoke-tagged routes, while the other exported hub-tagged routes.

• We configured **as-override**, advertise-peer-as, and AS loops to overcome the difficulty of using the same AS in three different places.

• We configured **SoO** to prevent the routes from looping.
