# CGNAT AE Interface Configuration Guide

> Generated deterministically from the approved grouping manifest.


## Source: `formatted/PR/using AE interfaces with SPC3.md`

# using AE interfaces with SPC3

USF-SPC3 : MX-SPC3 : Fabric hop optimization support while using AE interfaces with SPC3

With PR 1481140 [ OLYMPUS - MX ] Tracking PR for RLI 44531, The below mentioned issue got addressed when standalone interfaces are used. This PR opened to support the same while using AE interface with SPC3 in MX USF mode.

Problem & solution implemented as part of PR 1481140 :-

====================================================

a. All packets were going back to ingress PFE.

As in MX/USF we avoid software route-lookup. There is no way to egress

packet to PFE which is the egress PFE on which packet will exit the box.

b. Because of packet going back to ingress PFE which might not be the egress PFE,

will result in extra fabric hop for the packet. This extra hop results

in tail-drops on I/O card in case of scaled scenarios.

1. Solution(Limited to bi-directinal traffic): Fabric hop optimization for bi-directional traffic.

a. Learn fabricId of the ingress-PFE and stamp it on the session wing per packet.

b. Use the fabricId of the opposive wing to send the packet out of SPC3.

## Source: `formatted/TS_notes/high NPU CPU in CGNAT.md`

# high NPU CPU in CGNAT

```text
show interfaces mams-\* | match "mams-|rate"
```
- --

```text
> start shell
```
cli -c 'show services sessions interface mams-8/3/0' | grep Forward | awk '{if (int($7) > 1000000) print}'

cli -c 'show services sessions interface mams-8/3/0' | grep Forward | awk '{if (int($7) > 100000) print}'

cli -c 'show services sessions interface mams-8/0/0' | grep Forward | awk '{if (int($7) > 1000000) print}'

cli -c 'show services sessions interface mams-8/0/0' | grep Forward | awk '{if (int($7) > 100000) print}'
