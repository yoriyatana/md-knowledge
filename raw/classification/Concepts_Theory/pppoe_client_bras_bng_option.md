# pppoe client bras bng option

I'm not 100% sure but if your box is in flow mode, the underlying interface might have to be in a security zone. Otherwise this looks fine and should be working as long as there's not something specific the LNS is looking for in the PADIs.

idle-timeout 0 means, when there is no traffic, the PPPoe interface becomes idle and didn't negotiate with PPPoE server, When traffic from LAN side started to come to the router, the router will initiate a PPPoE request to PPPoE server and connection will establish, but in realtime it didn't work and I had to reboot my bridged modem to get the connection. So I put this command there and it normally doesn't allow PPPoE connection to go idle and show always up.

auto-reconnect means the router will try to reconnect the PPPoE server automatically when there is a disconnection. 
