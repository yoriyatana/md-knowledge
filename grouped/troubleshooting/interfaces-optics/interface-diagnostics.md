# Interface Diagnostics

> Generated deterministically from the approved grouping manifest.


## Source: `formatted/TS_notes/interfaces diagnostics optics.md`

# interfaces diagnostics optics

######

Show cfp :

MX2010-ADV-NPE-01:

> show interfaces extensive et-6/0/0 | no-more

> show interfaces diagnostics optics et-6/0/0 | no-more

> start shell pfe network fpc6

# show cfp list

# show cfp  alarms

# show cfp  diagnostics

# show cfp  identifier

# show cfp  info

# show cfp  mdio-bus-error-count

# show cmic 0 info

# show cmic 0 interrupts

# show mtip-cgpcs summary

# show mtip-cgpcs  registers

# show mtip-cgpcs  errors

# show mtip-cgpcs  error-count

# show mtip-cgpcs  block-lock

# show mtip-cgpcs  fault-condition

# show mtip-cgpcs  high-BER

# show mtip-cgpcs  link-status

# show syslog messages

# exit

###### #########

MX2010-GDI-P-01:

> show interfaces extensive et-3/0/1 | no-more

> show interfaces diagnostics optics et-3/0/1 | no-more

> start shell pfe network fpc3

## Source: `formatted/TS_notes/10GbE LAN-PHY_40GbE_100GbE LFS (Link fault signalling).md`

# 10GbE LAN-PHY/40GbE/100GbE LFS (Link fault signalling)

10GbE LAN-PHY/40GbE/100GbE LFS operates between remote Reconciliation Sublayers (RS) and local RS. Link faults detected between remote RSs and local RSs are received by local RSs. Only the RS originates Remote Fault signals. When this Local Fault status reaches an RS, the RS stops sending MAC data, and continuously generates a Remote Fault status on the transmit data path. When Remote Fault status is received by an RS, the RS stops sending MAC data, and continuously generates Idle control characters. When the RS no longer receives fault status messages, it returns to normal operation, sending MAC data

![](../../assets/interface-diagnostics/c5fe9577fa-a29c8b33b3303696d0641b4e0f996313)

![](../../assets/interface-diagnostics/b775079e65-56fd4a9d253fc2834603fafb0e64d8e5)

![](../../assets/interface-diagnostics/cba69894db-1c9c67fbaf70d67ac3e2bdd28d79c141)

![](../../assets/interface-diagnostics/b7c73abdac-4fb016033ce3685396eacd9e69017339)

## Source: `formatted/TS_notes/set link-speed 100G cho interface ae với et-8 interface.md`

# set link-speed 100G cho interface ae với et-8 interface

![](../../assets/interface-diagnostics/5cc96a11cc-8978cf3f97651ac41f377624e9931b65.png)
