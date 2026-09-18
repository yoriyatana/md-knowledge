# EoMPLS VC Type

Are you talking about EoMPLS VC Type? If Yes so

VC Type 4 is used for Ethernet VLAN mode.

VC Type 5 is used for Ethernet Port mode.

---
you are referring to EoMPLS Pseudowire Types (which are better defined in rfc4446 and not 4448) and indeed there are 2 ways to handle tags.

VC Type 4 : The original 802.1Q tag is inserted in the EoMPLS payload (along with the MPLS label) before forwarding it to the MPLS core. At the ingress of the remote end or receiving PE the 802.1Q tag is stripped off before its transmission to the internal bus. If a packet is received from the MPLS core without a tag (ether type of the packet is other than 0x8100) the packet is dropped.

VC Type 5 : In EoMPLS VLAN mode configuration, only the MPLS label is added to the packet transmitted to the MPLS core. On the ingress of the remote end or receiving PE the MPLS label stack is popped out before the transmission on the internal bus. If Port mode is configured instead, the 802.1Q tag is also carried along with the MPLS label

The actions taken by the PE interfaces facing the CE are solely determined by the specific interface configuration. If such configuration requires 802.1Q tagging, the egress frame is tagged; otherwise the egress frame is sent untagged. EoMPLS VC type 5 is the default configuration mode on the platforms supporting it. Meaning that the PEs will try to first negotiate and use VC 5, if one of them (or both) does not support it they will reverse to VC 4. EoMPLS type VLAN offers backward compatibility in case the remote peer does not support VC type Ethernet.

VC type 4 or VC type 5 is not a configurable option and is platform dependent, the capability is instead auto

sensed at control plane level"
