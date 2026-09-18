# DDOS pfe-RE TCP connections

DDOS pfe-RE TCP connections have a keep-alive expiry of 1.5 secs and if RE gets busy (high rate of traffic, high priority interrupt handling), then we could potentially see the drop in these connections. From the logs mentioned in the above timeline, it seems all the FPCs dropped their DDOS connections to the RE indicating RE was busy (we see a few jtask slips too; 6987 is DDOSD TCP server port) and then the reconnects happened within a sec.

Juniper tried to reproduce the issue in the lab by sending line rate of traffic to the RE with ddos disabled and we saw the same sequence as IBM during the outage time.

But once we got the DDOS statistic from the customer, we found the violation was only there for ARP and Resolve and the rate was very less.
