# Interface Diagnostics

> Generated deterministically from the approved grouping manifest.


## Source: `formatted/TS_notes/interfaces_diagnostics_optics.md`

# interfaces diagnostics optics

######

Show cfp :

MX2010-ADV-NPE-01:

> show interfaces extensive et-6/0/0 | no-more

> show interfaces diagnostics optics et-6/0/0 | no-more

> start shell pfe network fpc6

# show cfp list

# show cfp <index> alarms

# show cfp <index> diagnostics

# show cfp <index> identifier

# show cfp <index> info

# show cfp <index> mdio-bus-error-count

# show cmic 0 info

# show cmic 0 interrupts

# show mtip-cgpcs summary

# show mtip-cgpcs <index> registers

# show mtip-cgpcs <index> errors

# show mtip-cgpcs <index> error-count

# show mtip-cgpcs <index> block-lock

# show mtip-cgpcs <index> fault-condition

# show mtip-cgpcs <index> high-BER

# show mtip-cgpcs <index> link-status

# show syslog messages

# exit

###### #########

MX2010-GDI-P-01:

> show interfaces extensive et-3/0/1 | no-more

> show interfaces diagnostics optics et-3/0/1 | no-more

> start shell pfe network fpc3

## Source: `formatted/TS_notes/10GbE_LAN-PHY-40GbE-100GbE_LFS_(Link_fault_signalling).md`

# 10GbE LAN-PHY/40GbE/100GbE LFS (Link fault signalling)

10GbE LAN-PHY/40GbE/100GbE LFS operates between remote Reconciliation Sublayers (RS) and local RS. Link faults detected between remote RSs and local RSs are received by local RSs. Only the RS originates Remote Fault signals. When this Local Fault status reaches an RS, the RS stops sending MAC data, and continuously generates a Remote Fault status on the transmit data path. When Remote Fault status is received by an RS, the RS stops sending MAC data, and continuously generates Idle control characters. When the RS no longer receives fault status messages, it returns to normal operation, sending MAC data

![Attachment.png](../../assets/interface-diagnostics/9ef3a4b0c9-Attachment.png)

![Attachment-1.png](../../assets/interface-diagnostics/7843a0904d-Attachment-1.png)

![Attachment-2.png](../../assets/interface-diagnostics/03d20a8d86-Attachment-2.png)

![Attachment-3.png](../../assets/interface-diagnostics/3fb97c1e29-Attachment-3.png)

## Source: `formatted/TS_notes/set_link-speed_100G_cho_interface_ae_với_et-8_interface.md`

# set link-speed 100G cho interface ae với et-8 interface

![image.png](../../assets/interface-diagnostics/50bd5b1924-image.png)
